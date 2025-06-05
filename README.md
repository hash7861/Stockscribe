// Hello there- began on June 4th
// Initial project setup: folder structure, virtual env, README, dependencies
# Stockscribe

A stock summary LLM assistant that scrapes Reddit and financial news sources, extracts trending tickers, performs sentiment analysis, and generates a weekly natural-language digest using LLMs.

## Features
- Reddit scraping via PRAW
- Financial news API integration
- Ticker detection using NLP
- Sentiment scoring with FinBERT or TextBlob
- Summarization with Hugging Face or OpenAI LLMs

## How to Run
```bash
python run_summary.py