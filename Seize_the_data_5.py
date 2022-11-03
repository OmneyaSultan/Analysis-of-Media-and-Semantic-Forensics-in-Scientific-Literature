
#!/usr/bin/env python3
# -*- coding: ISO-8859-1 -*-
"""
Group: Sieze The Data
Course: DSCI 550 - Spring 2022
Filename: airquality_stepfive.py

Description:  Program contains 2022 air quality levels and population information
by country. The data's imported with .JSON, combined with another dataset called
"og_with_country_data.csv" Both datasets are then merged together by 'Country' values, 
merged dataset is then exported as a .tsv file

"""

# pandas supporting packages
import pandas as pd

def AQ_Population(tsv_file):
#Reading in database with Bik dataset with college dataset
	df1 = pd.read_csv(tsv_file,  sep='\t', encoding='ISO-8859-1')

	# second dataset load json file using pandas
	df2 = pd.read_json('AdditionalDatasets//airquality.json')

	#renamed country, particlePollution, and pop2022 to understandable variable names
	df2 = df2.rename(columns={"country" :"Country","particlePollution" : "AirQuality", "pop2022": "CountryPopulation"}) 

	#add a new row with airquality difference from highest AQ reading  
	aq = df2["AirQuality"]

	#locates the max airquality value in column AirQuality
	max_value = aq.max()

	#creates a new column in df and store the difference between worst AQ - current AQ
	df2["Compared to Worst AQ Recorded"] = (( df2["AirQuality"] - max_value)/(max_value))

	#joining both df1 and df2 by Country Column
	df3 = pd.merge(df1, df2, on='Country', how='left')

	#converts panda df to .tsv
	df3.to_csv('Final_Output.tsv', sep='\t', index=False)
	  
	# load the resultant csv file
	result = pd.read_csv('Final_Output.tsv', sep='\t')
	  
