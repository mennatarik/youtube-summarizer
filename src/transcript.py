"""YouTube helpers: extract the video ID and fetch the transcript."""
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """Extract the YouTube video ID from a URL.

    Supports youtu.be, youtube.com/watch?v=, /shorts/, /embed/, /live/, /v/.
    Raises ValueError if no video id can be found.
    """
    parsed = urlparse(url.strip())
    host = (parsed.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]

    if host == "youtu.be":
        video_id = parsed.path.lstrip("/").split("/")[0]
        if video_id:
            return video_id

    if host in ("youtube.com", "m.youtube.com", "music.youtube.com"):
        qs = parse_qs(parsed.query)
        if qs.get("v"):
            return qs["v"][0]

        parts = parsed.path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] in ("shorts", "embed", "live", "v"):
            return parts[1]

    raise ValueError(f"No video id found in URL: {url}")


def get_transcript(url: str, languages=("en",)) -> str:
    """Return the full transcript text of a YouTube video."""
    video_id = extract_video_id(url)
    api = YouTubeTranscriptApi()
    fetched = api.fetch(video_id, languages=list(languages))
    return "\n".join(snippet.text for snippet in fetched)
