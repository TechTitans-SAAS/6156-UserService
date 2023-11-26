from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class UserSignOutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'You have been logged out successfully.'}, status=status.HTTP_200_OK)
