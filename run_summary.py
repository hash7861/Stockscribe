import json
from app.sentiment_analyzer import annotate_posts_with_sentiment
from app.summarizer import load_summarizer_raw, generate_summary

# Load Reddit data
with open("data/reddit_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

# Annotate sentiments
annotated_posts = annotate_posts_with_sentiment(posts)

# Print sentiment breakdown
sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
for post in annotated_posts:
    sentiment_counts[post["sentiment"]] += 1
    print(f"[{post['sentiment'].upper()}] {post['title']}")

print("\nSentiment Breakdown:", sentiment_counts)

# ---- Test 1: distilbart-cnn-12-6 ----
print("\n🔹 Summary with distilbart-cnn-12-6")
model, tokenizer = load_summarizer_raw("sshleifer/distilbart-cnn-12-6")
summary = generate_summary(annotated_posts, model=model, tokenizer=tokenizer)
print(summary)

# ---- Test 2: bart-large-cnn-samsum ----
print("\n🔸 Summary with bart-large-cnn-samsum")
model, tokenizer = load_summarizer_raw("philschmid/bart-large-cnn-samsum")
summary = generate_summary(annotated_posts, model=model, tokenizer=tokenizer)
print(summary)