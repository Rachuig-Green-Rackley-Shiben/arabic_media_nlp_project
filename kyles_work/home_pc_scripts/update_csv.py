import os
import pandas as pd
import time
from datetime import datetime
import date_fixer

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
        daily_csv = date_fixer.make_datetime(daily_csv)
        print('writing csv...')
        daily_csv.to_csv(parent + f'daily{curr_time.month}_{curr_time.day}.csv', index=False)
        print(f'csv written. updating in google drive as of {curr_time.hour}:{curr_time.min}')
        waiting = True
    
