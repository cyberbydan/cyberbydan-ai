from ai.core.embedder import create_embeddings

texts = [
    "Jellyfin streams media.",
    "Restic creates backups.",
    "Ollama generates embeddings.",
    "Grafana visualizes metrics.",
]

vectors = create_embeddings(texts)

print(f"Created {len(vectors)} embeddings.\n")

for i, vector in enumerate(vectors, start=1):
    print(f"Embedding {i}:")
    print(f"Dimensions: {len(vector)}")
    print(vector[:5])  # Print the first 5 elements of the embedding vector
    print()  # Print a newline for better readability
