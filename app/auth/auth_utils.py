from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError, JWTClaimsError

import requests
from fastapi import HTTPException
from os import getenv

AUTH0_DOMAIN = getenv("AUTH0_DOMAIN")
API_AUDIENCE = getenv("AUTH0_API_AUDIENCE")
ALGORITHMS = [getenv("AUTH0_ALGORITHMS") or "RS256"]

def get_jwk_keys():
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    response = requests.get(jwks_url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Unable to fetch JWK keys")
    return response.json()["keys"]

def get_current_user_data(token: str) -> dict:
    try:
        unverified_header = jwt.get_unverified_header(token)
        jwks = get_jwk_keys()
        rsa_key = {}

        for key in jwks:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
                break

        if not rsa_key:
            raise HTTPException(status_code=401, detail="Appropriate key not found")

        payload = jwt.decode(
            token,
            key=rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/"
        )
        return {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "first_name": payload.get("given_name"),
            "last_name": payload.get("family_name")
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTClaimsError:
        raise HTTPException(status_code=401, detail="Incorrect claims. Check audience and issuer.")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")
