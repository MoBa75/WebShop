from app.auth.auth0_token_helper import get_machine_token

token = get_machine_token()
print("Access Token:", token)
