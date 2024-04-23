from os.path import join, dirname

import requests
from bs4 import BeautifulSoup
from dotenv import dotenv_values
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

ENV: dict[str, str] = dotenv_values(join(dirname(__file__), ".env"))


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def get_code_non_abrogated_articles(code_id: str) -> list[str]:
    """
    Args:
        code_id (str): Code id.

    Returns:
        list[str]: ids of non-abrogated articles within the Code.
    """
    soup = get_soup(join(ENV["CODES_DB_URL"], code_id, ENV["DATE"]))
    return [element.get("id")[3:] for element in soup.select(".articleLink:not(.abrogated)")]


def get_article_data(article_id: str, driver: webdriver) -> tuple[str, list[str]]:
    """
    Args:
        article_id (str): Article id.
        driver (webdriver): webdriver instance.

    Returns:
        tuple[str, list[str]: Article name and quoted Codes Article ids.
    """
    ###
    # An Article page could contain a button to display all the other Codes' Articles quoted within the Article
    # If so, we need to click on this button to make this information appear on the page
    driver.get(join(ENV["ARTICLES_DB_URL"], article_id, ENV["DATE"]))

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
        article_id = link.get("href").split("#")[1]
        article_name = link.text

        if article_name.split()[0] in ["Code",
                                       "Livre"]:  # Livre des procédures fiscales (2024-04-20)
            quoted_codes_article_ids.append(article_id)

    return name, quoted_codes_article_ids


def get_article_name(article_id: str) -> str:
    """
    Args:
        article_id (str): Article id.

    Returns:
        str: Article name.
    """
    soup = get_soup(join(ENV["ARTICLES_DB_URL"], article_id, ENV["DATE"]))
    return soup.select(".name-article span")[0].text
