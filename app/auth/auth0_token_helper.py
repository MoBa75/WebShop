import os
import requests
from dotenv import load_dotenv

load_dotenv()  # .env laden

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE")

def get_machine_token() -> str:
    """
    Retrieves a machine-to-machine access token from Auth0.

    Returns:
        str: The access token.
    Raises:
        RuntimeError: If the token request fails.
    """
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"Content-Type": "application/json"}
    payload = {
        "grant_type": "client_credentials",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": AUTH0_API_AUDIENCE
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to get token: {response.status_code} - {response.text}")

    return response.json()["access_token"]
