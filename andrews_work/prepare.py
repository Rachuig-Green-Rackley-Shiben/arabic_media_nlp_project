import pandas as pd
import date_fixer

from camel_tools.utils.normalize import normalize_unicode
from camel_tools.utils.normalize import normalize_alef_maksura_ar
from camel_tools.utils.normalize import normalize_alef_ar
from camel_tools.utils.normalize import normalize_teh_marbuta_ar
from camel_tools.utils.dediac import dediac_ar
from camel_tools.tokenizers.word import simple_word_tokenize
import re

def clean_text(df):
    cleaned_list = []
    for i in range(len(df)):
    # for i in range(10):
        text = df.text[i]
        text = normalize_unicode(text)
        text = re.sub(r"[+,*:;.|!()${}/«»\-\'\"،؟]|\n", '', text)
        text = re.sub(r"[0-9]", '', text)
        text = normalize_alef_ar(text)
        text = normalize_alef_maksura_ar(text)
        text = normalize_teh_marbuta_ar(text)
        text = dediac_ar(text)
        text = simple_word_tokenize(text)
        cleaned_list.append(text)
        print(i)
    df['cleaned_text'] = cleaned_list
    df.to_csv('/Users/amanda22/codeup-data-science/arabic_media_nlp_project/andrews_work/cleaned_df.csv', index=False)
    return df

def encode_sentiment(df, columns_to_encode):
    '''
    This function takes in a prepared dataframe and using one-hot encoding, encodes categorical variables. It does not drop the original
    categorical columns. This is done purposefully to allow for easier Exploratory Data Analysis.  Removal of original categorical columns
    will be done in a separate function later if desired.
    Arguments: df - a prepared dataframe with the expected feature names and columns
    Returns: encoded - a dataframe with all desired categorical columns encoded.
    '''
    dummies_list = columns_to_encode

    dummy_df = pd.get_dummies(df[dummies_list], drop_first=False)
    encoded = pd.concat([df, dummy_df], axis = 1)
    return encoded

def country_tagger(df):
    country_map = { 'Alittihad': 'emirates',
                    'Echoroukonline': 'algeria',
                    'Ryiadh': 'ksa',
                    'SaudiYoum': 'ksa',
                    'Techreen': 'syria',
                    'Alqabas': 'kuwait',
                    'Almustaqbal': 'lebanon',
                    'Almasryalyoum': 'egypt',
                    'Youm7': 'egypt',
                    'Sabanews': 'yemen',
                    }
    df['country'] = df.source.map(country_map)
    return df

