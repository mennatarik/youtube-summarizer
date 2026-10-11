"""Chunked summarization of long text with facebook/bart-large-cnn."""
from transformers import pipeline

MODEL_NAME = "facebook/bart-large-cnn"
CHUNK_SIZE = 900  # BART handles up to 1024 input tokens


def load_summarizer(model_name: str = MODEL_NAME):
    """Load the HuggingFace summarization pipeline."""
    return pipeline("summarization", model=model_name)


def split_into_chunks(text: str, summarizer, chunk_size: int = CHUNK_SIZE) -> list[str]:
    """Tokenize the text and split it into chunks of `chunk_size` tokens."""
    tokens = summarizer.tokenizer.encode(text, add_special_tokens=False)
    chunks = []
    for i in range(0, len(tokens), chunk_size):
        chunk_tokens = tokens[i : i + chunk_size]
        chunks.append(
            summarizer.tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        )
    return chunks


def summarize_chunks(
    chunks: list[str],
    summarizer,
    max_length: int = 130,
    min_length: int = 30,
    progress_callback=None,
) -> list[str]:
    """Summarize each chunk separately."""
    summaries = []
    for i, chunk in enumerate(chunks, start=1):
        output = summarizer(
            chunk,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
            truncation=True,
        )
        summaries.append(output[0]["summary_text"])
        if progress_callback:
            progress_callback(i, len(chunks))
    return summaries


def summarize_text(
    text: str,
    summarizer,
    max_length: int = 130, #by default
    min_length: int = 30,  #by default
    progress_callback=None,
) -> tuple[str, list[str]]:
    """Summarize a long text. Returns (final_summary, per_chunk_summaries)."""
    chunks = split_into_chunks(text, summarizer)
    summaries = summarize_chunks(
        chunks, summarizer, max_length, min_length, progress_callback
    )
    return " ".join(summaries), summaries
