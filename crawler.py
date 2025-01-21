from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from textblob import TextBlob  # Import TextBlob for text content analysis

app = Flask(__name__)

TOR_PROXY = {'http': 'socks5h://localhost:9150', 'https': 'socks5h://127.0.0.1:9150'}

KEYWORDS = {'market'} # Add Keywords According to your needs

def count_keyword_occurrences(html_content):
    keyword_occurrences = {keyword: 0 for keyword in KEYWORDS}

    for keyword in KEYWORDS:
        keyword_occurrences[keyword] = html_content.lower().count(keyword)

    return keyword_occurrences

def perform_web_crawl(url):
    start_time = datetime.now()
    
    results = []
    html = ""
    title = ""
    meta_tags = []
    links = []
    images = []
    text_content = ""
    social_media_tags = {}

    try:
        res = requests.get(url=url, proxies=TOR_PROXY)

        if res.status_code == 200:
            html = res.content.decode()

            # Extract title
            soup = BeautifulSoup(html, 'html.parser')
            title_tag = soup.find('title')
            title = title_tag.text if title_tag else 'Title not found'

            # Extract meta tags
            meta_tags = soup.find_all('meta')

            # Extract links
            links = [link.get('href') for link in soup.find_all('a', href=True)]

            # Extract images
            images = [img['src'] for img in soup.find_all('img', src=True)]

            # Extract text content
            text_content = soup.get_text()

            for keyword in KEYWORDS:
                if keyword in html.lower():
                    results.append(f'"{keyword}" found in {url}.')

            # Extract Social Media Tags (Open Graph and Twitter Card)
            for tag in meta_tags:
                if 'property' in tag.attrs and 'content' in tag.attrs:
                    if tag.attrs['property'].startswith('og:') or tag.attrs['property'].startswith('twitter:'):
                        social_media_tags[tag.attrs['property']] = tag.attrs['content']

        else:
            print(f'Something went wrong for {url} with status code: {res.status_code}.')

    except requests.exceptions.RequestException as e:
        print(f"An error occurred for {url}: {e}")

    except Exception as e:
        print(f"An unexpected error occurred for {url}: {e}")

    end_time = datetime.now()
    duration = end_time - start_time

    keyword_occurrences = count_keyword_occurrences(html)

    # Perform text content analysis
    blob = TextBlob(text_content)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    # Convert dict_keys and dict_values to lists
    keyword_occurrence_keys = list(keyword_occurrences.keys())
    keyword_occurrence_values = list(keyword_occurrences.values())

    return results, html, title, meta_tags, links, images, text_content, social_media_tags, duration, \
           keyword_occurrence_keys, keyword_occurrence_values, polarity, subjectivity

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    html_content = ""
    title = ""
    meta_tags = []
    links = []
    images = []
    text_content = ""
    social_media_tags = {}
    duration = ""
    keyword_occurrence_keys = []
    keyword_occurrence_values = []
    polarity = 0.0
    subjectivity = 0.0

    if request.method == 'POST':
        user_input_url = request.form['user_input_url']
        with ThreadPoolExecutor(max_workers=5) as executor:
            crawl_result = list(executor.map(perform_web_crawl, [user_input_url]))

        results.extend(crawl_result[0][0])
        html_content = crawl_result[0][1]
        title = crawl_result[0][2]
        meta_tags = crawl_result[0][3]
        links = crawl_result[0][4]
        images = crawl_result[0][5]
        text_content = crawl_result[0][6]
        social_media_tags = crawl_result[0][7]
        duration = crawl_result[0][8]
        keyword_occurrence_keys = crawl_result[0][9]
        keyword_occurrence_values = crawl_result[0][10]
        polarity = crawl_result[0][11]
        subjectivity = crawl_result[0][12]

    return render_template('dashboard.html', results=results, html_content=html_content,
                           title=title, meta_tags=meta_tags, links=links, images=images,
                           text_content=text_content, social_media_tags=social_media_tags,
                           duration=duration, keyword_occurrence_keys=keyword_occurrence_keys,
                           keyword_occurrence_values=keyword_occurrence_values,
                           polarity=polarity, subjectivity=subjectivity)

if __name__ == '__main__':
    app.run(debug=True, port=5511)