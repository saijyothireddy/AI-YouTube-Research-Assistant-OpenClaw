from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url):
    return re.search(r"(?:v=)([\w-]{11})", url).group(1)

def fetch_transcript(url):
    video_id = extract_video_id(url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join([t["text"] for t in transcript])
    return text
