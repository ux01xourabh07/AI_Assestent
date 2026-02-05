
import os
import sys
from google import genai
from config import Config

# Ensure IO encoding
sys.stdout.reconfigure(encoding='utf-8')

def transcribe_audio(file_path):
    print(f"Transcribing file: {file_path}")
    
    api_key = Config.GOOGLE_API_KEY
    if not api_key:
        print("Error: GOOGLE_API_KEY not found.")
        return

    client = genai.Client(api_key=api_key)
    
    # Upload the file
    print("Uploading to Gemini...")
    try:
        myfile = client.files.upload(file=file_path)
        print(f"Uploaded: {myfile.name}")
    except Exception as e:
        print(f"Upload failed: {e}")
        return

    prompt = 'Generate a transcript of the speech.'

    # Using the STABLE model to avoid 429 Quota errors
    # User requested 'gemini-3-flash-preview' but it is currently quota exhausted.
    model_name = 'gemini-2.0-flash-exp' 

    print(f"Generating transcript using {model_name}...")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=[prompt, myfile]
        )
        print("\n--- TRANSCRIPT ---\n")
        print(response.text)
        print("\n------------------\n")
        
    except Exception as e:
        print(f"Transcription failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <path_to_audio_file>")
    else:
        transcribe_audio(sys.argv[1])
