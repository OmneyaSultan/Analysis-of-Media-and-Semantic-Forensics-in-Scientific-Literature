# Import statements
import requests
import csv
import os

#
def write_html(content, doi, count):
    text = content.text
    file_name = (str(count) + '.html')
    name = file_name.replace('/', '.')
    file = open('htmls/' + name, 'w', encoding='UTF-8')
    file.write(text)
    file.close()


def save_html(tsv_file):
    #variables to store data
    og_dataset = {}
    data = [];
    problem_html=[]

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

    try:
        os.mkdir('htmls')
    except FileExistsError:
        pass


    count=1    
    for doi in og_dataset["DOI"]:#doi_first_auth_dict.keys():
            #if the keyword "pone" is in the doi url, request page and save html 
            if "pone" in doi:
                university = "";
                article = "https://doi.org/" + str(doi)
                content = requests.get(article)
                write_html(content, doi, count)
                            
            #if the keyword "pbio" or "pgen" or "ppat" or "pntd" is in the doi url,request page and save html 
            elif ("pbio" in doi) or ("pgen" in doi) or ("ppat" in doi) or ("pntd" in doi):
                university = "";
                article = "https://doi.org/" + str(doi)
                content = requests.get(article)
                write_html(content, doi, count)
                

            #if the keyword "mBio" or "IAI" or "JCM" is in the doi url, request page and save html 
            elif ("mBio" in doi) or ("IAI" in doi) or ("JCM" in doi):
                university = "";
                alt = "";
                article = "https://doi.org/" + str(doi)
                content = requests.get(article)
                write_html(content, doi, count)
                

                
                    
            #if the keyword "PMID" is in the doi url, request page and save html 
            #for this one, the url had to be adjusted
            elif ("PMID" in doi):
                university = "";
                dummy = "";
                doi = str(doi)
                idnum = doi.replace("PMID: ","")
                article = "https://pubmed.ncbi.nlm.nih.gov/" + str(idnum)
                content = requests.get(article)
                write_html(content, doi, count)
                
                        
            #if the keyword ".1155" is in the doi url, request page and save html 
            elif ".1155"  in doi:
                university = "";
                article = "https://doi.org/" + str(doi)
                content = requests.get(article)
                write_html(content, doi, count)
                    
                        

            #if the keyword "science" is in the doi url, request page and save html 
            elif "science" in doi:
                university = ""
                article = "https://doi.org/" + str(doi)
                content = requests.get(article)
                write_html(content, doi, count)
                
            
            #if the keyword "nature" or "onc" is not in the doi url and "1038" is in the doi url, request page and save html 
            elif ("nature" not in doi) and ("onc" not in doi) and ("1038" in doi):
                university = "";
                doi = str(doi)
                num = doi.replace("10.1038/", "")
                article = "https://www.nature.com/articles/" + str(num) + "#Aff1"
                content = requests.get(article)
                write_html(content, doi, count)
                        
                
            #if the keyword "nature" is in the doi url, request page and save html      
            elif "nature" in doi: 
                university = "";
                doi = str(doi)
                num = doi.replace("10.1038/", "")
                article = "https://www.nature.com/articles/" + str(num) + "#Aff1"
                content = requests.get(article)
                write_html(content, doi, count)
                

            #if the keyword "onc" is in the doi url, request page and save html 
            elif "onc" in doi:
                university = "";
                doi = str(doi)
                num = doi.replace("10.1038/", "")
                num = num.replace(".", "")

                article = "https://www.nature.com/articles/" + str(num) + "#Aff1"
                content = requests.get(article)
                write_html(content, doi, count)
                
                
            #if the keyword "ijo" is in the doi url, request page and save html 
            elif "ijo" in doi:
                university = "";
                article = "https://doi.org/" + str(doi)
                content = requests.get(article)
                write_html(content, doi, count)
                

            #if the keyword "pnas" is in the doi url, request page and save html 
            elif "pnas" in doi:
                university = "";
                article = "https://doi.org/" + str(doi)
                content = requests.get(article)
                write_html(content, doi, count)

            #if none of these cases work check is 1186 is in doi request page and save html
            #for all other left over cases, there were security/encryption issues so we had to manually extract 
            #The doi urls with issues, are saved to a list where the url can be accessed and the html can be manually extracted
            else:
                if "1186/"in doi:
                    article = "https://doi.org/" + str(doi)
                    content = requests.get(article)
                    write_html(content, doi, count)
                else:
                    problem_html.append([count, doi, article])
                
            count+=1
            





