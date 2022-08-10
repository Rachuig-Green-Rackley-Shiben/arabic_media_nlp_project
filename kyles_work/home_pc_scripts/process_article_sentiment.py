
import pandas as pd
from googletrans import Translator
from camel_tools.sentiment import SentimentAnalyzer
from transformers import pipeline
import os
import regex as re
import numpy as np
import torch.cuda


""" 
Change name to which file you're doing sentiment analysis on, NOT including the '.csv' 
Output file will be 'labeled_<filename>.csv'
"""

msa = pipeline('text-classification', model="CAMeL-Lab/bert-base-arabic-camelbert-msa-sentiment")



def load_and_label_df(name):
    path = 'split_articles/'
    df = load_csv(path + name)
    print(f'loaded {name}')
    print('labeling/scoring...')
    df = create_labels_scores(df, name)
    print('done labeling/scoring!')
    return df

def load_csv(filename):
    df = pd.read_csv(filename)
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
                score = (test_1[0]['score'] + test_2[0]['score'])/2
            done = [{'label': label, 'score': score}]
            return done
        except:
        
            try:
                beginning = msa(df_text[:round(len(df_text)/3)]) 
                middle = msa(df_text[round(len(df_text)/3):round(len(df_text)*2/3)])
                end = msa(df_text[round(len(df_text)*2/3):])

                if (beginning[0]['label'] == middle[0]['label']) and (beginning[0]['label'] == end[0]['label']):
                    label = first_half[0]['label']
                    score = (beginning[0]['score'] + middle[0]['score'] + end[0]['score'])/3
                    done = [{'label': label, 'score': score}]
                    return done
                else:
                    return 'sentiment of parts not equal'
            except:
                return '3 is not enough'
        
def analyze_text(df):
    scores = []
    print('analyzing_texts')
    scores = [make_msa(val) for val in df.text.values]
    return scores

def analyze_headline(df):
    print('analyzing headlines')
    headline_scores = [make_msa(val) for val in df.headline.values]
    return headline_scores

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
    df.to_csv('labeled_split_articles/labeled_'+ name + '.csv', index=False)

    return df

def split_tons_of_csvs():
    df = pd.read_csv('C:/Users/kyleg/codeup/all_articles.csv')
    
    end_point = 'C:/Users/kyleg/codeup/split_articles/'
    
    df_shape = df.shape[0]
    
    one_thousandth = int(df_shape/1000)
    
    for i in range(0, df_shape, one_thousandth):
        copy = df.iloc[i:i+one_thousandth].copy()
        copy.to_csv(end_point+str(i) + '.csv', index=False)


def make_random_indexes(list_of_files):
    unique_ = []
    length = len(list_of_files)
    unique_indexes= np.random.randint(0, length, size=length**2 , dtype=int)
    [unique_.append(val) for val in unique_indexes if val not in unique_]

    return unique_


#split_tons_of_csvs()

labeled = 'labeled_split_articles'
unlabeled = 'split_articles'

print(torch.cuda.is_available())

os.listdir(labeled)

unlabeled_files = os.listdir(unlabeled)
labeled_files = []

for path in os.listdir(labeled):
    labeled_files.append(re.search('\d*\.', path).group()[:-1])

print(labeled_files)
    
    
ul_files = unlabeled_files[:]
files_found  = []
for p in labeled_files:
    for pth in unlabeled_files:
        if p+'.csv' == pth:
            ul_files.remove(pth)

path = 'split_articles/'
unique_indexes  = make_random_indexes(ul_files)
print(unique_indexes)
for i in unique_indexes:
    load_and_label_df(ul_files[i])