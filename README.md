# Introduction to Basic Data-Mining Concepts
  In this project we worked out some basic data-mining concepts using python, jupyter notebooks, pandas software library and sklearn tools based on 2-year data of AirBnB's in Athens, Greece. The project is divided into two parts (1 & 2).

  The first one aims to clean the data and answer some basic questions which are described below for both years and build a System Recommendation based on cleaned data set.

  In the second part, a sentimental analysis is done using Hugging Face Model and with sklearn tools too. At the end, there are some functions the computes some basic metrics based on similarities.

### First Part (Data Exploration and System Recommendations)
In this part, a set of fourteen questions are answered for both years using Pandas software library and presented using matplotlib library after loading
and cleaning data. The questions :

1. Find the most common room type.
2. Show the progress of prices in the last 3 months.
3. Calculate top 5 neighbourhoods with the most reviews.
4. Find the neighbourhood with the most listing entries.
5. Find the listing entries by neighbourhood and by month.
6. Plot an histogram for 'neighbourhood' column.
7. Find the most common room_type for each neighbourhood.
8. Find the most expensive room type.
9. Create a folium map.
10. Create wordclouds based on comments, neighbourhood and description columns.
11. Create a new column that replaces the amenities by grouping them.
12. Average price for each neighoburhood that it's listing has two beds.
13. Extra questions (comments)
14. Find top 5 hosts with most listings

After presenting the results of above questions, a system recommendation built using TF-IDF matrix and cosine similarities.
At the end of first part, collocations of column description are computed.

### Second Part (Study Over Time, Sentimental Analysis, Metrics)
In this last part, firstly a sentimental analysis using a Hugging Face's model is done afer loading and cleaning data.
After that, two new sets are created in order to train the big set and test the other one trying to redo sentimental analysis
using sklearn algorithms as SVM, Random Forest and KNN. At the end, three functions are written for accordingly computing three metrics :

![screenshot](metrics/(a).png)
![screenshot](metrics/(b).png)
![screenshot](metrics/(c).png)








