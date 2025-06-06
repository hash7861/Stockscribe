from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, logging
import torch
import re

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

def generate_summary(posts, model=None, tokenizer=None, max_tokens=1024):
    if model is None or tokenizer is None:
        return "Summarization pipeline failed to load."

    # Combine posts into a single cleaned string
    combined_text = "\n".join(
        f"[{post['sentiment'].upper()}] Post {i+1}: {clean_text(post['title'])}. {clean_text(post.get('text', ''))}"
        for i, post in enumerate(posts)
    )

    # Tokenize with truncation
    inputs = tokenizer(
        combined_text,
        truncation=True,
        padding="longest",
        return_tensors="pt",
        max_length=max_tokens
    )

    print(f"🧠 Token count: {inputs['input_ids'].shape[1]}")
    print(f"📄 Input preview:\n{combined_text[:400]}...\n")

    try:
        with torch.no_grad():
            summary_ids = model.generate(
                inputs["input_ids"],
                num_beams=4,
                length_penalty=2.0,
                max_length=250,
                min_length=80,
                early_stopping=True
            )
        output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return output
    except Exception as e:
        return f"❌ Summarization failed: {str(e)}"