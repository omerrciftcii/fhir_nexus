import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class FHIRClient:
    """
    Enterprise-grade HTTP client for secure communication with OpenEMR FHIR API.
    Handles OAuth2 Bearer token retrieval and authenticated requests.
    """
    
    def __init__(self):
        self.base_url = os.getenv("OPENEMR_FHIR_BASE_URL")
        self.token_url = os.getenv("OPENEMR_TOKEN_URL")
        self.client_id = os.getenv("OPENEMR_CLIENT_ID")
        self.client_secret = os.getenv("OPENEMR_CLIENT_SECRET")
        self.access_token = None

    def authenticate(self) -> bool:
        """
        Retrieves the OAuth2 Bearer token using client credentials.
        """
        if not all([self.token_url, self.client_id, self.client_secret]):
            print("Error: Missing authentication credentials in the .env file.")
            return False

        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        try:
            # Set timeout to prevent hanging connections
            response = requests.post(self.token_url, data=payload, timeout=10)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            
            print("Successfully authenticated with OpenEMR FHIR API.")
            return True
            
        except requests.exceptions.RequestException as error:
            print(f"Authentication failed: {error}")
            return False

    def get_resource(self, resource_type: str, params: dict = None) -> dict:
        """
        Fetches a specific FHIR resource from the server.
        """
        if not self.access_token:
            print("Warning: No access token found. Attempting to authenticate...")
            if not self.authenticate():
                return {}

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/fhir+json"
        }
        
        endpoint = f"{self.base_url}/{resource_type}"
        
        try:
            response = requests.get(endpoint, headers=headers, params=params, timeout=15)
            response.raise_for_status()
            
            print(f"Successfully retrieved {resource_type} data.")
            return response.json()
            
        except requests.exceptions.RequestException as error:
            print(f"Error fetching FHIR resource '{resource_type}': {error}")
            return {}