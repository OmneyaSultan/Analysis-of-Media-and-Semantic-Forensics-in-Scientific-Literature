
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Group: Sieze The Data
Course: DSCI 550 - Spring 2022
Filename: Seize_the_data_3_v2

Description:  Program contains data population and fertility data for countries around the world. The data's imported with .csv, combined with another dataset called
'Bik_Step4_Complete.tsv'. From the bik dataset, we parse out the country name from the "Affiliated University" column. Both datasets are then merged together by 'Country' values, 
merged dataset is then exported as a .tsv file
"""

# pandas supporting packages
import pandas as pd
import numpy as np

def US_Population(tsv_file):

    #Reading in database with Bik dataset
    bik_data = pd.read_csv(tsv_file, sep='\t', encoding='utf-8')

    #reading in census.gov dataset to add additional features
    country_data = pd.read_csv('AdditionalDatasets//export.csv', sep=',', index_col='Row')

    #populating list called country_name to check for countries contained in ESG dataset
    country_name = []
    for index, row in country_data.iterrows():
        if row['Country/Area Name'] not in country_name:
            country_name.append(row['Country/Area Name'])
            
    #parsing country from Affiliation University columm
    country = []
    for index, row in bik_data.iterrows():
        country.append(row['Affiliation University'].split(',')[-1].lstrip())

    #populating list of US states so locations from Affiliation University column with states are classified as "United States"

    us_states = ['Alabama',
     'Alaska',
     'Arizona',
     'Arkansas',
     'California',
     'Colorado',
     'Connecticut',
     'Delaware',
     'Florida',
     'Georgia',
     'Hawaii',
     'Idaho',
     'Illinois',
     'Indiana',
     'Iowa',
     'Kansas',
     'Kentucky',
     'Louisiana',
     'Maine',
     'Maryland',
     'Massachusetts',
     'Michigan',
     'Minnesota',
     'Mississippi',
     'Missouri',
     'Montana',
     'Nebraska',
     'Nevada',
     'New Hampshire',
     'New Jersey',
     'New Mexico',
     'New York',
     'North Carolina',
     'North Dakota',
     'Ohio',
     'Oklahoma',
     'Oregon',
     'Pennsylvania',
     'Rhode Island',
     'South Carolina',
     'South Dakota',
     'Tennessee',
     'Texas',
     'Utah',
     'Vermont',
     'Virginia',
     'Washington',
     'West Virginia',
     'Wisconsin',
     'Wyoming']
     
     #iterate through country list from Affiliation University column to rename countries to match census.gov dataset
    for x in range(len(country)):
        for character in country[x]:
            if character.isdigit():
                numeric_filter = filter(str.isdigit, country[x])
                numeric_string = "".join(numeric_filter)
        if "USA" in country[x]:
            country[x] = 'United States'
        if "China" in country[x]:
            country[x] = 'China'
        if "UK" in country[x]:
            country[x] = 'United Kingdom'
        if "United States" in country[x]:
            country[x] = 'United States'
        if "Korea" in country[x]:
            country[x] = 'Korea, South'
        
        #Taiwan & Hong Kong listed as China in ESG dataset :/
        if "Hong Kong" in country[x]:
            country[x] = 'Hong Kong'
        if "Taiwan" in country[x]:
            country[x] = 'Taiwan'
        
        #checking if element is in us_states list and renaming as "United States"
        for element in us_states:
            if any(element in country[x] for element in us_states):
                country[x] = 'United States'
                break
                
        if country[x] not in country_name:
            country[x] = ''

    #assigning 'Country' column with values from country list
    bik_data['Country'] = country

    #values from growth_rate list will be added to column in main dataset
    growth_rate = []

    #iterates through country list and main dataset
    #if a country is contained in census.gov dataset
    #appends population growth rate for that year, for that country in growth_rate list
    for x in range(len(country)):
        if country[x] in country_name:
            growth_rate.append(float(country_data['Annual Growth Rate %'].loc[(country_data['Country/Area Name'] == country[x]) &
                                            (country_data['Year'] == bik_data["Year"].iloc[x])].values))
        else:
            growth_rate.append(np.nan)

    #adds growth rate column to bik dataset
    bik_data['Annual Growth Rate %'] = growth_rate

    #values from pop_density list will be added to column in main dataset
    pop_density = []

    #iterates through country list and main dataset
    #if a country is contained in census.gov dataset
    #appends population density for that year, for that country in pop_density list
    for x in range(len(country)):
        if country[x] in country_name:
            pop_density.append(float(country_data['Density (per sq km)'].loc[(country_data['Country/Area Name'] == country[x]) &
                                            (country_data['Year'] == bik_data["Year"].iloc[x])].values))
        else:
            pop_density.append(np.nan)
            
    #adds population density column to bik dataset
    bik_data['Population Density'] = pop_density

    #values from life_expectancy list will be added to column in main dataset
    life_expectancy = []

    #iterates through country list and main dataset
    #if a country is contained in census.gov dataset
    #appends life expectancy for that year, for that country in life_expectancy list
    for x in range(len(country)):
        if country[x] in country_name:
            life_expectancy.append(float(country_data['Life Expectancy at Birth'].loc[(country_data['Country/Area Name'] == country[x]) &
                                            (country_data['Year'] == bik_data["Year"].iloc[x])].values))
        else:
            life_expectancy.append(np.nan)

    #adds life expectancy column to bik dataset       
    bik_data['Life Expectancy'] = life_expectancy

    #converts panda df to .tsv
    bik_data.to_csv('Bik_with_colleges_data.tsv', sep='\t', index=False)

    # load the resultant csv file
    result = pd.read_csv('Bik_with_colleges_data.tsv', sep='\t')