import os
import base64
import secrets
import hashlib
from urllib.parse import urlencode


def request_authorisation():
    code_verifier = secrets.token_urlsafe(43)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode("utf-8")).digest()
    ).decode("utf-8")[:-1]
    
    params = {
        "client_id": os.environ["FITBIT_CLIENT_ID"],
        "response_type": "code",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "scope": "weight",
    }
    
    authorization_url = "https://www.fitbit.com/oauth2/authorize?" + urlencode(params)

    print("Open this URL in your browser:")
    print(authorization_url)