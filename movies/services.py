import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
from tenacity import retry, wait_exponential, stop_after_attempt
import environ

env = environ.Env()
environ.Env.read_env()

API_USERNAME = env('API_USERNAME')
API_PASSWORD = env('API_PASSWORD')

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
def fetch_movies(url):
    try:
        response = requests.get(url, auth=HTTPBasicAuth(API_USERNAME, API_PASSWORD),verify=False)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        raise
