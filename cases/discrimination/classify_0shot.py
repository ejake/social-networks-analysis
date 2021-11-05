from transformers import pipeline

import pandas as pd
import numpy as np
from tqdm import tqdm
import json

OUTPUT_PATH = './{}'

# Load data

DIRECT_DOWNLOAD_URL = 'https://drive.google.com/uc?export=download&id='
COMMENTS_URL = DIRECT_DOWNLOAD_URL + '1e-YnGo2oZeH8wUrJrenpQpBJyhOUf0DZ'

df_comments = pd.read_csv(COMMENTS_URL)
print(df_comments.info())

# 0-shot learning model

classifier = pipeline("zero-shot-classification", \
    model="vicgalle/xlm-roberta-large-xnli-anli")

params_classifier = json.load(open('params_0shot_classifier.json', 'r'))

candidate_labels_0 = params_classifier['candidate_labels_0']
candidate_labels_1 = params_classifier['candidate_labels_1']
hypothesis_template = params_classifier['hypothesis_template']

# Apply in a batch
def apply_0classifier(df, column_text, labels, hypothesis_template):
    for i in labels:
        if i not in df.columns:
            df[i] = np.nan

    for idx, row in tqdm(df.iterrows()):
        output = classifier(row[column_text],
                            labels, 
                            hypothesis_template = hypothesis_template)
        for i, lbl in enumerate(output['labels']):
            df.at[idx, lbl] = output['scores'][i]
    
    return df
  
apply_0classifier(df_comments, 
                  'comment_text', 
                  candidate_labels_0, 
                  hypothesis_template)

apply_0classifier(df_comments, 
                  'comment_text', 
                  candidate_labels_1, 
                  hypothesis_template)


df_comments.to_csv(OUTPUT_PATH.format('comments_classified_0shot.csv'),
                   index=False)