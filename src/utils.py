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
        code_id (str): id of a Code.

    Returns:
        list[str]: ids of non-abrogated articles within the Code.
    """
    soup = get_soup(join(ENV["CODES_DB_URL"], code_id, ENV["DATE"]))
    return [element.get("id")[3:] for element in soup.select(".articleLink:not(.abrogated)")]


def get_article_data(article_id: str) -> tuple[str, list[str]]:
    """
    Args:
        article_id (): id of an Article.

    Returns:
        tuple[str, list[str]]: name of the Article and Codes' Articles' id quoting the Article.
    """
    ###
    # An Article page could contain a button to display all the other Codes' Articles where the Article is quoted
    # If so, we need to click on this button to make these informations appear on the page
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")

    driver = webdriver.Firefox(options=options)
    driver.get(join(ENV["ARTICLES_DB_URL"], article_id, ENV["DATE"]))

    is_article_quoted = True
    try:
        driver.find_element(By.ID, f"tip-tab-liens-{article_id}-1-button").click()
    except NoSuchElementException:
        is_article_quoted = False

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    ###

    name = soup.select(".name-article span")[0].text
    relative_codes_article_ids = []

    if is_article_quoted:
        # Only keep quotations from other Code's Articles
        for link in soup.select(".relative-link li a"):
            _id = link.get("href").split("#")[1]
            text = link.text

            if text.split()[0] in ["Code", "Livre"]:  # "Livre" is for the Livre des procédures fiscales (2024-04-20)
                relative_codes_article_ids.append(_id)

    driver.quit()  # Exit now to avoid inconsistencies
    return name, relative_codes_article_ids
