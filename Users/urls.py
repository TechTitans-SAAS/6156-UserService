from django.urls import path, include
from rest_framework_simplejwt.views import TokenVerifyView

from Users import views
# from Users.views import UserSignInView, UserRegistrationView, UserSignOutView, UserProfileView, UserDeleteView, google_login_callback

from .views import UserSignInView, UserRegistrationView, UserSignOutView, UserProfileView, UserDeleteView, GoogleOauthJwtView, ApiGWGoogleView, RefreshJwtView


urlpatterns = [

    path("", views.hello, name="hello_url"),
    path('users/sign_in', UserSignInView.as_view(), name='sign_in'),
    path('users/sign_up', UserRegistrationView.as_view(), name='sign_up'),
    path('users/sign_out', UserSignOutView.as_view(), name='sign_out'),
    path('users/refresh', RefreshJwtView.as_view(), name= 'refresh_token'),
    path('users/google/token', GoogleOauthJwtView.as_view(), name='google_token'),
    # # provide a uniform url to check if user registered
    # path('users/verify', TokenVerifyView.as_view(), name='verify'),
    path('users/profile/<int:user_id>', UserProfileView.as_view(), name='user_profile'),
    path('users/delete', UserDeleteView.as_view(), name='user_delete'),
    path('users/google/sign_in', ApiGWGoogleView.as_view(), name='api_gw_google_sign_in'),





]