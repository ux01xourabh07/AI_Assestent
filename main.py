
import sys
import time
from systems import Systems

def main():
    print("Launching Shipra AI System (Voice CLI)...")
    
    # Initialize Systems
    brain = Systems.get_brain()
    audio = Systems.get_audio()
    
    print("\n--- SYSTEM READY ---")
    
    # Intro
    intro_text = "Namaste! Main Pushpak O 2 ki AI Assistant hoon. Boliye, main kya kar sakti hoon?"
    audio.speak(intro_text)
    
    while True:
        try:
            # 1. Listen
            user_text = audio.listen()
            
            if user_text:
                # 2. Check for Exit
                if "exit" in user_text.lower() or "bye" in user_text.lower() or "stop" in user_text.lower():
                    audio.speak("Dhanyavaad. Alvida!")
                    break
                
                # 3. Brain Processing
                response_text = brain.chat(user_text)
                
                # 4. Speak Response
                audio.speak(response_text)
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Loop Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()