from bs4 import BeautifulSoup

from src.utils import generate_api_token, API_BASE_URL, CODES_DB_URL, DATE, get_soup


def test_constants():
    assert API_BASE_URL == "https://sandbox-api.piste.gouv.fr/dila/legifrance/lf-engine-app"
    assert CODES_DB_URL == "https://www.legifrance.gouv.fr/codes/texte_lc"
    assert DATE == "2024-04-20"


def test_get_soup():
    with open("examplecom_response.txt", "r") as f:
        text = f.read()

    soup = get_soup("https://example.com")

    assert isinstance(soup, BeautifulSoup)
    assert BeautifulSoup(text, "html.parser") == soup


def test_generate_api_token():
    token = generate_api_token()

    assert isinstance(token, str)
    assert len(token) == 54
