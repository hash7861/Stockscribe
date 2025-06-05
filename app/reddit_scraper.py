import os
from dotenv import load_dotenv
import praw
import json

# Load variables from .env
load_dotenv()

# Create Reddit instance
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=None,  # Explicitly None for installed apps
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def fetch_posts(subreddit_name="stocks", query="Tesla", limit=25):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    for submission in subreddit.search(query, sort="new", limit=limit):
        posts.append({
            "title": submission.title,
            "text": submission.selftext,
            "score": submission.score,
            "url": submission.url,
            "created_utc": submission.created_utc
        })

    return posts

def save_posts_to_file(posts, filename="data/reddit_posts.json"):
    os.makedirs("data", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)
    print(f"Saved {len(posts)} posts to {filename}")

# Quick test(s)
# print("Reddit instance created successfully.")
# print("Sample subreddit title:", reddit.subreddit("stocks").title)

if __name__ == "__main__":
    print("Reddit instance created successfully.")
    print("Sample subreddit title:", reddit.subreddit("stocks").title)

    posts = fetch_posts("stocks", "Tesla", limit=10)
    print(f"\nFound {len(posts)} posts:\n")
    for post in posts:
        print("-", post["title"])

    save_posts_to_file(posts)
    print("Posts saved to file.")