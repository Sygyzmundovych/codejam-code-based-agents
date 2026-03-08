import os
import requests

class RPT1Client:
    def __init__(self):
        # Read env vars (assume dotenv already loaded in main)
        self.client_id = os.getenv("AICORE_CLIENT_ID")
        self.client_secret = os.getenv("AICORE_CLIENT_SECRET")
        self.auth_url = os.getenv("AICORE_AUTH_URL")
        self.deployment_url = os.getenv("RPT1_DEPLOYMENT_URL")
        self.token = self._fetch_token()
        self.resource_group = os.getenv("AICORE_RESOURCE_GROUP", "default")

    # Function to fetch OAuth token
    def _fetch_token(self, timeout: int = 30) -> str:
        if not self.auth_url:
            raise ValueError("AICORE_AUTH_URL must be provided (env or arg).")
        if not self.client_id:
            raise ValueError("AICORE_CLIENT_ID must be provided (env or arg).")
        if not self.client_secret:
            raise ValueError("AICORE_CLIENT_SECRET must be provided (env or arg).")
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        resp = requests.post(self.auth_url, data=data, headers=headers, timeout=timeout)
        resp.raise_for_status()
        token = resp.json()
        access_token = token["access_token"]
        return access_token

    def post_request(self, json_payload: dict, timeout: int = 60):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "AI-Resource-Group": self.resource_group
        }

        # Send the POST request to the deployment URL
        response = requests.post(
            self.deployment_url, json=json_payload, headers=headers
        )
        return response
