import requests
from bs4 import BeautifulSoup
from src.web.crawl import crawl, Page
import os

# get text from webpage
def scrape_page(url: str):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

# get text from website and store it
def scrape_site(root: Page, dir: str, parent: str = ""):
    page_name = root.link.split("/")[-1]
    partial_file_loc = page_name if parent == "" else parent + "/" + page_name
    file_loc = dir + "/" + partial_file_loc 
    os.makedirs(os.path.dirname(file_loc + ".txt"), exist_ok=True)
    directory_content = os.listdir(dir + "/" + parent)
    # fetch and write page contents if non existant
    if (not page_name in directory_content):
        text = scrape_page(root.link)
        with open(file_loc + ".txt", "w", encoding="utf-8") as file:
                file.write(text)
    # continue on child nodes
    for url in root.children:
        scrape_site(url, dir, partial_file_loc)

tree = crawl("https://www.planning.act.gov.au/community/build-or-renovate", 4)
scrape_site(tree, "./res/documents/web_data")