FILE : readme.txt
GROUP: Seize the Data
---------------------


## TABLE OF CONTENTS
---------------------

* Overview

* Requirements

* Python Libraries Used

* Execution Instructions

* Files / Description

* Links to Data Sources



OVERVIEW:
----------------------

In this project, we explored the given 'Big et al Media' dataset that contained a set of ~200 papers from a variety of biomedical and scientific literary research writings to draw several conclusions on possible causes of media manipulation. The following tasks included: finding additional information about each author, locating three additional datasets to draw possible contributions to the media manipulation issue, and utilizing Apache Tika to locate deduplication and cluster patterns with the newly combined data. 

'Final_Output.tsv' is our final updated tsv file with all added attributes- it can be found in the Expected_Output directory.


REQUIREMENTS 
----------------------
Python 3
Apache Tika


PYTHON LIBRARIES USED
----------------------
requests, pandas, csv, BeautifulSoup, re, time, numpy, sys



EXECUTION INSTRUCTIONS:
----------------------

There are 5 python scripts that together update the Bik et al dataset and
append the new features. The output .tsv file of each script is updated by
the next script, so the order in which the python scripts are run is
important. We recommend utilizing Control_Script.py which runs each Seize_the_data_X.py
script in order to compile all our data. Control_Script.py should be ran with arguments
that correspond with certain steps in the assignment.

**Please note: running 'python Control_Script.py --WebScrape_Full' from the terminal takes one hour to compile data.
It is only included to show that our Python script is working and compiles the appropriate data.
Please refer to #2: Control_Script.py in the FILES - DESCRIPTIONS section below for additional arguments that can
utilize static data that we have already compiled to save users' time.


FILES - DESCRIPTIONS
----------------------

#1: readme.txt

Description:
Contains overview of project, system requirements, python 3 libraries needed, execution instructions, file/description, and links to data sources.


#2: Control_Script.py 

Description: Our project utilizes Python scripts to access and join all of our data into a single .tsv file.
Running Control_Script.py along with '--WebScrape_Test' as an argument will scrape a small sample from data. 
We recommend utilizing this argument to get a feel for which data is collected for step 4.
Using '--WebScrape_Full' as an argument will do a full scrape from our sources, but takes 1 hour to run in total.
Using '--AdditionalData' as argument can be run to access a .tsv that has already been compiled after completing step 4 and adds additional features from three separate sources. 
We recommend utilizing this argument to see which features are added for step 5.
Using '--Extract_html' as argument will extract the .html for all records from https://doi.org.

All output .tsv files will be found in TEAM_SEIZE_THE_DATA_DSCI550_HW_BIGDATA directory as they are generated.


#3: create_htmls.py

Description: This script accesses each record in the original Bik data and collects the .html files from https://doi.org. The .html files are output into htmls directory.


#4: Seize_the_data_1.py 

Description: This script scrapes data from ResearchGate and Google Scholar based on the information provided by the Bik et Al dataset (named 'BIK_DATA.tsv').
We used the DOI and authors to collect the following features: Publication Rate, Lab Size, Other Journals, Degree Level, Career Duration. This script returns a BIK_OutputTest.tsv with the original Bik data along with the 5 added features.

#5: Seize_the_data_2.py

Description: This script scrapes data from the DOI article pages based on the information provided by the Bik et Al dataset (named 'BIK_DATA.tsv').
We used the DOI and authors to collect the following features: Affiliation and Degree Area
This script returns ‘Bik_Step4_Complete.tsv’ file with the original Bik data along with the 2 added features.

#6: Seize_the_data_3.py

Description:  Program contains population and fertility data for countries around the world. The data is imported with .csv, combined with another dataset called 'Bik_Step4_Complete.tsv'. 
From the bik dataset, we parse out the country name from the "Affiliated University" column. Both datasets are then merged together by 'Country' values, the merged dataset is then exported as ‘Bik_with_colleges_data.tsv’.

#7: Seize_the_data_4.py

Description:  Program contains data that measures environmental, social, and governance indicators for countries around the world. The data's imported with .xlsx, combined with another dataset called 'Bik_with_colleges_data.tsv'. From the bik dataset, we parse out the country name from the "Affiliated University" column. Both datasets are then merged together by 'Country' values, merged dataset is then exported as og_with_country_data.tsv. 

#8: Seize_the_data_5.py

Description:  Program contains 2022 air quality levels and population information
by country. The data's imported with .JSON, combined with another dataset called
"og_with_country_data.csv" Both datasets are then merged together by 'Country' values, 
the merged dataset is then exported as Final_Output.tsv.


#9: AdditionalDatasets 

Description: contains the three supporting dataset of MIME types .csv, .json, and .xlsx.

- export.csv
Contains data population and fertility data for countries around the world.

- Data_Extract_From_Environmental_and_Governance_(ESG)_Data.xlsx
Contains data that measures environmental, social, and governance indicators for countries around the world.

- airquality.json
Contains air quality levels and population information by country.

#10: Expected_Output

Expected_Output directory contains .tsv files that our team generated from each Seize_the_data_X.py file.  This directory contains what our code should output.

Bik_Step4_Test.tsv is generated when 'python Control_Script.py --WebScrape_Test' is ran from terminal.
Bik_Step4_Complete.tsv is generated when 'python Control_Script.py --WebScrape_Full' is ran from terminal.
Final_Output.tsv is generated when 'python Control_Script.py --AdditionalData' is ran from terminal.

Contained in the Expected_Output directory is htmls directory which compiles htmls for all records (along with those we manually saved) when 'python Control_Script.py --Extract_html' is run from terminal. These files are utilized to perform analysis using Tika similarity.


LINKS TO DATA SOURCES:
------------------------

- International DOI Foundations
https://doi.org/

- National Library of Medicine
https://pubmed.ncbi.nlm.nih.gov/

- Nature Research
https://www.nature.com/articles/

- Homeland Infrastructure Foundation-Level Data(HIFLD)
https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::colleges-and-universities-campuses/about

- U.S. Census Bureau, International Database
https://www.census.gov/data-tools/demo/idb/#/table?COUNTRY_YEAR=2022&COUNTRY_YR_ANIM=2022&menu=tableViz&POP_YEARS=2022&TABLE_YEARS=1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2022&TABLE_RANGE=1990,2014&TABLE_USE_RANGE=Y&TABLE_USE_YEARS=N&TABLE_STEP=1&quickReports=CUSTOM&CUSTOM_COLS=POP,GR,RNI,POP_DENS,TFR,CBR,E0,IMR,CDR,NMR 

- The World Bank, Environmental, Social, and Governance Data
https://datacatalog.worldbank.org/search/dataset/0037651

- World Population Review, Most Polluted Cities 2022
https://worldpopulationreview.com/country-rankings/most-polluted-countries





