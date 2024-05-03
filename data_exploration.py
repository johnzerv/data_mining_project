import pandas as pd
import sys
import matplotlib.pyplot as plt
import folium
import wordcloud
from collections import Counter
import numpy as np

# Load csv's and add a column 'month'
df_listings_june23 = pd.read_csv("data/2023/june/listings.csv")
df_listings_june23['month'] = 'june'
df_listings_march23 = pd.read_csv("data/2023/march/listings.csv")
df_listings_march23['month'] = 'march'
df_listings_sept23 = pd.read_csv("data/2023/september/listings.csv")
df_listings_sept23['month'] = 'september'

df_reviews_june23 = pd.read_csv("data/2023/june/reviews.csv")
df_reviews_march23 = pd.read_csv("data/2023/march/reviews.csv")
df_reviews_sept23 = pd.read_csv("data/2023/september/reviews.csv")

# Take all columns from official DataFrame that we're interested to
df_june23 = df_listings_june23[[
    'id', 'bedrooms', 'beds', 'review_scores_rating', 'number_of_reviews', 'neighbourhood_cleansed', 'name',
    'latitude', 'longitude', 'last_review', 'instant_bookable', 'host_since', 'host_response_rate',
    'host_has_profile_pic', 'first_review', 'description', 'accommodates', 'bathrooms_text', 'amenities', 
    'room_type', 'property_type', 'price', 'availability_365', 'minimum_nights', 'month'
]]

df_march23 = df_listings_march23[[
    'id', 'bedrooms', 'beds', 'review_scores_rating', 'number_of_reviews', 'neighbourhood_cleansed', 'name',
    'latitude', 'longitude', 'last_review', 'instant_bookable', 'host_since', 'host_response_rate',
    'host_has_profile_pic', 'first_review', 'description', 'accommodates', 'bathrooms_text', 'amenities', 
    'room_type', 'property_type', 'price', 'availability_365', 'minimum_nights', 'month'
]]


df_sept23 = df_listings_sept23[[
    'id', 'bedrooms', 'beds', 'review_scores_rating', 'number_of_reviews', 'neighbourhood_cleansed', 'name',
    'latitude', 'longitude', 'last_review', 'instant_bookable', 'host_since', 'host_response_rate',
    'host_has_profile_pic', 'first_review', 'description', 'accommodates', 'bathrooms_text', 'amenities', 
    'room_type', 'property_type', 'price', 'availability_365', 'minimum_nights', 'month'
]]

# Create an one-column dataframe for comments of 2023
df_comments_june23 = df_reviews_june23['comments']
df_comments_march23 = df_reviews_march23['comments']
df_comments_sept23 = df_reviews_sept23['comments']

df_comments_23 = pd.concat([df_comments_june23, df_comments_march23, df_comments_sept23])

# Concatenate DataFrames of each month to one
df_23 = pd.concat([df_june23, df_march23, df_sept23])



# Clean the column 'price'
df_23['price'] = df_23['price'].str.replace('.00', '').str.replace(',', '').str.replace('$', '').astype(float)

# For each column that contains numbers, fill NaN values with mean
numerical_columns = df_23.select_dtypes(include='number').columns
for col in numerical_columns:
    mean = df_23[col].mean()
    df_23[col] = df_23[col].fillna(value=mean)



# TODO: Decide what to do with NaN text
# For each column that contains text, fill NaN values with 'unknown'
# text_columns = df_23.select_dtypes(include='object').columns
# for col in text_columns:
#     df_23[col] = df_23[col].fillna(value='unknown')
# or
df_23.dropna(inplace=True, ignore_index=True)

# Replace all extreme values from column 'minimum_nights'
df_23.loc[df_23['minimum_nights'] > 365, 'minimum_nights'] = df_23['minimum_nights'].median()

# Export dataframe to .csv file
# df_23.to_csv('train_2023.csv', index=False)

##### 1.1 #####
room_type_freqs = df_23['room_type'].value_counts()

# print(df_23['room_type'].value_counts().idxmax()) ----> most commbon room type

# Histogram to show the frequencies of room type
# plot_1_1 = room_type_freqs.plot(kind='bar', x='room_type', y='count', color='tab:blue', figsize=(8, 6))
# plot_1_1.set_xlabel('Room Type', fontweight='bold')
# plot_1_1.set_ylabel('Count', fontweight='bold')
# plot_1_1.set_title('Room Type Distribution')
# plot_1_1.tick_params(axis='x', rotation=0)
# plot_1_1.bar_label(plot_1_1.containers[0], fmt='%d')
# plt.show()

##### 1.2 #####
price_month_df = df_23[['neighbourhood_cleansed', 'price', 'month']]
grouped_by_neighb_month = price_month_df.groupby(['neighbourhood_cleansed', 'month'])['price'].mean().reset_index()
temp_df = grouped_by_neighb_month.groupby(['month', 'neighbourhood_cleansed']).mean().reset_index()

# Add month as column 
avg_price_per_month_df = temp_df.pivot(index='neighbourhood_cleansed', columns='month', values='price')

# plot_1_2 = avg_price_per_month_df.plot(kind='barh', figsize=(15,15), width=0.8)
# plot_1_2.set_xlabel('Price', fontweight='bold')
# plot_1_2.set_ylabel('Neighbourhoods', fontweight='bold')
# plot_1_2.set_title('Average Price by Neighbourhood for Each Month')
# plt.show()

##### 1.3 #####
neighbourhoods_reviews_df = df_23[['neighbourhood_cleansed', 'number_of_reviews']]

# Group the dataframe by neighbourhoods and sum the number_of_reviews
grouped = neighbourhoods_reviews_df.groupby('neighbourhood_cleansed').sum()

# Sort this dataframe and keep top five most reviewd
tmp_df = grouped.sort_values(by=['number_of_reviews'], ascending=False).head(5)

# Make it again a dataframe 
top5_reviewed = tmp_df.reset_index()

# plot_1_3 = top5_reviewed.plot(kind='bar', x='neighbourhood_cleansed', y='number_of_reviews', color='tab:purple', figsize=(17, 6))
# plot_1_3.set_xlabel('Neighbourhoods', fontweight='bold')
# plot_1_3.set_ylabel('Number of Reviews', fontweight='bold')
# plot_1_3.set_title('Top 5 Reviewed Neighbourhoods')
# plot_1_3.tick_params(axis='x', rotation=0)
# plot_1_3.set_yticks([])
# plot_1_3.set_yticklabels([])
# plot_1_3.bar_label(plot_1_3.containers[0], fmt='%d')
# plt.show()

##### 1.4 #####
neighbourhoods_df = df_23['neighbourhood_cleansed'].value_counts()
# print(neighbourhoods_df.index[0])

##### 1.5 #####
# Entries per neighbourhood
# print(neighbourhoods_df)

# Entries per month
months_df = df_23['month'].value_counts()
# print(months_df)

##### 1.6 #####
# Answered in 1.5

##### 1.7 #####
neighbourhoods_roomtype_df = df_23[['neighbourhood_cleansed', 'room_type']]

# Group by neighbourhood and value for each neighbourhood which roomt type has
grouped_and_evaluated = neighbourhoods_roomtype_df.groupby('neighbourhood_cleansed').value_counts()
# Reset indexing and drop duplicates for each neighbourhood while keeping the first roomtype
top_roomtype_df = grouped_and_evaluated.reset_index().drop_duplicates(subset="neighbourhood_cleansed")

# print(top_roomtype_df)

# plot_1_7 = top_roomtype_df.sort_values(by='count', ascending=False).plot(kind='barh', x='neighbourhood_cleansed', y='count', color='skyblue', figsize=(100, 10))
# plot_1_7.set_xlabel('Count')
# plot_1_7.set_ylabel('Neighbourhoods')
# plot_1_7.set_title('Neighbourhoods with roomtype : Entire home/apt')
# plot_1_7.bar_label(plot_1_7.containers[0], fmt='%d')

# plt.show()

##### 1.8 #####
# roomtype_df = df_23['room_type']
# price_df = df_23['price']

# # Fix the price column from string to a float number in which we can apply sum()
# price_df=price_df.str.replace('.00', '').str.replace(',', '').str.replace('$', '').astype(float)

# roomtype_prices_df = pd.concat([roomtype_df, price_df], axis='columns')
roomtype_prices_df = df_23[['room_type', 'price']]

total_price_roomtypes = roomtype_prices_df.groupby('room_type').sum().reset_index()

# plot_1_8 = total_price_roomtypes.plot(kind='pie', y='price', labels=None, autopct='%.1f%%', startangle=140, figsize=(10, 10))
# plot_1_8.set_ylabel('')  # Remove y-axis label
# plot_1_8.set_title('Price Distribution by Room Type')
# plot_1_8.legend(total_price_roomtypes['room_type'], loc='upper right')  # Add legend with room types
# plt.show()

##### 1.9 #####
# property_locations = df_23[['latitude', 'longitude', 'room_type']]
# # Take a sample of rows in order to be the map usable 
# sample_of_locations = property_locations.sample(n=500)  

# properties_map = folium.Map(location=[sample_of_locations.latitude.mean(), sample_of_locations.longitude.mean()],
#                             zoom_start=14, control_scale=True)

# for index, location_info in sample_of_locations.iterrows():
#     folium.Marker([location_info["latitude"], location_info["longitude"]], popup=location_info["room_type"], ).add_to(properties_map)


# properties_map.save('properties_map.html')

##### 1.10 ######

# Word Cloud for comments of 2023
df_sample_comments_23 = df_comments_23.sample(200)
comments_text_23 = df_sample_comments_23.str.cat()
comments_text_23 = comments_text_23.replace("<br/>", "")

wcloud_comments_23 = wordcloud.WordCloud(width=800, height=400, background_color='white').generate(comments_text_23)

# Plot the word cloud
# plt.figure(figsize=(10, 5))
# plt.imshow(wcloud_comments_23)
# plt.axis('off')
# plt.show()


# TODO: Each row has to be treated as a word for neighbourhoodse
df_neighbourhoods_23 = df_23['neighbourhood_cleansed'].str.replace(' ', '-')
df_neighbourhoods_sample_23 = df_neighbourhoods_23.sample(200)
neighbourhoods_text_23 = df_neighbourhoods_sample_23.str.cat(sep=' ')

wcloud_neighbourhood_23 = wordcloud.WordCloud(width=800, height=400, background_color='white').generate(neighbourhoods_text_23)

# # Plot the word cloud
# plt.figure(figsize=(10, 5))
# plt.imshow(wcloud_neighbourhood_23)
# plt.axis('off')
# plt.show()

# Keep descriptions by replacing html code
df_descriptions_23 = df_23['description'].str.replace('<b>', '').str.replace('<br />', '').str.replace('<b>', '').str.replace('</b>', '')
df_descriptions_sample_23 = df_descriptions_23.sample(200)
descriptions_text_23 = df_descriptions_sample_23.str.cat(sep=' ')

wcloud_description_23 = wordcloud.WordCloud(width=800, height=400, background_color='white').generate(descriptions_text_23)

# plt.figure(figsize=(10, 5))
# plt.imshow(wcloud_description_23)
# plt.axis('off')
# plt.show()

##### 1.11 #####
# Convert amenities' column from sets of strings to lists of strings
df_amenities_23 = df_23['amenities'].str.replace(", ", ',').str.replace('"', '').str.replace('[', '').str.replace(']', '').str.split(',')
# Explode each list of amenities in order to keep unique amenities
df_unique_amenities_23 = df_amenities_23.explode().unique()

# Create a counter that counts unique words in order to see the most common amenities
amenity_frequency_counter = Counter()

for string in list(df_unique_amenities_23):
    words = string.split()
    amenity_frequency_counter.update(words)

# Extract most common and print to see it
most_common = dict(amenity_frequency_counter.most_common())
# print(most_common)

# Create a dictionary manually of common keywords for each category of amenities
categories = {'kitchen' : ['stove', 'steel', 'stainless', 'oven', 'refrigerator', 'kitchen', 'induction', 'olive', 'coffee', 'maker', 'rice', 'bbq'],
              'facilities' : ['parking', 'garage', 'building', 'premises', 'elevator', 'bedroom', 'bedrooms', 'bathroom', 'bathrooms', 'private', 'public', 'balcony', 'chair'],
              'electricity and technology' : ['dishwasher', 'microwave', 'ethernet', 'connection','hdtv', 'mbps', 'electric', 'wifi', 'fast', 'system', 'sound', 'tv', 'bluetooth', 'cable',
                                              'aux', 'netflix', 'bosch', 'chromecast', 'amazon', 'prime', 'video', 'disney+', 'pitsos', 'apple',
                                              'siemens', 'cd', 'dvd', 'lg', 'pitsos', 'bosch', 'morris', 'samsung', 'zanussi', 'game'],
              'security' : ['lock', 'alarm', 'fire', 'kit', 'security', 'cameras', 'emergency', 'escape', 'safe', 'pets', 'allowed'],
              'services' : ['service', 'heating', 'hot', 'water', 'linens', 'breakfast', 'dry', 'cleaning', 'laundry', 'pickup', 'rental', 'check-in', 'self', 'book', 'books'],
              'toiletries' : ['soap', 'body', 'hair', 'shampoo', 'conditioner', 'closet', 'miele', 'papoutsanis', 'shampoo', 'korres', 'pantene', 'shower', 'marseillais', 'le petite']
            }

# Method to find the category of an amenity
def find_category(amenity):
    for category, keywords in categories.items():
        for word in amenity.split():
            if word.lower() in keywords:
                return category
    return 'Other'

# Method that returns a list of corresponding categories from a list of amenities
def get_categorized_amenities(amenities):
    categorized_amenities = list()
    for amenity in amenities:
        categorized_amenities.append(find_category(amenity))
    
    return categorized_amenities

# Categorize the whole column
categorized_amenities = list()
for i in range(df_amenities_23.size):
    categorized_amenities.append(get_categorized_amenities(df_amenities_23.iloc[i]))

# After that, create a dataframe and concatenate it with the official dataframe for 2023
df_categorized_amenities = pd.DataFrame({'categorized_amenities' : categorized_amenities})

df_augmented_23 = pd.concat([df_23, df_categorized_amenities], axis=1)

df_categories_freq = df_categorized_amenities.explode('categorized_amenities').value_counts().reset_index()

# Histogram to show the frequencies of amenity's category
# plot_1_11 = df_categories_freq.plot(kind='bar', x='categorized_amenities', y='count', color='tab:olive', figsize=(17, 6))
# plot_1_11.set_xlabel('Categories', fontweight='bold')
# plot_1_11.set_ylabel('Count', fontweight='bold')
# plot_1_11.set_title('Amenity\'s Categories Distribution')
# plot_1_11.tick_params(axis='x', rotation=0)
# plot_1_11.set_yticks([])
# plot_1_11.set_yticklabels([])
# plot_1_11.bar_label(plot_1_11.containers[0], fmt='%d')
# plt.show()