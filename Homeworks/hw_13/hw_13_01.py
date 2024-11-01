"""
Парсинг новинного сайту для отримання останніх новин.

Вам потрібно створити Python-скрипт, який буде парсити головну сторінку новинного сайту
та збирати інформацію про останні новини. Ваш скрипт повинен отримувати заголовки новин,
посилання на повний текст новини, дату публікації та короткий опис (якщо він присутній на сторінці).
"""

import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


# ---- Function to Initialize WebDriver and Fetch Web Page ----
def get_page(url):
    """
    Retrieve and parse HTML content from a specified URL using Selenium and BeautifulSoup.

    :param url: URL of the webpage to scrape.
    :type url: str
    :return: Parsed HTML content of the page.
    :rtype: BeautifulSoup object
    :raises Exception: If there is an issue initializing WebDriver or fetching the page.
    """
    options = Options()
    options.headless = True

    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        raise

    try:
        print(f"Navigating to {url}")
        driver.get(url)
        time.sleep(5)  # Wait for JavaScript to load content
        html = driver.page_source
    except Exception as e:
        print(f"Error fetching page: {e}")
        driver.quit()
        raise

    driver.quit()
    soup = BeautifulSoup(html, 'lxml')
    return soup


# ---- Function to Parse News Articles ----
def parse_news(soup):
    """
    Extract news articles' details from HTML content.

    :param soup: Parsed HTML content of the page.
    :type soup: BeautifulSoup object
    :return: List of dictionaries containing news article data.
    :rtype: list of dict
    """
    articles = soup.find_all('li', class_='css-18yolpw')
    news = []

    if not articles:
        print("No articles found on the page.")

    for idx, article in enumerate(articles, start=1):
        extraction = {}

        # Extract title
        title_tag = article.find('h3')
        if title_tag:
            extraction['title'] = title_tag.get_text(strip=True)
        else:
            extraction['title'] = None
            print(f"Article {idx}: Title not found.")

        # Extract link
        link_tag = article.find('a')
        if link_tag and link_tag.get('href'):
            link = link_tag.get('href')
            if link.startswith('/'):
                link = 'https://www.nytimes.com' + link
            extraction['link'] = link
        else:
            extraction['link'] = None
            print(f"Article {idx}: Link not found.")

        # Extract publication date
        date_tag = article.find('span', attrs={'data-testid': 'todays-date'})
        if date_tag and date_tag.get_text(strip=True):
            extraction['date'] = date_tag.get_text(strip=True)
        else:
            extraction['date'] = None
            print(f"Article {idx}: Date not found.")

        # Extract summary/content
        summary_tag = article.find('p')
        if summary_tag:
            extraction['summary'] = summary_tag.get_text(strip=True)
        else:
            extraction['summary'] = None
            print(f"Article {idx}: Summary not found.")

        news.append(extraction)
    return news


# ---- Function to Save Parsed Data to CSV ----
def save_to_csv(news, filename="news.csv"):
    """
    Save list of news articles to a CSV file.

    :param news: List of dictionaries containing news article data.
    :type news: list of dict
    :param filename: Name of the CSV file to save data.
    :type filename: str
    :raises Exception: If there is an issue writing to the CSV file.
    """
    if not news:
        print("No data to save.")
        return

    fieldnames = news[0].keys()

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(news)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Failed to save data to CSV: {e}")


# ---- Main Program Execution ----
if __name__ == "__main__":
    url = 'https://www.nytimes.com/section/business?page=10'
    try:
        soup = get_page(url)
        news_items = parse_news(soup)
        # print(json.dumps(news_items, ensure_ascii=False, indent=4))
        save_to_csv(news_items)
    except Exception as e:
        print(str(e))
