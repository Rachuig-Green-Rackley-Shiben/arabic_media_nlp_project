# unicode, regex, json for text digestion
import unicodedata
import re
import json
import os
import numpy as np
import datetime as dt
import ahocorasick


# nltk: natural language toolkit -> tokenization, stopwords
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split

# pandas dataframe manipulation, acquire script, time formatting
import pandas as pd
from time import strftime

# shh, down in front
import warnings
warnings.filterwarnings('ignore')


import os
import pandas as pd
import time
from datetime import datetime
import regex as re
import pandas as pd
from googletrans import Translator
from camel_tools.sentiment import SentimentAnalyzer
from transformers import pipeline


topics = {'America' : 'أمريكا',
            'American' : 'أمريكيّ',
            'American (f)' : 'أمريكيّة',
            'American (pl)' : 'أمريكيّين',
            'The United States' : 'الولايات المتحدة',
            'The United States' : 'دول موحّدة',
            'Washington' : 'واشنطن',
            'Bush' : 'بوش',
            'Obama' : 'أوباما',
            'Cheney' : 'تشيني',
            'Clinton' : 'كلينتون',
            'Osama Bin Laden' : 'أسامة بن لادن',
            'Al Gore' : 'آل غور',
            'World Trade Center' : 'مركز التجارة العالمي',
            '9/11' : '9/11',
            'September 11' : '11 سبتمبر',
            'Gulf War' : 'حرب الخليج',
            'Google' : 'غوغل',
            'Facebook' : 'فيسبوك',
            'Al Qaida' : 'القاعدة'}


def flip_key_value_pairs(dicts):
    '''
    Flips key-value pairs of a dictionary and returns
    the dictionary.
    '''
    res = dict((v,k) for k,v in dicts.items())
    return res

def make_eng_tags(df_tags):
    eng_tags =[]
    rev_topics = flip_key_value_pairs(topics)
    for key, value in rev_topics.items():
        if key in df_tags:
            eng_tags.append(value)
    return eng_tags


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


def split_and_process_articles():
    labeled = 'labeled_split_articles'
    unlabeled = 'split_articles'

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

def within_30_days(df_dateline, date):
    
    if (df_dateline - date).days < 30 and (df_dateline - date).days > -30:
        return 1
    else:
        return 0

def create_date_features(df):
    important_dates = {
        'september_11th': pd.to_datetime('09-11-2001'),
        'capture_of_baghdad': pd.to_datetime('04-09-2003'),
        'nick_berg': pd.to_datetime('05-12-2004'),
        'iran_nulcear': pd.to_datetime('08-30-2006'),
        'arab_spring': pd.to_datetime('12-20-2011')
    }

    for event, date in important_dates.items():
        df[event] = df.dateline.apply(within_30_days)
        
    return df


def update_csv():
    waiting = False

    while True:
        time.sleep(5)
        curr_time = pd.Timestamp.now()

        if curr_time.hour % 2 != 0:
            waiting = False

        if curr_time.hour % 2 == 0 and not waiting:
            print('updating csv...')
            all_dfs = []
            path = 'C:/Users/kyleg/codeup/labeled_split_articles/'
            parent = 'E:/drive/arabic_NLP/'
            for fi in os.listdir(path):
                all_dfs.append(pd.read_csv(path + fi))

            daily_csv = pd.concat(all_dfs).reset_index()
            print('fixing dates...')
            daily_csv = make_datetime(daily_csv)
            print('writing csv...')
            daily_csv.to_csv(parent + f'daily{curr_time.month}_{curr_time.day}.csv', index=False)
            print(f'csv written. updating in google drive as of {curr_time.hour}:{curr_time.min}')
            waiting = True
    
def techreen_date(date_entry):
    '''
    This function takes in a date entry and applies a regex search to isolate just the relevant date info
    and returns it out.
    '''
    exp = r'(\d?\d)/(\d?\d)/(\d\d\d\d)'
    match = re.search(exp, str(date_entry))
    day =  match[1]
    month = match[2]
    year = match[3]
    date = year+ '-' + month + '-' + day
    return date

def saudiyoum_date(date_entry):
    '''
    This function takes in a date entry and applies a regex search to isolate just the relevant date info
    and returns it out.
    '''
    try:
        exp = r'(2\d\d\d)-(\d?\d)-(\d?\d)'
        match = re.search(exp, str(date_entry))
        day = match[3]
        month = match[2]
        year = match[1]
        date = year+ '-' + month + '-' + day
        return date
    except:
        exp = r'(\d\d\d\d)/(\d?\d)/(\d?\d)'
        match = re.search(exp, str(date_entry))
        day =  match[3]
        month = match[2]
        year = match[1]
        date = year+ '-' + month + '-' + day
        return date

def youm7_date(date_entry, months_map):
    exp = r'(\d?\d)(.*)(\d\d\d\d)'
    match = re.search(exp, date_entry)
    day =  match[1]
    month = match[2].strip()
    year = match[3]
    month = months_map[month]
    date = year+ '-' + month + '-' + day
    return date

def alittihad_date(date_entry, months_map):
    exp = r'(\d?\d)(.*)(\d\d\d\d)'
    match = re.search(exp, date_entry)
    day =  match[1]
    month = match[2].strip()
    year = match[3]
    month = months_map[month]
    date = year+ '-' + month + '-' + day
    return date

def almustaqbal_date(date_entry):
    arabic_months_map = {   'كانون الثاني':'01',
                            'شباط':'02',
                            'آذار':'03',
                            'نيسان':'04',
                            'أيار':'05',
                            'حزيران':'06',
                            'تموز':'07',
                            'آب':'08',
                            'أيلول':'09',
                            'تشرين الأول':'10',
                            'تشرين الثاني':'11',
                            'كانون الأول':'12'}
    exp = r'(\d?\d)\s(.*)\s(\d\d\d\d).+العدد'
    match = re.search(exp, date_entry)
    day =  match[1]
    month = match[2].strip()
    year = match[3]
    month = arabic_months_map[month]
    date = year+ '-' + month + '-' + day
    return date

def ryiadh_date(date_entry, months_map):
    try:
        exp = r'-\s?(\d?\d)\s?(.+)\s?(\d\d\d\d)\s?م'
        match = re.search(exp, date_entry)
        day =  match[1]
        month = match[2].strip()
        year = match[3]
        month = months_map[month]
        date = year+ '-' + month + '-' + day
        return date

    except:
        try:
            exp = r'(\d?\d)/(\d?\d)/(\d\d\d\d)'
            match = re.search(exp, date_entry)
            day =  match[1]
            month = match[2].strip()
            year = match[3]
            date = year+ '-' + month + '-' + day
            return date
        except:
            try:
                exp = r'(\d\d\d\d)-(\d?\d)-(\d?\d)'
                match = re.search(exp, date_entry)
                day =  match[3]
                month = match[2].strip()
                year = match[1]
                date = year+ '-' + month + '-' + day
                return date
            except:
                return pd.NaT

def alqabas_date(date_entry):
    exp = r'(\d\d\d\d)/(\d?\d)/(\d?\d)'
    match = re.search(exp, date_entry)
    day =  match[3]
    month = match[2]
    year = match[1]
    date = year+ '-' + month + '-' + day
    return date

def almasryalyoum_date(date_entry):
    exp = r'(\d?\d)/(\d?\d)/(\d\d\d\d)'
    match = re.search(exp, date_entry)
    day =  match[1]
    month = match[2]
    year = match[3]
    date = year+ '-' + month + '-' + day
    return date

def sabanews_date(date_entry, months_map):
    exp = r'(\d?\d)/(.+)/(\d\d\d\d)'
    match = re.search(exp, date_entry)
    day =  match[1]
    month = match[2].strip()
    month = months_map[month]
    year = match[3]
    date = year+ '-' + month + '-' + day
    return date

def echoroukonline_date(date_entry):
    exp = r'(\d\d\d\d)/(\d?\d)/(\d?\d)'
    match = re.search(exp, date_entry)
    day =  match[3]
    month = match[2]
    year = match[1]
    date = year+ '-' + month + '-' + day
    return date

def make_datetime(dataframe):
    # This function works, ignore the one above
    df = dataframe.dropna()
    months_map = {'يناير':'01',
        'ينابر':'01',
        'فبراير':'02',
        'مارس':'03',
        'أبريل':'04',
        'ابريل':'04',
        'مايو':'05',
        'يونيو':'06',
        'يوليو':'07',
        'أغسطس':'08',
        'اغسطس':'08',
        'سبتمبر':'09',
        'أكتوبر':'10',
        'اكتوبر':'10',
        'نوفمبر':'11',
        'ديسمبر':'12',
        'إبريل':'04',
        'ماي':'05',
        'يونيه':'06',
        'يوليه':'07'}
    m_maps = months_map
    date_list = []

    for i in range(len(df)):

        if df.iloc[i].source == 'SaudiYoum':
            date_list.append(saudiyoum_date(df.iloc[i]['dateline']))
            #print(df.id.iloc[i] + ' successful')
            
        elif df.iloc[i].source == 'Techreen':
            date_list.append(techreen_date(df.iloc[i]['dateline']))
            #print(df.id.iloc[i] + ' successful')

        elif df.iloc[i].source == 'Youm7':
            date_list.append(youm7_date(df.iloc[i]['dateline'], m_maps))
            #print(df.id.iloc[i] + ' successful')

        elif df.iloc[i].source == 'Alittihad':
            date_list.append(alittihad_date(df.iloc[i]['dateline'], m_maps))
            #print(df.id.iloc[i] + ' successful')

        elif df.iloc[i].source == 'Almustaqbal':
            date_list.append(almustaqbal_date(df.iloc[i]['dateline']))
            #print(df.id.iloc[i] + ' successful')

        elif df.iloc[i].source == 'Ryiadh':
            date_list.append(ryiadh_date(df.iloc[i]['dateline'], m_maps))
            #print(df.id.iloc[i] + ' successful')

        elif df.iloc[i].source == 'Alqabas':
            date_list.append(alqabas_date(df.iloc[i]['dateline']))
            #print(df.id.iloc[i] + ' successful')

        elif df.iloc[i].source == 'Almasryalyoum':
            date_list.append(almasryalyoum_date(df.iloc[i]['dateline']))
            #print(df.id.iloc[i] + ' successful')

        elif df.iloc[i].source == 'Sabanews':
            date_list.append(sabanews_date(df.iloc[i]['dateline'], m_maps))
            #print(df.id.iloc[i] + ' successful')
            
        elif df.iloc[i].source == 'Echoroukonline':
            date_list.append(echoroukonline_date(df.iloc[i]['dateline']))
            #print(df.id.iloc[i] + ' successful')
    df['dateline'] = pd.to_datetime(date_list)
    df = df.dropna()
    return df

def using_ahocorasick(col, lst):
    A = ahocorasick.Automaton(ahocorasick.STORE_INTS)
    for word in lst:
        A.add_word(word.lower())
    A.make_automaton() 
    col = col.astype(str)
    col = col.str.lower()
    mask = col.apply(lambda x: bool(list(A.iter(x))))
    tags = col.apply(lambda x: list(A.iter(x)))
    return mask, tags

def look_for_words_in_text(df_text):
    
    topics = {'America' : 'أمريكا',
            'American' : 'أمريكيّ',
            'American (f)' : 'أمريكيّة',
            'American (pl)' : 'أمريكيّين',
            'The United States' : 'الولايات المتحدة',
            'The United States' : 'دول موحّدة',
            'Washington' : 'واشنطن',
            'Bush' : 'بوش',
            'Obama' : 'أوباما',
            'Cheney' : 'تشيني',
            'Clinton' : 'كلينتون',
            'Osama Bin Laden' : 'أسامة بن لادن',
            'Al Gore' : 'آل غور',
            'World Trade Center' : 'مركز التجارة العالمي',
            '9/11' : '9/11',
            'September 11' : '11 سبتمبر',
            'Gulf War' : 'حرب الخليج',
            'Google' : 'غوغل',
            'Facebook' : 'فيسبوك',
            'Al Qaida' : 'القاعدة'}
    
    topics = flip_key_value_pairs(topics)
    
    tags = []
    for key in topics.keys():
        if key in df_text:
            tags.append(key)
            
    return tags

def make_relevant_tagged_df(df):
    topics = {'America' : 'أمريكا',
            'American' : 'أمريكيّ',
            'American (f)' : 'أمريكيّة',
            'American (pl)' : 'أمريكيّين',
            'The United States' : 'الولايات المتحدة',
            'The United States' : 'دول موحّدة',
            'Washington' : 'واشنطن',
            'Bush' : 'بوش',
            'Obama' : 'أوباما',
            'Cheney' : 'تشيني',
            'Clinton' : 'كلينتون',
            'Osama Bin Laden' : 'أسامة بن لادن',
            'Al Gore' : 'آل غور',
            'World Trade Center' : 'مركز التجارة العالمي',
            '9/11' : '9/11',
            'September 11' : '11 سبتمبر',
            'Gulf War' : 'حرب الخليج',
            'Google' : 'غوغل',
            'Facebook' : 'فيسبوك',
            'Al Qaida' : 'القاعدة'}


    topics = flip_key_value_pairs(topics)
    mask, tags = using_ahocorasick(df.text, list(topics.keys()))

    copied = df[mask].copy()

    return copied, tags

def ramadan(df):
    date_list = []
    for i in range(len(df)):
        if (
        (df.dateline[i] >=dt.datetime(2001, 11, 17)) & (df.dateline[i] <= dt.datetime(2001, 12, 16))
        or (df.dateline[i] >=dt.datetime(2002, 11, 6)) & (df.dateline[i] <= dt.datetime(2002, 12, 5))
        or (df.dateline[i] >=dt.datetime(2003, 10, 27)) & (df.dateline[i] <= dt.datetime(2003, 11, 25))
        or (df.dateline[i] >=dt.datetime(2004, 10, 16)) & (df.dateline[i] <= dt.datetime(2004, 11, 13))
        or (df.dateline[i] >=dt.datetime(2005, 10, 5)) & (df.dateline[i] <= dt.datetime(2005, 11, 2))
        or (df.dateline[i] >=dt.datetime(2006, 9, 24)) & (df.dateline[i] <= dt.datetime(2006, 10, 23))
        or (df.dateline[i] >=dt.datetime(2007, 9, 13)) & (df.dateline[i] <= dt.datetime(2007, 10, 12))
        or (df.dateline[i] >=dt.datetime(2008, 9, 2)) & (df.dateline[i] <= dt.datetime(2008, 10, 1))
        or (df.dateline[i] >=dt.datetime(2009, 8, 22)) & (df.dateline[i] <= dt.datetime(2009, 9, 20))
        or (df.dateline[i] >=dt.datetime(2010, 8, 11)) & (df.dateline[i] <= dt.datetime(2010, 9, 9))
        or (df.dateline[i] >=dt.datetime(2011, 8, 1)) & (df.dateline[i] <= dt.datetime(2011, 8, 30))
        or (df.dateline[i] >=dt.datetime(2012, 7, 20)) & (df.dateline[i] <= dt.datetime(2012, 8, 18))
        or (df.dateline[i] >=dt.datetime(2013, 7, 9)) & (df.dateline[i] <= dt.datetime(2013, 8, 7))
        or (df.dateline[i] >=dt.datetime(2014, 6, 29)) & (df.dateline[i] <= dt.datetime(2014, 7, 28))):
            date_list.append(1)
        else:
            date_list.append(0)
        
    return date_list

def encode_tags(df):

    list_of_tags = []
    for tag in df.tags.values:
        list_of_tags.extend([val[1:-1] for val in tag[1:-1].split(', ')])

    tag_list = list(set(list_of_tags))

    for tag in tag_list:
        df[tag] = 0

    for i, tag in enumerate(df.tags):
        for t in tag_list:
            if t in tag:
                df[t].iloc[i] = 1
                
    return df
