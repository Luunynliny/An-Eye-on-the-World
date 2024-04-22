import pytest
from bs4 import BeautifulSoup
from selenium import webdriver

from src.utils import get_soup, get_code_non_abrogated_articles, get_article_data

CODE_CIVIL_ID: str = "LEGITEXT000006070721"
CODE_CIVIL_ARTICLE_1_ID: str = "LEGIARTI000006419280"
CODE_CIVIL_ARTICLE_2_ID: str = "LEGIARTI000006419281"

CODE_DEONTOLOGIE_ARCHITECTES_ID: str = "LEGITEXT000006074232"
CODE_DEONTOLOGIE_ARCHITECTES_ARTICLE_1_ID: str = "LEGIARTI000006842411"


@pytest.fixture
def driver():
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")

    driver = webdriver.Firefox(options=options)
    yield driver

    driver.quit()


def test_get_soup():
    with open("examplecom_response.txt", "r") as f:
        text = f.read()

    soup = get_soup("https://example.com")

    assert isinstance(soup, BeautifulSoup)
    assert BeautifulSoup(text, "html.parser") == soup


def test_get_code_non_abrogated_articles():
    article_ids = get_code_non_abrogated_articles(CODE_CIVIL_ID)

    assert isinstance(article_ids, list)
    assert len(article_ids) == 2883
    assert isinstance(article_ids[0], str)
    assert article_ids[0] == CODE_CIVIL_ARTICLE_1_ID

    article_ids = get_code_non_abrogated_articles(CODE_DEONTOLOGIE_ARCHITECTES_ID)

    assert isinstance(article_ids, list)
    assert len(article_ids) == 48
    assert isinstance(article_ids[0], str)
    assert article_ids[0] == CODE_DEONTOLOGIE_ARCHITECTES_ARTICLE_1_ID


def test_get_article_data(driver):
    # Article is quoted within other Codes
    article_data = get_article_data(CODE_CIVIL_ARTICLE_1_ID, driver)

    assert isinstance(article_data, tuple)
    assert len(article_data) == 2

    assert isinstance(article_data[0], str)
    assert article_data[0] == "Article 1"

    assert isinstance(article_data[1], list)
    assert len(article_data[1]) == 2
    assert isinstance(article_data[1][0], str)
    assert article_data[1] == ["LEGIARTI000031367546", "LEGIARTI000006450479"]

    # Article is not quoted within other Codes
    article_data = get_article_data(CODE_CIVIL_ARTICLE_2_ID, driver)

    assert isinstance(article_data, tuple)
    assert len(article_data) == 2

    assert isinstance(article_data[0], str)
    assert article_data[0] == "Article 2"

    assert isinstance(article_data[1], list)
    assert len(article_data[1]) == 0

    # Article is never quoted
    article_data = get_article_data(CODE_DEONTOLOGIE_ARCHITECTES_ARTICLE_1_ID, driver)

    assert isinstance(article_data, tuple)
    assert len(article_data) == 2

    assert isinstance(article_data[0], str)
    assert article_data[0] == "Article 1"

    assert isinstance(article_data[1], list)
    assert len(article_data[1]) == 0
