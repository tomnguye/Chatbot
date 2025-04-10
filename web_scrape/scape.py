import requests
from bs4 import BeautifulSoup
from web.crawl import crawl, Page
import os
import sys

# get text from webpage
def scrape_page(url: str):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

# get text from website and store it
def scrape_site(root: Page, dir: str):
    page_name = root.link.split("/")[-1]
    file_loc = os.path.join(dir, page_name)
    os.makedirs(os.path.dirname(file_loc + ".txt"), exist_ok=True)
    directory_content = os.listdir(dir)
    # fetch and write page contents if non existant
    if (not page_name in directory_content):
        text = scrape_page(root.link)
        with open(file_loc + ".txt", "w", encoding="utf-8") as file:
                file.write(text)
    # continue on child nodes
    for url in root.children:
        scrape_site(url, file_loc)

# "https://www.planning.act.gov.au/community/build-or-renovate"
def main(path):
    tree = crawl(path, 4)
    scrape_site(tree, "./res/documents/web_data")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else: 
        print("Not enough arguments provided")