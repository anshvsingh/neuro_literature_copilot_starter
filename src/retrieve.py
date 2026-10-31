import json
import argparse
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent.parent
CHUNKS_FILE = ROOT / "data" / "processed" / "chunks.jsonl"
DB_DIR = ROOT / "data" / "processed" / "chroma_db"
COLLECTION_NAME = "neuro_papers"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_chunks():
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            f"{CHUNKS_FILE} not found. Run: python -m src.ingest"
        )

    with CHUNKS_FILE.open("r", encoding="utf-8") as file:
        chunks = [json.loads(line) for line in file if line.strip()]

    if not chunks:
        raise ValueError("No chunks found in chunks.jsonl")

    return chunks


def build_index():
    chunks = load_chunks()
    print(f"Loading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    client = chromadb.PersistentClient(path=str(DB_DIR))

    # Rebuild the collection so repeated runs do not create duplicates.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    batch_size = 64

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]

        documents = [item["text"] for item in batch]
        embeddings = model.encode(
            documents,
            normalize_embeddings=True,
            show_progress_bar=False,
        ).tolist()

        metadata = [
            {
                "paper_id": str(item["paper_id"]),
                "condition": str(item["condition"]),
                "condition_key": str(item["condition_key"]),
                "source_file": str(item["source_file"]),
                "page": int(item["page"]),
                "chunk_index_on_page": int(item["chunk_index_on_page"]),
            }
            for item in batch
        ]

        collection.add(
            ids=[item["chunk_id"] for item in batch],
            documents=documents,
            embeddings=embeddings,
            metadatas=metadata,
        )

        print(f"Indexed {min(start + batch_size, len(chunks))}/{len(chunks)}")

    print(f"\nIndex complete. Stored {collection.count()} chunks.")
    print(f"Database: {DB_DIR}")


def search(query, top_k=5, condition=None):
    client = chromadb.PersistentClient(path=str(DB_DIR))
    collection = client.get_collection(COLLECTION_NAME)

    model = SentenceTransformer(MODEL_NAME)
    query_embedding = model.encode(
        [query], normalize_embeddings=True
    ).tolist()

    search_args = {
        "query_embeddings": query_embedding,
        "n_results": min(top_k, collection.count()),
        "include": ["documents", "metadatas", "distances"],
    }

    if condition:
        search_args["where"] = {"condition_key": condition}

    results = collection.query(**search_args)
    evidence = []

    print(f"\\nQuestion: {query}")
    print(f"Retrieved {len(results['ids'][0])} passages\\n")

    for rank, (chunk_id, document, metadata, distance) in enumerate(
        zip(
            results["ids"][0],
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ),
        start=1,
    ):
        item = {
            "rank": rank,
            "chunk_id": chunk_id,
            "paper_id": metadata["paper_id"],
            "condition": metadata["condition"],
            "condition_key": metadata["condition_key"],
            "page": metadata["page"],
            "source_file": metadata["source_file"],
            "cosine_distance": float(distance),
            "passage": document,
        }
        evidence.append(item)

        print("=" * 80)
        print(f"Result {rank} | Chunk: {chunk_id}")
        print(f"Paper: {metadata['paper_id']}")
        print(f"Condition: {metadata['condition']}")
        print(f"Page: {metadata['page']}")
        print(f"Source: {metadata['source_file']}")
        print(f"Cosine distance: {distance:.4f}")
        print("\\nPassage:")
        print(document[:1800])
        print()

    return evidence


def main():
    parser = argparse.ArgumentParser(description="Neuro paper semantic retrieval")
    parser.add_argument(
        "--build", action="store_true", help="Build or rebuild the vector index"
    )
    parser.add_argument("--query", type=str, help="Research question to search")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument(
        "--condition",
        choices=["alzheimers", "epilepsy", "parkinsons", "schizophrenia"],
        help="Restrict search to one condition",
    )
    args = parser.parse_args()

    if args.build:
        build_index()
    elif args.query:
        search(args.query, args.top_k, args.condition)
    else:
        parser.error("Use --build or --query")


if __name__ == "__main__":
    main()
