from os.path import join

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from src.utils import get_soup

ARTICLES_DB_URL = "https://www.legifrance.gouv.fr/codes/article_lc"
DATE: str = "2024-04-20"

ARTICLE_HIERARCHY = ["LO",  # Article LO119 Code électoral (2024-04-20)
                     "L",  # Article L101-1 Code de l'urbanisme (2024-04-20)
                     "R**",  # Article R**273 Code électoral (2024-04-20)
                     "R*",  # Article R*121-1-1 Code de l'urbanisme (2024-04-20)
                     "R",  # Article R1 Code électoral (2024-04-20)
                     "D*",  # Article D*752-25 Code monétaire et financier (2024-04-20)
                     "D",  # Article D1 Code de procédure pénale (2024-04-20)
                     "A"]  # Article A424-1 Code de l'urbanisme (2024-04-20)


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
    Get Article name.

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


def get_article_text_length(article_soup: BeautifulSoup) -> int:
    """
    Get Article text length.

    Args:
        article_soup (BeautifulSoup): Article soup.

    Returns:
        int: Article number of words.
    """
    return len(article_soup.select(".list-article-consommation .content p")[0].text.strip().split())


def get_article_quote_ids(article_soup: BeautifulSoup, driver: webdriver) -> list[str]:
    """
    Get Code Article ids quoted by the Article.

    Args:
        article_soup (BeautifulSoup): Article soup.
        driver (webdriver): webdriver instance.

    Returns:
        list[str]: quoted Article ids.
    """
    article_id = article_soup.select(".name-article")[0].attrs["data-anchor"]

    ###
    # An Article page could contain a button to display all the other Codes' Articles quoted within the Article
    # If so, we need to click on this button to make this information appear on the page
    driver.get(join(ARTICLES_DB_URL, article_id, DATE))

    is_article_orphan = False
    try:
        driver.find_element(By.ID, f"tip-tab-liens-{article_id}-1-button").click()
    except NoSuchElementException:
        is_article_orphan = True

    clicked_article_soup = BeautifulSoup(driver.page_source, 'html.parser')
    ###

    if is_article_orphan:
        return []

    # Check if Article is quoting
    if (quotations := clicked_article_soup.find("strong", text="Cite")) is None:
        return []

    # Only keep quotations of other Code's Articles
    quoted_codes_article_ids = []
    for link in quotations.find_next("ul").select("a"):
        quoted_article_id = link.get("href").split("#")[1]
        link_name = link.text

        if link_name.split()[0] not in ["Code",
                                        "Livre"]:  # Livre des procédures fiscales (2024-04-20)
            continue

        # Avoid abrogated unremoved quotation (e.g. Code du domaine de l'Etat Article R1 (2024-04-20))
        if "art." not in link_name:
            continue
        if is_article_abrogated(get_article_soup(quoted_article_id)):
            continue

        quoted_codes_article_ids.append(quoted_article_id)

    return quoted_codes_article_ids


def get_article_hierarchy(article_soup: BeautifulSoup) -> str:
    """
    Get article hierarchy.

    Args:
        article_soup (BeautifulSoup): Article soup.

    Returns:
        str: Article hierarchy group.
    """
    article_code = get_article_name(article_soup).split()[1]

    for code in ARTICLE_HIERARCHY:
        if code in article_code:
            return code

    # Special case for the Code with no division in parts
    # Code civil, Code de déontologie architectes...
    return "NC"


def get_article_code_id(article_soup: BeautifulSoup) -> str:
    """
    Get Article parent Code id.
    Args:
        article_soup (BeautifulSoup): Article soup.

    Returns:
        str: Code id.
    """
    return article_soup.select(".summary-header a")[0].attrs["href"].split("/")[3]
