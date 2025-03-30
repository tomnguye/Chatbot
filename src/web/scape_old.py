
import requests
from bs4 import BeautifulSoup
from .crawl_old import crawl
import os

# removes "/"" from string
def encode(text: str, remove: str = None):
    if remove != None:
        text = text.replace(remove, "")
    output = text.replace("/", " ")
    return output

# removes "https" from string
def url_encode(text):
    return encode(text, "https:")

# get text from site
def scrape_text(url: str):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

# get text from site and write into txt files
def get_data(root: str, depth: int, store: str):
    urls = crawl(root, depth)
    file_location = store + "/" + url_encode(root)
    for url in urls:
        print(url)
        file_name = encode(url, root) + ".txt"
        print(file_name)
        os.makedirs(os.path.dirname(file_location + "/" + file_name), exist_ok=True)
        directory_content = os.listdir(file_location) 
        exists = False
        for file in directory_content:
            if file == file_name:
                exists = True
                break
        if (not exists):
            text = scrape_text(url)
            with open(file_location + "/" + file_name, "w", encoding="utf-8") as file:
                file.write(text)

