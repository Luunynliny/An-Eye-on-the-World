import requests
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from os.path import join, dirname

config = dotenv_values(join(dirname(__file__), ".env"))

API_BASE_URL: str = "https://sandbox-api.piste.gouv.fr/dila/legifrance/lf-engine-app"
CODES_DB_URL: str = "https://www.legifrance.gouv.fr/codes/texte_lc"

DATE: str = "2024-04-20"


def get_soup(url: str) -> BeautifulSoup:
    """
    Create a BeautifulSoup object from a URL.

    Args:
        url (str): URL to parse.

    Returns:
        BeautifulSoup: BeautifulSoup object.
    """
    response = requests.get(url)

    return BeautifulSoup(response.text, 'html.parser')


def generate_api_token() -> str:
    """
    Generate an API token to acces Légifrance data.

    Returns:
        str: Bearer token.
    """
    url = "https://sandbox-oauth.piste.gouv.fr/api/oauth/token"
    data = {"grant_type": "client_credentials"}
    auth = (config["CLIENT_ID"], config["CLIENT_SECRET"])

    response = requests.post(url, data=data, auth=auth)

    return response.json()["access_token"]
