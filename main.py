import os
import sys
import time
from openai import OpenAI, RateLimitError, APIError
from dotenv import load_dotenv

def configure_client():
    """Load API key and configure OpenAI Client for Gemini."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("\n[ERROR] GEMINI_API_KEY not found.")
        print("Please create a .env file with: GEMINI_API_KEY=your_key_here\n")
        return None
        
    try:
        # Initialize OpenAI client pointing to Google's endpoint
        client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        return client
    except Exception as e:
        print(f"\n[ERROR] Failed to configure Client: {e}\n")
        return None

def main():
    """Main Chat Loop."""
    print("--- Gemini AI Assistant (Robust) ---")
    print("Type 'exit' to quit.\n")
    
    client = configure_client()
    if not client:
        return

    # Chat History
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    model_name = "gemini-3-flash-preview" # More stable for free tier

    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            # Add user message to history
            messages.append({"role": "user", "content": user_input})
            
            print("Gemini: ...", end='\r')
            
            # Retry Loop for Rate Limiting
            max_retries = 3
            backoff = 2
            
            for attempt in range(max_retries):
                try:
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=messages
                    )
                    reply_content = response.choices[0].message.content
                    
                    # Add assistant reply to history
                    messages.append({"role": "assistant", "content": reply_content})
                    
                    # Print response
                    sys.stdout.write("\033[K")
                    print(f"Gemini: {reply_content}")
                    break # Success, exit retry loop

                except RateLimitError as e:
                    if attempt < max_retries - 1:
                        wait = backoff * (2 ** attempt)
                        sys.stdout.write("\033[K")
                        print(f"[Rate Limit] Retrying in {wait} seconds...", end='\r')
                        time.sleep(wait)
                    else:
                        sys.stdout.write("\033[K")
                        print(f"\n[Error] Rate limit exceeded after retries. Please wait a moment.")
                except APIError as e:
                     sys.stdout.write("\033[K")
                     print(f"\n[Error] API Error: {e}")
                     break
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n[Error] {e}")

if __name__ == "__main__":
    main()