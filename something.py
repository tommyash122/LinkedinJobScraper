from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
import os
from os.path import join, dirname
from datetime import date
from job_element import JobElement,update_excel

dotenv_path = join(dirname(__file__), 'config.env')
load_dotenv(dotenv_path)
EMAIL = os.environ.get("EMAIL")
PWD = os.environ.get("PWD")
LINKEDIN_JOB_URL = os.environ.get("LINKEDIN_JOB_URL")

driver = webdriver.Chrome(executable_path=r"C:\Users\dankv\Desktop\resumeAutomation/chromedriver.exe")

driver.get(LINKEDIN_JOB_URL)
WebDriverWait(driver , 5)
driver.find_element_by_link_text("Sign in").click()

WebDriverWait(driver , 30)

email = driver.find_element_by_id("username")
pwd = driver.find_element_by_id("password")
email.send_keys(EMAIL)
pwd.send_keys(PWD)
pwd.send_keys(Keys.ENTER)

job_listings = driver.find_elements_by_class_name("reusable-search__result-container")

jobs = []
job_links = []

try:
    for page in range(2,20):
        job_listings = driver.find_elements_by_class_name("reusable-search__result-container")
        for job in job_listings:
            links = job.find_elements_by_css_selector("a.app-aware-link[href]")
            for link in links:
                job_links.append(link.get_attribute("href"))
                jobs.append(job.text.split('\n'))

        try:
            next_button = driver.find_element_by_xpath(f"//button[@aria-label='Page {page}']")
        except NoSuchElementException:
            break

        next_button.click()
        WebDriverWait(driver,10)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    print(f"Found {len(jobs)} job listings.")
        
objects_list = []
for i in range(len(jobs)):
    description, company, location = jobs[i][:3]
    link = job_links[i]
    data = JobElement(description,company,location,link)
    objects_list.append(data)
    
for i in objects_list:
    print(i.getAsDictionary())

update_excel(objects_list)
print(len(objects_list))
driver.quit()