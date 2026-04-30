from core.brain import Brain

def main():
    brain = Brain()
    print("JARVIS online. Talk to me.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("JARVIS offline.")
            break

        response = brain.chat(user_input)
        print(f"\nJARVIS: {response}\n")

if __name__ == "__main__":
    main()