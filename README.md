// Hello there- began on June 4th; concluded main work on June 8th; see end for future modifications

# Stockscribe

Stockscribe is a Reddit-powered financial sentiment and summarization tool. It scrapes posts from r/stocks based on a keyword (e.g., `NVIDIA`), annotates them with sentiment, and generates a short AI-driven executive summary using a transformer model. Perfect for general folk and investors who want fast insights from social chatter.

---

## 🚀 Features

- ✅ Keyword-based scraping from r/stocks (e.g., "NVIDIA")
- ✅ Filters titles containing the keyword
- ✅ Sentiment analysis with `vaderSentiment`
- ✅ Summarization using [BART large CNN SAMSum](https://huggingface.co/philschmid/bart-large-cnn-samsum)
- ✅ Outputs a summary with sentiment breakdown to `outputs/summary.txt`
- ✅ Clean CLI interface for scraping and summarizing

---

## 📁 Project Structure

Stockscribe/
├── app/
    ├── reddit_scraper.py # Fetches Reddit posts using PRAW
    ├── sentiment_analyzer.py # Classifies posts using VADER
    ├── summarizer.py # Uses HuggingFace Transformers for summarization
├── data/
    │── reddit_posts.json # Raw scraped posts
├── outputs/
    │── summary.txt # Final saved summary
├── run_summary.py # Main entry for filtering, sentiment, and summarization
├── requirements.txt
└── README.md

---

## ⚙️ Setup

1. Clone the repository

git clone https://github.com/yourusername/Stockscribe.git
cd Stockscribe

2. Setup Virtual Environment (optional)
python -m venv venv-stockscribe
source venv-stockscribe/bin/activate  # On Windows: venv-stockscribe\Scripts\activate

3. Create .env File for Reddit API
pip install -r requirements.txt

4. Create .env File for Reddit API
REDDIT_CLIENT_ID=your_client_id
REDDIT_USER_AGENT=stockscribe-agent
You can get these values by creating a Reddit app at https://www.reddit.com/prefs/apps.

---

## ⚙️ Usage

1. Scrape posts
python app/reddit_scraper.py NVIDIA 

This fetches the latest 10 posts from r/stocks with "NVIDIA" in the title and saves them to data/reddit_posts.json

2. Summarize and analyze
python run_summary.py
outputs/summary.txt

This loads the scraped posts, filters them again, runs sentiment classification, groups them by tone, summarizes each group, and finally saves results to the summary.txt

---

📌 To-Do Improvements

 Add GUI dashboard (Streamlit or Flask)

 Support multi-keyword batching

 Add database support (MongoDB or SQLite)

 Connect to Slack/Telegram for automated daily updates

 Allow users to choose what stock topics they want to scrape (ex: Tesla, Apple, S&p 500)