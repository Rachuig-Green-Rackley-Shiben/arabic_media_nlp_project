import os
import pandas as pd
import time
from datetime import datetime

import pyautogui


pyautogui.PAUSE = 15
pyautogui.FAILSAFE = True

waiting = False

while True:

    pyautogui.moveTo(100, 200, 2)
    time.sleep(5)
    curr_time = pd.Timestamp.now()
    pyautogui.moveTo(200,100, 2)


    if curr_time.hour == 0:
        waiting = False
    if curr_time.hour == 7 and not waiting:

        all_dfs = []
        path = '/Users/kylegreen/codeup-data-science/arabic_media_nlp_project/kyles_work/labeled_split_articles/'
        parent = '/Users/kylegreen/My Drive/arabic_NLP/'
        for fi in os.listdir('/Users/kylegreen/codeup-data-science/arabic_media_nlp_project/kyles_work/labeled_split_articles'):
            all_dfs.append(pd.read_csv(path + fi))

        daily_csv = pd.concat(all_dfs).reset_index()
        daily_csv.to_csv(parent + f'daily{curr_time.month}_{curr_time.day}.csv', index=False)
        waiting = True
