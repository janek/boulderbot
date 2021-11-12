from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
service = Service(os.environ.get("CHROMEDRIVER_PATH"))
driver = webdriver.Chrome(options=chrome_options, service=service)

# Now you can start using Selenium
driver.get("https://www.google.com")
print(driver.page_source)
