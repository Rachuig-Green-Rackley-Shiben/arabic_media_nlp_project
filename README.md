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
- [] Final Notebook
- [] Scripting Files
- [] Google Slides (~10-25 for presentation)

###  Executive Summary: 

  
        
### Initial Hypothesis/Questions: 
- What’s the relationship between article sentiment and world events? (Post MVP)
- What is the relationship between news sources and the target? 
- What is the relationship between country of source and target?
- What is the relationsheep between tag and target?
- Is there a relationship between time and sentiment?
- Is there a relationship between sentiment of the headline and sentiment of text?

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
| text_label | object |  |
| text_score | object | sentiment score for text in article |
| headline_label | object |  |
| headline_score | object | sentiment score for headline of an article | 

***

## <a name="wrangle"></a>Data Acquisition and Preparation
  
## Acquire
- All data was sourced from the [Abu El-Khair Corpus](http://abuelkhair.net/index.php/en/arabic/abu-el-khair-corpus)
    - Includes more than five million Arabic news articles from 2000-2014
- Downloaded 10 separate XML files containing all the articles (~ 20 GB)

[[Back to top](#top)]

## Prepare
- Parse through each individual XML file and convert to CSV files
- Filter articles for relevant topics pertaining to America
- Combine all results into a single CSV with topics tagged in a new feature column
- Drop nulls from the dataset
- Clean dates and create datetime column for exploration
- Clean the articles:
  - Normalize the Arabic text
  - Remove all non text characters
  - Remove all diacritical marks (هركات)
  - Tokenize the text
- Run sentiment analysis using Camel_Tools to gauge sentiment of the article text and the headline

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

## <a name="model"></a>Modeling:

  
[[Back to top](#top)]



## <a name="conclusion"></a>Conclusion:
  
 # Conclusion:




  
### With more time:

## Recomendations: 
####

[[Back to top](#top)]
  
  
  **How to Reproduce**
- [x] Read this README.md

