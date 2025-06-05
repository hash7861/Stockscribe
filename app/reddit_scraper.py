import os
from dotenv import load_dotenv
import praw

# Load variables from .env
load_dotenv()

# Create Reddit instance
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=None,  # Explicitly None for installed apps
    user_agent=os.getenv("REDDIT_USER_AGENT")
)



# Quick test
print("Reddit instance created successfully.")
print("Sample subreddit title:", reddit.subreddit("stocks").title)
