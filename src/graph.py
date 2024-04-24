from selenium import webdriver

from src.gexf_document import GEXFDocument
from src.utils import get_code_non_abrogated_articles, get_article_data, get_article_name, get_code_name


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
    seen_article_ids: set[str] = set()

    for article_id in get_code_non_abrogated_articles(code_id):
        article_data = get_article_data(article_id, driver)

        if article_id not in seen_article_ids:
            # Create GEXF node
            gexf_doc.add_node(article_id, article_data["name"])
            seen_article_ids.add(article_id)

        # Create quotation links
        for quoted_article_id in article_data["quotation_ids"]:
            gexf_doc.add_edge(article_id, quoted_article_id)

            if quoted_article_id not in seen_article_ids:
                # Create quoted nodes
                gexf_doc.add_node(quoted_article_id, get_article_name(quoted_article_id))
                seen_article_ids.add(quoted_article_id)

    # Save result
    gexf_doc.save(get_code_name(code_id))
    driver.quit()
