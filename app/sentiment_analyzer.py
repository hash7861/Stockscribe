from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Ranges from -1.0 (neg) to 1.0 (pos)

def classify_sentiment(polarity):
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"

def annotate_posts_with_sentiment(posts):
    for post in posts:
        combined_text = post["title"] + " " + post.get("text", "")
        polarity = analyze_sentiment(combined_text)
        sentiment = classify_sentiment(polarity)

        post["polarity"] = polarity
        post["sentiment"] = sentiment

    return posts