
import os
import time
import json
from google import genai
from google.genai import types
import yt_dlp
from config import Config

class VideoProcessor:
    def __init__(self):
        # Initialize the new GenAI Client
        # Note: Config.GOOGLE_API_KEY must be valid
        self.api_key = Config.GOOGLE_API_KEY
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found.")
            
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-3-flash-preview" # Fallback/Default
        # Using the user's requested model if available, else standard
        # The user requested 'gemini-3-flash-preview', we can try using it or Config.MODEL_NAME
        if "gemini-3" in Config.MODEL_NAME or "preview" in Config.MODEL_NAME:
             self.model_name = Config.MODEL_NAME

    def download_audio(self, youtube_url, output_path="temp_audio"):
        """Downloads audio from YouTube URL using yt-dlp (Native format, no FFmpeg)."""
        print(f"Downloading Audio from: {youtube_url}")
        
        # Cleanup previous runs
        for file in os.listdir("."):
            if file.startswith(output_path + "."):
                try:
                    os.remove(file)
                except:
                    pass

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"{output_path}.%(ext)s",
            'quiet': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
            
        # Find the downloaded file
        final_filename = None
        for file in os.listdir("."):
             if file.startswith(output_path + "."):
                 final_filename = file
                 break
        
        if not final_filename:
            raise FileNotFoundError("Download failed: No audio file found.")

        print(f"Downloaded: {final_filename}")
        return final_filename

    def upload_to_gemini(self, file_path, mime_type=None):
        """Uploads the file to Gemini File API."""
        if not mime_type:
            ext = file_path.split('.')[-1].lower()
            mime_map = {
                'mp3': 'audio/mp3',
                'wav': 'audio/wav',
                'm4a': 'audio/x-m4a',
                'aac': 'audio/aac',
                'flac': 'audio/flac',
                'webm': 'audio/webm',
                'ogg': 'audio/ogg'
            }
            mime_type = mime_map.get(ext, 'audio/mp3') # Default fallback

        print(f"Uploading {file_path} ({mime_type}) to Gemini...")
        
        # 1. Upload
        file_ref = self.client.files.upload(file=file_path)
        print(f"File Uploaded: {file_ref.name}")
        
        # 2. Wait for processing (Verification)
        # Usually audio is instant, but video/large files need state check
        while file_ref.state == "PROCESSING":
            print("Processing file remotely...")
            time.sleep(2)
            file_ref = self.client.files.get(name=file_ref.name)
            
        if file_ref.state != "ACTIVE":
             raise RuntimeError(f"File processing failed: {file_ref.state}")
             
        print("File is ACTIVE.")
        return file_ref

    def process_video(self, youtube_url):
        """Orchestrates the full pipeline: Download -> Upload -> Analyze."""
        audio_file = None
        try:
            # Step 1: Download
            audio_file = self.download_audio(youtube_url)
            
            # Step 2: Upload
            remote_file = self.upload_to_gemini(audio_file)
            
            # Step 3: Generate Content
            print(f"Analyzing with model: {self.model_name}...")
            
            prompt = """
            Process the audio file and generate a detailed transcription.

            Requirements:
            1. Identify distinct speakers (e.g., Speaker 1, Speaker 2).
            2. Provide accurate timestamps (Format: MM:SS).
            3. Detect primary language of each segment.
            4. If segment is not English, provide English translation.
            5. Identify primary emotion: Happy, Sad, Angry, Neutral.
            6. Provide a brief summary at the beginning.
            """

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[
                    types.Content(
                        parts=[
                            types.Part(
                                file_data=types.FileData(
                                    file_uri=remote_file.uri,
                                    mime_type=remote_file.mime_type
                                )
                            ),
                            types.Part(
                                text=prompt
                            )
                        ]
                    )
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "summary": types.Schema(type=types.Type.STRING),
                            "segments": types.Schema(
                                type=types.Type.ARRAY,
                                items=types.Schema(
                                    type=types.Type.OBJECT,
                                    properties={
                                        "speaker": types.Schema(type=types.Type.STRING),
                                        "timestamp": types.Schema(type=types.Type.STRING),
                                        "content": types.Schema(type=types.Type.STRING),
                                        "language": types.Schema(type=types.Type.STRING),
                                        "translation": types.Schema(type=types.Type.STRING),
                                        "emotion": types.Schema(
                                            type=types.Type.STRING,
                                            enum=["happy", "sad", "angry", "neutral"]
                                        )
                                    },
                                    required=["speaker", "timestamp", "content", "emotion"]
                                )
                            )
                        }
                    )
                )
            )
            
            # Cleanup remote file? (Optional, maybe keep for cache?)
            # self.client.files.delete(name=remote_file.name)
            
            return response.parsed # Returns the dict directly if schema is valid
            
        except Exception as e:
            print(f"Video Processing Error: {e}")
            return {"error": str(e)}
        finally:
            # Cleanup local
            if audio_file and os.path.exists(audio_file):
                os.remove(audio_file)

if __name__ == "__main__":
    # Test
    processor = VideoProcessor()
    # Test URL from user
    url = "https://www.youtube.com/watch?v=ku-N-eS1lgM"
    result = processor.process_video(url)
    print(json.dumps(result, indent=2))
