import pytest
from selenium import webdriver

from src.article import get_article_data, get_article_name, get_article_soup, is_article_abrogated

CODE_CIVIL_ARTICLE_1_ID: str = "LEGIARTI000006419280"
CODE_CIVIL_ARTICLE_21_19_ID: str = "LEGIARTI000006419879"
CODE_CIVIL_ARTICLE_92_ID: str = "LEGIARTI000006421376"

CODE_DEONTOLOGIE_ARCHITECTES_ARTICLE_1_ID: str = "LEGIARTI000006842411"

CODE_DOMAINE_ETAT_ARTICLE_R1_ID: str = "LEGIARTI000006350500"
CODE_DOMAINE_ETAT_ARTICLE_L3_ID: str = "LEGIARTI000006350304"


@pytest.fixture
def driver():
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")

    driver = webdriver.Firefox(options=options)
    yield driver

    driver.quit()


def test_get_article_name():
    code_civil_article_1_soup = get_article_soup(CODE_CIVIL_ARTICLE_1_ID)
    code_civil_article_21_19_soup = get_article_soup(CODE_CIVIL_ARTICLE_21_19_ID)
    code_deontologie_architectes_article_1_soup = get_article_soup(CODE_DEONTOLOGIE_ARCHITECTES_ARTICLE_1_ID)

    assert get_article_name(code_civil_article_1_soup) == "Article 1"
    assert get_article_name(code_civil_article_21_19_soup) == "Article 21-19"
    assert get_article_name(code_deontologie_architectes_article_1_soup)


def test_is_article_abrogated():
    code_civil_article_92_soup = get_article_soup(CODE_CIVIL_ARTICLE_92_ID)
    code_domaine_etat_article_L3_soup = get_article_soup(CODE_DOMAINE_ETAT_ARTICLE_L3_ID)

    assert not is_article_abrogated(code_civil_article_92_soup)
    assert is_article_abrogated(code_domaine_etat_article_L3_soup)


def test_get_article_data(driver):
    # Article quote other Codes Articles
    article_data = get_article_data(CODE_CIVIL_ARTICLE_92_ID, driver)

    assert isinstance(article_data, dict)
    assert list(article_data.keys()) == ["name", "quotation_ids"]
    for value, value_type in zip(article_data.values(), [str, list]):
        assert isinstance(value, value_type)

    assert article_data == {"name": "Article 92",
                            "quotation_ids": ["LEGIARTI000006421855", "LEGIARTI000006421836", "LEGIARTI000006421846",
                                              "LEGIARTI000039367547"]}

    # Article quote abrogated Code Articles
    article_data = get_article_data(CODE_DOMAINE_ETAT_ARTICLE_R1_ID, driver)

    assert isinstance(article_data, dict)
    assert list(article_data.keys()) == ["name", "quotation_ids"]
    for value, value_type in zip(article_data.values(), [str, list]):
        assert isinstance(value, value_type)

    assert article_data == {"name": "Article R1",
                            "quotation_ids": ["LEGIARTI000006350687", "LEGIARTI000006350304"]}

    # Article does not quoted other Codes Articles
    article_data = get_article_data(CODE_CIVIL_ARTICLE_21_19_ID, driver)

    assert isinstance(article_data, dict)
    assert list(article_data.keys()) == ["name", "quotation_ids"]
    for value, value_type in zip(article_data.values(), [str, list]):
        assert isinstance(value, value_type)

    assert article_data == {"name": "Article 21-19",
                            "quotation_ids": []}

    # Article does not quoted
    article_data = get_article_data(CODE_CIVIL_ARTICLE_1_ID, driver)

    assert isinstance(article_data, dict)
    assert list(article_data.keys()) == ["name", "quotation_ids"]
    for value, value_type in zip(article_data.values(), [str, list]):
        assert isinstance(value, value_type)

    assert article_data == {"name": "Article 1",
                            "quotation_ids": []}

    # Article is an orphan
    article_data = get_article_data(CODE_DEONTOLOGIE_ARCHITECTES_ARTICLE_1_ID, driver)

    assert isinstance(article_data, dict)
    assert list(article_data.keys()) == ["name", "quotation_ids"]
    for value, value_type in zip(article_data.values(), [str, list]):
        assert isinstance(value, value_type)

    assert article_data == {"name": "Article 1",
                            "quotation_ids": []}
