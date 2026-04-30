from core.brain import Brain
from voice.listener import Listener
from voice.speaker import Speaker

def main():
    brain = Brain()
    listener = Listener()
    speaker = Speaker()
    
    print("\nJARVIS online. Press Enter to talk, speak, then press Enter again to stop.\n")

    while True:
        try:
            input("[ Press Enter to speak ]")
            user_input = listener.listen()
            
            if not user_input:
                print("Didn't catch that. Try again.")
                continue
                
            print(f"\nYou: {user_input}")
            
            if any(word in user_input.lower() for word in ["exit", "quit", "goodbye", "shut down"]):
                speaker.speak("Shutting down. Goodbye Anady.")
                break
                
            response = brain.chat(user_input)
            speaker.speak(response)

            if any(word in user_input.lower() for word in ["exit", "quit", "goodbye", "shut down", "close yourself"]):
                speaker.speak("Got it. Shutting down. Goodbye Anady.")
                break
            
        except KeyboardInterrupt:
            speaker.speak("Shutting down. Goodbye Anady.")
            break

if __name__ == "__main__":
    main()