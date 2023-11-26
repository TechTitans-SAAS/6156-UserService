import requests
from django.http import HttpResponseForbidden
import google.auth.jwt

from Users.views import get_authorization_header


def check_access_token():
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            authorization_header = get_authorization_header(request)
            # authorization_header = request.headers.get('Authorization', '')
            if authorization_header:
                jwt_token = authorization_header.split(' ')[1]
                decoded_token = google.auth.jwt.decode(jwt_token, verify=False)

                if decoded_token["login_type"] == "Google":
                    access_token = decoded_token.get('access_token')

                    if not access_token:
                        return HttpResponseForbidden("Access token is missing in the JWT payload")

                    # google oauth2 client id for web application
                    google_client_id = '258239284713-8nb3h72ebnp38b2a1i093t6fd2og177p.apps.googleusercontent.com'
                    google_token_info_url = f'https://www.googleapis.com/oauth2/v3/tokeninfo?access_token={access_token}'
                    response = requests.get(google_token_info_url)

                    if response.status_code == 200:
                        token_info = response.json()

                        # Check that the audience matches your Google OAuth client ID
                        if token_info.get('aud') != google_client_id:
                            return HttpResponseForbidden("Invalid audience")

                        return func(request, *args, **kwargs)
                    else:
                        return HttpResponseForbidden("Invalid access token")
                return func(request, *args, **kwargs)

            else:
                return HttpResponseForbidden()
        return wrapper

    return decorator


