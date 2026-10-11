"""Streamlit GUI for the YouTube summarizer."""
import streamlit as st

from src.summarizer import load_summarizer, summarize_text
from src.transcript import get_transcript

st.set_page_config(page_title="YouTube Summarizer", page_icon="🎬")
st.title("🎬 YouTube Video Summarizer")
st.caption("Paste a YouTube link and get a summary of the video transcript (BART).")


@st.cache_resource(show_spinner="Loading summarization model (first run only)...")
def get_model():
    return load_summarizer()


url = st.text_input("YouTube link", placeholder="https://youtu.be/...")

with st.expander("Settings"):
    max_len = st.slider("Max summary length per chunk", 60, 250, 130)
    min_len = st.slider("Min summary length per chunk", 10, 100, 30)

if st.button("Summarize", type="primary"):
    if not url.strip():
        st.warning("Please enter a YouTube link.")
        st.stop()

    try:
        with st.spinner("Fetching transcript..."):
            text = get_transcript(url)
    except Exception as e:
        st.error(f"Could not get the transcript: {e}")
        st.stop()

    summarizer = get_model()
    bar = st.progress(0.0, text="Summarizing...")

    def on_progress(done, total):
        bar.progress(done / total, text=f"Summarizing chunk {done}/{total}")

    final_summary, chunk_summaries = summarize_text(
        text, summarizer, max_len, min_len, on_progress
    )
    bar.empty()

    st.subheader("Summary")
    st.write(final_summary)
    st.download_button("Download summary", final_summary, file_name="summary.txt")

    with st.expander("Chunk-by-chunk summaries"):
        for i, s in enumerate(chunk_summaries, 1):
            st.markdown(f"**Chunk {i}:** {s}")

    with st.expander("Full transcript"):
        st.text(text)
