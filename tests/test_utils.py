import pytest
from bs4 import BeautifulSoup
from selenium import webdriver

from src.utils import get_soup, get_code_non_abrogated_articles, get_article_data, get_article_name, \
    is_quoted_article_abrogated, get_code_name

CODE_CIVIL_ID: str = "LEGITEXT000006070721"
CODE_CIVIL_ARTICLE_1_ID: str = "LEGIARTI000006419280"
CODE_CIVIL_ARTICLE_21_19_ID: str = "LEGIARTI000006419879"
CODE_CIVIL_ARTICLE_92_ID: str = "LEGIARTI000006421376"

CODE_DEONTOLOGIE_ARCHITECTES_ID: str = "LEGITEXT000006074232"
CODE_DEONTOLOGIE_ARCHITECTES_ARTICLE_1_ID: str = "LEGIARTI000006842411"

CODE_DOMAINE_ETAT_ID: str = "LEGITEXT000006070208"
CODE_DOMAINE_ETAT_ARTICLE_R1_ID: str = "LEGIARTI000006350500"
CODE_DOMAINE_ETAT_ARTICLE_L3_ID: str = "LEGIARTI000006350304"


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
    # Article quote other Codes Articles
    article_data = get_article_data(CODE_CIVIL_ARTICLE_92_ID, driver)

    assert isinstance(article_data, tuple)
    assert len(article_data) == 2

    assert isinstance(article_data[0], str)
    assert article_data[0] == "Article 92"

    assert isinstance(article_data[1], list)
    assert len(article_data[1]) == 4
    assert isinstance(article_data[1][0], str)
    assert article_data[1] == ["LEGIARTI000006421855", "LEGIARTI000006421836", "LEGIARTI000006421846",
                               "LEGIARTI000039367547"]

    # Article quote abrogated Code Articles
    article_data = get_article_data(CODE_DOMAINE_ETAT_ARTICLE_R1_ID, driver)

    assert isinstance(article_data, tuple)
    assert len(article_data) == 2

    assert isinstance(article_data[0], str)
    assert article_data[0] == "Article R1"

    assert isinstance(article_data[1], list)
    assert len(article_data[1]) == 2
    assert isinstance(article_data[1][0], str)
    assert article_data[1] == ["LEGIARTI000006350687", "LEGIARTI000006350304"]

    # Article does not quoted other Codes Articles
    article_data = get_article_data(CODE_CIVIL_ARTICLE_21_19_ID, driver)

    assert isinstance(article_data, tuple)
    assert len(article_data) == 2

    assert isinstance(article_data[0], str)
    assert article_data[0] == "Article 21-19"

    assert isinstance(article_data[1], list)
    assert len(article_data[1]) == 0

    # Article does not quoted
    article_data = get_article_data(CODE_CIVIL_ARTICLE_1_ID, driver)

    assert isinstance(article_data, tuple)
    assert len(article_data) == 2

    assert isinstance(article_data[0], str)
    assert article_data[0] == "Article 1"

    assert isinstance(article_data[1], list)
    assert len(article_data[1]) == 0

    # Article is an orphan
    article_data = get_article_data(CODE_DEONTOLOGIE_ARCHITECTES_ARTICLE_1_ID, driver)

    assert isinstance(article_data, tuple)
    assert len(article_data) == 2

    assert isinstance(article_data[0], str)
    assert article_data[0] == "Article 1"

    assert isinstance(article_data[1], list)
    assert len(article_data[1]) == 0


def test_get_article_name():
    assert get_article_name(CODE_CIVIL_ARTICLE_1_ID) == "Article 1"
    assert get_article_name(CODE_DEONTOLOGIE_ARCHITECTES_ARTICLE_1_ID) == "Article 1"
    assert get_article_name(CODE_CIVIL_ARTICLE_92_ID) == "Article 92"
    assert get_article_name(CODE_CIVIL_ARTICLE_21_19_ID) == "Article 21-19"


def test_is_quoted_article_abrogated():
    assert not is_quoted_article_abrogated(CODE_CIVIL_ARTICLE_92_ID)
    assert is_quoted_article_abrogated(CODE_DOMAINE_ETAT_ARTICLE_L3_ID)


def test_get_code_name():
    assert get_code_name(CODE_CIVIL_ID) == "Code_civil"
    assert get_code_name(CODE_DEONTOLOGIE_ARCHITECTES_ID) == "Code_de_déontologie_des_architectes"
    assert get_code_name(CODE_DOMAINE_ETAT_ID) == "Code_du_domaine_de_l_Etat"
