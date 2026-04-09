import os
import chromadb

def get_collection():
    client = chromadb.PersistentClient(
        path=os.path.join(os.path.dirname(__file__), "..", "chromadb_store")
    )
    collection = client.get_or_create_collection(
        name="sql_examples",
        metadata={"hnsw:space": "cosine"}
    )
    return collection

def add_example(question, sql):
    collection = get_collection()
    collection.add(
        documents=[question],
        metadatas=[{"sql": sql}],
        ids=[str(abs(hash(question)))]
    )
    print(f"Added: {question[:50]}...")

def find_similar(question, n_results=2):
    collection = get_collection()

    count = collection.count()
    if count == 0:
        return []

    results = collection.query(
        query_texts=[question],
        n_results=min(n_results, count)
    )

    examples = []
    for i in range(len(results["documents"][0])):
        examples.append({
            "question": results["documents"][0][i],
            "sql":      results["metadatas"][0][i]["sql"]
        })
    return examples

def get_count():
    collection = get_collection()
    return collection.count()