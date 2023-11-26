from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from Users.decorators import check_access_token
from Users.serializers import UserSerializer
from Users.views import validate_address


class UserProfileView(APIView):
    @method_decorator(check_access_token())
    def get(self,request, user_id):
        User = get_user_model()
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        user_json = JSONRenderer().render(serializer.data).decode('utf-8')
        return HttpResponse(user_json, content_type='application/json')



    @method_decorator(check_access_token())
    def put(self, request, user_id):
        User = get_user_model()
        user = get_object_or_404(User, id=user_id)
        # Get user address details from the registration form
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        is_valid_address = None
        if address or state or zip_code or city:
        # Run SmartyStreets address validations
            address = address or user.address
            zip_code = zip_code or user.zip_code
            city = city or user.city
            state = state or user.state
            is_valid_address = validate_address(address, zip_code,city, state)
            if is_valid_address is None:
                return Response({'error': 'Address is not valid!'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            json_data = serializer.data
            if is_valid_address is not None:
                user.city = is_valid_address['city']
                json_data['city'] = is_valid_address['city']
                user.state = is_valid_address['state']
                json_data['state'] = is_valid_address['state']
                user.address = is_valid_address['address']
                json_data['address'] = is_valid_address['address']
                user.zip_code = is_valid_address['zip_code']
                json_data['zip_code'] = is_valid_address['zip_code']
                user.save()
            return Response(json_data, content_type='application/json',  status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



