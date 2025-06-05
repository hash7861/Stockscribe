import json
from app.sentiment_analyzer import annotate_posts_with_sentiment
from app.summarizer import generate_summary

# Load saved Reddit data
with open("data/reddit_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

# Annotate with sentiment
annotated_posts = annotate_posts_with_sentiment(posts)

# Print a summary
sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
for post in annotated_posts:
    sentiment_counts[post["sentiment"]] += 1
    print(f"[{post['sentiment'].upper()}] {post['title']}")

print("\nSentiment Breakdown:", sentiment_counts)

# from app.summarizer import generate_summary

summary = generate_summary(annotated_posts)
print("\n📢 Summary:\n", summary)