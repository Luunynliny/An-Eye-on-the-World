from selenium import webdriver

from src.article import get_article_name, get_article_soup, get_article_quote_ids, get_article_hierarchy, \
    get_article_text_length, get_article_code_id
from src.code import get_code_non_abrogated_articles, get_code_name, get_code_soup
from src.gexf_document import GEXFDocument


def create_code_graph(code_id: str) -> None:
    """
    Create a GEFX document graph of a Code.

    Args:
        code_id (str): Code id.

    Returns:
        None
    """
    # Init webdriver
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")

    driver = webdriver.Firefox(options=options)

    # Init GEXF document
    gexf_doc: GEXFDocument = GEXFDocument()

    # Retrieve all Code Articles
    code_soup = get_code_soup(code_id)
    seen_article_ids: set[str] = set()

    for article_id in get_code_non_abrogated_articles(code_soup):
        article_soup = get_article_soup(article_id)

        if article_id not in seen_article_ids:
            article_quote_ids = get_article_quote_ids(article_soup, driver)

            # Create GEXF node
            gexf_doc.add_node(article_id, get_article_name(article_soup),
                              node_attributes=[code_id, get_article_hierarchy(article_soup),
                                               str(get_article_text_length(article_soup)),
                                               str(len(article_quote_ids))])

            seen_article_ids.add(article_id)

        # Create quotation links
        for quoted_article_id in article_quote_ids:
            quoted_article_soup = get_article_soup(quoted_article_id)
            gexf_doc.add_edge(article_id, quoted_article_id)

            if quoted_article_id not in seen_article_ids:
                # Create quoted nodes
                gexf_doc.add_node(quoted_article_id, get_article_name(quoted_article_soup),
                                  node_attributes=[get_article_code_id(quoted_article_soup),
                                                   get_article_hierarchy(quoted_article_soup),
                                                   str(get_article_text_length(quoted_article_soup)),
                                                   str(len(get_article_quote_ids(quoted_article_soup, driver)))])

                seen_article_ids.add(quoted_article_id)

    # Save result
    gexf_doc.save(get_code_name(code_soup))
    driver.quit()
