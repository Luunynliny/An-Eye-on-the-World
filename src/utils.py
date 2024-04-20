import bs4.element as bs4e
import requests
from bs4 import BeautifulSoup


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def get_non_abrogated_articles(soup: BeautifulSoup) -> bs4e.ResultSet:
    return soup.select(".articleLink:not(.abrogated)")


soup = get_soup("https://example.com")
