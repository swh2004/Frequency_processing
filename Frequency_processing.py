import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import defaultdict
from urllib.parse import urljoin
import datetime

# Define the URLs of the finance websites with their names
websites = {
    'Yahoo Finance': 'https://finance.yahoo.com/topic/latest-news/',
    'ETF News': 'https://www.etf.com/news',
    'Stock Analysis': 'https://stockanalysis.com/news/',
    'Trading View': 'https://www.tradingview.com/news/',
}

# Define the keywords you're interested in
keywords = ['Technology', 'AI', 'Cloud', 'Japan', 'US', 'China']

# Initialize a dictionary to hold our results
# Count is for frequency of the words
# News is for frequency of the news
results = defaultdict(lambda: defaultdict(lambda: {'count': 0, 'news': 0}))

# Function to fetch and parse the HTML content of a page
def get_page_content(full_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {full_url}: {str(e)}")
        return None

# Function to process the news content and count keyword frequency
def process_news_content(site_name, content):
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text().lower()
    words = text.split()  # Split the text into words
    words = [word.strip() for word in words]  # Strip whitespace from each word
    for keyword in keywords:
        keyword_lower = keyword.lower()
        # Count occurrences of the keyword in the list of words
        count = sum(1 for word in words if keyword_lower == word)
        if count > 0:
            results[site_name][keyword]['count'] += count
            results[site_name][keyword]['news'] += 1

# Function to filter out non-news links
def is_news_link(link):
    exclude_patterns = ['login', 'signup', 'subscribe', 'about', 'help', 'profile']
    include_patterns = ['news', 'article', str(datetime.datetime.now().year)]
    link = link.lower()
    if any(x in link for x in exclude_patterns):# If is add or something else
        return False
    if any(x in link for x in include_patterns):# If is news or articles for sure
        return True
    return False

# Main loop to process each website
for site_name, website in websites.items():
    response = requests.get(website)
    soup = BeautifulSoup(response.content, 'html.parser')
    base_url = response.url  # Get the base URL of the website

    links = [a['href'] for a in soup.find_all('a', href=True) if a['href'] and is_news_link(a['href'])][:10]

    for link in links:
        full_url = urljoin(base_url, link)
        content = get_page_content(full_url)
        if content:
            process_news_content(site_name, content)

# Prepare the DataFrame
data = []
for keyword in keywords:
    row = [keyword]
    for site_name in websites.keys():
        count = results[site_name][keyword]['count']
        news = results[site_name][keyword]['news']
        row.extend([count, news])
    data.append(row)

column_headers = ['Keywords']
for site_name in websites.keys():
    column_headers.extend([f"{site_name} Count", f"{site_name} News"])

df = pd.DataFrame(data, columns=column_headers)

# Save the results to a CSV file
df.to_csv('frequency.csv', index=False)
