import os
import pandas as pd
import time
from datetime import datetime

if __name__ == '__main__':

    curr_time = pd.Timestamp.now()
    parent = 'E:/drive/arabic_NLP/'

    df = pd.read_csv(parent + f'daily{curr_time.month}_{curr_time.day}.csv')
    print(df.head())
    print(df.shape)
    print('showing datetime')
    print(df.dateline)