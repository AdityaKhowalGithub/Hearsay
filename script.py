

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def summarize_html(html_content, headers):
    """
    Send the HTML content to the LLM to summarize.
    """
    data = {'inputs': html_content}
    response = requests.post(base_url + '/summarize', json=data, headers=headers)  # Corrected endpoint
    print("API Response:", response.json())  # Debug output to see what the API returns
    if response.status_code == 200:
        try:
            return response.json()['summary']  # Assuming 'summary' is the correct key
        except KeyError:
            return "No 'summary' key found in the response"
    else:
        return "Error summarizing HTML, status code: " + str(response.status_code)

def describe_website(summary, headers):
    """
    Get a user-friendly description of the website and follow-up navigation questions.
    """
    data = {'inputs': summary}
    response = requests.post(base_url + '/describe', json=data, headers=headers)  # Corrected endpoint
    if response.status_code == 200:
        return response.json()
    else:
        return "Error getting website description."

# Selenium setup
chromedriver_path = '/Users/adityakhowal/Downloads/chromedriver-mac-arm64/chromedriver'
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)
base_url = "http://localhost:1234/v1"
api_key = "lm-studio"
headers = {'Authorization': 'Bearer ' + api_key}  # Define headers here to use across functions

# Open the target website
driver.get("https://swecc.org/")
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    html_content = driver.page_source

    # Process the HTML content through the LLM
    summary = summarize_html(html_content, headers)
    description = describe_website(summary, headers)
    print(description)

finally:
    driver.quit()

