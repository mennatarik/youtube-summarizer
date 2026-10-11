"""Command-line version of the notebook (lab1-tips-hind.ipynb)."""

import argparse

from src.summarizer import load_summarizer, split_into_chunks, summarize_chunks
from src.transcript import get_transcript

DEFAULT_URL = "https://youtu.be/Pv3r_BxuttA?si=PSlryO98akx0d_Fx"


def main():
    parser = argparse.ArgumentParser(description="Summarize a YouTube video.")
    parser.add_argument("url", nargs="?", default=DEFAULT_URL, help="YouTube video link")
    args = parser.parse_args()

    print("Fetching transcript...")
    text = get_transcript(args.url)
    print(text)

    print("\nLoading model...")
    summarizer = load_summarizer()

    chunks = split_into_chunks(text, summarizer)
    print("Number of chunks:", len(chunks))

    summaries = summarize_chunks(chunks, summarizer)
    print(summaries)

    final_summary = " ".join(summaries)
    print("\n===== FINAL SUMMARY =====")
    print(final_summary)


if __name__ == "__main__":
    main()
