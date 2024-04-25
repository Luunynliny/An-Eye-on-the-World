from os.path import join
from typing import Union

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from src.utils import get_soup

ARTICLES_DB_URL = "https://www.legifrance.gouv.fr/codes/article_lc"
DATE: str = "2024-04-20"


def get_article_soup(article_id: str) -> BeautifulSoup:
    """
    Get Code BeautifulSoup objec.

    Args:
        article_id (str): Code id.

    Returns:
        BeautifulSoup: BeautifulSoup object.
    """
    return get_soup(join(ARTICLES_DB_URL, article_id, DATE))


def get_article_name(article_soup: BeautifulSoup) -> str:
    """
    Retrieve the name of an Article.

    Args:
        article_soup (BeautifulSoup): Article soup.

    Returns:
        str: Article name.
    """
    return article_soup.select(".name-article span")[0].text


def is_article_abrogated(article_soup: BeautifulSoup) -> bool:
    """
    Check if an Article has an abrogated.

    Args:
        article_soup (BeautifulSoup): Article soup.

    Returns:
        bool: True if article is abrogated, False otherwise.
    """
    return "depuis" not in article_soup.select(".version-article")[0].text


def get_article_data(article_id: str, driver: webdriver) -> dict[str, Union[str, list[str]]]:
    """
    Retrieve useful data of an Article:
    - Article name
    - quoted Code Article ids

    Args:
        article_id (str): Article id.
        driver (webdriver): webdriver instance.

    Returns:
        dict[str, Union[str, list[str]]]: Article data.
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

    article_soup = BeautifulSoup(driver.page_source, 'html.parser')
    ###

    name = get_article_name(article_soup)

    if is_article_orphan:
        return {"name": name, "quotation_ids": []}

    # Check if Article is quoting
    if (quotations := article_soup.find("strong", text="Cite")) is None:
        return {"name": name, "quotation_ids": []}

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
        if is_article_abrogated(article_soup):
            continue

        quoted_codes_article_ids.append(quoted_article_id)

    return {"name": name, "quotation_ids": quoted_codes_article_ids}
