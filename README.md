# Gemini Assistant (OpenAI Compatible)

A simple AI assistant that uses the `openai` Python library to talk to Google Gemini models.

## How it Works
It connects to Google's OpenAI-compatible API endpoint:
`https://generativelanguage.googleapis.com/v1beta/openai/`

## Requirements
- `openai`
- `python-dotenv`
- Google Gemini API Key

## Usage
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Set your API key in `.env`:
    ```
    GEMINI_API_KEY=your_key_here
    ```
3.  Run:
    ```bash
    python main.py
    ```