import json
# Save final summary to outputs/summary.txt
import os
from app.sentiment_analyzer import annotate_posts_with_sentiment
from app.summarizer import load_summarizer_raw, generate_summary

# Load Reddit data
with open("data/reddit_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

# Optional: set a keyword filter (e.g., 'NVIDIA')
keyword_filter = "NVIDIA"

# Filter posts before annotating
filtered_posts = [
    post for post in posts
    if keyword_filter.lower() in post["title"].lower()
]


# Annotate sentiments
annotated_posts = annotate_posts_with_sentiment(filtered_posts)

# Print filtered titles
print(f"\n🧃 Filtered Posts on '{keyword_filter}':")
sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
for post in annotated_posts:
    sentiment_counts[post["sentiment"]] += 1
    print(f"[{post['sentiment'].upper()}] {post['title']}")

print("\nSentiment Breakdown:", sentiment_counts)

# Load model
print("\n🔸 Summary with bart-large-cnn-samsum")
model, tokenizer = load_summarizer_raw("philschmid/bart-large-cnn-samsum")

# Generate summaries
summary = generate_summary(
    annotated_posts,
    model=model,
    tokenizer=tokenizer,
    max_tokens=1024,
    keyword=keyword_filter
)

# Print final summary
print(summary)

os.makedirs("outputs", exist_ok=True)
with open("outputs/summary.txt", "w", encoding="utf-8") as f:
    f.write(summary)
print("\n📁 Summary saved to outputs/summary.txt")
