#import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as plt
import matplotlib.pyplot as plt
import re
import datetime as dt
import warnings
from scipy import stats
from scipy.stats import pearsonr, spearmanr
from textwrap import wrap
from googletrans import Translator
from datetime import datetime
from datetime import timedelta
from textwrap import wrap
from sklearn.model_selection import train_test_split


def graph_source(df):
    source_perc = pd.crosstab(df.source, df.text_label, margins=True)
    source_perc = source_perc.apply(lambda x: x / x['All'] * 100, axis=1)
    source_perc = source_perc.drop(columns=['All'])
    source_perc = source_perc.reset_index()
    tech_saba = source_perc[(source_perc.source == 'Techreen') | (source_perc.source == 'Sabanews') | (source_perc.source == 'All')]
    tech_saba = tech_saba.set_index(tech_saba.source)
    #tech_saba = tech_saba.drop(columns=['source'])
    source_perc = source_perc.set_index(source_perc.source)
    plt.rcParams["figure.figsize"] = (20, 6)

    ax1 = source_perc.plot(kind='bar', color=['tomato', 'burlywood', 'royalblue'])
    ax2 = tech_saba.plot(kind='barh', color=['tomato', 'burlywood', 'royalblue'])

    ax1.set_xlabel("News Source", fontsize=20)
    ax2.set_xlabel("Sentiment Percentage", fontsize=20)

    ax1.set_ylabel("Sentiment Percentage", fontsize=20)
    ax2.set_ylabel("News Source", fontsize=20)

    xlabels = ax1.get_xticklabels() 
    ax1.set_xticklabels(labels=xlabels, rotation=45, fontsize=18)
    xlabels = ax2.get_xticklabels() 
    ax2.set_xticklabels(labels=xlabels, rotation=45, fontsize=18)

    ax1.set_title('Distributions of Sentiment Lablels per News Source', size=30)
    ax1.legend(fontsize=12, title='Article Sentiment',title_fontsize=15)

    ax2.set_title("Distributions of Sentiment Lablels of Techreen and Saba News", size=30)
    ax2.legend(fontsize=12, title='Article Sentiment',title_fontsize=15)

    plt.show()
    #view distributions of news sources w/target

def words():
    words = pd.read_csv('single_word_counts.csv')
    return words

def bigrams():
    bigrams = pd.read_csv('all_bigrams.csv')
    return bigrams 

def trigrams():
    trigrams = pd.read_csv('all_trigrams.csv')
    return trigrams

def print_list(list):
    print('\n'.join(list))


def encode_values(df, columns_to_encode):
    '''
    This function takes in a prepared dataframe and using one-hot encoding, encodes categorical variables. It does not drop the original
    categorical columns. This is done purposefully to allow for easier Exploratory Data Analysis.  Removal of original categorical columns
    will be done in a separate function later if desired.
    Parameters: df - a prepared dataframe with the expected feature names and columns
    Returns: encoded - a dataframe with all desired categorical columns encoded.
    '''
    df = df.reset_index()
    df['dateline'] = pd.to_datetime(df['dateline'])
    df.iloc[237549, df.columns.get_loc('dateline')] = '2008-04-02 00:00:00'
    dummies_list = columns_to_encode

    dummy_df = pd.get_dummies(df[dummies_list], drop_first=False)
    encoded = pd.concat([df, dummy_df], axis = 1)
    return encoded

def encoded_time(encoded):

    encoded = encoded.set_index('dateline').sort_index()
    encoded_1 = encoded.reset_index()
    time_1 = encoded_1[encoded_1.dateline < '2007-10-25']
    time_2 = encoded_1[encoded_1.dateline >= '2007-10-25']
    time_1 = time_1.set_index('dateline').sort_index()
    time_2 = time_2.set_index('dateline').sort_index()

    return time_1, time_2


def graph_timeline(time_1, time_2):

    plt.rcParams["figure.figsize"] = (16, 12)
    fig, ax = plt.subplots(2, 1)
    sns.lineplot(data = time_1.resample('1M').mean(), x = 'dateline', y = 'text_label_negative', label = 'neg', lw=3.5, color='tomato', ax=ax[0])
    sns.lineplot(data = time_1.resample('1M').mean(), x = 'dateline', y = 'text_label_neutral', label = 'neut', lw=3.5, color='burlywood', ax=ax[0])
    sns.lineplot(data = time_1.resample('1M').mean(), x = 'dateline', y = 'text_label_positive', label = 'pos', lw=3.5, color='royalblue', ax=ax[0])
    ax[0].axvline(dt.datetime(2001, 9, 11), c = 'slategrey', lw=2)
    ax[0].text(dt.datetime(2001, 9, 11),.7,'<-- 9/11',c = 'slategrey', size= 20, weight='bold')
    ax[0].axvline(dt.datetime(2003, 3, 1), c = 'slategrey', lw=2) # (something happened)
    ax[0].text(dt.datetime(2003, 3, 1),.95,'<-- Iraq invasion', c = 'slategrey', size= 20, weight='bold')
    ax[0].axvline(dt.datetime(2002, 7, 1), c = 'slategrey', lw=2) # (something happened)
    ax[0].text(dt.datetime(2002, 7, 1),.8,'<-- Al Yaum added',c = 'slategrey', size= 20, weight='bold')
    ax[0].axvline(dt.datetime(2003, 4, 9), c = 'slategrey', lw=2) # (something happened)
    ax[0].text(dt.datetime(2003, 4, 9),.89,'<-- Baghdad captured', c = 'slategrey', size= 20, weight='bold')
    #ax1.set_title('Distributions of Sentiment Lablels per News Source', size=30)

    ax[0].axvline(dt.datetime(2004, 11, 2), c = 'slategrey', lw=2) # (something happened)
    ax[0].text(dt.datetime(2004, 11, 2),.5,'<-- US election', c = 'slategrey', size= 20, weight='bold')
    ax[0].axvline(dt.datetime(2004, 5, 12), c = 'slategrey', lw=2) # (something happened)
    ax[0].text(dt.datetime(2004, 5, 12),.4,'<-- Nick Berg video', c = 'slategrey', size= 20, weight='bold')
    ax[0].axvline(dt.datetime(2004, 1, 1), c = 'slategrey', lw=2) # (something happened)
    ax[0].text(dt.datetime(2004, 1, 1),.15,'<-- Tishreen added', c = 'slategrey', size= 20, weight='bold')
    ax[0].axvline(dt.datetime(2006, 8, 30), c = 'slategrey', lw=2) # (something happened)
    ax[0].text(dt.datetime(2006, 8, 30),.8, '<-- Iran Nuclear Standoff', c = 'slategrey', size= 20, weight='bold')

    ax[0].set_xlabel("Timeline", fontsize=20, c = 'slategrey')
    ax[0].set_ylabel("Average Sentiment", fontsize=20, c = 'slategrey')
    #xlabels = ax[0].get_xticklabels() 
    #ax[0].set_xticklabels(labels=xlabels, rotation=45, fontsize=18)
    ax[0].set_title('Change in Sentiment: 2000 - 2008', fontsize=30, c = 'darkslategrey', weight='bold')
    ax[0].legend(fontsize=12, title='Percentage of Articles',title_fontsize=15, loc= 'lower right')
    # ax[1].set_xlabel("Timeline", fontsize=20, c = 'darkslategrey')
    # ax[1].set_ylabel("Average Sentiment", fontsize=20, c = 'darkslategrey')
    # #xlabels_1 = ax[1].get_xticklabels() 
    # #ax[1].set_xticklabels(labels=xlabels_1, rotation=45, fontsize=18)
    # ax[1].set_title('Change in Sentiment: 2004 - 2008', fontsize=30, c = 'darkslategrey', weight='bold')
    # ax[1].legend(fontsize=12, title='Percentage of Articles',title_fontsize=15, loc= 'right')


    sns.lineplot(data = time_2.resample('1M').mean(), x = 'dateline', y = 'text_label_negative', lw=3.5, color='tomato', label = 'neg', ax=ax[1])
    sns.lineplot(data = time_2.resample('1M').mean(), x = 'dateline', y = 'text_label_neutral', lw=3.5, color='burlywood',label = 'neut', ax=ax[1])
    sns.lineplot(data = time_2.resample('1M').mean(), x = 'dateline', y = 'text_label_positive', lw=3.5, color='royalblue', label = 'pos', ax=ax[1])

    ax[1].axvline(dt.datetime(2008, 11, 4), c = 'slategrey', lw=2) # (something happened)
    ax[1].text(dt.datetime(2008, 11, 4),.5,'<-- US election', c = 'slategrey', size= 20, weight='bold')
    ax[1].axvline(dt.datetime(2012, 11, 6), c = 'darkslategrey', lw=2) # (something happened)
    ax[1].text(dt.datetime(2012, 11, 6),.6,'<-- US election',  c = 'slategrey', size= 20, weight='bold')
    ax[1].axvline(dt.datetime(2011, 12, 20), c = 'darkslategrey', lw=2) # (something happened)
    ax[1].text(dt.datetime(2011, 12, 20),.4,'<-- Arab Spring Starts', c = 'slategrey', size= 20, weight='bold')

    ax[1].set_xlabel("Timeline", fontsize=20, c = 'slategrey')
    ax[1].set_ylabel("Average Sentiment", fontsize=20, c = 'slategrey')
    #xlabels_1 = ax[1].get_xticklabels() 
    #ax[1].set_xticklabels(labels=xlabels_1, rotation=45, fontsize=18)
    ax[1].set_title('Change in Sentiment: 2008 - 2014', fontsize=30, c = 'darkslategrey', weight='bold')
    ax[1].legend(fontsize=12, title='Percentage of Articles',title_fontsize=15, loc= 'lower right')

    fig.subplots_adjust(hspace=.4)
    fig.show()


'-------------------------------------------------------------------------------------'


def graph_tech(encoded):

    encoded = encoded.set_index('dateline').sort_index()
    techreen = encoded[encoded.source=='Techreen']
    not_tech = encoded[encoded.source!='Techreen']
    techreen = techreen[techreen.index > '2004-01-01']
    not_tech = not_tech[not_tech.index > '2004-01-01']

    plt.rcParams["figure.figsize"] = (16, 6)

    ax = sns.lineplot(data = techreen.resample('6M').mean(), x = 'dateline', y = 'text_label_negative', label = 'Negative Techreen', lw=8, color='tomato')
    ax = sns.lineplot(data = techreen.resample('6M').mean(), x = 'dateline', y = 'text_label_neutral', label = 'Neutral Techreen', lw=8, color='burlywood')

    ax = sns.lineplot(data = not_tech.resample('6M').mean(), x = 'dateline', y = 'text_label_negative', label = 'Negative Other', lw=2, color='tomato', linestyle='--')
    ax = sns.lineplot(data = not_tech.resample('6M').mean(), x = 'dateline', y = 'text_label_neutral', label = 'Neutral Other', lw=2, color='burlywood', linestyle='--')

    ax.set_xlabel("Timeline", fontsize=20, c = 'slategrey')
    ax.set_ylabel("Percentage of Articles", fontsize=20, c = 'slategrey')
        #xlabels = ax[0].get_xticklabels() 
        #ax[0].set_xticklabels(labels=xlabels, rotation=45, fontsize=18)
    ax.set_title('Timeline of Sentiment Change: Techreen compared to All Others', fontsize=30, c = 'darkslategrey', weight='bold')
    ax.legend(fontsize=12, title='Article Sentiment',title_fontsize=15, loc= 'lower right')

    plt.show()


'-------------------------------------------------------------------------------------'

def split_data(df):
    
    '''
    This function takes in a dataframe and splits it into three subgroups: train, test, validate
    for proper evalution, statistical testing, and modeling. Three dataframes are returned.
    '''

    train, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train, test_size=.3, random_state=123)
    
    return train, validate, test


def graph_source_perc(train):

    source_perc = pd.crosstab(train.source, train.text_label, margins=True)
    source_perc = source_perc.apply(lambda x: x / x['All'] * 100, axis=1)
    source_perc = source_perc.drop(columns=['All'])

    transcription_table=pd.DataFrame(
        {
            'source': ['Ryiadh','SaudiYoum' ,'Almasryalyoum', 'Youm7', 'Alittihad','Echoroukonline','Techreen', 'Alqabas', 'Almustaqbal', 'Sabanews'],
            'country': ["Ryiadh- Saudi_Arabia",'SaudiYoum- Saudi_Arabia', 'Almasryalyoum- Egypt','Youm7- Egypt', 'Alittihad- UAE','Echoroukonline- Algeria','Techreen- Syria', 'Alqabas- Kuwait', 'Almustaqbal- Lebanon','Sabanews- Yemen']
        }
    )

    mapping = transcription_table.set_index('source').to_dict()['country']

    train['country'] = train['source'].apply(lambda x: mapping.get(x))
    #map country to news source

    country_perc = pd.crosstab(train.country, train.text_label, margins=True)
    country_perc = country_perc.apply(lambda x: x / x['All'] * 100, axis=1)
    country_perc = country_perc.drop(columns=['All'])

    source_perc = source_perc.reset_index()

    tech_saba = source_perc[(source_perc.source == 'Techreen') | (source_perc.source == 'Sabanews') | (source_perc.source == 'All')]
    tech_saba = tech_saba.set_index(tech_saba.source)
    tech_saba = tech_saba.drop(columns=['source'])


    plt.rcParams["figure.figsize"] = (20, 6)

    ax1 = source_perc.plot(kind='bar', color=['tomato', 'burlywood', 'royalblue'])
    ax2 = tech_saba.plot(kind='barh', color=['tomato', 'burlywood', 'royalblue'])

    ax1.set_xlabel("News Source", fontsize=20)
    ax2.set_xlabel("Sentiment Percentage", fontsize=20)

    ax1.set_ylabel("Sentiment Percentage", fontsize=20)
    ax2.set_ylabel("News Source", fontsize=20)

    labels = [ '\n'.join(wrap(l, 14)) for l in country_perc.index]
    ax1.set_xticklabels(labels=labels, rotation=50, fontsize=18, ha='right', rotation_mode='anchor')
    xlabels = ax2.get_xticklabels() 
    ax2.set_xticklabels(labels=xlabels, rotation=45, fontsize=18)

    ax1.set_title('Distributions of Sentiment Lablels per News Source/Country', size=30)
    ax1.legend(fontsize=12, title='Article Sentiment',title_fontsize=15, loc='upper right')

    ax2.set_title("Distributions of Sentiment Lablels of Techreen and Saba News", size=30)
    ax2.legend(fontsize=12, title='Article Sentiment',title_fontsize=15, loc='upper right')

    plt.subplots_adjust(hspace=.8)
    plt.show()


def stat_test_1(train):

    alpha =.05

    observed = pd.crosstab(train.source, train.text_label)

    chi2, p, degf, expected = stats.chi2_contingency(observed)
    if p < alpha:
        print('Reject the null hypothesis.')
    else:
        print('Fail to reject the null hypothesis.')

def stat_test_2(train):

    transcription_table=pd.DataFrame({'source': ['Ryiadh','SaudiYoum' ,'Almasryalyoum', 'Youm7', 'Alittihad','Echoroukonline','Techreen', 'Alqabas', 'Almustaqbal', 'Sabanews'],'country': ["Ryiadh- Saudi_Arabia",'SaudiYoum- Saudi_Arabia', 'Almasryalyoum- Egypt','Youm7- Egypt', 'Alittihad- UAE','Echoroukonline- Algeria','Techreen- Syria', 'Alqabas- Kuwait', 'Almustaqbal- Lebanon','Sabanews- Yemen']})

    mapping = transcription_table.set_index('source').to_dict()['country']

    train['country'] = train['source'].apply(lambda x: mapping.get(x))
    
    alpha =.05
    observed = pd.crosstab(train.country, train.text_label)

    chi2, p, degf, expected = stats.chi2_contingency(observed)
    if p < alpha:
        print('Reject the null hypothesis.')
    else:
        print('Fail to reject the null hypothesis.')


def flip_key_value_pairs(dicts):
    
    res = dict((v,k) for k,v in dicts.items())    
    return res


def make_eng_tags(df_tags):
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
    eng_tags =[]
    
    rev_topics = flip_key_value_pairs(topics)
    for key, value in rev_topics.items():
        if key in df_tags:
            eng_tags.append(value)
            
    return eng_tags


def graph_tags(top_20):

    top_perc = pd.crosstab(top_20.en_tags, top_20.text_label, margins=True)
    top_perc = top_perc.apply(lambda x: x / x['All'] * 100, axis=1)
    top_perc = top_perc.drop(columns=['All'])

    tech_tags = top_20[(top_20.source == 'Techreen')]
    tech_tags = tech_tags.set_index(tech_tags.source)
    tech_tags = tech_tags.drop(columns=['source'])
    tech_tags = pd.crosstab(tech_tags.en_tags, tech_tags.text_label, margins=True)
    tech_tags = tech_tags.apply(lambda x: x / x['All'] * 100, axis=1)
    tech_tags = tech_tags.drop(columns=['All'])

    saba_tags = top_20[(top_20.source == 'Sabanews')]
    saba_tags = saba_tags.set_index(saba_tags.source)
    saba_tags = saba_tags.drop(columns=['source'])
    saba_tags = pd.crosstab(saba_tags.en_tags, saba_tags.text_label, margins=True)
    saba_tags = saba_tags.apply(lambda x: x / x['All'] * 100, axis=1)
    saba_tags = saba_tags.drop(columns=['All'])

    plt.rcParams["figure.figsize"] = (20, 4)

    ax1= top_perc.head(10).plot(kind='bar', color=['tomato', 'burlywood', 'royalblue'])
    ax2= top_perc.tail(10).plot(kind='bar', color=['tomato', 'burlywood', 'royalblue'])
    ax3= tech_tags.head(10).plot(kind='bar',color=['tomato', 'burlywood', 'royalblue'])
    ax4= saba_tags.head(10).plot(kind='bar',color=['tomato', 'burlywood', 'royalblue'])
    ax5= tech_tags.tail(10).plot(kind='bar',color=['tomato', 'burlywood', 'royalblue'])
    ax6= saba_tags.tail(10).plot(kind='bar',color=['tomato', 'burlywood', 'royalblue'])

    ax1.set_xlabel("News Source", fontsize=20) 
    ax2.set_xlabel("News Source", fontsize=20)
    ax3.set_xlabel("News Source", fontsize=20)
    ax4.set_xlabel("News Source", fontsize=20)
    ax5.set_xlabel("News Source", fontsize=20)
    ax6.set_xlabel("News Source", fontsize=20)

    ax1.set_ylabel("Sentiment Percentage", fontsize=20)
    ax2.set_ylabel("Sentiment Percentage", fontsize=20)
    ax3.set_ylabel("Sentiment Percentage", fontsize=20)
    ax4.set_ylabel("Sentiment Percentage", fontsize=20)
    ax5.set_ylabel("Sentiment Percentage", fontsize=20)
    ax6.set_ylabel("Sentiment Percentage", fontsize=20)

    labels = ax1.get_xticklabels() 
    ax1.set_xticklabels(labels=labels, rotation=50, fontsize=18, ha='right', rotation_mode='anchor')

    xlabels = ax2.get_xticklabels() 
    ax2.set_xticklabels(labels=xlabels, rotation=55, fontsize=18, ha='right', rotation_mode='anchor', wrap=True )

    xlabels = ax3.get_xticklabels() 
    ax3.set_xticklabels(labels=xlabels, rotation=55, fontsize=18, ha='right', rotation_mode='anchor' )
    xlabels = ax4.get_xticklabels() 
    ax4.set_xticklabels(labels=xlabels, rotation=55, fontsize=18, ha='right', rotation_mode='anchor' )
    xlabels = ax5.get_xticklabels() 
    ax5.set_xticklabels(labels=xlabels, rotation=55, fontsize=18, ha='right', rotation_mode='anchor' )
    xlabels = ax6.get_xticklabels() 
    ax6.set_xticklabels(labels=xlabels, rotation=55, fontsize=18, ha='right', rotation_mode='anchor' )

    ax1.set_title('Top 10 Most Occuring Tags', size=30)
    ax1.legend(fontsize=12, title='Article Sentiment',title_fontsize=15)
    # ax1.xticks(x_axis, [textwrap.fill(label, 10) for label in labels], 
    #            rotation = 10, fontsize=8, horizontalalignment="center")

    ax2.set_title('Next 10 (10-20) Most Occuring Tags', size=30)
    ax2.legend(fontsize=12, title='Article Sentiment',title_fontsize=15)

    ax3.set_title('Top 10 Most Occuring Tags: Techreen', size=30)
    ax3.legend(fontsize=12, title='Article Sentiment',title_fontsize=15)

    ax4.set_title('Top 10 Most Occuring Tags: Saba News', size=30)
    ax4.legend(fontsize=12, title='Article Sentiment',title_fontsize=15)

    ax5.set_title('Next 10 (10-20) Most Occuring Tags: Techreen ', size=30)
    ax5.legend(fontsize=12, title='Article Sentiment',title_fontsize=15)

    ax6.set_title('Next 10 (10-20) Most Occuring Tags: Saba News', size=30)
    ax6.legend(fontsize=12, title='Article Sentiment',title_fontsize=15)

    plt.show()


def stat_test_3(top_20):
    alpha =.05
    #set alpha
    observed = pd.crosstab(top_20.en_tags, top_20.text_label)

    chi2, p, degf, expected = stats.chi2_contingency(observed)
    if p < alpha:
        print('Reject the null hypothesis.')
    else:
        print('Fail to reject the null hypothesis.')

def graph_pres(train):

    train['english_tags'] = train['english_tags'].apply(lambda x: ','.join(map(str, x)))
    bush = train[(train['english_tags'] == 'Bush')]
    obama = train[(train['english_tags'] == 'Obama')]
    clinton = train[(train['english_tags'] == 'Clinton')]

    presidents = pd.concat([bush, obama, clinton])
    #dfs for presidents

    pres_perc = pd.crosstab(presidents.source, presidents.text_label, margins=True)
    pres_perc = pres_perc.apply(lambda x: x / x['All'] * 100, axis=1)
    pres_perc = pres_perc.drop(columns=['All'])

    clinton_perc = pd.crosstab(clinton.source, clinton.text_label, margins=True)
    clinton_perc = clinton_perc.apply(lambda x: x / x['All'] * 100, axis=1)
    clinton_perc = clinton_perc.drop(columns=['All'])

    bush_perc = pd.crosstab(bush.source, bush.text_label, margins=True)
    bush_perc = bush_perc.apply(lambda x: x / x['All'] * 100, axis=1)
    bush_perc = bush_perc.drop(columns=['All'])

    obama_perc = pd.crosstab(obama.source, obama.text_label, margins=True)
    obama_perc = obama_perc.apply(lambda x: x / x['All'] * 100, axis=1)
    obama_perc = obama_perc.drop(columns=['All'])

    plt.rcParams["figure.figsize"] = (20, 6)

    ax1= pres_perc.plot(kind='bar', color=['tomato', 'burlywood', 'royalblue'])
    ax2= clinton_perc.plot(kind='bar', color=['tomato', 'burlywood', 'royalblue'])
    ax3= bush_perc.plot(kind='bar', color=['tomato', 'burlywood', 'royalblue'])
    ax4= obama_perc.plot(kind='bar', color=['tomato', 'burlywood', 'royalblue'])

    ax1.set_xlabel("News Source", fontsize=20)
    ax2.set_xlabel("News Source", fontsize=20)
    ax3.set_xlabel("News Source", fontsize=20)
    ax4.set_xlabel("News Source", fontsize=20)

    ax1.set_ylabel("Sentiment Percentage", fontsize=20)
    ax2.set_ylabel("Sentiment Percentage", fontsize=20)
    ax3.set_ylabel("Sentiment Percentage", fontsize=20)
    ax4.set_ylabel("Sentiment Percentage", fontsize=20)


    xlabels = ax1.get_xticklabels() 
    ax1.set_xticklabels(labels=xlabels, rotation=45, fontsize=18)
    xlabels = ax2.get_xticklabels() 
    ax2.set_xticklabels(labels=xlabels, rotation=45, fontsize=18)
    xlabels = ax3.get_xticklabels() 
    ax3.set_xticklabels(labels=xlabels, rotation=45, fontsize=18)
    xlabels = ax4.get_xticklabels() 
    ax4.set_xticklabels(labels=xlabels, rotation=45, fontsize=18)


    ax1.set_title('Average Sentiments of All 3 President Tags', size=30)
    ax1.legend(fontsize=12, title='Article Sentiment',title_fontsize=15)

    ax2.set_title('Tag: President Clinton & Sentiment per Source', size=30)
    ax2.legend(fontsize=12, title='Article Sentiment',title_fontsize=15)

    ax3.set_title('Tag: President Bush & Sentiment per Source', size=30)
    ax3.legend(fontsize=12, title='Article Sentiment',title_fontsize=15)

    ax4.set_title('Tag: President Obama & Sentiment per Source', size=30)
    ax4.legend(fontsize=12, title='Article Sentiment',title_fontsize=15)


    plt.show()


def stat_test_4(train):
    bush = train[(train['english_tags'] == 'Bush')]
    obama = train[(train['english_tags'] == 'Obama')]
    clinton = train[(train['english_tags'] == 'Clinton')]

    presidents = pd.concat([bush, obama, clinton])
    alpha =.05

    observed = pd.crosstab(presidents.english_tags, presidents.text_label)

    chi2, p, degf, expected = stats.chi2_contingency(observed)
    if p < alpha:
        print('Reject the null hypothesis.')
    else:
        print('Fail to reject the null hypothesis.')

def graph_top_tags(train):
    train['english_tags'] = train.tags.apply(make_eng_tags)
    train['english_tags'] = train['english_tags'].apply(lambda x: ','.join(map(str, x)))
    top_20 = train[train['tags'].map(train['tags'].value_counts()) >= 720]
    top_20['en_tags'] = top_20['english_tags'].apply(lambda x: ','.join(map(str, x)))
    washington = train[(train['english_tags'] == 'Washington')]
    al_q = train[(train['english_tags'] == 'Al Qaida')]
    america = train[(train['english_tags'] == 'America')]

    america_perc = pd.crosstab(america.source, america.text_label, margins=True)
    america_perc = america_perc.apply(lambda x: x / x['All'] * 100, axis=1)
    america_perc = america_perc .drop(columns=['All'])

    alq_perc = pd.crosstab(al_q.source, al_q.text_label, margins=True)
    alq_perc = alq_perc.apply(lambda x: x / x['All'] * 100, axis=1)
    alq_perc = alq_perc.drop(columns=['All'])

    wash_perc = pd.crosstab(washington.source, washington.text_label, margins=True)
    wash_perc = wash_perc.apply(lambda x: x / x['All'] * 100, axis=1)
    wash_perc = wash_perc.drop(columns=['All'])

    plt.rcParams["figure.figsize"] = (20, 6)

    ax1 = wash_perc.plot(kind='bar', color=['tomato', 'burlywood', 'royalblue'])
    ax2 = alq_perc.plot(kind='bar', color=['tomato', 'burlywood', 'royalblue'])
    ax3 = america_perc.plot(kind='bar', color=['tomato', 'burlywood', 'royalblue'])

    ax1.set_xlabel("News Source", fontsize=20)
    ax2.set_xlabel("News Source", fontsize=20)
    ax3.set_xlabel("News Source", fontsize=20)

    ax1.set_ylabel("Sentiment Percentage", fontsize=20)
    ax2.set_ylabel("Sentiment Percentage", fontsize=20)
    ax3.set_ylabel("Sentiment Percentage", fontsize=20)

    xlabels = ax1.get_xticklabels() 
    ax1.set_xticklabels(labels=xlabels, rotation=45, fontsize=18)
    xlabels = ax2.get_xticklabels() 
    ax2.set_xticklabels(labels=xlabels, rotation=45, fontsize=18)
    xlabels = ax3.get_xticklabels() 
    ax3.set_xticklabels(labels=xlabels, rotation=45, fontsize=18)

    ax1.set_title('Tag: Washington & Sentiment per Source', size=30)
    ax1.legend(fontsize=12, title='Article Sentiment',title_fontsize=15)

    ax2.set_title('Tag: Al Queda & Sentiment per Source', size=30)
    ax2.legend(fontsize=12, title='Article Sentiment',title_fontsize=15)

    ax3.set_title('Tag: America & Sentiment per Source', size=30)
    ax3.legend(fontsize=12, title='Article Sentiment',title_fontsize=15)

    plt.show()




