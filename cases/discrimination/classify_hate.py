import pandas as pd
import numpy as np

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
  
DIRECT_DOWNLOAD_URL = 'https://drive.google.com/uc?export=download&id='
COMMENTS_URL = DIRECT_DOWNLOAD_URL + '1e-YnGo2oZeH8wUrJrenpQpBJyhOUf0DZ'
OUTPUT_PATH = "/home/administrador/output-language/{}"
OUTPUT_FILE = 'comments_hate_20211111.csv'


def get_hate_score(text):
    try:
        output = nlp(text)
    except RuntimeError:
        return None
    if len(output) > 0:
        if output[0]['label'] == 'NON_HATE':
            return 1 - output[0]['score']
        if output[0]['label'] == 'HATE':
            return output[0]['score']


if __name__ == "__main__":
    # 1. Load data
    print("Loading data...")
    df_comments = pd.read_csv(COMMENTS_URL)
    print(df_comments.info())
    # 2. Model
    print("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained("Hate-speech-CNERG/dehatebert-mono-spanish")
    model = AutoModelForSequenceClassification.from_pretrained("Hate-speech-CNERG/dehatebert-mono-spanish")
    nlp = pipeline("text-classification", 
               model=model, 
               tokenizer=tokenizer)
    # 3. Apply model
    df_comments['hate'] = df_comments.comment_text.apply(get_hate_score)
    print(df_comments.hate.describe())
    df_comments.to_csv(OUTPUT_PATH.format(OUTPUT_FILE), index=False)
    
