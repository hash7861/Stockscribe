from transformers import pipeline, logging

# Silence unnecessary warnings from transformers
logging.set_verbosity_error()

# Load Hugging Face summarizer model (lightweight)
try:
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
except Exception as e:
    print("❌ Error loading summarizer pipeline:", str(e))
    summarizer = None

def generate_summary(posts, max_input_chars=1024):
    if summarizer is None:
        return "Summarization pipeline failed to load."

    # Combine title and text from all posts
    combined_text = " ".join(post["title"] + " " + post.get("text", "") for post in posts)

    # Truncate to safe length
    combined_text = combined_text[:max_input_chars]

    try:
        result = summarizer(combined_text, max_length=250, min_length=80, do_sample=False)
        return result[0]["summary_text"]
    except Exception as e:
        return f"❌ Summarization failed: {str(e)}"