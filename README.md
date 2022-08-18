# <center><a name="top"></a>Arabic Media NLP Capstone Project

<img src="andrews_work/final_intro_map_cropped.png">

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
The United States has made itself a key player in the Middle East by using its diplomatic, economic, and military power in support of national and international interests. Since the 9/11 terrorist attacks on U.S. soil, one of the most consequntial events in the modern world, tensions between the two regions have been undoubtedly high. With remarkable communication and technology enhancements in the 21st century, we've become more aware of biases portrayed in mainstream media, and Middle Eastern media is no exception. Two-thirds of Arab nationals overall say they trust mass media such as newspapers, TV, and radio to report news fully, fairly, and accurately (mideastmedia.org, 2017). Using a set of 5.2 million Arabic news articles written between 2000 and 2014 from 10 different Middle Eastern news outlets, we can see how different factors (such as international events) may drive overall sentiment and sentiment towards America. Having this kind of insight may inform policy makers and influence decision making moving forward. This project can deliver an integral piece of the puzzle of America's foreign policy towards the world.

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
Using our sentiment analysis tool (Camel-BERT), we discovered that approximently 73% of articles relating to America have a neutral sentiment, 23% were negative, and 4% were positive. 

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
Preparation for the data took a more considerable amount of effort. Upon inspection, we found that the XML contained errors, so we created a series of regular expressions to isolate, and pull the data we needed which we then compiled into a dataframe.

With the new dataframe, we used keywords related to America (e.g 'George Bush, Barack Obama, America, The United States, The White House') and came out with about 360,000 articles to isolate and explore on.

Crucially, we also labeled each article as positive, neutral, or negative. This was done using Camel-Tools Sentiment Analyzer which runs on Pytorch and employs a pretrained model to make determinations of text. This step took approximately 55 hours.

## Cleaning
Before we could move on to exploration and modeling we had to clean the data. The following steps were undertaken:

- Standardization of datetimes
  - All sources used their own datetime system and we needed a uniform date for Time Series Analysis
- Standardization of Arabic text and words
  - Remove unneccesary special characters
  - Delete any possible diacritical marks
  - Tokenize individual words 

[[Back to top](#top)]


  
## <a name="explore"></a>Data Exploration:
For this step we had to sift through a mountain of data to find useful takeaways.

- Explore on the data using various Natural Language Processing techniques
  - Word counts, bigrams, trigrams, unique terms by source, etc.
- Explore on the data using various Time Series Analysis techniques
  - Looking at sentiment over time, by source and by keywords
- Create visualizations of discoveries
- Hypothesis test ideas
- Feature Engineering
  - Add new features derived from discoveries made during Exploration

 
[[Back to top](#top)]

### Takeaways from exploration:
From our exploration we were able to get a sense of how news sources presented specific topics to its readers. From the information present in the dataset alone we cannot determine a causal relationship and say that topics related to America are causing the sentiment, but we can show a relationship between certain topics, words, publications, events, and sentiment. 

A major takeaway that we found was that it seems rather obvious that Techreen either has a negative bias when America related topics are discussed OR it selects to write more about negative things when discussing America.

## <a name="model"></a>Modeling:
<b> Looking at the baseline we need to beat:</b>

Before we model, we establish our baseline by picking the most frequently occurring target. In this case, neutral appears 72.6% of the time, making our baseline accuracy 72.6%. Anything higher than this means our model is more predictive.

<b>How did we decide our model?</b>

After creating 150 different models, we came to the conlcusion that random forests models were performing best. By minimizing the difference in train and validate accuracy in the random forest model, the result is a model that is generalizable and not overfit. 

Our final model has a depth of 14, and a minimum sample leaf of one. After selecting this as our best model, we ran it on out of sample data.

<b>Results:</b>
Our final result is that our model had an accuracy of **73.9%** on out of sample data.
  
[[Back to top](#top)]



## <a name="conclusion"></a>Conclusion:

- With an accuracy of **73.9%** on out of sample data, our model beats baseline by **1.8%** which is not strong enough and thus we do not feel confident to recommend it without further exploring other potential features.
    
## Recommendations: 
With the current prediction score, we cannot endorse utilization of our model with the current set of features to predict sentiment. However, our model did give us insight into understanding how certain factors played into sentiment and this fueled further exploration of the textual data. Specifically, it reinforced findings about news sources and countries as well highlighted which keywords and events were the most impactful.

That said, we do recommend using our analysis and findings as an informative tool to help assess and potentially improve America's relations with the Middle East.

### Next steps:

- improve predictive ability by finding more valuable features to pass into the model.
- acquire news articles written in English and Arabic by the same news source to compare the sentiment by language. 
####

[[Back to top](#top)]
  
  
  **How to Reproduce**
- [x] Read this README.md
- [x] Follow the Data Science pipeline outlined above.
- [x] Download and install normal Data Science python libraries for use: Pandas, Seaborn, Matplotlib, Numpy, Scikit-Learn
- [x] Download and install Camel-Tools for Arabic text manipulation. (<a href = https://camel-tools.readthedocs.io/en/latest/> See Camel-Tools documentaton.</a>)
- [x] Download and install Transformers for further NLP tools. (<a href = https://huggingface.co/docs/transformers/index> Transformers documentation<a/>)
- [x] Download XML files for the source articles from the <a href = http://abuelkhair.net/index.php/en/arabic/abu-el-khair-corpus > Abu El-Khair Corpus </a>.
- [x] Use a text editor to save each XML file as a plain text file.
- [x] Use the functions contained in our prepare.py to pull out article text and data where specific keywords are present. Use this information to save text, tags, date, and other info to a dataframe. Save the data!
- [x] Perform sentiment analysis of text and add results to the dataframe.
  - NB: Running the sentiment analysis requires significant CPU time and will likely take days even when only running on articles filtered for specific keywords relating to America.
- [x] Explore the data using functions stored in our explore.py file.
- [x] Model the data using functions stored in our modeling.py file.
- [x] Reference our final_notebook.ipynb file to show clear steps taken to move the data through the pipeline.
