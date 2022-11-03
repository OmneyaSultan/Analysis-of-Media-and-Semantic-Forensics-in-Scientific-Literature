"""
Group: Sieze The Data
Course: DSCI 550 - Spring 2022

Description: This script scrapes data from the DOI article pages based on the information provided by the Bik et Al dataset (named 'BIK_DATA.tsv').
We used the DOI and authors to collect the following features: Affiliation and Degree Area
This script returns a tsv file with the original Bik data along with the 2 added features.

"""
# Import statements
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

# --------------------------Read TSV File and Create Dictionaries Section --------------------------------------------
def Scrape_affil(tsv_file, output_file):        
    #variables to store data
    og_dataset = {}
    data = [];

    #Read TSV File
    og_tsv=open(tsv_file, encoding='ISO-8859-1')
    read_tsv= csv.reader(og_tsv, delimiter='\t')

    #put all of the rows in the tsv into a list
    for row in read_tsv:
        data.append(row);
        
    #put the headers of the tsv in a separate list
    headers = data.pop(0);

    #go through each column in the dataset and store it into a dictionary where the key is the header and the value
    #is a list of all of the values in that column.
    for i in range(len(headers)):
        interim = [];
        for j in range(len(data)):
            interim.append(data[j][i])
        og_dataset[headers[i]] = interim;

            
    # -------------------------- Build Affiliations List Section --------------------------------------------



    #create an empty list to hold all of the affiliations per each first author which will then be appended to the dataset
    affiliations = [];
    #for each doi in the first author dictionary 
    for doi in og_dataset["DOI"]:#doi_first_auth_dict.keys():
        #if the keyword "pone" is in the doi url, create a soup and then parse the website 
        #to find the affiliated university and then append to affiliations list
        if "pone" in doi:
            university = "";
            article = "https://doi.org/" + str(doi)
            content = requests.get(article)
            soup = BeautifulSoup(content.content, 'html.parser')
            
            affi = soup.find_all("p", id="authAffiliations-0");
            
            for p in affi:
                university = p.get_text();
                university = university[16:]
                university = university.rstrip("\n  ")
                break
                
            #if not possible to scrape webpage   
            if not university:
                affiliations.append("-1")
            else:
                affiliations.append(university)
                        
        #if the keyword "pbio" or "pgen" or "ppat" or "pntd" is in the doi url, create a soup and then parse the website 
        #to find the affiliated university and then append to affiliations list
        elif ("pbio" in doi) or ("pgen" in doi) or ("ppat" in doi) or ("pntd" in doi):
            university = "";
            article = "https://doi.org/" + str(doi)
            content = requests.get(article)
            soup = BeautifulSoup(content.content, 'html.parser')
        
            for tag in soup.find_all("meta"):
                if tag.get("name", None) == "citation_author_institution":
                    university = tag.get("content", None)
                    break
            
            #if not possible to scrape webpage   
            if not university:
                affiliations.append("-1")
            else:
                affiliations.append(university)        
            

        #if the keyword "mBio" or "IAI" or "JCM" is in the doi url, create a soup and then parse the website 
        #to find the affiliated university and then append to affiliations list
        elif ("mBio" in doi) or ("IAI" in doi) or ("JCM" in doi):
            university = "";
            alt = "";
            article = "https://doi.org/" + str(doi)
            content = requests.get(article)
            soup = BeautifulSoup(content.content, 'html.parser')

            for tag in soup.find_all("div"):
                if tag.get("property", None) == "organization":
                    university = tag.get_text()
                    break
                
            #if not possible to scrape webpage   
            if not university:
                affiliations.append("-1")
            else:
                affiliations.append(university)  
            

            
                
        #if the keyword "PMID" is in the doi url, create a soup and then parse the website 
        #to find the affiliated university and then append to affiliations list
        #for this one, the url had to be adjusted before creating the soup
        elif ("PMID" in doi):
            university = "";
            dummy = "";
            doi = str(doi)
            idnum = doi.replace("PMID: ","")
            article = "https://pubmed.ncbi.nlm.nih.gov/" + str(idnum)
            content = requests.get(article)
            soup = BeautifulSoup(content.content, 'html.parser')

            for tag in soup.find_all("meta"):
                if tag.get("name", None) == "citation_doi":
                    dummy = tag.get("content", None);
                    break

            article = "https://doi.org/" + dummy
            content = requests.get(article)
            soup = BeautifulSoup(content.content, 'html.parser')

            for tag in soup.find_all("div"):
                if tag.get("property", None) == "organization":
                    university = tag.get_text();
                    break
            
            #if not possible to scrape webpage   
            if not university:
                affiliations.append("-1")
            else:
                affiliations.append(university)  
            
                    
        #if the keyword ".1155" is in the doi url, create a soup and then parse the website 
        #to find the affiliated university and then append to affiliations list
        elif ".1155"  in doi:
            university = "";
            article = "https://doi.org/" + str(doi)
            content = requests.get(article)
            soup = BeautifulSoup(content.content, 'html.parser')

            for tag in soup.find_all("div", class_="sc-fHxwqH dMuGGA isHide") or soup.find_all("div", class_="sc-fHxwqH dMuGGA"):
                span = tag.find_all("span")
                for univ in span:
                    university = univ.get_text();
                    break
            
            #if not possible to scrape webpage   
            if not university:
                affiliations.append("-1")
            else:
                affiliations.append(university)  
            
                    

        #if the keyword "science" is in the doi url, create a soup and then parse the website 
        #to find the affiliated university and then append to affiliations list
        elif "science" in doi:
            university = ""
            article = "https://doi.org/" + str(doi)
            content = requests.get(article)
            soup = BeautifulSoup(content.content, 'html.parser')

            for tag in soup.find_all("div", class_="affiliations"):
                span = tag.find_all("span")
                for univ in span:
                    university = univ.get_text();
                    break
                break
                
            #if not possible to scrape webpage   
            if not university:
                affiliations.append("-1")
            else:
                affiliations.append(university) 
            
        
        #if the keyword "nature" or "onc" is not in the doi url and "1038" is in the doi url, 
        #create a soup and then parse the website to find the affiliated university and then 
        #append to affiliations list
        elif ("nature" not in doi) and ("onc" not in doi) and ("1038" in doi):
            university = "";
            doi = str(doi)
            num = doi.replace("10.1038/", "")
            article = "https://www.nature.com/articles/" + str(num) + "#Aff1"
            content = requests.get(article)
            soup = BeautifulSoup(content.content, 'html.parser')

            for tag in soup.find_all("p", class_="c-article-author-affiliation__address"):
                university = tag.get_text();
                break
            
            #if not possible to scrape webpage   
            if not university:
                affiliations.append("-1")
            else:
                affiliations.append(university) 
                
            
        #if the keyword "nature" is in the doi url, create a soup and then parse the website 
        #to find the affiliated university and then append to affiliations list      
        elif "nature" in doi: 
            university = "";
            doi = str(doi)
            num = doi.replace("10.1038/", "")
            article = "https://www.nature.com/articles/" + str(num) + "#Aff1"
            content = requests.get(article)
            soup = BeautifulSoup(content.content, 'html.parser')

            for tag in soup.find_all("p", class_="c-article-author-affiliation__address"):
                university = tag.get_text()
                break

            #if not possible to scrape webpage   
            if not university:
                affiliations.append("-1")
            else:
                affiliations.append(university) 
            

        #if the keyword "onc" is in the doi url, create a soup and then parse the website 
        #to find the affiliated university and then append to affiliations list
        elif "onc" in doi:
            university = "";
            doi = str(doi)
            num = doi.replace("10.1038/", "")
            num = num.replace(".", "")

            article = "https://www.nature.com/articles/" + str(num) + "#Aff1"
            content = requests.get(article)
            soup = BeautifulSoup(content.content, 'html.parser')

            for tag in soup.find_all("p", class_="c-article-author-affiliation__address"):
                university = tag.get_text();
                break
            
            #if not possible to scrape webpage   
            if not university:
                affiliations.append("-1")
            else:
                affiliations.append(university) 
            
            
        #if the keyword "ijo" is in the doi url, create a soup and then parse the website 
        #to find the affiliated university and then append to affiliations list
        elif "ijo" in doi:
            university = "";
            article = "https://doi.org/" + str(doi)
            content = requests.get(article)
            soup = BeautifulSoup(content.content, 'html.parser')

            for tag in soup.find_all("div", class_="toggle"):
                span = tag.find_all("span")
                for univ in span:
                    if univ.get_text() == "Affiliations: ":
                        continue
                    else:
                        university = univ.get_text()
                break
            
            #if not possible to scrape webpage   
            if not university:
                affiliations.append("-1")
            else:
                affiliations.append(university) 
            

        #if the keyword "pnas" is in the doi url, create a soup and then parse the website 
        #to find the affiliated university and then append to affiliations list
        elif "pnas" in doi:
            university = "";
            article = "https://doi.org/" + str(doi)
            content = requests.get(article)
            soup = BeautifulSoup(content.content, 'html.parser')

            for tag in soup.find_all("li", class_="aff"):
                address = tag.find_all("address")
                for univ in address:
                    univ = univ.get_text();
                    university = univ[1:]
                    break
                break
            
            #if not possible to scrape webpage   
            if not university:
                affiliations.append("-1")
            else:
                affiliations.append(university) 
            

        #if none of these cases work, append a 0 because our parser could not parse the website due to different reasons
        #whether that is security issues or the beautiful soup returned was not in a parseable format
        else:
            affiliations.append("-1")         
        
    # -------------------------- Find Degree Area of First Author Section --------------------------------------------


    #variables to store information
    meantime = [];
    degreeArea = [];

    #going through the affiliations list collected above, go through each affiliated university and department.
    #then pull out the keywords related to department area that end in the following endings for each affiliation 
    #and append that to degreeArea list, which will then be appended to the dataset
    for a in affiliations:
        a = str(a);
        words = [];
        words = a.split(" ") 
        
        #meantime is used as a temporary list to store all of the department related words per affiliation that relate 
        #to possible degreeArea. meantime is then appended to degreeArea.
        meantime = [];
        
        for word in words:
            if ("ology" in word):
                meantime.append(word);
            elif ("acy" in word):
                meantime.append(word);
            elif ("try" in word):
                meantime.append(word);
            elif ("ics" in word):
                meantime.append(word);
            elif ("omy" in word):
                meantime.append(word);
            elif ("ation" in word):
                meantime.append(word);
            elif ("phy" in word):
                meantime.append(word);
            elif ("ence" in word):
                meantime.append(word);
        #if there are no words that end in any of these endings in the affiliation, then append a -1.
        if not meantime:
            meantime.append("-1")    
        degreeArea.append(meantime)
        
        
    # --------------------------Putting Together the DataFrame Section --------------------------------------------

    #add into the dictionary the affiliation university and the degree area
    og_dataset["Affiliation University"] = affiliations;
    og_dataset["Author 1 Degree Area"] = degreeArea;


    #create the dataframe out of the dictionary
    df = pd.DataFrame(og_dataset)

    #export dataframe as tsv
    df.to_csv(output_file, sep="\t")