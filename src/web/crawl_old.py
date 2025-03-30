import requests 
from bs4 import BeautifulSoup

def crawl(root_url: str, max_crawl: int = 4):
    urls_to_visit = [root_url]
    crawl_count = 0
    while urls_to_visit and crawl_count < max_crawl: 
        crawl_count += 1
        # select site from stack
        current_url = urls_to_visit.pop()
        response = requests.get(current_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # get links from site
        link_elements = soup.select("a[href]")
        for link_element in link_elements:
            url = link_element["href"]
            if not url.startswith("http"):
                absolute_url = requests.compat.urljoin(root_url, url)
            else: 
                absolute_url = url
            # push new links
            if (absolute_url.startswith(root_url)
                and absolute_url not in urls_to_visit):
                urls_to_visit.append(absolute_url)
    return urls_to_visit
