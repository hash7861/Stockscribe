from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, logging
import torch
import re
from collections import defaultdict

logging.set_verbosity_error()

def clean_text(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # remove bold
    text = re.sub(r'\.{2,}', '.', text)           # fix multiple dots
    return text.strip()

def load_summarizer_raw(model_name="sshleifer/distilbart-cnn-12-6"):
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        return model, tokenizer
    except Exception as e:
        print("❌ Error loading model:", str(e))
        return None, None

def summarize_chunk(chunk_texts, model, tokenizer, max_tokens, chunk_num):
    chunk_text = "\n".join(chunk_texts)
    inputs = tokenizer(chunk_text, truncation=True, padding="longest", return_tensors="pt", max_length=max_tokens)
    print(f"🧠 Token count (Chunk {chunk_num}): {inputs['input_ids'].shape[1]}")
    print(f"📄 Input preview (Chunk {chunk_num}):\n{chunk_text[:400]}...\n")
    with torch.no_grad():
        summary_ids = model.generate(
            inputs["input_ids"],
            num_beams=4,
            length_penalty=2.0,
            max_length=250,
            min_length=80,
            early_stopping=True
        )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def filter_by_keyword(posts, keyword):
    keyword_lower = keyword.lower()
    return [
        post for post in posts
        if keyword_lower in post["title"].lower()
    ]


def generate_summary(posts, model=None, tokenizer=None, max_tokens=1024, keyword=None):
    if model is None or tokenizer is None:
        return "Summarization pipeline failed to load."

    if keyword:
        posts = filter_by_keyword(posts, keyword)
        if not posts:
            return f"No posts found containing keyword: {keyword}"
        print(f"\n✅ {len(posts)} posts matched keyword '{keyword}':")
        for p in posts:
            print("-", p["title"])

    # Group by sentiment
    grouped_posts = defaultdict(list)
    for post in posts:
        grouped_posts[post["sentiment"].lower()].append(post)

    final_output = []

    for sentiment, sentiment_posts in grouped_posts.items():
        print(f"\n🔹 Processing sentiment group: {sentiment.upper()} ({len(sentiment_posts)} posts)")
        chunk_summaries = []
        current_chunk = []
        current_token_count = 0

        def tokenize_post(post):
            text = f"[{post['sentiment'].upper()}] {clean_text(post['title'])}. {clean_text(post.get('text', ''))}"
            return text, tokenizer(text, return_tensors="pt", truncation=False)["input_ids"].shape[1]

        # Stage 1: Chunking and summarizing
        for i, post in enumerate(sentiment_posts):
            text, tokens = tokenize_post(post)

            if current_token_count + tokens > max_tokens:
                chunk_summary = summarize_chunk(current_chunk, model, tokenizer, max_tokens, len(chunk_summaries)+1)
                chunk_summaries.append(chunk_summary)
                current_chunk = [text]
                current_token_count = tokens
            else:
                current_chunk.append(text)
                current_token_count += tokens

        if current_chunk:
            chunk_summary = summarize_chunk(current_chunk, model, tokenizer, max_tokens, len(chunk_summaries)+1)
            chunk_summaries.append(chunk_summary)

        # Stage 2: Executive summary
        meta_input = "\n\n".join(chunk_summaries)
        meta_inputs = tokenizer(meta_input, truncation=True, padding="longest", return_tensors="pt", max_length=max_tokens)

        print(f"\n🧠 Token count for executive summary: {meta_inputs['input_ids'].shape[1]}")
        print(f"📄 Executive summary input preview:\n{meta_input[:400]}...\n")

        try:
            with torch.no_grad():
                meta_ids = model.generate(
                    meta_inputs["input_ids"],
                    num_beams=4,
                    length_penalty=2.0,
                    max_length=250,
                    min_length=80,
                    early_stopping=True
                )
            meta_summary = tokenizer.decode(meta_ids[0], skip_special_tokens=True)
        except Exception as e:
            meta_summary = f"❌ Final summary generation failed: {str(e)}"

        sentiment_output = "\n\n".join(
            [f"📌 Chunk {i+1} Summary:\n{summary}" for i, summary in enumerate(chunk_summaries)]
            + [f"\n🧠 Executive Summary ({sentiment.upper()}):\n{meta_summary}"]
        )

        final_output.append(sentiment_output)

    return "\n\n==============================\n\n".join(final_output)
