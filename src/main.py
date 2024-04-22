from icecream import ic
from selenium import webdriver

from utils import get_code_non_abrogated_articles, get_article_data

CODE_DEONTOLOGIE_ARCHITECTES_ID: str = "LEGITEXT000006074232"
articles: dict[str, dict[str, list[str]]] = {}

options = webdriver.FirefoxOptions()
options.add_argument("-headless")

driver = webdriver.Firefox(options=options)

for article_id in get_code_non_abrogated_articles(CODE_DEONTOLOGIE_ARCHITECTES_ID):
    article_name, article_links = get_article_data(article_id, driver)

    ic(article_name, article_links)

driver.quit()
