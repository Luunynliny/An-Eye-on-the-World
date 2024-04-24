from os.path import join

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

ARTICLES_DB_URL = "https://www.legifrance.gouv.fr/codes/article_lc"
CODES_DB_URL = "https://www.legifrance.gouv.fr/codes/texte_lc"
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


def get_code_non_abrogated_articles(code_id: str) -> list[str]:
    """
    Get the non-abrogated Articles from a Code.

    Args:
        code_id (str): Code id.

    Returns:
        list[str]: non-abrogated article ids.
    """
    soup = get_soup(join(CODES_DB_URL, code_id, DATE))
    return [element.get("id")[3:] for element in soup.select(".articleLink:not(.abrogated)")]


def get_article_data(article_id: str, driver: webdriver) -> tuple[str, list[str]]:
    """
    Retrieve useful data of an Article:
    - Article name
    - quoted Code Article ids

    Args:
        article_id (str): Article id.
        driver (webdriver): webdriver instance.

    Returns:
        tuple[str, list[str]: Article name and quoted Codes Article ids.
    """
    ###
    # An Article page could contain a button to display all the other Codes' Articles quoted within the Article
    # If so, we need to click on this button to make this information appear on the page
    driver.get(join(ARTICLES_DB_URL, article_id, DATE))

    is_article_orphan = False
    try:
        driver.find_element(By.ID, f"tip-tab-liens-{article_id}-1-button").click()
    except NoSuchElementException:
        is_article_orphan = True

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    ###

    name = get_article_name(article_id)

    if is_article_orphan:
        return name, []

    # Check if Article is quoting
    if (quotations := soup.find("strong", text="Cite")) is None:
        return name, []

    # Only keep quotations of other Code's Articles
    quoted_codes_article_ids = []
    for link in quotations.find_next("ul").select("a"):
        quoted_article_id = link.get("href").split("#")[1]
        quoted_article_name = link.text

        if quoted_article_name.split()[0] not in ["Code",
                                                  "Livre"]:  # Livre des procédures fiscales (2024-04-20)
            continue

        # Avoid abrogated unremoved quotation (e.g. Code du domaine de l'Etat Article R1 (2024-04-20))
        if "art." not in quoted_article_name:
            continue
        if is_quoted_article_abrogated(quoted_article_id):
            continue

        quoted_codes_article_ids.append(quoted_article_id)

    return name, quoted_codes_article_ids


def get_article_name(article_id: str) -> str:
    """
    Retrieve the name of an Article.

    Args:
        article_id (str): Article id.

    Returns:
        str: Article name.
    """
    soup = get_soup(join(ARTICLES_DB_URL, article_id, DATE))
    return soup.select(".name-article span")[0].text


def is_quoted_article_abrogated(quoted_article_id: str) -> bool:
    """
    Check if an Article has an abrogated.

    Args:
        quoted_article_id (): Article id.

    Returns:
        bool: True if article is abrogated, False otherwise.
    """
    soup = get_soup(join(ARTICLES_DB_URL, quoted_article_id, DATE))
    return "depuis" not in soup.select(".version-article")[0].text


def get_code_name(code_id: str) -> str:
    """
    Retrieve the name of a Code.

    Args:
        code_id (str): Code id.

    Returns:
        str: Code name.
    """
    soup = get_soup(join(CODES_DB_URL, code_id, DATE))
    return soup.select(".main-title")[0].text.replace("'", " ").replace(" ", "_")
