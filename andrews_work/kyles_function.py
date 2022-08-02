import pandas as pd
from googletrans import Translator
from camel_tools.sentiment import SentimentAnalyzer
from transformers import pipeline

""" 
Change name to which file you're doing sentiment analysis on, NOT including the '.csv' 
Output file will be 'labeled_<filename>.csv'
"""

msa = pipeline('text-classification', model="CAMeL-Lab/bert-base-arabic-camelbert-msa-sentiment")
name = 'block_2_0'


def load_and_label_df(name):
    df = load_csv('/Users/amanda22/codeup-data-science/arabic_media_nlp_project/andrews_work/'+name+'.csv')
    print(f'loaded {name}.csv')
    print('labeling/scoring...')
    df = create_labels_scores(df, name)
    print('done labeling/scoring!')
    return df

def load_csv(filename):
    df = pd.read_csv(filename)
    df['text_label'] = 'invalid'
    df['text_score'] = 'invalid'
    df['headline_label'] = 'invalid'
    df['headline_score'] = 'invalid'
    return df

def make_msa(df_text):
    try:
        done = msa(df_text)
        return done
    except:
        
        try:
            first_half = msa(df_text[:round(len(df_text)/2)]) 
            second_half = msa(df_text[round(len(df_text)/2):])
            if first_half[0]['label'] == second_half[0]['label']:
                label = first_half[0]['label']
                score = (first_half[0]['score'] + second_half[0]['score'])/2
            done = [{'label': label, 'score': score}]
            return done
        except:
            return [{'label': 'unlabeled', 'score': 'unscored'}]
        
def analyze_text(df):
    scores = []
    scores = df.text.apply(make_msa)
    return scores

def analyze_headline(df):
    headline_scores = []
    scores = df.headline.apply(make_msa)
    return scores

def label_and_scores(msa_scores):
    labels = []
    scores = []
    for val in msa_scores:
        try:
            labels.append(val[0]['label'])
            scores.append(val[0]['score'])
        except:
            labels.append(False)
            scores.append(False)

    return labels, scores

def create_labels_scores(df, name):
    text_scores = analyze_text(df)
    labels, scores = label_and_scores(text_scores)
    df['text_label'] = labels
    df['text_score'] = scores

    headline_scores = analyze_headline(df)
    labels, scores = label_and_scores(headline_scores)
    df['headline_label'] = labels
    df['headline_score'] = scores

    # CHANGE 'BLOCK_NAME' TO WHATEVER YOU WANT
    df.to_csv('labeled_'+ name + '.csv', index=False)

    return df

load_and_label_df('block_2_0')