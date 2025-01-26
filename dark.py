from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from textblob import TextBlob
import ibm_db

app = Flask(__name__)

TOR_PROXY = {"http": "socks5h://localhost:9050", "https": "socks5h://127.0.0.1:9050"}


# IBM Watson NLU URL and API Key
url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/3fb1ae40-a0d1-471c-b276-529079543d07"
api_key = "0bOh_-bbt8DimU2Em7ccfVaKcsQUPpkmzGsv2SDYud-g"


DB2_DATABASE = "bludb"
DB2_HOSTNAME = "21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud"
DB2_PORT = "31864"
DB2_UID = "mvg73722"
DB2_PWD = "fELvh99ikevEUAk3"
DB2_PROTOCOL = "TCPIP"
DB2_DRIVER = "IBM DB2 ODBC DRIVER"
DB2_SECURITY = "SSL"


clientId = "cc1146fc-d1d5-43bc-9aa0-898c84707582"
tenantId = "37e46843-2380-412b-864d-d0ca533d3e8c"
secret = "NjUxMGJlNDQtYWQzNy00N2ZlLWI1NzItZDEyMjg0NmVkN2Y4"
oAuthServerUrl = (
    "https://au-syd.appid.cloud.ibm.com/oauth/v4/37e46843-2380-412b-864d-d0ca533d3e8c"
)
profilesUrl = "https://au-syd.appid.cloud.ibm.com"
discoveryEndpoint = "https://au-syd.appid.cloud.ibm.com/oauth/v4/37e46843-2380-412b-864d-d0ca533d3e8c/.well-known/openid-configuration"


DB2_CONN_STR = (
    f"DATABASE={DB2_DATABASE};"
    f"HOSTNAME={DB2_HOSTNAME};"
    f"PORT={DB2_PORT};"
    f"PROTOCOL=TCPIP;"
    f"UID={DB2_UID};"
    f"PWD={DB2_PWD};"
)

dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};"
).format(
    DB2_DRIVER,
    DB2_DATABASE,
    DB2_HOSTNAME,
    DB2_PORT,
    DB2_PROTOCOL,
    DB2_UID,
    DB2_PWD,
    DB2_SECURITY,
)

try:
    conn = ibm_db.connect(dsn, "", "")
    print(
        "Connected to database: ",
        DB2_DATABASE,
        "as user: ",
        DB2_UID,
        "on host: ",
        DB2_HOSTNAME,
    )

except:
    print("Unable to connect: ", ibm_db.conn_errormsg())


def count_keyword_occurrences(html_content, keyword):
    return html_content.lower().count(keyword.lower())


def perform_web_crawl(url, keyword):
    start_time = datetime.now()
    results = []
    html, title, text_content = "", "", ""
    meta_tags, links, images, social_media_tags = [], [], [], {}

    try:
        res = requests.get(url=url, proxies=TOR_PROXY)

        if res.status_code == 200:
            html = res.content.decode()
            soup = BeautifulSoup(html, "html.parser")

            title_tag = soup.find("title")
            title = title_tag.text if title_tag else "Title not found"

            meta_tags = soup.find_all("meta")
            links = [link.get("href") for link in soup.find_all("a", href=True)]
            images = [img["src"] for img in soup.find_all("img", src=True)]
            text_content = soup.get_text()

            if keyword.lower() in html.lower():
                results.append(f'"{keyword}" found in {url}.')

            for tag in meta_tags:
                if "property" in tag.attrs and "content" in tag.attrs:
                    if tag.attrs["property"].startswith("og:") or tag.attrs[
                        "property"
                    ].startswith("twitter:"):
                        social_media_tags[tag.attrs["property"]] = tag.attrs["content"]
        else:
            print(f"Error {res.status_code} for {url}")

    except requests.exceptions.RequestException as e:
        print(f"Error crawling {url}: {e}")

    end_time = datetime.now()
    duration = end_time - start_time

    keyword_count = count_keyword_occurrences(html, keyword)
    sentiment = TextBlob(text_content).sentiment

    return {
        "url": url,
        "title": title,
        "keyword_count": keyword_count,
        "links": links,
        "images": images,
        "duration": str(duration),
        "polarity": sentiment.polarity,
        "subjectivity": sentiment.subjectivity,
        "social_media_tags": social_media_tags,
    }


def store_in_db2(data):
    try:
        conn = ibm_db.connect(dsn, "", "")
        sql = """
        INSERT INTO WEB_CRAWL_DATA (
            URL, TITLE, KEYWORD_COUNT, LINKS, IMAGES, DURATION, POLARITY, SUBJECTIVITY, SOCIAL_MEDIA_TAGS
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, data["url"])
        ibm_db.bind_param(stmt, 2, data["title"])
        ibm_db.bind_param(stmt, 3, data["keyword_count"])
        ibm_db.bind_param(stmt, 4, str(data["links"]))
        ibm_db.bind_param(stmt, 5, str(data["images"]))
        ibm_db.bind_param(stmt, 6, data["duration"])
        ibm_db.bind_param(stmt, 7, data["polarity"])
        ibm_db.bind_param(stmt, 8, data["subjectivity"])
        ibm_db.bind_param(stmt, 9, str(data["social_media_tags"]))
        ibm_db.execute(stmt)
        ibm_db.close(conn)
        print(f"Data stored in Db2 for URL: {data['url']}")
    except Exception as e:
        print(f"Error storing data in Db2: {e}")


def search_ahmia(keyword):
    search_url = f"https://ahmia.fi/search/?q={keyword}"
    try:
        links = []
        res = requests.get(search_url, proxies=TOR_PROXY)
        soup = BeautifulSoup(res.text, "html.parser")
        for anchor in soup.find_all("a", href=True):
            links.append(anchor["href"])
        return [
            link.get("href")
            for link in soup.find_all("a", href=True)
            if link["href"].startswith("http")
        ]
    except requests.exceptions.RequestException as e:
        print(f"Ahmia search failed: {e}")
        return []


@app.route("/", methods=["GET", "POST"])
def index():
    crawled_data = []
    keyword = ""

    if request.method == "POST":
        keyword = request.form["keyword"]
        urls = search_ahmia(keyword)

        with ThreadPoolExecutor(max_workers=5) as executor:
            crawled_data = list(
                executor.map(lambda url: perform_web_crawl(url, keyword), urls)
            )

        for data in crawled_data:
            store_in_db2(data)

    return render_template(
        "newdash.html",
        crawled_data=crawled_data,
        keyword=keyword,
    )


if __name__ == "__main__":

    app.secret_key = (
        "super secret key Super jhbvfjhbkvbfduyvgueyrlybvuyrbyubverbuyuyybveiunvuibveb"
    )
    app.run(debug=True, port=5510)
