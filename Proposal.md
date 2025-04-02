# Final Project Proposal

**GitHub Repo URL**: https://github.com/CMU-IDS-Spring-2025/final-project-s25-parkrangers/blob/main/Proposal.md

<!-- A short summary (3-4 paragraphs, about one page) of the data science problem you are addressing and what your solution will address. Feel free to include a figure or sketch to illustrate your project.

Each group should submit the URL pointing to this document on your github repo. -->


# National Parks Visitation Analysis and Recommendation System

## Group members: 
Aditi Saini, Ananya Angadi, Mahita Kandala, Rupsa Dhar

## Problem Statement

The US has a great variety of national parks with rich biodiversity. Each national park is known for its unique features. While some national parks remain popular tourist destinations, there are some that are underrated and need more attention. According to Strava, parks like North Cascades National Park, Washington and Isle Royal National Park, Michigan are top 2 places that are not as popular but are an “adventurer’s paradise”. There are websites that provide suggestions on which parks to visit, but none allow users to filter based on their specific criteria and offer personalized recommendations tailored to their preferences.

The aim of this project is to use datasets of national parks in the U.S. to gain insights into their unique features, biodiversity, climate change and visitor trends, ultimately helping users make informed decisions about which parks to visit based on their preferences. This will not only boost the popularity of underrated national parks but also align more closely with users' preferences. Additionally, it will encourage them to explore parks that are less crowded and off the beaten path. 

## Proposed Solution 

The clear problem statement for this project is to create a recommender system for users who are looking to explore national parks based on their trip preferences and interests. We will be focusing on Content based filtering methods to give a soft match based on user information like location, weather, season, trip type, biodiversity and finally whether the user wants to explore popular or underrated places. Additionally, we will incorporate interactive visualizations to help users select and refine their preferences for the parks they wish to visit. 

## Primary Dataset 

We plan to use the [U.S. National Park Visit Data (1979-2023)](https://www.responsible-datasets-in-context.com/posts/np-data/?tab=explore-the-data) for our project, which contains monthly visitation numbers and details for US National Parks between 1979 and 2023. It also categorizes visits based on the visit type (recreational, non-recreational, camping trip, etc.).  

To serve our purpose of recommending national parks to visit based on location and season, we plan to augment our data with [weather information](https://www.ncei.noaa.gov/cdo-web/datasets) to enable weather-based analysis and modelling. For example, some national parks may be more popular than others in the winter. Moreover, incorporating weather information will provide insights on how climate change has affected visitation numbers. 

We will also augment our dataset with [national park location data](https://www.kaggle.com/datasets/aliamini587/biodiversity-in-national-parks) to enable geospatial analysis, and data related to [park biodiversity](https://www.kaggle.com/datasets/nationalparkservice/park-biodiversity?select=species.csv) for richer visualizations. 


## Sketches and Data Analysis

### Data Processing. 
1. Do you have to do substantial data cleanup? 
Ans: We have not done any substantial 


2. What quantities do you plan to derive from your data? 
Ans: 

3. How will data processing be implemented?  

4. Show some screenshots of your data to demonstrate you have explored it.

We have explored the data across different features and dimensions to extract patterns from  the chosen datasets. We have used different kinds of visualization techniques such as bar graphs, histograms, correlation heatmap and stacked charts to show different characteristics of the data. Let’s take a look at a few examples:

<p align="left">
  <img src="images/parks_by_region_count.png" alt="Count of parks per region"/>
  <br>
  <strong>Count of parks per region</strong>
  <br>
  <br>
</p>

<p align="left">
  <img src="images/total_visits_per_park.png" alt="Total number of visits per park on the map from 1979 to 2023"/>
  <br>
  <strong>Total number of visits per park on the map from 1979 to 2023</strong>
  <br>
  <br>
</p>

<p align="left">
  <img src="images/visits_per_month.png" alt="Visits per month"/>
  <br>
  <strong>Visits per month</strong>
  <br>
  <br>
</p>

<p align="left">
  <img src="images/heatmap.png" alt="Correlations between visits, campers and park size"/>
  <br>
  <strong>Correlations between visits, campers and park size</strong>
  <br>
  <br>
</p>

<p align="left">
  <img src="images/total_visitors_per_month.png" alt="Total visitors per month per region of national park based on geography"/>
  <br>
  <strong>Total visitors per month per region of national park based on geography</strong>
  <br>
  <br>
</p>

<p align="left">
  <img src="images/total_visits_by_state.png" alt="Visits by state"/>
  <br>
  <strong>Visits by state</strong>
  <br>
  <br>
</p>

<p align="left">
  <img src="images/diversity.png" alt="Diversity of national parks per region"/>
  <br>
  <strong>Diversity of national parks per region</strong>
  <br>
  <br>
</p>

<!-- ![Parks by region count](images/parks_by_region_count.png) -->


# System Design. 
## How will you display your data? 
To display the data effectively, we will display the data in multiple formats . The main page (Top Parks page from the Survey.png) will feature a survey where users answer a series of questions about their travel preferences. Based on their responses, the system will generate a list of 5-6 recommended national parks, each presented as an info card containing key details such as park location, best visit seasons, popular activities, and flora/fauna information. These recommendations will help users quickly identify parks that suit their needs and make informed travel decisions.
  
  In addition to the national park info cards, we will also display data in the form of interactive visualizations as a part of Explore pages. This will include a maps page and additional data visualization page, allowing users to browse and filter national park data on their own. The exploration pages will provide interactive visualizations and dynamic filtering options, enabling users to refine their search based on factors like months/year, number of visitors, types or parks, etc. 

## What types of interactions will you support?
Our system will support two main interaction modes. First, users can receive personalized recommendations by interacting with the system through a questionnaire designed to understand their travel preferences. This questionnaire would become the basis of our Machine Learning Recommendation model which would make it easy for the users to find suitable parks without extensive searching. 

  Second, users can take a more hands-on approach by exploring and interacting with the dataset through maps and filters available in the exploration and maps pages. These pages would allow them to customize their search criteria according to their specific interests and visualize the data about the National Parks in a clear and concise manner. By offering these two modes, our system would ensure that users can either get quick, curated recommendations or explore the data in a more interactive and personalized way.
  
## Provide some sketches that you have for the system design.
<p align="left">
  <img src="images/Survey.png" alt="Questionnaire Presented to Users For Recommendations"/>
  <br>
  <strong>Questionnaire Presented to Users For Recommendations</strong>
  <br>
  <br>
</p>

<p align="left">
  <img src="images/Recommendations.png" alt="The Recommendations Based on User Responses"/>
  <br>
  <strong>The Recommendations Based on User Responses</strong>
  <br>
  <br>
</p>

<p align="left">
  <img src="images/Maps.png" alt="Data Visulizations with Filters For More Personalized Searches"/>
  <br>
  <strong>Data Visulizations with Filters For More Personalized Searches</strong>
  <br>
  <br>
</p>
