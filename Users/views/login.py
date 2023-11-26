import json

from allauth.socialaccount.models import SocialToken, SocialAccount
from django.contrib.auth import authenticate, logout, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from google.oauth2 import id_token
import google.auth.jwt

from Users.serializers import UserSerializer
from Users.utils.jwt import generate_jwt

import requests


# This is the helper function to retrieve the authorization header from the request
def get_authorization_header(request):
    authorization_header = request.headers.get('Authorization')
    x_apigateway_userinfo = request.headers.get('X-Forwarded-Authorization')
    return authorization_header if authorization_header else x_apigateway_userinfo

# A help function to generate extra data to included to the JWT token
def generate_token_claim(user_id, login_type):
    # find the user and use the serializer to retrieve the user info
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user)
    basic_data= serializer.data
    # add social access token to the JWT token
    # check if the current login user has a social account associated with the user or not
    social_account = SocialAccount.objects.filter(user_id=user.id).first()
    if social_account:
        social_token = SocialToken.objects.filter(account_id=social_account.id).first()
        basic_data.update({"access_token": social_token.token})
    else:
        basic_data.update({"access_token": None})
    basic_data.update({"login_type" : login_type})
    return basic_data

# a helper function to refresh the social token and the jwt token
def refresh_social_token(refresh_token):
    token_url = "https://www.googleapis.com/oauth2/v4/token"

    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': '258239284713-8nb3h72ebnp38b2a1i093t6fd2og177p.apps.googleusercontent.com',
        'client_secret': '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'
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        # Successful response
        token_data = response.json()
        new_access_token = token_data.get('access_token')
        new_refresh_token = token_data.get('refresh_token', refresh_token)  # Google may or may not include a new refresh token
        return new_access_token, new_refresh_token
    else:
        # Handle error
        print(f"Error refreshing token: {response.status_code} - {response.text}")
        return None, None

@api_view(["GET"])
def hello(request):
    # Print request GET parameters
    if request.method == "GET":
        # check if there is a bearer token in the request
        authorization_header = get_authorization_header(request)
        if authorization_header and authorization_header.startswith('Bearer '):
            token = authorization_header.split(' ')[1]
            data = {'token': token}
            payload = google.auth.jwt.decode(token, verify=False)
            User = get_user_model()
            user = get_object_or_404(User, id=payload["id"])
            serializer = UserSerializer(user)
            user_info = json.loads(JSONRenderer().render(serializer.data).decode('utf-8'))
            data.update({"user_info": user_info})
        elif request.user.is_authenticated:
            token = request.session.get('token', {})
            data = {'token': token}
            User = get_user_model()
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user)
            user_info = json.loads(JSONRenderer().render(serializer.data).decode('utf-8'))
            data.update({"user_info": user_info})
        else:
            print("no token provided")
            return Response(data="Hello from users API, you are not logged in, no token to retrieve",
                            status=status.HTTP_200_OK)

        json_string = JsonResponse(data).content.decode('utf-8')
        # redirect back to the front end after getting the token
        redirect_url = f"https://thriftustore-web.s3.amazonaws.com/public/index.html?data={json_string}"
        return HttpResponseRedirect(redirect_url)


# This is the user sign in view for logging in via email and password
class UserSignInView(APIView):
    # post method to sign in via user email and password
    def post(self, request):
        # retrieve the email and password from the request
        email = request.data.get('email')
        password = request.data.get('password')
        # authenticate the identity of the user via email and password
        user = authenticate(request, username=email, password=password)
        # log in successfully
        if user is not None:
            # generate extra fields to included in the JWT token
            personalized_claims = generate_token_claim(user.id, login_type="Password")
            # generate the token by using the Google service account with extra fields generated before
            token = generate_jwt(sa_keyfile="user-microservice-apigw.json" ,personalized_claims=personalized_claims)
            request.session['token'] = token
            login(request, user)

            # return the json data with token and user_info included
            User = get_user_model()
            user = get_object_or_404(User, id=user.id)
            serializer = UserSerializer(user)
            user_info = json.loads(JSONRenderer().render(serializer.data).decode('utf-8'))
            return Response({'token': str(token),"user_info": user_info}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    # A simple test view
    def get(self,request):
        return Response(data="Hello from users API", status=status.HTTP_200_OK)







# This is the view for generating the JWT token when logging in via Google Oauth2
class GoogleOauthJwtView(APIView):
    @method_decorator(login_required)
    def get(self, request):
        # get the user and the corresponding social account info
        user = request.user
        social_account = SocialAccount.objects.get(user_id=user.id)
        name = social_account.extra_data["name"]

        # update the username in the social account
        user.full_name = name
        user.save()
        # generate the personalized the data to encapsulate into the JWT token
        personalized_claims = generate_token_claim(user.id, login_type="Google")
        token = generate_jwt(sa_keyfile="user-microservice-apigw.json", personalized_claims=personalized_claims)
        request.session['token'] = token
        request.session["access_token"] = personalized_claims['access_token']
        return redirect("hello_url")


class ApiGWGoogleView(APIView):
    def get(self, request):
        return redirect("https://user-microservice-402518.ue.r.appspot.com/users/google/login/")

class RefreshJwtView(APIView):
    def get(self, request):

        authorization_header = get_authorization_header(request)
        if authorization_header and authorization_header.startswith('Bearer '):
            token = authorization_header.split(' ')[1]
            payload = google.auth.jwt.decode(token, verify=False)
            login_type = payload["login_type"]
            id = payload["id"]
            social_account = SocialAccount.objects.filter(user_id=id).first()
            # if logged in via google, then generate a new pair of social access token and refresh token
            if social_account:
                social_token = SocialToken.objects.filter(account_id=social_account.id).first()
                refresh_token = social_token.token_secret
                new_access_token, new_refresh_token = refresh_social_token(refresh_token)
                social_token.token = new_access_token
                social_token.token_secret = new_refresh_token
                social_token.save()
            personalized_claims = generate_token_claim(id, login_type)
            new_token = generate_jwt(sa_keyfile="user-microservice-apigw.json", personalized_claims=personalized_claims)
            # return the new jwt token
            return  Response({'token': new_token}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)





