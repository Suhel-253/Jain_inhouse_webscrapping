from bs4 import BeautifulSoup
import lxml
import requests
import mysql.connector
import sys

def If_database_exist(host,user,password):
    def If_connection_established():
        try:
            mydb=mysql.connector.connect(
            host=host,
            user=user,
            password=password
            )
            return mydb.is_connected()
        except mysql.connector.Error as err:
            print(f'Unable to Establish Connection: {err}')
            return False

    if If_connection_established():
        print("Connection Established!!")
        database=input("Enter the Database you wanna work on: ")
        print("Checking if Database Exists...")
        cur=mydb.cursor()
        cur.execute('SHOW DATABASES')
        databases=[row[0] for row in cur.fetchall()]
        if database in databases:
            print("Database Exists!!")
            cur.close()
            cur=mydb.cursor()
            cur.execute(f"USE {database}")
            print('Ready to use database!!')
            return cur
        else:
            # Assuming you have a cursor object after connecting to MySQL (not shown here)
            cur.execute(f"CREATE DATABASE {database}")
            # (Optional) Use the new database
            cur.execute(f"USE {database}")
            print('Ready to use database!!')
            return cur
    else:
        print("Try to fix the code...Unable to connect")
        sys.exit(-1)

def check_table(cur):
    cut.execute('SHOW TABLES')
print("Establishing Connection...")
# Extracting html code directly from the website for realtime data to the total no.of pages
internshala_html_data=requests.get("https://internshala.com/jobs/").text

# Using BeautifulSoup for parsing through the data
soup=BeautifulSoup(internshala_html_data,'lxml')
soup.prettify()

# Using soup to find the no.of pages
no_of_pages=soup.find('div',class_="page_number heading_6").text
no_of_pages=list(map(int,no_of_pages.split('/')))

# Loop for each page numbers
for each_page_no in range(no_of_pages[0],5):

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

