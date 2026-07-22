from ai.core.embedder import create_embedding

vector = create_embedding(
    "Jellyfin streams media from your server to any device, anywhere, for free."
)

print(type(vector))
print(len(vector))
print(vector[:10])  # Print the first 10 elements of the embedding vector
