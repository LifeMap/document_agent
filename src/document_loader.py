from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from chromadb import Client as ChromaClient
from chromadb.utils import embedding_functions

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
    

def embed_text_chunks():
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

    chunked_text = chunk_text_document()
    text = [chunk.page_content for chunk in chunked_text]
    embeddings = model.encode(text)
    return embeddings

def save_chromadb(origin_text, chunked_text):
    embedded_text = embed_text_chunks()

    chroma_client = ChromaClient()
    chroma_client.create_collection(name="my_collection")
    # chroma_client.get_collection(name="my_collection").add(
    #     ids = [f"doc_{i}" for i in range(len(embedded_text))],
    #     embeddings = embedded_text.tolist(),
    #     documents = origin_text
    # )
    collection = chroma_client.get_or_create_collection(name="my_collection")

    collection.add(
        ids=[f"doc_{i}" for i in range(len(embedded_text))],
        embeddings=embedded_text.tolist(),
        documents=[chunk.page_content for chunk in chunked_text],
    )
    
    return chroma_client

def chromadb_embed_save():
    chunked_text = chunk_text_document()
    
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    chroma_client = ChromaClient()
    collection = chroma_client.create_collection(
        name="my_collection2",
        embedding_function=embedding_function,
    )
    collection.add(
        ids=[f"doc_{i}" for i in range(len(chunked_text))],
        documents=[chunk.page_content for chunk in chunked_text],
    )
    
    return chroma_client




def search_chromadb(chroma_client, collection_name, query):
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    query_embedding = model.encode([query])
    collection = chroma_client.get_collection(name=collection_name)
    results = collection.query(query_embeddings=query_embedding.tolist(), n_results=5)
    
    for i, doc in enumerate(results['documents'][0]):
      print(f"[결과 {i+1}]")
      print(doc)
      print()

    print("--------------------------------")
    
    for i, (doc, dist) in enumerate(zip(results['documents'][0], results['distances'][0])):
      print(f"[결과 {i+1}] 거리: {dist:.4f}")
      print(doc)
      print()

    return results



def main():
    # # 문서 청킹
    # text_chunks = chunk_text_document()
    # print(text_chunks) 
    # # 300/20 : len() = 46
    # # 500/20 : len() = 23
    # # 500/10 : len() = 23

    # # 문서 임베딩
    # embedded_text = embed_text_chunks()
    # print(embedded_text)

    # # 직접 embed, chromadb 저장
    # origin_text = load_text_document()
    # chunked_text = chunk_text_document()
    # chroma_client = save_chromadb(origin_text, chunked_text)
    # search_chromadb(chroma_client,  "my_collection",  "개발 경력")

    # chromadb embed 저장
    chroma_client = chromadb_embed_save()
    search_chromadb(chroma_client, "my_collection2", "개발 경력")


if __name__ == "__main__":
    main()

