from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from src.database.embedding import get_embedding_function
from langchain_chroma import Chroma
from os import listdir

CHROMA_PATH = "./data_base"

def load_documents(source: str, type: str = "pdf"):
    if type == "pdf":
        document_loader = PyPDFDirectoryLoader(source)
        return document_loader.load()
    if type == "txt":
        text = []
        for file in listdir(source):
            text_loader = TextLoader(source + "/" + file, "utf-8")
            docs = text_loader.load()
            for doc in docs:
                text.append(doc)
        return text

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def encode_chunks(chunks: list[Document]):
    last_page_id = None 
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        
        current_page_id = f"{source}:{page}"
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0
        last_page_id = current_page_id
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        chunk.metadata["id"] = chunk_id

def add_to_chroma(chunks: list[Document]):
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_function()
    )

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
    if len(new_chunks) > 0:
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)

def upload(path):
    documents = load_documents(path, "txt")
    chunks = split_documents(documents)
    encode_chunks(chunks)
    add_to_chroma(chunks)

