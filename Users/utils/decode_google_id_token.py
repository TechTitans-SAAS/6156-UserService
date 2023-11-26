from google.auth.transport import requests
from google.oauth2 import id_token

def verify_google_id_token(token, client_id):
    try:
        # Verify and decode the ID Token
        id_info = id_token.verify_oauth2_token(token, requests.Request(), client_id)
        # Extract user information
        user_id = id_info['sub']
        user_email = id_info['email']
        user_name = id_info['name']
        token_exp = id_info['exp']
        return {'user_id': user_id, 'user_email': user_email, 'name' : user_name, 'exp':token_exp, }
    except ValueError as e:
        # Handle invalid token
        print(f"Invalid token: {e}")
        return None

# Example usage
google_id_token = 'eyJ0eXAiOiAiSldUIiwgImFsZyI6ICJSUzI1NiIsICJraWQiOiAiNjlkMmY3NzBkYzUwMTY5YTRhMzcwMGFkMjQ5OWY1MDYwYmRjZDZjOSJ9.eyJpYXQiOiAxNzAwOTQyODcwLCAiZXhwIjogMTcwMDk0NjQ3MCwgImlzcyI6ICJqd3QtMTgyQHVzZXItbWljcm9zZXJ2aWNlLTQwMjUxOC5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsICJhdWQiOiAiaHR0cHM6Ly90aHJpZnR1c3RvcmUtYXBpLTJ1YnZkazE1N2VjdmguYXBpZ2F0ZXdheS51c2VyLW1pY3Jvc2VydmljZS00MDI1MTguY2xvdWQuZ29vZyIsICJzdWIiOiAiand0LTE4MkB1c2VyLW1pY3Jvc2VydmljZS00MDI1MTguaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCAiZW1haWwiOiAiZ3ctdGVzdDJAY29sdW1iaWEuZWR1IiwgImlkIjogMTAsICJmdWxsX25hbWUiOiAiIiwgImNyZWF0ZWRfYXQiOiAiMjAyMy0xMS0xNVQxOTo0ODo1OC43Mzg3NDFaIiwgInVwZGF0ZWRfYXQiOiAiMjAyMy0xMS0yNVQwNDo0NTozNS45NzQxNTNaIiwgImFkZHJlc3MiOiAiNTM1IFcgMTE2dGggU3QiLCAiemlwX2NvZGUiOiAiMTAwMjciLCAiY2l0eSI6ICJOZXcgWW9yayIsICJzdGF0ZSI6ICJOWSIsICJjb3VudHJ5IjogIiIsICJkZXNjcmlwdGlvbiI6ICIiLCAiYWNjZXNzX3Rva2VuIjogbnVsbCwgImxvZ2luX3R5cGUiOiAiUGFzc3dvcmQifQ.HR7huK6N00WU7cMUZG_BDobugSRiZhzSrJmKGYgQnBBHpn7zTSKQ8sFJaEplRADBOssY0U10K6EVoD_XG8WFiXMG249XWOboUoFCQkKQfVVbV7fKPxts1SwovtEJ2wNcGlyjgw_uHWVIz15MnTvrua-tm-EqicztQGY4jtHKx6-5OPwSSWevniC5oRkuRVLQfwqaYk8LDT00sbaKozSedA1VSyGsGVQqCg6Al26SDoS24UTZApy2X5dm8QlpfQM9wu5eGTQVHv_5TWE3kBay3IrL9aNLpxke9CMM0XIYv2NT6SUGXs_NUI_TsrtkalkI_f4Hs0dSskoPbPHuw1cz9A'
google_client_id = 'jwt-182@user-microservice-402518.iam.gserviceaccount.com'
decoded_info = verify_google_id_token(google_id_token, google_client_id)
if decoded_info:
    print(decoded_info)

