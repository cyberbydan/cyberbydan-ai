"""
chat.py
-------
Command-line interface (CLI) for CyberByDan AI
"""

from chat.engine import chat

def main():
    print("=" * 60)
    print("CyberByDan AI")
    print("=" * 60)

    while True:
        question = input("\nYou: ")

        if question.lower() in {
            "exit",
            "quit",
            "bye",
            "q",
        }:
            print("\nGoodbye!")
            break

        answer = chat(question)
        print()
        print(answer)

if __name__ == "__main__":
    main()
