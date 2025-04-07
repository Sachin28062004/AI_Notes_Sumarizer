# utils/summarizer.py

from transformers import BartTokenizer, BartForConditionalGeneration
import torch

tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

def summarize(text, length='medium', output_format='paragraph'):
    if length == 'short':
        max_length = 60
        min_length = 15
    elif length == 'large':
        max_length = 200
        min_length = 100
    else:
        max_length = 120
        min_length = 40

    inputs = tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    if output_format == 'bullets':
        bullets = summary.split('. ')
        return '\n'.join(f'• {b.strip()}' for b in bullets if b.strip())
    else:
        return summary
