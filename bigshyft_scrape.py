import requests
from bs4 import BeautifulSoup

def insert_values(cur,table_name):
    count=0
    for page in range(2,7):
        url= f"https://www.bigshyft.com/backend-jobs-page-{page}-skl"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        items=soup.body.section.find_all('div',class_='relative rounded-2xl bg-white px-5 pb-6 pt-5 shadow-D2 flex-shrink-0 h-[298px] cursor-pointer h-[280px] !pb-3')
        for x in items:
            title_element = x.find('div', class_='text-body1Bold text-TextD2 overflow-hidden text-ellipsis whitespace-nowrap w-[216px]')
            company_element = x.find('div', class_='flex flex-col gap-0.5').find('div')
            location_element = x.find('div', class_='overflow-hidden text-ellipsis whitespace-nowrap text-body1SemiBold text-TextD2 w-[85%]')
            skills_element = x.find('div', class_='overflow-hidden text-ellipsis whitespace-nowrap text-body1SemiBold text-TextD2 w-[85%]')
            exp_element = x.find('div', class_='text-body1SemiBold text-TextD2')
            salary_element = x.find('div', class_='flex gap-1.5')

            job_title = title_element.text.strip() if title_element  else 'No Title'
            company_name = company_element.text.strip() if company_element else 'No Company'
            location = location_element.text.strip() if location_element else 'No Location'
            skills = skills_element.text.strip() if skills_element else 'No Skills Specified'
            experience = exp_element.text.strip() if exp_element else 'No Experience Required'
            salary = salary_element.text.strip() if salary_element else 'No Experience Required'
            #sal= salary1.encode('utf-8')
            print()
            count+=1
            print(f'Inserting Bigshyft- job {count} ',end="...")
            cur.execute(f"""
            INSERT INTO {table_name} VALUES
            ('{job_title}',
             '{company_name}',
             '{skills}',
             '{experience}',
             '{salary}',
             '{location}');""")
            print(f"job {count} inserted")
    #print(jobs)
    return cur