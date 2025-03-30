import src.database.update_database as update_database
from src.web import preprocess, scape_old

source = "./res/documents/web_data"
urls = ["https://www.planning.act.gov.au/community/build-or-renovate"]

for url in urls:
    scape_old.get_data(url, 4, source)
    preprocess.preprocess_directory(source + "/" + scape_old.url_encode(url))
    # update_database.upload(source + "/" + web_scaper.url_encode(url))