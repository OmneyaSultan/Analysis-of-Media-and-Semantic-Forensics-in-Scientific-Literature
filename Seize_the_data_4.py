
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Group: Sieze The Data
Course: DSCI 550 - Spring 2022
Filename: Seize_the_data_4

Description:  Program contains data that measures environmental, social, and governance indicators for countries around the world. The data's imported with .xlsx, combined with another dataset called
'Bik_with_colleges_data.tsv'. From the bik dataset, we parse out the country name from the "Affiliated University" column. Both datasets are then merged together by 'Country' values, 
merged dataset is then exported as a .tsv file
"""

# pandas supporting packages
import pandas as pd
import numpy as np

def Country_Values(tsv_file):
#Reading in database with Bik dataset with college dataset
    bik_data = pd.read_csv(tsv_file, sep='\t', encoding='ISO-8859-1')

    #reading in Envornment, Soecial, and Governance (ESG) dataset to add additional features
    country_data = pd.read_excel('AdditionalDatasets//Data_Extract_From_Environment_Social_and_Governance_(ESG)_Data.xlsx')

    #removing records that will not be used to add features to bik_data
    country_data.drop(country_data.tail(5).index,
            inplace = True)
    country_data = country_data.drop(columns=["2050 [YR2050]","Series Code","Country Code"])
    country_data = country_data[(country_data['Series Name'] == 'Scientific and technical journal articles') | 
                                (country_data['Series Name'] == 'Control of Corruption: Estimate') |
                                (country_data['Series Name'] == 'Government expenditure on education, total (% of government expenditure)')]

    #renaming columns to simplify adding features
    country_data = country_data.rename(columns={"2012 [YR2012]": "2012", "2013 [YR2013]": "2013", "2014 [YR2014]": "2014", "2015 [YR2015]": "2015",
                                "2016 [YR2016]": "2016", "2017 [YR2017]": "2017", "2018 [YR2018]": "2018", "2019 [YR2019]": "2019", 
                                 "2020 [YR2020]": "2020"})
    							 
    #replacing ".." which indicates null values to np.nan
    country_data = country_data.replace('..', np.nan)

    #populating list called countr_name to check for countries contained in ESG dataset
    country_name = []
    for index, row in country_data.iterrows():
        if row['Country Name'] not in country_name:
            country_name.append(row['Country Name'])

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
     
    #iterate through country list from Affiliation University column to rename countries to match ESG dataset
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
            country[x] = 'Korea, Rep.'
        
        #Taiwan & Hong Kong listed as China in ESG dataset :/
        if "Hong Kong" in country[x]:
            country[x] = 'China'
        if "Taiwan" in country[x]:
            country[x] = 'China'
        if "Iran" in country[x]:
            country[x] = 'Iran, Islamic Rep.'
        
        #checking if element is in us_states list and renaming as "United States"
        for element in us_states:
            if any(element in country[x] for element in us_states):
                country[x] = 'United States'
                break
                
        if country[x] not in country_name:
            country[x] = ''

    #assigning 'Country' column with values from country list
    bik_data['Country'] = country

    #values from control of corrupt list will be added to column in main dataset
    control_of_corrupt = []

    #iterates through country list and main dataset
    #if a country is contained in ESG dataset AND the year article was published is beetween 2012 and 2020,
    #appends control_of_corruption for that year, for that country in control of corrupt list
    for x in range(len(country)):
        if country[x] in country_name and bik_data["Year"].iloc[x] >= 2012 and bik_data["Year"].iloc[x] <= 2020:
            control_of_corrupt.append(float(country_data[str(bik_data["Year"].iloc[x])].loc[(country_data['Country Name'] == country[x]) &
                                            (country_data['Series Name'] == 'Control of Corruption: Estimate')]))    
        else:
            control_of_corrupt.append(np.nan)

    #populate new column in main dataset
    bik_data['Control of Corruption'] = control_of_corrupt

    #values from education_expenditure will be added to column in main dataset
    education_expenditure = []

    #iterates through country list and main dataset
    #if a country is contained in ESG dataset AND the year article was published is beetween 2012 and 2020,
    #appends education_expenditure for that year, for that country in education_expenditure list
    for x in range(len(country)):
        if country[x] in country_name and bik_data["Year"].iloc[x] >= 2012 and bik_data["Year"].iloc[x] <= 2020:
            education_expenditure.append(float(country_data[str(bik_data["Year"].iloc[x])].loc[(country_data['Country Name'] == country[x]) &
                                            (country_data['Series Name'] == 'Government expenditure on education, total (% of government expenditure)')]))
        else:
            education_expenditure.append(np.nan)

    #populate new column in main dataset
    bik_data['Education Expenditure'] = education_expenditure

    #values from journal_articles will be added to column in main dataset
    journal_articles = []

    #iterates through country list and main dataset
    #if a country is contained in ESG dataset AND the year article was published is beetween 2012 and 2020,
    #appends journal_articles for that year, for that country in journal_articles list
    for x in range(len(country)):
        if country[x] in country_name and bik_data["Year"].iloc[x] >= 2012 and bik_data["Year"].iloc[x] <= 2020:
            journal_articles.append(float(country_data[str(bik_data["Year"].iloc[x])].loc[(country_data['Country Name'] == country[x]) &
                                            (country_data['Series Name'] == 'Scientific and technical journal articles')]))
        else:
            journal_articles.append(np.nan)
    		
    #populate new column in main dataset
    bik_data['Scientific Journal Articles'] = journal_articles

    #converts panda df to .tsv
    bik_data.to_csv('og_with_country_data.tsv', sep='\t', index=False)
      
    # load the resultant csv file
    result = pd.read_csv('og_with_country_data.tsv', sep='\t')