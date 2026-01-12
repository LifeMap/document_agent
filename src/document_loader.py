from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path = "assets/2026_jaykim.txt"

def load_text_document():
    loader = TextLoader(file_path)
    data = loader.load()
    return data

def chunk_text_document():
    data = load_text_document()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=30,
        length_function=len,
    )
    text_chunks = text_splitter.split_documents(data)

    return text_chunks
    

def main():
    text_chunks = chunk_text_document()
    print(text_chunks) 
    # 300/20 : len() = 46
    # 500/20 : len() = 23
    # 500/10 : len() = 23

if __name__ == "__main__":
    main()

