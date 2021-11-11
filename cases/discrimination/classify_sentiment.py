import pandas as pd
import numpy as np

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
  
DIRECT_DOWNLOAD_URL = 'https://drive.google.com/uc?export=download&id='
COMMENTS_URL = DIRECT_DOWNLOAD_URL + '1e-YnGo2oZeH8wUrJrenpQpBJyhOUf0DZ'
OUTPUT_PATH = "/home/administrador/output-language/{}"
OUTPUT_FILE = 'comments_sentiment_20211111.csv'


def get_sentiment_score(text):
    pos, neg, neu = 0,0,0
    try:
        output = nlp(text)
    except RuntimeError:
        return None    
    if len(output) > 0:
        for element in output:
            if element['label'] == 'POS':
                pos = element['score']
            if element['label'] == 'NEG':
                neg = element['score']
            if element['label'] == 'NEU':
                neu = element['score']
    return pos, neg, neu



if __name__ == "__main__":
    # 1. Load data
    print("Loading data...")
    df_comments = pd.read_csv(COMMENTS_URL)
    print(df_comments.info())
    # 2. Model
    print("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained("finiteautomata/beto-sentiment-analysis")
    model = AutoModelForSequenceClassification.from_pretrained("finiteautomata/beto-sentiment-analysis")
    nlp = pipeline("text-classification", 
               model=model, 
               tokenizer=tokenizer)
    # 3. Apply model
    df_comments['sentiment'] =  df_comments.comment_text.apply(get_sentiment_score)
    df_comments['sent_positive'] = df_comments.sentiment.apply(lambda x : x[0] if x else None)
    df_comments['sent_negative'] = df_comments.sentiment.apply(lambda x : x[1] if x else None)
    df_comments['sent_neutral'] = df_comments.sentiment.apply(lambda x : x[2] if x else None)
    print(df_comments[['sent_positive', 'sent_negative', 'sent_neutral']].describe())
    df_comments.to_csv(OUTPUT_PATH.format(OUTPUT_FILE), index=False)
    
