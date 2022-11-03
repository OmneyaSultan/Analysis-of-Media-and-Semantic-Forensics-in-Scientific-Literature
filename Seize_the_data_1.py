"""
Group: Sieze The Data
Course: DSCI 550 - Spring 2022

Description: This script scrapes data from Research Gate and Google Scholar based on the information provided by the Bik et Al dataset (named 'BIK_DATA.tsv').
We used the DOI and authors to collect the following features: Publication Rate, Lab Size, Other Journals, Degree Level, Career Duration.
This script returns a tsv file with the original Bik data along with the 5 added features.

"""

# Import statements
from bs4 import BeautifulSoup
import requests
import csv
import requests
import re
import time
import pandas as pd

# --------------------------Merge Data--------------------------------------------

def merge_tsv(tsvlst):
    tsv_df=[]
    for f in tsvlst:
        tsv_df.append(pd.read_csv(f, sep='\t'))
    df=pd.concat(tsv_df)
    df.to_csv('BIK_Researchgate.tsv', sep="\t")
    
    
# --------------------------Usefule Functions --------------------------------------------
#Cleans the name of authors 
def name_check(name):
    profile_check=name.split(" ")
    if profile_check[0]=="":
        profile_check.pop(0)
    if profile_check[-1]=="":
        profile_check.pop(0)
    if profile_check[-1]== "Jr.":
        profile_check=profile_check[:-1] 
    if profile_check[0]=="Dr.":
        profile_check.pop(0)
    if profile_check[0]=="and" or profile_check[0]==" and":
        profile_check.pop(0)
    if len(profile_check)>2:
        name=profile_check[0]+" "+profile_check[-1]
    else:
        name=profile_check[0]+" "+profile_check[-1]
      
    if "\x92" in name:
        name=name.replace("\x92", "i")
    if "\x97" in name:
        name=name.replace("\x97", "o")
    if "\x87" in name:
        name=name.replace("\x87", "a")

    new_name=name
    new_name=new_name.replace("marõa", "maria")
    new_name=new_name.replace("Õ","")
    new_name=new_name.replace("õ","")
    new_name=new_name.replace("_","")
    new_name=new_name.replace("'","")  
    return new_name.lower()

#Finds earliest publication date and tracks other journals the author was published in
def earliest_pubdate(jdetails):
    months= ["JAN ", "FEB ", "MAR ", "APR ", "MAY ", "JUN ", "JUL ", "AUG ", "SEP ", "OCT ", "NOV ", "DEC "]
    journal_lst=[]
    earliest_pub=2022
    duration=-1
    for j in jdetails:
        journal=j.get_text()
        journal= journal.upper()
        true_j = any(months in journal for months in months)
        if true_j==True:
            year_pub= int(journal[4:])
            if year_pub<earliest_pub:
                earliest_pub=year_pub
        if true_j==False and (journal not in journal_lst):
            journal_lst.append(journal)

    if journal_lst==[]:
        journal_lst.append(str(-1))

    duration=2022-earliest_pub
    
    if duration==0:
            duration=-1

    return [duration, journal_lst]

#Combine the list of lists of other journals into a string 
def combine_journals(journ_lst):
    new_str=""
    for i in journ_lst:
        try:
            for w in i:
                w=str(w)
                new_str+=w
                new_str+=", "   
            new_str+="; "
        except:
            new_str+="-1 ;"
    new_str=new_str[:len(new_str)-4]
    new_str=new_str.replace(", ;", ";")
    new_str=new_str.replace("-,", "-")
    new_str=new_str.replace(", ,", ",")
    new_str=new_str.replace(",,", ",")
    return new_str 

# --------------------------Read TSV File and Create Dictionaries Section --------------------------------------------
og_tsv=open('OriginalDatasets//BIK_DATA.tsv', encoding='ISO-8859-1')
read_tsv= csv.reader(og_tsv, delimiter='\t')

# Create Dictionary with DOI as Key and list of authors as value
# Does not include header and ignores blank values from read function

doi_all_auth_dict={} # dictionary for all authors

doi_first_auth_dict={} # dictionary for just first author


for row in read_tsv:
    all_auth_clean=[]
    if row[3] != "" and row[3] != "DOI":
        names=row[0]
        if ", and " in names or ",and " in names:
            names.replace("and", "")
        elif "and " in names and "," not in names:
            names.replace("and", ",")
        all_auth=list(names.split(","))
        for a in all_auth:
            first_auth= all_auth[0]
            all_auth_clean.append(name_check(a))
        doi_all_auth_dict[row[3]]= all_auth_clean
        doi_first_auth_dict[row[3]]=first_auth

# --------------------------Open Session and Log in to Research Gate--------------------------------------------
username="perkinsm@usc.edu"
password="pass123!"

login_url="https://www.researchgate.net/application.Login.html"
s = requests.Session()
login = s.get(login_url)
RGSoup= BeautifulSoup(login.text, 'html.parser')
attrs={"name":"request_token"}
request = RGSoup.find("input",attrs)["value"]
params = {"login": username, "password": password,"request_token":request,"invalidPasswordCount":"0","setLoginCookie":"yes"}
s.post(login_url, data = params)

# --------------------------Function to Scrape Web--------------------------------------------
def WebScrape(tsv_file,output):
    
    # Read TSV File
    og_tsv=open(tsv_file, encoding='ISO-8859-1')
    read_tsv= csv.reader(og_tsv, delimiter='\t')

    # Create Dictionary with DOI as Key and list of authors as value
    # Does not include header and ignores blank values from read function

    doi_all_auth_dict={} # dictionary for all authors
    doi_first_auth_dict={} # dictionary for just first author

    for row in read_tsv:
        all_auth_clean=[]
        if row[3] != "" and row[3] != "DOI":
            names=row[0]
            if ", and " in names or ",and " in names:
                names.replace("and", "")
            elif "and " in names and "," not in names:
                names.replace("and", ",")
            all_auth=list(names.split(","))
            for a in all_auth:
                first_auth= all_auth[0]
                all_auth_clean.append(name_check(a))
            doi_all_auth_dict[row[3]]= all_auth_clean
            doi_first_auth_dict[row[3]]=first_auth


    #Dictionaries to link each attribute to the correct DOI
    doi_pub_dict={}
    doi_labsize={}
    doi_journals={}
    degree_level={}
    career_len={}
    total_auth={}

    #keeping track of list iem
    count=0

    #Loop through each DOI
    for o_doi in doi_all_auth_dict:
        total_auth[o_doi]= len(doi_all_auth_dict[o_doi])

        #Set variables for this DOIs authors
        pub_rate=[]
        other_journal=[]
        lab_size=[]
        highest_d=-1
        first_career_duration=-1

        #Adjust to handle a few special cases
        special_cases={}
        if "Ð" in o_doi:
            og_doi=doi
            doi=doi.replace("Ð","-") 
            special_cases[doi]=og_doi
        elif o_doi == 'PMID: 8675338':
            doi = "10.1128/iai.64.6.2282-2287.1996"
            special_cases[doi]='PMID: 8675338'
        elif o_doi == 'PMID: 9864199 ':
            doi = "10.1128/IAI.67.1.80-87.1999"
            special_cases[doi]='PMID: 9864199 '
        elif o_doi == 'PMID: 9620397 ':
            doi = "10.1128/JCM.36.6.1666-1673.1998"
            special_cases[doi]='PMID: 9620397 '


        if o_doi not in special_cases.keys():
            doi=o_doi
        else:
            doi=special_cases[o_doi]
            
        #Open the Researchgate page for the article
        article="https://www.researchgate.net/search.Search.html?type=publication&query="+str(doi)
        cont = s.get(article)
        soup = BeautifulSoup(cont.content, 'html.parser')


        #Retrieve accessible profile links from Research Gate
        authlinks={}

        for link in soup.find_all("a", {"class":"nova-legacy-e-link nova-legacy-e-link--color-inherit nova-legacy-e-link--theme-bare research-detail-author"}):
            profile=link.get_text()
            profile=name_check(profile)
            authlinks[profile]="https://www.researchgate.net/" + str(link.get('href'))

        #Count authors: for list length and to keep track of first author
        auth_num=1
        

        #Loop through each author in this DOI
        for profile in doi_all_auth_dict[o_doi]:

        	#Check to see if this author has an accessible researchgate link
            try:
                if profile in authlinks.keys():
                    have_link=True
                else:
                    have_link=False

                # --------------------------For authors with Research Gate URL--------------------------------------------
                if have_link==True:

                    content=s.get(authlinks[profile])
                    soup = BeautifulSoup(content.content, 'html.parser')

                    #For those without an account
                    authordetails=soup.find_all("h2", {"class":"nova-legacy-e-text nova-legacy-e-text--size-m nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-inherit"})


                    # --------------------------For Research Gate Authors with Profile--------------------------------------------
                    if authordetails==[]:
                        authordetails=soup.find_all("div", {"class":"nova-legacy-e-text nova-legacy-e-text--size-xl nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-inherit"})


                        #First Author Degree Level 

                        count_again=0
                        if auth_num==1:
                            try:
                                degrees=soup.find_all("li", {"class":"nova-legacy-e-list__item"})
                                if degrees!=[]:
                                    d_count = 0
                                    while d_count<4:
                                        for deg in degrees:
                                            d=deg.get_text()

                                            d=d.replace(" ","")
                                            if d!="":
                                                if ("MD" in d):
                                                    highest_d="MD"
                                                if ("Ph" in d )or ("ph" in d) or ("doc" in d) or ("Doc" in d):
                                                    if highest_d!="MD":
                                                        highest_d="PhD"
                                                elif ("ms" in d) or ("MS" in d )or ("Ms" in d) or ("Masters in d"):
                                                      if highest_d!= "PhD":
                                                            highest_d = "Masters"
                                                elif (d[0]== "Ba" or d[0]=="ba" or d[0]== "Bs" or d[0]=="bs" or d[0]== "BS" or d[0]=="BA"):
                                                    if highest_d != "PhD" or highest_d!="Masters":
                                                        highest_d = "Bachelors"
                                            d_count+=1
                
                                    degree_level[o_doi]=highest_d 
                                else:
                                    degree_level[o_doi]=-1

                            except:
                                degree_level[o_doi]=-1



                        #Find Lab Members and append to lab_size list
                        lab=soup.find_all("div", {"class":"nova-legacy-e-text nova-legacy-e-text--size-s nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-xxs nova-legacy-e-text--color-grey-400"})
                        if lab==[]:
                            lab_size.append(str(-1))
                        else:
                            for l in lab:
                                labmem=l.get_text()
                                if "Lab members" in labmem:
                                    labmem= labmem[13:].replace(")","")
                                    lab_size.append(str(labmem))
                                    break

                            if len(lab_size)!=auth_num:
                                lab_size.append(str(-1))



                        #Other Journals for those with account & duration of career

                        try:
                            journ_cont=s.get(authlinks[profile]+"/research")
                            jsoup = BeautifulSoup(journ_cont.content, 'html.parser')
                            jdetails=jsoup.find_all("li", {"class":"nova-legacy-e-list__item nova-legacy-v-publication-item__meta-data-item"})
                            j=earliest_pubdate(jdetails)
                            if j[1]==[]:
                                other_journal.append(str(-1))
                            else:
                                other_journal.append(j[1])

                            if auth_num==1:
                                if j==[]:
                                    first_career_duration=-1
                                    career_len[o_doi]=first_career_duration
                                else:
                                    first_career_duration=j[0]
                                    career_len[o_doi]=first_career_duration
                        except:
                            if auth_num==1:
                                career_len[o_doi]=-1
    

                            other_journal.append(str(-1))


                        #Append items to pub_rate dicitionary 
                        try:
                            item=authordetails[0].get_text()
                            pub_rate.append(item)
                        except:
                            pub_rate.append(str(-1))


                    # --------------------------For Research Gate Authors WITHOUT Profile--------------------------------------------
                    else:
                        
                		#Find Publication Rate
                        for item in authordetails:
                            if "Publications" in item.get_text():
                                itemtxt=item.get_text()[14:16]
                                itemtxt=itemtxt.replace(")","")
                                try:
                                    int(itemtxt)
                                    pub_rate.append(itemtxt)
                                except:
                                    pub_rate.append(str(-1))
                        if len(pub_rate)!=auth_num:
                            pub_rate.append(str(-1))

                        
                        #Other Journals & Career Duration
                        jdetails=soup.find_all("li", {"class":"nova-legacy-e-list__item publication-item-meta-items__meta-data-item"})
                        j=earliest_pubdate(jdetails)
                        if j[1]==[]:
                            other_journal.append(str(-1))
                        else:
                            other_journal.append(j[1])

                        if auth_num==1:
                            career_len[o_doi]=j[0]
                            degree_level[o_doi]=-1

                        #Lab Size (by co-authors)
                        jdetails=soup.find_all("h2", {"class":"nova-legacy-e-text nova-legacy-e-text--size-m nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-inherit"})
                        for ca in jdetails:
                            if "Top co-authors" in ca.get_text():
                                ca=ca.get_text()[15:17]
                                ca=ca.replace(")","")
                                try:
                                    int(ca)
                                    lab_size.append(ca)
                                except:
                                    lab_size.append(str(-1))

                        if len(lab_size)!=auth_num:
                                lab_size.append(str(-1))


                # --------------------------For authors WITHOUT Research Gate URL--------------------------------------------
                #Search Google Scholar
                elif have_link == False:
                    search_url="https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors="+ profile.replace(" ", "+") +"&btnG="
                    search= requests.get(search_url)
                    search_soup=BeautifulSoup(search.content, 'html.parser')
                    no_match=search_soup.find_all("p")

                    # --------------------------Author Not Found on Google Scholar-------------------------------------------
                    if no_match != [] :
                        for suggest in no_match:
                            if "didn't match" in suggest.get_text():
                                pub_rate.append(str(-1))
                                other_journal.append(str(-1))
                                lab_size.append(str(-1))

                                if auth_num==1:
                                    career_len[o_doi]=-1
                                    degree_level[o_doi]=-1
                                break

                    # --------------------------Author Found on Google Scholar-------------------------------------------
                    else:
                        for link in search_soup.find_all("a", {"class":"gs_ai_pho"}):
                            url="https://scholar.google.com" + str(link.get('href'))+"&view_op=list_works&sortby=title&pagesize=300"
                            #taking first/best option from list
                            break
                        
                        #special case that kept getting errors
                        if url=="https://scholar.google.com/citations?hl=en&user=KMwUGM8AAAAJ&view_op=list_works&sortby=title&pagesize=300":
                            other_journal.append(str(-1))
                            pub_rate.append(str(-1))

                        else:
                            gs_con=requests.get(url)
                            g_soup=BeautifulSoup(gs_con.content, 'html.parser')

                            #Publication Rate
                            for r in g_soup.find_all("span",{"id":"gsc_a_nn"}):
                                rate=r.get_text()
                                rate=rate.split("–")
                                rate=int(rate[1])
                                if rate== int("000"):
                                    rate=-1
                                pub_rate.append(str(rate))
                            if len(pub_rate)!=(auth_num):
                                pub_rate.append(str(-1))

                            #Check Other Journals
                            j_list=[]
                            for j in g_soup.find_all("div",{"class":"gs_gray"}):
                                if '(' in j.get_text():
                                    oj=j.get_text()
                                    oj=re.split('(\d+)', oj)
                                    oj=oj[0][:-1]
                                    try:
                                        oj=oj.upper()
                                    except:
                                        oj=oj
                                    if oj not in j_list:
                                        j_list.append(oj)

                            if j_list==[]:
                                other_journal.append(str(-1))
                            else:
                                other_journal.append(j_list)

                            #Check Career Duration
                            if auth_num==1:
                                lowest_y=2022
                                for y in g_soup.find_all("span",{"class":"gsc_a_h gsc_a_hc gs_ibl"}):
                                    ye=y.get_text()
                                    try:
                                        year=int(ye)
                                        if int(ye)<lowest_y:
                                            lowest_y=int(ye)
                                        first_career_duration=2022-lowest_y
                                    except:
                                        first_career_duration=-1
                                career_len[o_doi]=first_career_duration
                                degree_level[o_doi]=-1

                            #Check for Lab Size(by co-author)
                            lab_authors=0
                            others=g_soup.find_all("a", {"tabindex":"-1"})
                            for ca in others:
                                co_a=ca.get_text()
                                if "Sort" not in co_a:
                                    lab_authors+=1
                            if lab_authors==0:
                                lab_authors=-1
                            lab_size.append(str(lab_authors))


                #Ensures that all dictionaries have the appropriate number of items before iterating to the next author       
                if len(pub_rate)!=(auth_num):
                    pub_rate.append(str(-1))
                if other_journal==[]:
                    other_journal.append(str(-1))
                if len(lab_size)!=(auth_num):
                    lab_size.append(str(-1))
                if auth_num==1 and len(career_len)!=count+1:
                    career_len[o_doi]=(-1)
                if auth_num==1 and len(degree_level)!=count+1:                
                    degree_level[o_doi]=(-1)


            #Ensure that nothing is empty if the code crashes due to security issues
            #If this print, it's likely that we were blocked by the website
            except:
                if len(pub_rate)!=(auth_num):
                    pub_rate.append(str(-1))
                if len(other_journal)!=auth_num:
                    other_journal.append(str(-1))
                if len(lab_size)!=(auth_num):
                    lab_size.append(str(-1))
                if auth_num==1 and len(career_len)!=count+1:
                    career_len[o_doi]=(-1)
                if auth_num==1 and len(degree_level)!=count+1:                
                    degree_level[o_doi]=(-1)
                print(doi)
                print(auth_num)


            #iterate to next auth
            auth_num+=1  

        #Check for errors in this DOI
        if (total_auth[o_doi]!=len(pub_rate)):
            print(total_auth[o_doi])
            print("pub")
            print(len(pub_rate), pub_rate)
        if (total_auth[o_doi]!=len(lab_size)):
            print(total_auth[o_doi])
            print("lab")
            print(len(lab_size), lab_size)
        if (total_auth[o_doi]!=len(other_journal)):
            print(total_auth[o_doi])
            print("journal")
            print(len(other_journal))
        if auth_num==1 and len(career_len)!= count+1:
            career_len[o_doi]=(-1)
        if auth_num==1 and len(degree_level)!= count+1:                
            degree_level[o_doi]=(-1)    
        if career_len[o_doi]==0:
            career_len[o_doi]=-1

        pub_rate=', '.join(pub_rate)
        lab_size=', '.join(lab_size)

        #Append lists to Dictionary per DOI
        doi_pub_dict[o_doi]=pub_rate
        doi_labsize[o_doi]=lab_size
        doi_journals[o_doi]= other_journal

        #Check to see if it is running
        print(count, o_doi)
        count+=1

        #Pauses loop after 10 DOIs to avoid security issues (although they still happen)
        if count%10==0:
            time.sleep(120)   
    
    #Join other journals into string
    clean_journ={}
    for doi in doi_journals.keys():
        clean_journ[doi]=combine_journals(doi_journals[doi])

    
    # --------------------------Add Data to a New TSV File------------------------------------------
    og_dataset = {}
    data = [];
    og_tsv=open(tsv_file, encoding='ISO-8859-1')
    read_tsv= csv.reader(og_tsv, delimiter='\t')

    for row in read_tsv:
        if row[0] == "":
            continue
        else:
            data.append(row);

    headers = data.pop(0);

    for i in range(len(headers)):
        interim = [];
        for j in range(len(data)):
            interim.append(data[j][i])
        og_dataset[headers[i]] = interim;

    og_dataset["Total Authors"]=total_auth.values();
    og_dataset["Publication Rates"] = doi_pub_dict.values();
    og_dataset["Other Journals"] = clean_journ.values();
    og_dataset["Lab Size"] = doi_labsize.values();
    og_dataset["Degree Level"] = degree_level.values();
    og_dataset["Duration of Career"] = career_len.values();

    df = pd.DataFrame(og_dataset)
    df.to_csv(output, sep="\t")























