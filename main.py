
import sys
import time
from systems import Systems

def main():
    print("Launching Shipra AI System (Voice CLI)...")
    
    # Initialize Systems
    brain = Systems.get_brain()
    audio = Systems.get_audio()
    
    print("\n--- SYSTEM READY ---")
    print("Shipra is listening continuously. Speak anytime!\n")
    
    # Intro
    intro_text = "Namaste! Main Pushpak O 2 ki AI Assistant hoon. Boliye, main kya kar sakti hoon?"
    audio.speak(intro_text)
    
    while True:
        try:
            # Continuously listen for user input
            user_text = audio.listen()
            
            if user_text:
                # Check for Exit - respond based on the word used
                if any(word in user_text.lower() for word in ['alvida', 'tata']):
                    audio.speak("Dhanyavaad. Alvida! Jay Shree Ram.")
                    break
                elif any(word in user_text.lower() for word in ['exit', 'bye', 'goodbye', 'stop']):
                    audio.speak("Thank you. Goodbye! Jay Shree Ram.")
                    break
                
                # Brain Processing
                response_text = brain.chat(user_text)
                
                # Speak Response
                audio.speak(response_text)
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Loop Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()