# 🎬 YouTube Video Summarizer

Fetches a YouTube video's existing captions and summarizes them with
`facebook/bart-large-cnn` (chunked, so long videos work). Includes a simple
Streamlit GUI that can be shared publicly through ngrok.

> This project does **not** transcribe audio. The video must already have
> captions (English by default).

## Project structure

```
youtube-summarizer/
├── app.py              # Streamlit GUI
├── run_ngrok.py        # Starts Streamlit + ngrok public tunnel
├── main.py             # CLI version (the notebook as a .py script)
├── src/
│   ├── __init__.py
│   ├── transcript.py   # video-id extraction + transcript fetching
│   └── summarizer.py   # BART loading, chunking, summarizing
├── notebooks/
|   ├── run_youtube_summarizer.ipynb   # run notebook
|   ├── lab1-tips-hind.ipynb           # original notebook
├── requirements.txt
├── .gitignore
└── README.md
```

## Run on Google Colab (recommended)

### 1. Add your ngrok token (once)
1. Create a free account at [ngrok.com](https://ngrok.com) and copy your authtoken from the dashboard.
2. In Colab, open the 🔑 **Secrets** tab on the left, add a secret named `NGROK_AUTHTOKEN`, paste the token as its value, and turn on **Notebook access**.

### 2. Run these cells in order

**Cell 1 – clone the repo**
```python
!git clone "https://github.com/mennatarik/youtube-summarizer"
```
If you re-run this in the same session you'll see `destination path ... already exists`. That's harmless, so just continue.

**Cell 2 – enter the project folder**
```python
%cd youtube-summarizer
```

**Cell 3 – install dependencies**
```python
%pip install -r requirements.txt
```

**Cell 4 – load the ngrok token from Colab Secrets**
```python
import os
from google.colab import userdata

os.environ["NGROK_AUTHTOKEN"] = userdata.get("NGROK_AUTHTOKEN")
```

**Cell 5 – start the app with a public link**
```python
!python run_ngrok.py
```
After a few seconds it prints:
```
🌍 Public URL: https://xxxx.ngrok-free.app
```
Open that link in your browser (click **Visit Site** if ngrok shows a warning page).
Keep this cell running while you use the app. Stopping it closes the tunnel.

> Don't run `!streamlit run app.py` before this. The `localhost` / `172.x` / `8.x`
> addresses it prints are inside Colab and can't be opened from your browser,
> and it will occupy port 8501, which `run_ngrok.py` needs.

Colab sessions are wiped when they end, so repeat cells 1–5 each new session.

## Run locally

```bash
git clone https://github.com/mennatarik/youtube-summarizer
cd youtube-summarizer
pip install -r requirements.txt
```

**CLI**
```bash
python main.py "https://youtu.be/kJf4MmouR-s"
```

**GUI (local only)**
```bash
streamlit run app.py        # opens http://localhost:8501
```

**GUI + public link**
```bash
export NGROK_AUTHTOKEN=your_token     # Windows: set NGROK_AUTHTOKEN=your_token
python run_ngrok.py
```
