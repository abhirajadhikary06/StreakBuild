import requests
from youtube_transcript_api import YouTubeTranscriptApi

# Constants
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
GEMINI_API_KEY = "AIzaSyAJ3uU_eH5sPsRkadJl2Fg1k6nEglQA34o"

def get_video_id(url):
    """Extracts the video ID from a YouTube URL."""
    import re
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

def get_transcript(video_id):
    """Fetches the transcript of a YouTube video using youtube_transcript_api."""
    try:
        # Fetch the transcript for the given video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine all text parts into a single string
        text = " ".join([entry['text'] for entry in transcript])
        return text
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def generate_mcqs(transcript):
    """Generates 10 MCQ questions using the Gemini API."""
    prompt = f"Generate 10 multiple-choice questions (MCQs) based on the following transcript:\n\n{transcript}"
    
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    response = requests.post(
        f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        response_data = response.json()
        mcqs = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        return mcqs
    else:
        print(f"Error generating MCQs: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def main():
    while True:
        # Get YouTube video URL from the user
        youtube_url = input("Enter YouTube video URL (or 'quit' to exit): ").strip()
        
        if youtube_url.lower() == "quit":
            print("Exiting...")
            break
        
        video_id = get_video_id(youtube_url)
        
        if not video_id:
            print("Invalid YouTube URL.")
            continue
        
        # Fetch the transcript
        print("Fetching transcript...")
        transcript = get_transcript(video_id)
        
        if not transcript:
            print("Could not fetch transcript. Make sure the video has closed captions available.")
            continue
        
        # Generate MCQs using Gemini API
        print("Generating MCQs...")
        mcqs = generate_mcqs(transcript)
        
        if mcqs:
            print("\nGenerated MCQs:\n")
            print(mcqs)
        else:
            print("Failed to generate MCQs.")

if __name__ == "__main__":
    main()