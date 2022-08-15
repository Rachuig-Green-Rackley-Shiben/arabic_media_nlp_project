# <center><a name="top"></a>Arabic Media NLP Capstone Project

by: Andrew Rachuig, Kyle Green, Mindy Shiben, and Paige Rackley </center>



 * * *  
[[Project Description](#project_description)]
[[Project Planning](#planning)]
[[Data Dictionary](#dictionary)]
[[Data Acquire and Prep](#wrangle)]
[[Data Exploration](#explore)]
[[Modeling](#model)]
[[Conclusion](#conclusion)]
___



## <a name="project_description"></a>Project Description:

## <a name="planning"></a>Project Planning:
  
  
 ### Project Goals: 
The goal of this project is to use the data we have acquired from our sources to build a classification model that can help predict an articles sentiment towards America. Through exploration using Natural Language Processing (NLP) and data visualizations, we want to find trends that will help us determine features to use in our model that will help us predict sentiment. By using NLP, we can deep dive into features further to even find correlations between specific words and sentiment that will help our predictions.
  
  
 ### Deliverables:
- [x] Clean Repo
- [x] README.md
- [x] Final Notebook
- [x] Scripting Files
- [x] Google Slides (~10-25 for presentation)

###  Executive Summary: 
Using our sentiment analysis tool (BERT), we discovered that approximently 73% of articles relating to America have a neutral sentiment, 23% were negative, and 4% were positive. 

Through exploration using Time Series analysis and Natural Language Processing (NLP), we also discovered notable outliers in sentiment from news sources and that some world events might have a relationship with article sentiment swings.

Our Random Forest model beat the baseline of 72.6% with an accuracy of 73.9%. This does beat our baseline, but is not predictive enough to be used to generalize sentiment in articles.
  
        
### Initial Hypothesis/Questions: 
<b>Through NLP exploration:</b>

- What is the frequency of sentiment labels (negative, positive, neutral) per news source?
- What is the subject matter of the majority of articles per source?
- What topics do news sources cover most frequently?

<b>Through Time Series analysis:</b>
- How does article sentiment change over time?
- Is there a relationship between article sentiment and world events?
- How does the sentiment of Techreen aricles over time compare to Non-Techreen articles?

<b>Through exploration of drivers of article sentiment:</b>
- What (if any) is the relationship between news sources & country to article sentiment?
- What (if any) is the relationship between tag (article topic) to article sentiment?
- Are there any sources that have change in sentiment based on president tag?
- What (if any) is the relationship of the top 3 occuring tags (excluding president names) and article sentiment by individual news sources?
- What (if any) is the relationship between Ramadan to article sentiment?


[[Back to top](#top)]


## <a name="dictionary"></a>Data Dictionary  
[[Back to top](#top)]

|Column Name|Datatype|Definition|
|:-------|:--------|:----------|
| id       | object |    id of article |
| url       | object |    URL to article |
| headline       | object |    Headline to article |
| dateline       | datetime64[ns] |    Date/Time article was published |
| text      | object |   Text in article |
| tags       | object |    Tags for article |
| source | object | Website/newspaper that published the article |
| text_label | object | the text within the article which is categorized as either positive, negative or neutral |
| text_score | object | sentiment score for text in article |
| headline_label | object | the headline of the article which is categorized as either positive, negative, or neutral  |
| headline_score | object | sentiment score for headline of an article | 

***

## <a name="wrangle"></a>Data Acquisition and Preparation
  
## Acquire
- All data was sourced from the [Abu El-Khair Corpus](http://abuelkhair.net/index.php/en/arabic/abu-el-khair-corpus)
    - Includes more than five million Arabic news articles from 2000-2014
- Downloaded 10 separate XML files containing all the articles (~ 20 GB)

[[Back to top](#top)]

## Prepare
Preparation for the data took a more considerable amount of effort. Upon inspection, we found that the XML contained errors, so we created a series of expressions to pull the data we needed and compiled it all into a dataframe.

With the new dataframe, we used keywords related to America (e.g 'George Bush, Barack Obama, America, The United States, The White House') and came out with about 360,000 articles to isolate and explore on.

<b>Cleaning:</b>

    - Sentiment analysis using Camel-Tools
    - remove unneccesary special characters
    - delete any possible diacritical marks
    - tokenize individual words 

[[Back to top](#top)]


  
## <a name="explore"></a>Data Exploration:
##  Explore
- Explore on the data using various Natural Language Processing techniques
- Create visualizations of discoveries
- Hypothesis test ideas
- Feature Engineering
  - Add new features derived from discoveries made during Exploration

 
[[Back to top](#top)]

### Takeaways from exploration:
Through exploration, we were able to get a sense of how news sources presented specific topics to its readers. From the information present in the dataset alone we cannot determine a causal relationship and say that topics related to America are causing the sentiment, but we can show a relationship between certain topics, words, publications, events, and sentiment. 

A major takeaway that we found was that it seems rather obvious that Techreen either has a negative bias when America related topics are discussed OR it selects to write more about negative things when discussing America.

## <a name="model"></a>Modeling:
<b> Looking at the baseline we need to beat:</b>
Before we model, we establish our baseline by picking the most frequently occurring target. In this case, neutral appears 72.6% of the time, making our baseline accuracy 72.6%. Anything higher than this means our model is more predictive.

<b>How did we decide our model?</b>
After creating 150 different models, we came to the conlcusion that random forests models were performing best. These are shown above. By minimizing the difference in train and validate accuracy in the random forest model, we have a model that is generalizable and not overfitting. 

Our final model has a depth of 14, and a minimum sample leaf of one. After choosing our model, we can run it on our test set.

<b>Results:</b>
Our final result is that our model had an accuracy of **73.9%** on our test set.
  
[[Back to top](#top)]



## <a name="conclusion"></a>Conclusion:
  
 # Conclusion:

> * Our model had an accuracy of **73.9%** on our test set, beating baseline by **1.8%**.
> * Our model is a Random Forest Classification Model, with a depth of 14 and a minimum sample leaf of one.
> * Although our model beats baseline, we do not feel confident enough to recommend it without further exploring other potential features.


  
### With more time:
    - improve predictive ability by finding more valuable features to pass into the model.
    - acquire news articles written in English and Arabic by the same news source to compare the sentiment by language. 
    
## Recomendations: 
With the current prediction score, we cannot endorse utilization of our model with the current set of features to predict sentiment. However, our model did give us insight into understanding how certain factors played into sentiment and this fueled further exploration of the textual data. Specifically, it reinforced findings about news sources and countries as well highlighted which keywords and events were the most impactful.
####

[[Back to top](#top)]
  
  
  **How to Reproduce**
- [x] Read this README.md
- [] 
