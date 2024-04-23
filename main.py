from icecream import ic
from selenium import webdriver

from src.gexf_document import GEXFDocument
from src.utils import get_code_non_abrogated_articles, get_article_data, get_article_name

CODE_DEONTOLOGIE_ARCHITECTES_ID: str = "LEGITEXT000006074232"
articles: dict[str, dict[str, list[str]]] = {}

# Init webdriver
options = webdriver.FirefoxOptions()
options.add_argument("-headless")

driver = webdriver.Firefox(options=options)

# Init GEXF document
gexf_doc: GEXFDocument = GEXFDocument()

# Retrieve all Code Articles
seen_article_ids: set[str] = set()

for article_id in get_code_non_abrogated_articles(CODE_DEONTOLOGIE_ARCHITECTES_ID):
    article_name, quoted_article_ids = get_article_data(article_id, driver)

    ic(article_name)

    if article_id not in seen_article_ids:
        # Create GEXF node
        gexf_doc.add_node(article_id, article_name)
        seen_article_ids.add(article_id)

    # Create quotation links
    for quoted_article_id in quoted_article_ids:
        gexf_doc.add_edge(article_id, quoted_article_id)

        if quoted_article_id not in seen_article_ids:
            # Create quoted nodes
            gexf_doc.add_node(quoted_article_id, get_article_name(quoted_article_id))
            seen_article_ids.add(quoted_article_id)

# Save result
gexf_doc.save("Code_de_deontologie")

driver.quit()
