from os.path import join

import requests
from bs4 import BeautifulSoup

from src.utils import API_BASE_URL, get_soup, DATE, CODES_DB_URL


def get_non_abrogated_codes(api_token: str) -> list[tuple[str, str]]:
    """
    Get all non-abrogated codes.

    Args:
        api_token (str): API token.

    Returns:
        list[tuple[str, str]]: Codes' id and their title.
    """
    url = f"{API_BASE_URL}/list/code"
    headers = {"Authorization": f"Bearer {api_token}"}

    data = {
        "pageSize": 100,  # As for now, May 2024, there are 77 Codes in effect
        "sort": "TITLE_ASC",
        "pageNumber": 1,
        "states": [
            "VIGUEUR"
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    return [(r["id"], r["titre"]) for r in response.json()["results"]]


def get_code_soup(code_id: str) -> BeautifulSoup:
    """
    Get Code BeautifulSoup objec.

    Args:
        code_id (str): Code id.

    Returns:
        BeautifulSoup: BeautifulSoup object.
    """
    return get_soup(join(CODES_DB_URL, code_id, DATE))


def get_code_non_abrogated_articles(code_soup: BeautifulSoup) -> list[str]:
    """
    Get the non-abrogated Articles from a Code.

    Args:
        code_soup (BeautifulSoup): Code soup.

    Returns:
        list[str]: non-abrogated article ids.
    """
    return [element.get("id")[3:] for element in code_soup.select(".articleLink:not(.abrogated)")]


def get_code_title(api_token: str, code_id: str) -> str:
    """
    Get the title of a Code.

    Args:
        api_token (str): API token.
        code_id (str): Code id.

    Returns:
        str: Title of the Code.
    """
    url = f"{API_BASE_URL}/consult/code"
    headers = {"Authorization": f"Bearer {api_token}"}

    data = {
        "textId": code_id,
        "date": DATE,
        "sctCid": ""
    }

    response = requests.post(url, json=data, headers=headers).json()

    return response["title"].replace("'", " ").replace(" ", "_")
