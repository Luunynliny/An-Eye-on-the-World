from os.path import join

from bs4 import BeautifulSoup

from src.utils import get_soup

CODES_DB_URL = "https://www.legifrance.gouv.fr/codes/texte_lc"
DATE: str = "2024-04-20"


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


def get_code_name(code_soup: BeautifulSoup) -> str:
    """
    Retrieve the name of a Code.

    Args:
        code_soup (BeautifulSoup): Code soup.

    Returns:
        str: Code name.
    """
    return code_soup.select(".main-title")[0].text.replace("'", " ").replace(" ", "_")
