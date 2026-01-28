#!/usr/bin/env python3
"""
Ultra-fast model setup for instant Shipra responses
"""
import subprocess
import sys

def pull_ultra_fast_model():
    """Pull the fastest available model"""
    models = ["phi3:mini", "gemma2:2b", "llama3.2:1b"]
    
    for model in models:
        try:
            print(f"Trying {model}...")
            result = subprocess.run(
                ["ollama", "pull", model], 
                capture_output=True, 
                text=True,
                timeout=180
            )
            
            if result.returncode == 0:
                print(f"✅ {model} installed!")
                
                # Update config automatically
                with open("config.py", "r") as f:
                    content = f.read()
                
                # Replace model name
                content = content.replace('MODEL_NAME = "llama3.2:1b"', f'MODEL_NAME = "{model}"')
                
                with open("config.py", "w") as f:
                    f.write(content)
                
                print(f"✅ Config updated to use {model}")
                return True
                
        except Exception as e:
            print(f"❌ {model} failed: {e}")
            continue
    
    return False

if __name__ == "__main__":
    print("🚀 Setting up ULTRA-FAST Shipra...")
    
    if pull_ultra_fast_model():
        print("\n⚡ ULTRA-FAST setup complete!")
        print("💨 Shipra will now respond in under 2 seconds!")
    else:
        print("\n❌ Could not install ultra-fast model")
        print("💡 Try manually: ollama pull phi3:mini")