#!/usr/bin/env python3
"""
Quick setup script to pull the faster Llama model for Shipra
"""
import subprocess
import sys

def pull_fast_model():
    """Pull the smaller, faster Llama model"""
    try:
        print("Pulling llama3.2:1b (faster model)...")
        result = subprocess.run(
            ["ollama", "pull", "llama3.2:1b"], 
            capture_output=True, 
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print("✅ Fast model pulled successfully!")
            return True
        else:
            print(f"❌ Error pulling model: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout while pulling model")
        return False
    except FileNotFoundError:
        print("❌ Ollama not found. Please install Ollama first.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_ollama():
    """Check if Ollama is running"""
    try:
        result = subprocess.run(
            ["ollama", "list"], 
            capture_output=True, 
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except:
        return False

if __name__ == "__main__":
    print("🚀 Setting up Shipra for faster responses...")
    
    if not check_ollama():
        print("❌ Ollama is not running. Please start Ollama first.")
        sys.exit(1)
    
    if pull_fast_model():
        print("\n✅ Setup complete! Shipra will now respond faster.")
        print("💡 The smaller model (llama3.2:1b) provides quicker responses.")
    else:
        print("\n❌ Setup failed. You may need to manually run: ollama pull llama3.2:1b")
        sys.exit(1)