#!/usr/bin/env python3
"""
Test ultra-fast Shipra responses
"""
from brain import ShipraBrain

def test_responses():
    brain = ShipraBrain()
    
    test_queries = [
        "Hello",
        "What is Pushpak O2?",
        "What is the capacity?",
        "Who is the pilot?",
        "Who are you?",
        "Random question"
    ]
    
    print("Testing Ultra-Fast Shipra Responses:\n")
    
    for query in test_queries:
        response = brain.chat(query)
        print(f"Q: {query}")
        print(f"A: {response}\n")

if __name__ == "__main__":
    test_responses()