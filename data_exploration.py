import pandas as pd
import sys
import matplotlib.pyplot as plt

df_listings_june23 = pd.read_csv("data/2023/june/listings.csv")
df_listings_june23['month'] = 'june'
df_listings_march23 = pd.read_csv("data/2023/march/listings.csv")
df_listings_march23['month'] = 'march'
df_listings_sept23 = pd.read_csv("data/2023/september/listings.csv")
df_listings_sept23['month'] = 'september'


# Take all columns from official DataFrame that we're interested to

df_june23 = df_listings_june23[[
    'id', 'bedrooms', 'beds', 'review_scores_rating', 'number_of_reviews', 'neighbourhood', 'name',
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


# Concatenate DataFrames of each month to one
df_23 = pd.concat([df_june23, df_march23, df_sept23])


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
# df_23.dropna()

# Replace all extreme values from column 'minimum_nights'
df_23.loc[df_23['minimum_nights'] > 365, 'minimum_nights'] = df_23['minimum_nights'].median()

# Export dataframe to .csv file
# df_23.to_csv('train_2023.csv', index=False)

##### 1.1 #####
room_type_freqs = df_23['room_type'].value_counts()

# print(df_23['room_type'].value_counts().idxmax()) ----> most commbon room type

# Histogram to show the frequencies of room type
# ax = room_type_freqs.plot(kind='bar', x='room_type', y='count', color='tab:blue', figsize=(8, 6))
# ax.set_xlabel('Room Type', fontweight='bold')
# ax.set_ylabel('Count', fontweight='bold')
# ax.set_title('Room Type Distribution')
# ax.tick_params(axis='x', rotation=0)
# plt.show()

##### 1.2 #####



##### 1.3 #####
neighbourhoods_reviews_df = df_23[['neighbourhood_cleansed', 'number_of_reviews']]

# Group the dataframe by neighbourhoods and sum the number_of_reviews
grouped = neighbourhoods_reviews_df.groupby('neighbourhood_cleansed').sum()

# Sort this dataframe and keep top five most reviewd
tmp_df = grouped.sort_values(by=['number_of_reviews'], ascending=False).head(5)

# Make it again a dataframe 
top5_reviewed = tmp_df.reset_index()

# ax = top5_reviewed.plot(kind='bar', x='neighbourhood_cleansed', y='number_of_reviews', color='tab:purple', figsize=(17, 6))
# ax.set_xlabel('Neighbourhoods', fontweight='bold')
# ax.set_ylabel('Number of Reviews', fontweight='bold')
# ax.set_title('Top 5 Reviewed Neighbourhoods')
# ax.tick_params(axis='x', rotation=0)
# ax.set_yticks([])
# ax.set_yticklabels([])
# ax.bar_label(ax.containers[0], fmt='%d')
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
grouped_and_evaluated = neighbourhoods_roomtype_df.groupby('neighbourhood_cleansed').value_counts()
df1 = grouped_and_evaluated.reset_index()
df2 = df1.drop_duplicates(subset="neighbourhood_cleansed")

print(df2)
