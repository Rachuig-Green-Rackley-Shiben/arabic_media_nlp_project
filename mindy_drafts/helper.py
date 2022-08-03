import pandas as pd
import re


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

# def main(dataframe):
#     df = dataframe
#     months_map = {'يناير':'01',
#         'ينابر':'01',
#         'فبراير':'02',
#         'مارس':'03',
#         'أبريل':'04',
#         'ابريل':'04',
#         'مايو':'05',
#         'يونيو':'06',
#         'يوليو':'07',
#         'أغسطس':'08',
#         'اغسطس':'08',
#         'سبتمبر':'09',
#         'أكتوبر':'10',
#         'اكتوبر':'10',
#         'نوفمبر':'11',
#         'ديسمبر':'12',
#         'إبريل':'04',
#         'ماي':'05',
#         'يونيه':'06',
#         'يوليه':'07'}

#     for i in range(len(df)):
#         try:
#             if df.iloc[i].source == 'SaudiYoum':
#                 df.iloc[i]['dateline'] = saudiyoum_date(df.iloc[i]['dateline'])
            
#             elif df.iloc[i].source == 'Techreen':
#                 df.iloc[i]['dateline'] = techreen_date(df.iloc[i]['dateline'])
                
#             elif df.iloc[i].source == 'Youm7':
#                 df.iloc[i]['dateline'] = youm7_date(df.iloc[i]['dateline'], months_map)
                
#             elif df.iloc[i].source == 'Alittihad':
#                 df.iloc[i]['dateline'] = alittihad_date(df.iloc[i]['dateline'], months_map)
                
#             elif df.iloc[i].source == 'Almustaqbal':
#                 df.iloc[i]['dateline'] = almustaqbal_date(df.iloc[i]['dateline'])
                
#             elif df.iloc[i].source == 'Ryiadh':
#                 df.iloc[i]['dateline'] = ryiadh_date(df.iloc[i]['dateline'], months_map)
                
#             elif df.iloc[i].source == 'Alqabas':
#                 df.iloc[i]['dateline'] = alqabas_date(df.iloc[i]['dateline'])
                
#             elif df.iloc[i].source == 'Almasryalyoum':
#                 df.iloc[i]['dateline'] = almasryalyoum_date(df.iloc[i]['dateline'])
                
#             elif df.iloc[i].source == 'Sabanews':
#                 df.iloc[i]['dateline'] = sabanews_date(df.iloc[i]['dateline'], months_map)
                
#             elif df.iloc[i].source == 'Echoroukonline':
#                 df.iloc[i]['dateline'] = echoroukonline_date(df.iloc[i]['dateline'])
#         except:
#             return 'invalid'
#     return df

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
            print(df.id.iloc[i] + ' successful')
            
        elif df.iloc[i].source == 'Techreen':
            date_list.append(techreen_date(df.iloc[i]['dateline']))
            print(df.id.iloc[i] + ' successful')

        elif df.iloc[i].source == 'Youm7':
            date_list.append(youm7_date(df.iloc[i]['dateline'], m_maps))
            print(df.id.iloc[i] + ' successful')

        elif df.iloc[i].source == 'Alittihad':
            date_list.append(alittihad_date(df.iloc[i]['dateline'], m_maps))
            print(df.id.iloc[i] + ' successful')

        elif df.iloc[i].source == 'Almustaqbal':
            date_list.append(almustaqbal_date(df.iloc[i]['dateline']))
            print(df.id.iloc[i] + ' successful')

        elif df.iloc[i].source == 'Ryiadh':
            date_list.append(ryiadh_date(df.iloc[i]['dateline'], m_maps))
            print(df.id.iloc[i] + ' successful')

        elif df.iloc[i].source == 'Alqabas':
            date_list.append(alqabas_date(df.iloc[i]['dateline']))
            print(df.id.iloc[i] + ' successful')

        elif df.iloc[i].source == 'Almasryalyoum':
            date_list.append(almasryalyoum_date(df.iloc[i]['dateline']))
            print(df.id.iloc[i] + ' successful')

        elif df.iloc[i].source == 'Sabanews':
            date_list.append(sabanews_date(df.iloc[i]['dateline'], m_maps))
            print(df.id.iloc[i] + ' successful')
            
        elif df.iloc[i].source == 'Echoroukonline':
            date_list.append(echoroukonline_date(df.iloc[i]['dateline']))
            print(df.id.iloc[i] + ' successful')
    df['dateline'] = pd.to_datetime(date_list)
    df = df.dropna()
    return df