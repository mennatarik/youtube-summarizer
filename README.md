# 🎬 YouTube Video Summarizer

Fetches a YouTube video's transcript and summarizes it with `facebook/bart-large-cnn`
(chunked, so long videos work). Includes a simple Streamlit GUI that can be shared
publicly via ngrok.

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
├── run_youtube_summarizer.ipynb   # original notebook
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
```

## Run

**CLI**
```bash
python main.py "https://youtu.be/kJf4MmouR-s"
```

**GUI (local)**
```bash
streamlit run app.py
```

**GUI + public link with ngrok**
```bash
export NGROK_AUTHTOKEN=your_token      # Windows: set NGROK_AUTHTOKEN=your_token
python run_ngrok.py
```
Open the printed `https://xxxx.ngrok-free.app` URL.

### On Kaggle / Colab
```python
!pip install -r requirements.txt
import os; os.environ["NGROK_AUTHTOKEN"] = "your_token"
!python run_ngrok.py
```

## Notes
- The video must have captions (English by default; edit `languages` in `src/transcript.py`).
- First run downloads the BART model (~1.6 GB).
