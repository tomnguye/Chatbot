from os import listdir

def remove_newlines(path: str):
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()
    with open(path, "w", encoding="utf-8") as file:
        text = text.replace("\n", "")
        file.write(text)

def preprocess_directory(path: str):
    for file in listdir(path):
        file_path = path + "/" + file
        remove_newlines(file_path)
