from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from journals import journals
import pandas as pd
import time
import re

import os
from huggingface_hub import login
from datasets import Dataset


def scrape_journal(journal_name, journal_url):

    chrome_service = Service(ChromeDriverManager(driver_version="128.0.6613.0", chrome_type=ChromeType.CHROMIUM).install())

    chrome_options = Options()
    options = [
        "--headless",
        "--disable-gpu",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]
    for option in options:
        chrome_options.add_argument(option)

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    driver.get(journal_url)
    articles = []

    current_link = None
    links = driver.find_elements(By.TAG_NAME, 'a')
    for link in links:
        current_link = link.get_attribute('href')
        if current_link and 'issue/current' in current_link:
            print(f"Current Issue link found for {journal_name}: {current_link}")
            break

    if current_link:
        driver.get(current_link)
        time.sleep(2)  # Wait for page to load

        article_links = driver.find_elements(By.TAG_NAME, 'a')
        print(f"Scraping Current Issue articles for {journal_name}")
        for article in article_links:
            text = article.text.lower()
            if any([
                "download" in text,
                "pdf" in text,
                "link" in text,
                text.isdigit(),
                re.search(r'\d+\.\d+', article.text.strip())  # Skip DOI-like patterns
            ]):
                continue

            article_url = article.get_attribute('href')
            article_name = article.text.strip()
            if article_url and article_name and 'article/view' in article_url:
                articles.append({
                    'journal_name': journal_name,
                    'article_name': article_name,
                    'article_url': article_url
                })
    else:
        print(f"No Current Issue link found for {journal_name}")

    driver.quit()
    return articles
    
all_articles = []

for journal_name, journal_url in journals.items():
    print(f"\nScraping journal: {journal_name}")
    articles = scrape_journal(journal_name, journal_url)
    all_articles.extend(articles)

df = pd.DataFrame(all_articles)

hf_dataset = Dataset.from_pandas(df)

hf_token = os.getenv("HF_TOKEN")
login(hf_token)

repo_name = "damand2061/id_cs_journal_articles"
hf_dataset.push_to_hub(repo_name, private=True)