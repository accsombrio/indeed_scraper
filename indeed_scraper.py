from bs4 import BeautifulSoup
import requests
import csv
import os.path
import sys
import time
from os import path

print("Indeed Job Posts Generator")
print("Author: Aaron Christian Sombrio")

num_results = 0
query_input = input("Search For (Job Title, Keyword, Company Name): ").strip()
location_input = input("Location: ").strip()

url = "https://ph.indeed.com/jobs?q={}&l={}".format(query_input.replace(" ", "+"), location_input.replace(" ", "+"))

try:
    csv_file = open('./output/scraper_results.csv', 'w')
except Exception as e:
    os.mkdir('./output')
    csv_file = open('./output/scraper_results.csv', 'w')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Job Title', 'Company', 'Location', 'Salary', 'Job Link'])

#check if there is still a url
while len(url) > 0:
    source = requests.get(url).text

    soup = BeautifulSoup(source, 'lxml')

    try:
        table1 = soup.find('table', id="resultsBody").tbody.tr.td
    except Exception as e:
        print("No results for this search query")
        sys.exit()

    table2 = table1.find('table', id="pageContent").tr
    results = table2.find('td', id="resultsCol")
    result1 = results.find_all('div', class_='jobsearch-SerpJobCard')

    #loop through job posts per page
    for result in result1: 
        position_title = result.h2.a['title']

        try:
            company = result.find('div', class_='sjcl').div.span.text
        except Exception as e:
            company = "Not Indicated"

        try:
            location = result.find('div', class_='sjcl').find('span', class_='location').text
        except Exception as e:
            location = "Not Indicated"

        try:
            salary = result.find('div', class_='salarySnippet').span
            salary_text = salary.find('span').text
        except Exception as e:
            salary_text = "Not Indicated"
        
        job_post_link = "https://ph.indeed.com{}".format(result.h2.a['href'])

        csv_writer.writerow([position_title.strip(),company.strip(),location.strip(), salary_text.strip(), job_post_link])
    
    #check for next page
    num_results += len(result1)
    try:
        pagination_nav_list = results.find('nav').ul.find_all('li')
        next_page_url = pagination_nav_list[-1].a['href']
        url = "https://ph.indeed.com{}".format(next_page_url)
        
    except Exception as e:
        url = ''
    
print("number of results: {}".format(num_results))
csv_file.close()
time.sleep(3)