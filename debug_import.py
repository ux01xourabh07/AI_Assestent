import sys
import os

print("--- Python Path ---")
for p in sys.path:
    print(p)

print("\n--- Google Namespace ---")
try:
    import google
    print(f"google package path: {getattr(google, '__path__', 'No Path')}")
    print(f"google package file: {getattr(google, '__file__', 'No File')}")
except ImportError as e:
    print(f"Error importing google: {e}")

print("\n--- GenAI Import ---")
try:
    from google import genai
    print("Success: from google import genai")
except ImportError as e:
    print(f"Failure: {e}")
    
try:
    import google.genai
    print("Success: import google.genai")
except ImportError as e:
    print(f"Failure: import google.genai -> {e}")

print("\n--- GenerativeAI Import ---")
try:
    import google.generativeai
    print("Success: import google.generativeai")
except ImportError as e:
    print(f"Failure: import google.generativeai -> {e}")
