from src.database.embedding import get_embedding_function
from langchain_chroma import Chroma

CHROMA_PATH = "./data_base"

embedding_function = get_embedding_function()
db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding_function)

def query_rag(query_text: str):
    results = db.similarity_search_with_score(query_text, k=4)
    filtered_results = []
    for result in results:
        if result[1] < 0.8:
            filtered_results.append(result)
    if (len(filtered_results) == 0):
        return ""
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in filtered_results])
    return context_text
