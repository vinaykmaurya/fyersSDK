import urllib.parse
import hashlib
from fyers_api.services import FyersService
from fyers_api import config

class SessionModel:
    def __init__(self, client_id=None, redirect_uri=None, response_type=None, scope=None, state=None, nonce=None, secret_key=None, grant_type=None):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.scope = scope
        self.state = state
        self.nonce = nonce
        self.secret_key = secret_key
        self.grant_type = grant_type

    def generate_authcode(self):
        data = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": self.response_type,
            "state": self.state
        }
        if self.scope is not None:
            data["scope"] = self.scope
        if self.nonce is not None:
            data["nonce"] = self.nonce
        
        url_params = urllib.parse.urlencode(data)
        return f"{config.Api}{config.auth}?{url_params}"

    def get_hash(self):
        hash_val = hashlib.sha256(f"{self.client_id}:{self.secret_key}".encode())
        return hash_val

    def set_token(self, token):
        self.auth_token = token

    def generate_token(self):
        data = {
            "grant_type": self.grant_type,
            "appIdHash": self.get_hash().hexdigest(),
            "code": self.auth_token
        }
        service = FyersService()
        response = service.postCall(config.generateAccessToken, "", data)
        return response
