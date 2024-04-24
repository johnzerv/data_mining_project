import pandas as pd
import sys

df_listings_june23 = pd.read_csv("data/2023/june/listings.csv")
df_listings_march23 = pd.read_csv("data/2023/march/listings.csv")
df_listings_sept23 = pd.read_csv("data/2023/september/listings.csv")


# Take all columns from official DataFrame that we're interested to

df_june23 = df_listings_june23[[
    'id', 'bedrooms', 'beds', 'review_scores_rating', 'number_of_reviews', 'neighbourhood', 'name',
    'latitude', 'longitude', 'last_review', 'instant_bookable', 'host_since', 'host_response_rate',
    'host_has_profile_pic', 'first_review', 'description', 'accommodates', 'bathrooms_text', 'amenities', 
    'room_type', 'property_type', 'price', 'availability_365', 'minimum_nights'
]]

df_march23 = df_listings_march23[[
    'id', 'bedrooms', 'beds', 'review_scores_rating', 'number_of_reviews', 'neighbourhood', 'name',
    'latitude', 'longitude', 'last_review', 'instant_bookable', 'host_since', 'host_response_rate',
    'host_has_profile_pic', 'first_review', 'description', 'accommodates', 'bathrooms_text', 'amenities', 
    'room_type', 'property_type', 'price', 'availability_365', 'minimum_nights'
]]

df_sept23 = df_listings_sept23[[
    'id', 'bedrooms', 'beds', 'review_scores_rating', 'number_of_reviews', 'neighbourhood', 'name',
    'latitude', 'longitude', 'last_review', 'instant_bookable', 'host_since', 'host_response_rate',
    'host_has_profile_pic', 'first_review', 'description', 'accommodates', 'bathrooms_text', 'amenities', 
    'room_type', 'property_type', 'price', 'availability_365', 'minimum_nights'
]]

# Concatenate DataFrames of each month to one
df_june = pd.concat([df_june23, df_march23, df_sept23])


# For each column that contains numbers, fill NaN values with mean
numerical_columns = df_june.select_dtypes(include='number').columns
for col in numerical_columns:
    mean = df_june[col].mean()
    df_june[col] = df_june[col].fillna(value=mean)


# For each column that contains text, fill NaN values with ''
text_columns = df_june.select_dtypes(include='object').columns
for col in text_columns:
    df_june[col] = df_june[col].fillna(value='')


# Replace all extreme values from column 'minimum_nights'
df_june.loc[df_june['minimum_nights'] > 365, 'minimum_nights'] = df_june['minimum_nights'].median()

# Export dataframe to .csv file
# df_june.to_csv('train_2023.csv', index=False)