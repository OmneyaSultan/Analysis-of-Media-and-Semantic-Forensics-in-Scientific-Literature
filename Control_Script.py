#Group: Sieze The Data
#Course: DSCI 550 - Spring 2022

import Seize_the_data_1 as RGscrape
import Seize_the_data_2
import Seize_the_data_3
import Seize_the_data_4
import Seize_the_data_5
import create_htmls
import sys


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Please Run --WebScrape_Test or --Webscrape_Full or --AdditionalData or --Extract_html")

    elif sys.argv[1] == '--WebScrape_Test':
        # Scrapes small sample of ResearchGate, Google Scholar, and doi websites and adds attributes to orignal datset
        exec(open("Seize_the_data_1.py").read())
        RGscrape.WebScrape("OriginalDatasets//BIK_DATATest.tsv","BIK_OutputTest.tsv")
        Seize_the_data_2.Scrape_affil("BIK_OutputTest.tsv", "Bik_Step4_Test.tsv")

    elif sys.argv[1] == '--WebScrape_Full':
        #Takes more than 1 hour to run.  Scrapes ResearchGate, Google Scholar, and doi websites and adds attributes to orignal datset
        exec(open("Seize_the_data_1.py").read())
        RGscrape.WebScrape("OriginalDatasets//BIK_DATA.tsv","BIK_Researchgate.tsv")
        Seize_the_data_2.Scrape_affil("BIK_Researchgate.tsv", "Bik_Step4_Complete.tsv")

    elif sys.argv[1] == '--AdditionalData':
        #Adds additional attributes from the three new datasets to the original dataset
        Seize_the_data_3.US_Population("Bik_Step4_Complete.tsv")
        Seize_the_data_4.Country_Values("Bik_with_colleges_data.tsv")
        Seize_the_data_5.AQ_Population("og_with_country_data.tsv")

    elif sys.argv[1] == '--Extract_html':
        #Extract the htmls that do not have encoding errors and saves into a folder
        create_htmls.save_html("BIK_Researchgate.tsv")

    #Covers any naming errors
    else:
        print("Please Run --WebScrape_Test or --Webscrape_Full or --AdditionalData or --Extract_html")
