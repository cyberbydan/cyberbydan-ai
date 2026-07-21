from loaders import discover_documents

def main():
    documents = discover_documents()

    print(f"\nFound {len(documents)} document(s):\n")

    for doc in documents:
        print(doc)

if __name__ == "__main__":
    main()
