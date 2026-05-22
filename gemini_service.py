import os
import time
import random
from google import genai
from google.genai import types
from google.genai.errors import APIError

def upload_files_to_api(file_paths: list) -> list:
    """
    Uploads a list of local file paths to the Gemini Files API.
    Returns a list of uploaded file objects.
    """
    uploaded_media_objects = []
    if not file_paths:
        return uploaded_media_objects
        
    try:
        client = genai.Client()
        for path in file_paths:
            if not os.path.exists(path):
                print(f"[Service Error] File not found: {path}")
                continue
                
            print(f"[Service] Uploading {path} to Gemini Files API...")
            uploaded_file = client.files.upload(file=path)
            uploaded_media_objects.append(uploaded_file)
            print(f"[Service] Uploaded: {uploaded_file.uri}")
            
        return uploaded_media_objects
    except Exception as e:
        print(f"[Service Error] Failed to upload files: {str(e)}")
        return []

def generate_response(
    prompt: str, 
    model: str = "gemini-2.5-flash-lite", 
    max_retries: int = 5, 
    base_delay: float = 2.0,
    attached_files: list = None,
    warning_callback=None
) -> str:
    """
    Query Google Gemini model with exponential delay-based retries.
    Accepts a list of attached file objects and an optional callback for quota warnings.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY environment variable is not configured."
        
    client = genai.Client()
    config = types.GenerateContentConfig(
        system_instruction="You are an analytic assistant and impartial.",
        temperature=0.2
    )

    contents = []
    if attached_files:
        contents.extend(attached_files)
    contents.append(prompt)

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=config
            )
            return response.text
            
        except APIError as e:
            if e.code == 429:
                if attempt == max_retries - 1:
                    return f"Error: Maximum retry count exceeded ({max_retries}). Persistent quota limit."
                
                exponential_delay = base_delay * (2 ** attempt)
                jitter = random.uniform(0, 1.0)
                wait_time = exponential_delay + jitter
                
                # Execute UI callback if provided, otherwise fallback to print
                msg = f"Quota limit reached. Retrying {attempt + 1}/{max_retries} in {wait_time:.2f} seconds..."
                if warning_callback:
                    warning_callback(msg)
                else:
                    print(f"[Service Warning] {msg}")
                    
                time.sleep(wait_time)
            else:
                return f"API critical error ({e.code}): {e.message}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"