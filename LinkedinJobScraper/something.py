import os
from os.path import join, dirname

from dotenv import load_dotenv
from job_element import JobElement, update_excel
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

dotenv_path = join(dirname(__file__), 'config.env')
load_dotenv(dotenv_path)
EMAIL = os.environ.get("EMAIL")
PWD = os.environ.get("PWD")
LINKEDIN_JOB_URL = os.environ.get("LINKEDIN_JOB_URL")

# Get our current directory
directory = os.getcwd()

driver = webdriver.Chrome(service=Service(directory + "/chromedriver.exe"))

driver.get(LINKEDIN_JOB_URL)
WebDriverWait(driver, timeout=5)

# Wait for login button to be clickable
login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign in")))
login_button.click()

email = driver.find_element(By.ID, "username")
pwd = driver.find_element(By.ID, "password")
email.send_keys(EMAIL)
pwd.send_keys(PWD)
pwd.send_keys(Keys.ENTER)

job_listings = driver.find_elements(By.CLASS_NAME, "reusable-search__result-container")

jobs = []
job_links = []

try:
    for page in range(2, 20):
        job_listings = driver.find_elements(By.CLASS_NAME, "reusable-search__result-container")
        for job in job_listings:
            links = job.find_elements(By.CSS_SELECTOR, "a.app-aware-link[href]")
            for link in links:
                job_links.append(link.get_attribute("href"))
                jobs.append(job.text.split('\n'))

        try:
            next_button = driver.find_element(By.XPATH, f"//button[@aria-label='Page {page}']")
        except NoSuchElementException:
            break

        next_button.click()
        WebDriverWait(driver, 10)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    print(f"Found {len(jobs)} job listings.")

objects_list = []
for i in range(len(jobs)):
    description, company, location = jobs[i][:3]
    link = job_links[i]
    data = JobElement(description, company, location, link)
    objects_list.append(data)

for i in objects_list:
    print(i.getAsDictionary())

update_excel(objects_list)
print(len(objects_list))
driver.quit()
