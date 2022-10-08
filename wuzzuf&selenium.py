from Tools.scripts.serve import app
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

jobs = []
companies = []
address = []
url = []
details = []
description = []
date = []
req = []
page_number = 0
job_number = 1

while True:
    try:

        # get web
        web = webdriver.Chrome()
        web.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_number}")
        web.minimize_window()
        pages_limit = int(web.find_element(By.TAG_NAME, "strong").text)
        if page_number > pages_limit // 15:
            print("pages ended")
            break

        # Get Elements
        job_name = web.find_elements(By.CLASS_NAME, "css-m604qf")
        company_name = web.find_elements(By.CLASS_NAME, "css-17s97q8")
        company_address = web.find_elements(By.CLASS_NAME, "css-5wys0k")
        job_description = web.find_elements(By.CLASS_NAME, "css-y4udm8")
        new_posted = web.find_elements(By.CLASS_NAME, "css-4c4ojb")
        old_posted = web.find_elements(By.CLASS_NAME, "css-do6t5g")

        # Extract data
        for x in range(len(job_name)):
            jobs.append(job_name[x].text)
            url.append("https://wuzzuf.net" + job_name[x].find_element(By.TAG_NAME, "a").get_dom_attribute("href"))
            companies.append(company_name[x].text)
            address.append(company_address[x].text)
            description.append(job_description[x].text.replace("\n", " "))
        page_number += 1
        print(f" page number {page_number}", " switched")
        print(len(url))


    except:
        print("Error")

try:
    # Inner page
    for i in url:
        web.get(i)
        job_details = web.find_element(By.CLASS_NAME, "css-3kx5e2")
        details.append(job_details.text.replace("Job Details", " ").replace("\n", ""))
        job_requirements = web.find_element(By.CLASS_NAME, "css-1t5f0fr")
        req.append(job_requirements.text.replace("\n", ""))
        print(f"job numder {job_number} from {pages_limit}")
        job_number += 1
    print(len(req))
    # Write data
    df = pd.DataFrame(
        {"Job title": jobs, "Company name": companies, "Company address": address, "Job description": description,
         "Job details": details, "Jobrequirements": req, "Links": url})
    df.to_csv('wuzzuf_scraping.csv', index=False)
    print("process done")
except:
    print("error2")
