from attr import validate
from regex import E
from sklearn.neighbors import KNeighborsClassifier

import scipy.stats as stats
import pandas as pd
import numpy as np
import seaborn as sns
import os
import split
import matplotlib.pyplot as plt
import itertools

import datetime as dt
from sklearn.preprocessing import MinMaxScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

def impute_value(train, validate, test, col_names, strategy='most_frequent'):
    '''imputes value for given column names for tain, validate, and test sets using mode.'''
    for col in col_names:
        imputer = SimpleImputer(missing_values= np.NaN, strategy=strategy)
        imputer = imputer.fit(train[[col]])

        train[[col]] = imputer.transform(train[[col]])
        validate[[col]] = imputer.transform(validate[[col]])
        test[[col]] = imputer.transform(test[[col]])

    return train, validate, test

def all_reports(train, validate, test, target_var):
    '''Runs several different classification models and returns results of each.'''
    models, reports = decision_tree(train, validate, test, target_var)
    dt_mods = Results(models, reports, target_var)
    
    models, reports = random_forests(train, validate, test, target_var)
    rf_mods = Results(models, reports, target_var)
    
    models, reports = knearest_neightbors(train, validate, test, target_var)
    knn_mods = Results(models, reports, target_var)

    models, reports = logistic_regression(train, validate, test, target_var)
    lr_mods = Results(models, reports, target_var)
    


    return dt_mods, rf_mods, knn_mods, lr_mods

def xy_train_validate_test(train, validate, test, target_var):
    '''
    Splits train, validate and test sets by target variable to 
    model-compatible x and y inputs.
    '''
    id= 'customer_id'
    
    x_train = train.drop(columns=[target_var])
    y_train = train[target_var]

    x_validate = validate.drop(columns=[target_var])
    y_validate = validate[target_var]

    X_test = test.drop(columns=[target_var])
    Y_test = test[target_var]

    return x_train, y_train, x_validate, y_validate, X_test, Y_test

def random_forests(train, validate, test, target_var, 
                   min_sample_leaf=3, depth=15, inverse=True):
    '''
    Iterates through random forest models.
    '''
    x_train, y_train, x_validate, y_validate, X_test, Y_test = xy_train_validate_test(train,
                                                                                      validate,
                                                                                      test, 
                                                                                      target_var)
    models = []
    model_type = 'random_forests'
    reports = []
                                                                             
    for num in range(1, depth + 1):
        # Have min_sample_leafs decrease as depth increases
        if inverse:
            min_sample_leaf = abs((depth+1)-num)

        clf = RandomForestClassifier(max_depth=num, min_samples_leaf=min_sample_leaf, random_state=123)
        models.append(fit_score_train_validate(clf, num, x_train, x_validate, 
                                               y_train, y_validate, model_type,
                                               min_sample_leaf)[0])
        reports.append(fit_score_train_validate(clf, num, x_train, x_validate, y_train, y_validate, model_type)[1])
        
    models = make_model_results_into_df(models)
    
    return models, reports

def knearest_neightbors(train, validate, test, target_var, n_neighbors=list(range(1,15))):
    '''
    Iterates through knn models.
    '''
    x_train, y_train, x_validate, y_validate, X_test, Y_test = xy_train_validate_test(train,
                                                                                      validate,
                                                                                      test, 
                                                                                      target_var)
    models = []
    reports = []
    model_type = 'knn'
    weights = ['uniform', 'distance']

    for weight in weights:
        model_type = 'knn_' + weight
        for n in n_neighbors:
            knn = KNeighborsClassifier(n_neighbors=n, weights=weight)
            models.append(fit_score_train_validate(knn, n, x_train, x_validate, y_train, y_validate, model_type)[0])
            reports.append(fit_score_train_validate(knn, n, x_train, x_validate, y_train, y_validate, model_type)[1])
        
    models = make_model_results_into_df(models)

    return models, reports


def decision_tree(train, validate, test, target_var, depth=10, loop=True):
    '''
    Iterates through decision tree models.
    '''
    x_train, y_train, x_validate, y_validate, X_test, Y_test = xy_train_validate_test(train,
                                                                                      validate,
                                                                                      test, 
                                                                                      target_var)
    models = []
    reports = []
    model_type = 'decision_tree'

    if loop:                                                                      
        for num in range(1, depth + 1):
            clf = DecisionTreeClassifier(max_depth=num, random_state=123)
            models.append(fit_score_train_validate(clf, num, x_train, x_validate, y_train, y_validate, model_type)[0])
            reports.append(fit_score_train_validate(clf, num, x_train, x_validate, y_train, y_validate, model_type)[1])
        
        models = make_model_results_into_df(models)
    else:
        clf = DecisionTreeClassifier(max_depth=depth, random_state = 123)
        models.append(fit_score_train_validate(clf, depth, x_train, x_validate, y_train, y_validate, model_type)[0])
        reports.append(fit_score_train_validate(clf, depth, x_train, x_validate, y_train, y_validate, model_type)[1])
        models = make_model_results_into_df(models)

    return models, reports


def logistic_regression(train, validate, test, target_var, c=10, solver='lbfgs'):
    '''
    Iterates through logistic regression models.
    '''
    x_train, y_train, x_validate, y_validate, X_test, Y_test = xy_train_validate_test(train,
                                                                                      validate,
                                                                                      test,
                                                                                      target_var)
    models = []
    reports = []
    model_type = 'logistic_regression'
    solver=solver
    fit_intercept = False
    if solver=='liblinear':
        fit_intercept=True
                                                                 
    for num in np.arange(.1, c+.1, .1):
        logit = LogisticRegression(C=c, random_state=123, fit_intercept=fit_intercept, intercept_scaling=7.5, solver=solver)
        models.append(fit_score_train_validate(logit, num, x_train, x_validate, y_train, y_validate, model_type)[0])
        reports.append(fit_score_train_validate(logit, num, x_train, x_validate, y_train, y_validate, model_type)[1])
    
    models = make_model_results_into_df(models)

    return models, reports

def fit_score_train_validate(clf, num, x_train, x_validate, 
                             y_train, y_validate, model_type,
                             min_sample_leaf=""):
    '''
    Fits a model and scores it on train and validate sets, then returns the results
    and classification reports.
    '''
    clf = clf.fit(x_train, y_train)
    results = []
    
    # predictions on train observations
    y_pred_train = clf.predict(x_train)
    train_score = clf.score(x_train, y_train)
    #print(train_score)
    train_class_report = classification_report(y_train, y_pred_train, output_dict=True)
    train_class_report = pd.DataFrame(train_class_report).T
    labels = sorted(y_train.unique())
    train_confusion_matrix = pd.DataFrame(confusion_matrix(y_train, y_pred_train), index=labels, columns=labels)

    y_pred_validate = clf.predict(x_validate)
    validate_score = clf.score(x_validate, y_validate)
    #print(validate_score)
    
    validate_confusion_matrix = pd.DataFrame(confusion_matrix(y_validate, y_pred_validate), index=labels, columns=labels)
    validate_class_report = classification_report(y_validate, y_pred_validate, output_dict=True)
    validate_class_report = pd.DataFrame(validate_class_report).T

    results = make_model_stats(num, train_score, validate_score, 
                               train_class_report, validate_class_report,
                               min_sample_leaf, model_type)


    reports = {'train_report': train_class_report, 
               'validate_report': validate_class_report,
               'train_confusion_matrix': train_confusion_matrix, 
               'validate_confusion_matrix': validate_confusion_matrix,
               #'class_names': clf.classes_.as_type('str'),
               'clf': clf
               }

    return results, reports

def make_model_stats(num, train_score, validate_score, 
                     train_class_report, validate_class_report,
                     min_sample_leaf, model_type):

    '''
    Creates DataFrame-compatible dictionaries based off of model scores and parameters.
    '''

    results = ({'depth': num,
                'C': num,
                'min_samples_leaf': min_sample_leaf, 
                'n_nearest_neighbor': num,
                'train_accuracy': train_score, 
                'validate_accuracy': validate_score, 
                'difference': train_score - validate_score,
                'percent_diff': round((train_score - validate_score) / train_score * 100, 2),
                'classification_report_validate': validate_class_report,
                'classification_report_train': train_class_report,
                'model_type': model_type
              })
    
    results = edit_results(results, model_type)
    return results

def edit_results(results, model_type):
    '''
    Edits model results based off of model type and parameters,
    returns the edited results.
    '''
    
    if model_type[:3] == 'knn':
        del(results['depth'])
        del(results['min_samples_leaf'])
        del(results['C'])
        
        return results
    elif model_type == 'decision_tree':
        del(results['n_nearest_neighbor'])
        del(results['min_samples_leaf'])
        del(results['C'])
        
        return results
    elif model_type == 'random_forests':
        del(results['n_nearest_neighbor'])
        del(results['C'])
        
        return results
    if model_type == 'logistic_regression':
        del(results['depth'])
        del(results['n_nearest_neighbor'])
        del(results['min_samples_leaf'])

        return results


def make_model_results_into_df(models):
    '''
    Takes the model results and turns it into a DataFrame.
    '''
    models= pd.DataFrame(models)
    
    return models

def summary_results(models):
    '''
    Returns a summary of all models and their results.
    '''
    summary_cols = list(models.columns)
    summary_cols.remove('model_type')
    summary_cols.remove('classification_report_train')
    summary_cols.remove('classification_report_validate')
    summary_cols.insert(0, 'model_type')

    return models[summary_cols]

def difference_means(models):
    differences = {'difference_mean': models.difference.mean(),
                   'percent_diff_mean': models.percent_diff.mean()}

    return differences

def make_total_summary(all_Results):
    
    total = pd.DataFrame()
    all_summaries = [result for result in all_Results]
    
    for summary in all_summaries:
        total = pd.concat([total, summary])
    
    return total


    
class Results:
    all_instances = []
    baseline = ''
    total_summary = pd.DataFrame()

    def __init__(self, models_df, reports, target_var):
        self.target_var = target_var
        self.reports = reports
        self.df = models_df
        self.columns = self.df.columns
        self.diff_mean = difference_means(self.df)['difference_mean']
        self.percent_diff_mean = difference_means(self.df)['percent_diff_mean']

        self.summary = summary_results(self.df)
        self.model_types = self.df.model_type.unique()
        
        Results.all_instances.append(self.summary)

        Results.total_summary = make_total_summary(Results.all_instances) 

    def set_baseline(self,baseline):
        if self.baseline:
            return self.baseline
        else:
            self.baseline = baseline

    def add_baseline_to_summary(self):
        if self.baseline:
            if 'baseline' in self.summary.columns:
                return self.summary
            else:
                self.summary['baseline'] = self.baseline
                return self.summary
        else:
            return 'baseline not set!'

    def remove_baseline_from_summary(self):
        if self.baseline:
            if 'baseline' in self.summary.columns:
                self.summary = self.summary.drop(columns='baseline')
                return self.summary
            else:
                return self.summary
        else:
            return 'baseline not set!'

    def add_model_type_to_summary(self):
        if 'model_type' not in self.summary.columns:
            self.summary['model_type'] = self.model_type
            return self.summary
        else:
            return self.summary

    def remove_model_type_from_summary(self):
        if 'model_type' in self.summary.columns:
            self.summary = self.summary.drop(columns='model_type')
            return self.summary
        else:
            return self.summary

    def report(self, index=0):
        for i, report in enumerate(self.reports):
            if index and i == index:
                print(f'Training report for index {i}:\n', report["train_report"], '\n')
                print(f'Validate report for index {i}:\n', report["validate_report"], '\n')
                return report['train_report'], report['validate_report']
            elif not index:
                print(f'Train report for index {i}:\n', report['train_report'], '\n')
                print(f'Validate report for index {i}:\n', report['validate_report'], '\n')
    
    def train_confusion_matrix(self, index=None):
        for i, report in enumerate(self.reports):
            if index==None:
                print(f'Train report for index {i}:\n', report['train_confusion_matrix'], '\n')
            elif i == index:
                print(f'Train Confusion Matrix for index {i}: \n', report['train_confusion_matrix'])
                return report['train_confusion_matrix']

    def validate_confusion_matrix(self, index=None):
        for i, report in enumerate(self.reports):
            if index==None:
                print(f'Validate report for index {i}:\n', report['validate_confusion_matrix'], '\n')
            elif i == index:
                print(f'Validate Confusion Matrix for index {i}: \n', report['train_confusion_matrix'])
                return report['train_confusion_matrix']
            
    def train_report(self, index=0):
        for i, report in enumerate(self.reports):
            if index and i == index:
                print(f'Train report for index {i}:\n', report["train_report"], '\n')
                return report['train_report']
            elif not index:
                print(f'Train report for index {i}:\n', report['train_report'], '\n')

    def validate_report(self, index=0):
        for i, report in enumerate(self.reports):
            if index and i == index:
                print(f'Validate report for index {i}:\n', report["validate_report"], '\n')
                return report['validate_report']
            elif not index:
                print(f'Validate report for index {i}:\n', report['validate_report'], '\n')

    def by_min_sample_leaf_equals(self, N, inclusive=False):
        return self.df[self.df.min_samples_leaf == N]

    def by_min_sample_leaf_gtr_than(self, N, inclusive=False):
        if inclusive:
            return self.df[self.df.min_samples_leaf >= N]
        else:
            return self.df[self.df.min_samples_leaf > N]

    def by_min_sample_leaf_less_than(self, N, inclusive=False):
        if inclusive:
            return self.df[self.df.min_samples_leaf <= N]
        else:
            return self.df[self.df.min_samples_leaf < N]

    def by_depth_equals(self, depth):
        return self.df[self.df.depth == depth]

    def by_depth_gtr_than(self, depth, inclusive=False):
        
        if inclusive:
            return self.df[self.df.depth >= depth]
        else:
            return self.df[self.df.depth >  depth]
    
    def by_depth_less_than(self, depth, inclusive=False):
        if inclusive:
            return self.df[self.df.depth <= depth]
        else:
            return self.df[self.df.depth < depth]

    def by_percent_diff_less_than(self, num, inclusive=False):
        if inclusive:
            return self.df[self.df.percent_diff <= num]
        else:
            return self.df[self.df.percent_diff < num]
    
    def by_percent_diff_gtr_than(self, num, inclusive=False):
        if inclusive:
            return self.df[self.df.percent_diff >= num]
        return self.df[self.df.percent_diff > num]

    def by_train_acc_less_than(self, num, inclusive=False):
        if inclusive:
            return self.df[self.df.train_accuracy <= num]
        else:
            return self.df[self.df.train_accuracy < num]

    def by_train_acc_gtr_than(self, num, inclusive=False):
        if inclusive:
            return self.df[self.df.train_accuracy >= num]
        else:
            return self.df[self.df.train_accuracy > num]

    def by_validate_acc_less_than(self, num, inclusive=False):
        if inclusive:
            return self.df[self.df.validate_accuracy <= num]
        else:
            return self.df[self.df.validate_accuracy < num]

    def by_validate_acc_gtr_than(self, num, inclusive=False):
        if inclusive:
            return self.df[self.df.validate_accuracy >= num]
        else:
            return self.df[self.df.validate_accuracy > num]

    def by_mod_types(df, model_types):
        fin_df = pd.DataFrame()

        for a_type in model_types:
            fin_df =  pd.concat([fin_df, df[df.model_type == a_type]])
        
        return fin_df

def model_train_val_test(encoded_df):
    train, validate, test = split.train_validate_test_split(encoded_df, 'text_label')
    clf = RandomForestClassifier(max_depth=14, min_samples_leaf=1, random_state=0)

    x_train = train.drop(columns='text_label')
    y_train = train['text_label']
    
    x_validate = validate.drop(columns='text_label')
    y_validate = validate['text_label']

    x_test = test.drop(columns='text_label')
    y_test = test['text_label']

    clf.fit(x_train, y_train)

    train_score = clf.score(x_train, y_train)
    validate_score = clf.score(x_validate, y_validate)
    test_score = clf.score(x_test, y_test)
    
    results = pd.DataFrame({
        'model': 'random_forests',
        'depth': '14',
        'min_sample_leaf': '1',
        'train_acc': round(train_score * 100,1),
        'validate_acc': round(validate_score * 100,1),
        'test_acc': round(test_score * 100, 1)
        }, index=range(1))
    
    return results, clf

def encode_data():
    '''
    Encodes and adds features to the final DataFrame loaded from final_df.csv
    '''
    df = pd.read_csv('final_df.csv')
    df.dateline = df.dateline.astype('datetime64')

    def is_gov_controlled(entry):
        if entry in ['Alqabas', 'Echoroukonline', 'Ryiadh', 'Saudiyoum', 'Almustaqbal', 'Youm7', 'Almasryalyoum']:
            return 1
        else:
            return 0

    df['ownership_status'] = df.source.apply(is_gov_controlled)


    def encode_values(df, columns_to_encode):
        '''
        This function takes in a prepared dataframe and using one-hot encoding, encodes categorical variables. It does not drop the original
        categorical columns. This is done purposefully to allow for easier Exploratory Data Analysis.  Removal of original categorical columns
        will be done in a separate function later if desired.
        Parameters: df - a prepared dataframe with the expected feature names and columns
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

    def within_30_days(df_dateline, date):

        if (df_dateline - date).days < 30 and (df_dateline - date).days > -30:
            return 1
        else:
            return 0

    important_dates = {
        'september_11th': pd.to_datetime('09-11-2001'),
        'capture_of_baghdad': pd.to_datetime('04-09-2003'),
        'nick_berg': pd.to_datetime('05-12-2004'),
        'iran_nulcear': pd.to_datetime('08-30-2006'),
        'arab_spring': pd.to_datetime('12-20-2011')
    }

    for event, date in important_dates.items():
        df[event] = df.dateline.apply(within_30_days, args = (date,))

    df = country_tagger(df)


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


    df = encode_tags(df)

    df.head()
    #print('encoding...')
    encoded = encode_values(df, ['source', 'country'])
    encoded.head()

    #print('scaling...')
    df['scaled_date'] = (df.dateline.astype('datetime64') - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

    scaler = MinMaxScaler()

    scaler.fit(df[['scaled_date']])

    df['scaled_date'] = scaler.transform(df[['scaled_date']])
    #print('encoding...')

    #print('dropping non-encoded columns')

    tags_to_drop = ['id', 'url', 'headline', 'dateline', 'text', 'tags', 'source', 'text_score', 'headline_label', 'headline_score', 'country']

    encoded = encoded.rename(columns={'scaled_date': 'scaled_pub_date'})

    encoded = encoded.drop(columns=tags_to_drop)
    #print('splitting...')
    encoded.text_label = encoded.text_label.map({'neutral': 0, 'negative': -1, 'positive': 1})

    return encoded


def encode_and_model():
    encoded = encode_data()

    features = ['source_Techreen', 'country_syria', 'source_Almasryalyoum', 'country_emirates', 'source_Alittihad', 'source_Youm7', 'source_SaudiYoum', 'country_yemen', 'source_Sabanews', 'country_ksa', 'capture_of_baghdad', 'ownership_status', 'source_Alqabas', 'country_kuwait', 'nick_berg', 'text_label']

    words = '??????, ????????????, ????????, ??????????, ?????? ????????????'
    words = words.split(', ')
    features.extend(words)

    to_remove = ['country_syria', 'source_Alittihad', 'source_Sabanews']
    [features.remove(x) for x in to_remove]


    results, clf = model_train_val_test(encoded[features])
    return results