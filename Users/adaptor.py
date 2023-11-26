from allauth.account.utils import perform_login
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

from Users.models import User


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        print(user)
        print(user.id)
        if user.id:
            return
        else:
            User = get_user_model()
            existing_user = User.objects.filter(email=user.email).first()

            if existing_user:
                print("existing user, ", existing_user.id)
                print("existing user, ", existing_user)
                # Connect the social account to the existing user
                sociallogin.connect(request, existing_user)
                sociallogin.state['process'] = 'login'
                sociallogin.state['user'] = existing_user
