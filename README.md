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

  
  
 ### Deliverables:
[X] Clean Repo

[X] README.md

[] Final Notebook

[] Scripting Files

[] Google Slides (~10-25 for presentation)

###  Executive Summary: 

  
        
### Initial Hypothesis/Questions: 


[[Back to top](#top)]


## <a name="dictionary"></a>Data Dictionary  
[[Back to top](#top)]

id | non-null | object        
url | non-null | object        
headline |non-null | object        
dateline |non-null | datetime64[ns]
text |non-null | object        
tags |non-null | object        
source | non-null | object        
text_label | non-null | object        
text_score | non-null | object        
headline_label | non-null | object        
headline_score | non-null | float64 


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

