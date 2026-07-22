from chat.retriever import retrieve

results = retrieve(
    "Where are my backup scripts?",
    n_results=3,
)

for result in results:

    print("-" * 60)

    print(result["document"])
    print(result["section"])

    print()

    print(result["content"][:300])
