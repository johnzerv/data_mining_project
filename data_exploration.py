import pandas as pd
import sys
import matplotlib.pyplot as plt
import folium

df_listings_june23 = pd.read_csv("data/2023/june/listings.csv")
df_listings_june23['month'] = 'june'
df_listings_march23 = pd.read_csv("data/2023/march/listings.csv")
df_listings_march23['month'] = 'march'
df_listings_sept23 = pd.read_csv("data/2023/september/listings.csv")
df_listings_sept23['month'] = 'september'


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


# Concatenate DataFrames of each month to one
df_23 = pd.concat([df_june23, df_march23, df_sept23])
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
# df_23.dropna()

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
property_locations = df_23[['latitude', 'longitude', 'room_type']]
# Take a sample of rows in order to be the map usable 
sample_of_locations = property_locations.sample(n=500)  

properties_map = folium.Map(location=[sample_of_locations.latitude.mean(), sample_of_locations.longitude.mean()],
                            zoom_start=14, control_scale=True)

for index, location_info in sample_of_locations.iterrows():
    folium.Marker([location_info["latitude"], location_info["longitude"]], popup=location_info["room_type"], ).add_to(properties_map)


properties_map.save('properties_map.html')

##### 1.10 ######




