from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrap_books():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
     base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    all_books = []

    for page in range(1, 51):  # 50 páginas
        driver.get(base_url.format(page))
        time.sleep(1)

        books = driver.find_elements(By.CSS_SELECTOR, ".product_pod h3 a")
        book_links = [b.get_attribute("href") for b in books]

        for link in book_links:
            driver.get(link)
            time.sleep(0.5)

            #titulo
            title = driver.find_element(By.TAG_NAME, "h1").text

            #precio
            price = driver.find_element(By.CLASS_NAME, "price_color").text.replace("£", "")
            price = float(price)



 
 
