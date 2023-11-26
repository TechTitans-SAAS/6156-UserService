import google.auth.crypt


import time

import requests
from google.auth import jwt


# the audience is the api gw client id
def generate_jwt(
    sa_keyfile= '../user-microservice-apigw.json',
    sa_email="jwt-182@user-microservice-402518.iam.gserviceaccount.com",
    audience="https://thriftustore-api-2ubvdk157ecvh.apigateway.user-microservice-402518.cloud.goog",
    expiry_length=3600,
    personalized_claims=None,
):
    """Generates a signed JSON Web Token using a Google API Service Account."""
    now = int(time.time())
    # build payload
    payload = {
        "iat": now,
        # expires after 'expiry_length' seconds.
        "exp": now + expiry_length,
        # iss must match 'issuer' in the security configuration in your
        # swagger spec (e.g. service account email). It can be any string.
        "iss": sa_email,
        "aud": audience,
        # sub and email should match the service account's email address
        "sub": sa_email,
        "email": sa_email,
    }

    # Add personalized claims to the payload
    if personalized_claims:
        payload.update(personalized_claims)

    # sign with keyfile
    signer = google.auth.crypt.RSASigner.from_service_account_file(sa_keyfile)
    jwt = google.auth.jwt.encode(signer, payload).decode("utf-8")
    # payload = google.auth.jwt.decode(jwt)
    print(jwt)
    # print(payload)
    return jwt

if __name__ == '__main__':
    token = "eyJ0eXAiOiAiSldUIiwgImFsZyI6ICJSUzI1NiIsICJraWQiOiAiNjlkMmY3NzBkYzUwMTY5YTRhMzcwMGFkMjQ5OWY1MDYwYmRjZDZjOSJ9.eyJpYXQiOiAxNzAwOTcyNDEyLCAiZXhwIjogMTcwMDk3NjAxMiwgImlzcyI6ICJqd3QtMTgyQHVzZXItbWljcm9zZXJ2aWNlLTQwMjUxOC5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsICJhdWQiOiAiaHR0cHM6Ly90aHJpZnR1c3RvcmUtYXBpLTJ1YnZkazE1N2VjdmguYXBpZ2F0ZXdheS51c2VyLW1pY3Jvc2VydmljZS00MDI1MTguY2xvdWQuZ29vZyIsICJzdWIiOiAiand0LTE4MkB1c2VyLW1pY3Jvc2VydmljZS00MDI1MTguaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCAiZW1haWwiOiAidGVzdGFkZHJlZHNhc2FzZGRAY29sdW1iaWEuZWR1YSIsICJpZCI6IDIyMiwgImZ1bGxfbmFtZSI6ICJaaGljaGVuZ3MiLCAiY3JlYXRlZF9hdCI6ICIyMDIzLTExLTI1VDAxOjE0OjU2LjE2MDI1M1oiLCAidXBkYXRlZF9hdCI6ICIyMDIzLTExLTI1VDE5OjU2OjEyLjYyODQ2MVoiLCAiYWRkcmVzcyI6ICI1MzUgVyAxMTZ0aCBTdCIsICJ6aXBfY29kZSI6ICIxMDAyNyIsICJjaXR5IjogIk5ldyBZb3JrIiwgInN0YXRlIjogIk5ZIiwgImNvdW50cnkiOiAiIiwgImRlc2NyaXB0aW9uIjogInRoaXMgaXMgYSB0ZXN0IGRlc2NyaXB0aW9uIiwgImFjY2Vzc190b2tlbiI6IG51bGwsICJsb2dpbl90eXBlIjogIlBhc3N3b3JkIn0.XdL5Q596MhnmFET9Z9FOMnOhmm3Z8BD3LmO0F9YoFs7pJ_KB-QYUa0sDXvuEsJlcMmYkGdaj4K8qTDSyjRKa3SqOpD816YkzhxBjHuGkn3rbQe6otfzh7Wntdt64UJoPy4hbYp8zWkaqduCWLgOVdO7JpxJu5gYyj1VRnwgVVtK8JPoq78xRWG9PHhtUiVy8ZkbA3DHV8kJvnixCSvpsAQmO9_ywDO4NLJNvWw9QEhvKtVGAS62JiBu71Zb4rxUbwC-n5IUa2d_OcpF0NCRHBInDfFtPD1Wpfm1fgIduEFFwjupeplCKAPywVYWqRi_Hdg95JOoVxj4HdJlvQAb3ww"
    audience = "https://thriftustore-api-2ubvdk157ecvh.apigateway.user-microservice-402518.cloud.goog"

    # Public key URL for the service account
    public_key_url = 'https://www.googleapis.com/robot/v1/metadata/x509/jwt-182@user-microservice-402518.iam.gserviceaccount.com'

    # Fetch the public keys from the URL
    response = requests.get(public_key_url)
    public_keys = response.json()

    # Verify the JWT token using the fetched public keys
    decoded_token = jwt.decode(token, certs=public_keys, audience=audience)
    # The token is verified, and 'decoded_token' contains the decoded information
    print(decoded_token)

