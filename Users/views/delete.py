from django.contrib.auth import logout, get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from django.contrib import messages
from rest_framework.response import Response
import google.auth.jwt

from Users.views import get_authorization_header


class UserDeleteView(APIView):

    def delete(self, request):
        # authorization_header = request.headers.get('Authorization', '')
        authorization_header = get_authorization_header(request)
        jwt_token = authorization_header.split(' ')[1]
        payload = google.auth.jwt.decode(jwt_token, verify=False)
        # print(payload)
        user_id = payload['id']
        User = get_user_model()
        user = get_object_or_404(User, id=user_id)
        # if user exists, delete user
        if user:
            user.delete()
            logout(request)  # logout
            messages.success(request, 'Your account has been deleted.')
            return Response({'message': 'Account deleted successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)