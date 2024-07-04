from bs4 import BeautifulSoup
import lxml
import requests

# Extracting html code directly from the website for realtime data to the total no.of pages
internshala_html_data=requests.get("https://internshala.com/jobs/").text

# Using BeautifulSoup for parsing through the data
soup=BeautifulSoup(internshala_html_data,'lxml')
soup.prettify()

# Using soup to find the no.of pages
no_of_pages=soup.find('div',class_="page_number heading_6").text
no_of_pages=list(map(int,no_of_pages.split('/')))

# Loop for each page numbers
for each_page_no in range(no_of_pages[0],3):

    # Getting the listed jobs on each page
    each_page_request_data=requests.get(f"https://internshala.com/jobs/page-{each_page_no}").content
    soup=BeautifulSoup(each_page_request_data,'lxml')
    soup.prettify()

    data=soup.find_all('div',class_='container-fluid individual_internship view_detail_button visibilityTrackerItem')
    for each_job in data:
        jobdetail_page_link=str(each_job.get("data-href")) #to get the link of the each job details page
        print(each_job.h3.text.strip()) #jobtitle
        print(each_job.p.text.strip()) #jobcompany
        print(each_job.span.a.text.strip()) #joblocation
        print(each_job.find('div',class_="item_body desktop-text").text) #jobexperience
        print(each_job.find('span',class_="mobile").text.strip()) #jobsalary

        jobdetail_page=requests.get(f"https://internshala.com{jobdetail_page_link}")
        soup=BeautifulSoup(jobdetail_page.text,'lxml')

        content=soup.find('div',id="content")
        idetails=content.find('div',class_="round_tabs_container")
        list_of_skills=[]
        for span_tag in idetails.find_all('span',class_="round_tabs"):
            list_of_skills.append(span_tag.text)

        print(list_of_skills)
        print()

