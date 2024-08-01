import httpx
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

import pandas as pd

JOB = "machine learning"
jobs_titles = []
companies_names = []
dates  = []
locations = []
skills = []
links = []
salaries = []
jobs_req = []
page_number = 0
while True :
    url = f"https://wuzzuf.net/search/jobs/?a=hpb&q={JOB}&start={page_number}"
    try:
        page = httpx.get(url, timeout=30.0)  # Set the timeout to 10 seconds
        page.raise_for_status()  # Raise an exception for HTTP errors
    except :
        continue
    soup = BeautifulSoup(page.text, "lxml")
    pages= int(soup.find("strong").text)
    
    jobs = soup.find_all("div", class_="css-d7j1kk")
    titles = soup.find_all("h2", class_="css-m604qf")
    companies = soup.find_all("a", class_="css-17s97q8")
    jobs_dates = soup.find_all("div" , class_=("css-do6t5g" , "css-4c4ojb"))
    jobs_locations = soup.find_all("span", class_="css-5wys0k")
    jobs_skills = soup.find_all("div", class_="css-y4udm8")


    
    i = 0


    for i in range(len(jobs)):
        jobs_titles.append(titles[i].text)
        links.append(titles[i].find("a").attrs["href"])
        
        companies_names.append(companies[i].text)
        dates.append(jobs_dates[i].text)
        locations.append(jobs_locations[i].text)
        skills.append(jobs_skills[i].text.replace(" ·"," "))
        i += 1

    
    for link in links:
        result = httpx.get(link)
        soup = BeautifulSoup(result.text, "lxml")
        job_req = soup.find("div", class_="css-1t5f0fr")
        if job_req is None:
            jobs_req.append("No Job Requirements Mentioned") 
        else:
            jobs_req.append(job_req.text)
                


  
        

    file_list = [jobs_titles, companies_names, dates, locations, skills , links , jobs_req]
    exported = zip_longest(*file_list)


    

            
 

    page_number += 1
    if page_number > pages // 15 + 1 :
      print("Done")
      break
    else:
      print("Page number : " , page_number)
      

    with open("wuzzuf.csv", "w" ,   encoding="utf-8") as csv_file:
       writer = csv.writer(csv_file)
       writer.writerow(["Title", "Company", "Date", "Location", "Skills" , "Links" , "Job Requirements"])
       writer.writerows(exported)
            
    

df = pd.read_csv("wuzzuf.csv")
print(df)

