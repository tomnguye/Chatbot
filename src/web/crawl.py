import requests 
from bs4 import BeautifulSoup

class Page:
    def __init__(self, name: str):
        self.link: str = name
        self.children = []

#crawl a site from root address returning pages visited as a tree
def crawl(root:str, depth_limit:int, bredth_limit:int = 10):
    current_url = root
    response = requests.get(current_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    #get next links
    link_elements = soup.select("a[href]")
    steps = set()
    for link_element in link_elements:
        url = link_element["href"]
        if url.startswith(current_url) and url != current_url:
            tail = url.replace(current_url + "/", "")
            if (tail != url): 
                shortest_step = tail.split("/")[0]
                steps.add(current_url + "/" + shortest_step)
    node = Page(root)
    count = 0
    #crawl to children
    if (depth_limit > 0):
        for step in steps:
            count += 1
            child = crawl(step, depth_limit - 1)
            node.children.append(child)
            if count >= bredth_limit:
                break
    return node
