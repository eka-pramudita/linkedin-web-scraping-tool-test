import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

start = time.time()

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

job_titles, company_names = [], []
posting_times, number_of_applicants = [], []
seniorities, employment_types, job_functions, industries = [], [], [], []
descriptions = []
sizes_of_employee = []

links = ['https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Indonesia&geoId=102478259&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
         'https://www.linkedin.com/jobs/search?keywords=Senior%20Data%20Scientist&location=Indonesia&geoId=102478259&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
         'https://www.linkedin.com/jobs/search?keywords=Data%20Engineer&location=Indonesia&geoId=102478259&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
         'https://www.linkedin.com/jobs/search?keywords=Senior%20Data%20Engineer&location=Indonesia&geoId=102478259&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
         'https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=Indonesia&geoId=102478259&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
         'https://www.linkedin.com/jobs/search?keywords=Senior%20Data%20Analyst&location=Indonesia&geoId=102478259&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
         'https://www.linkedin.com/jobs/search?keywords=Business%20Intelligence%20%28BI%29&location=Indonesia&geoId=102478259&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
         'https://www.linkedin.com/jobs/search?keywords=Senior%20Business%20Intelligence%20Analyst&location=Indonesia&geoId=102478259&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0']

try:
    for link in links:
        driver.get(link)
        time.sleep(5)
        # page_per_click = driver.find_elements_by_class_name("result-card__full-card-link")
        page_per_click = []
        for i in range(1,21):
            job_card = driver.find_elements_by_xpath("//li[@data-row='" + str(i) + "']")
            page_per_click.append(job_card)
        page_per_click = list(filter(lambda x: x != [], page_per_click))

        for i in range(len(page_per_click)):
            if page_per_click[i][0].is_displayed():
                driver.execute_script("arguments[0].click();", page_per_click[i][0])
                element_present = EC.presence_of_element_located((By.CLASS_NAME, 'details-pane__content--show'))
                WebDriverWait(driver, 10).until(element_present)
                show_more = driver.find_elements_by_class_name("show-more-less-html__button")
                driver.execute_script("arguments[0].click();", show_more[0])
            job_cards = driver.find_elements_by_class_name('results__detail-view')
            result_html = job_cards[0].get_attribute('innerHTML')
            soup = BeautifulSoup(result_html, 'html.parser')

            try:
                job_title = soup.find('h2', class_='topcard__title').get_text()
            except:
                job_title = 'None'

            job_title = job_title.strip()
            job_titles.append(job_title)

            try:
                company_name = soup.find('a', class_='topcard__org-name-link').get_text()
            except:
                company_name = 'None'

            company_name = company_name.strip()
            company_names.append(company_name)

            sub_title = soup.find_all('h3', class_='topcard__flavor-row')
            posting_x_applicants = sub_title[1].contents
            job_posting = posting_x_applicants[0].get_text()
            applicant = posting_x_applicants[1].get_text()
            posting_times.append(job_posting)
            number_of_applicants.append(applicant)

            job_criteria = soup.find_all('li', class_='job-criteria__item')

            if len(job_criteria) == 4:
                seniority_list = job_criteria[0].contents
                seniority = seniority_list[1].get_text()
                seniorities.append(seniority)

                employment_list = job_criteria[1].contents
                employment_type = employment_list[1].get_text()
                employment_types.append(employment_type)

                job_function_list = job_criteria[2].contents
                job_function = job_function_list[1].get_text()
                if len(job_function_list) > 2:
                    for i in range(2, len(job_function_list)):
                        job_function = job_function + ', ' + job_function_list[i].get_text()
                job_functions.append(job_function)

                industry_list = job_criteria[3].contents
                industry = industry_list[1].get_text()
                if len(industry_list) > 2:
                    for i in range(2, len(industry_list)):
                        industry = industry + ', ' + industry_list[i].get_text()
                industries.append(industry)
            else:
                seniority_list = job_criteria[0].contents
                seniority = seniority_list[1].get_text()
                seniorities.append(seniority)

                employment_list = job_criteria[1].contents
                employment_type = employment_list[1].get_text()
                employment_types.append(employment_type)

                industry_list = job_criteria[2].contents
                industry = industry_list[1].get_text()
                if len(industry_list) > 2:
                    for i in range(2, len(industry_list)):
                        industry = industry + ', ' + industry_list[i].get_text()
                industries.append(industry)

                job_functions.append('None')

            description = soup.find('div', class_='show-more-less-html__markup')
            desc = description.get_text('\n')
            descriptions.append(desc)
except TimeoutException as err:
    print('Handling time-out-exception error:', err)

dataset = pd.DataFrame([job_titles, company_names, posting_times,
                        number_of_applicants, seniorities, sizes_of_employee,
                        industries, descriptions, employment_types, job_functions]).transpose()
dataset.columns =['Job Title', 'Company Name', 'Job Posting Time', 'Number of Applicants', 
                  'Seniority Level', 'Size of Employee', 'Company Industry', 'Detail Description', 
                  'Employment Type', 'Job Function']
dataset = dataset.drop_duplicates()
dataset.to_csv(r'C:\Users\ekaap\OneDrive\Documents\linkedin-web-scraping-tool-test\venv\linkedin_dataset.csv')

end = time.time()

print(end-start)