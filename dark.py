from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from textblob import TextBlob

app = Flask(__name__)

TOR_PROXY = {"http": "socks5h://localhost:9050", "https": "socks5h://127.0.0.1:9050"}


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


def search_ahmia(keyword):
    search_url = f"https://ahmia.fi/search/?q={keyword}"
    try:
        links = []
        res = requests.get(search_url, proxies=TOR_PROXY)
        soup = BeautifulSoup(res.text, "html.parser")
        for anchor in soup.find_all("a", href=True):
            links.append(anchor["href"])
        print("The second rs is", links)
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
    if session.get("username") == False or session.get("username") == None:
        print(session)
        return redirect("/login")
    else:
        crawled_data = []
        keyword = ""

        if request.method == "POST":
            keyword = request.form["keyword"]
            urls = search_ahmia(keyword)

            with ThreadPoolExecutor(max_workers=5) as executor:
                crawled_data = list(
                    executor.map(lambda url: perform_web_crawl(url, keyword), urls)
                )

        return render_template(
            "newdash.html",
            crawled_data=crawled_data,
            keyword=keyword,
            username=session.get("username"),
        )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        therealusername = "gyanranjan"
        therealpassword = "gyanranjan"
        username = request.form["username"].lower()
        password = request.form["password"].lower()
        if username == therealusername and password == therealpassword:
            print(username, password)
            session["username"] = username
            flash("Login successful!")
            return redirect("/")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


if __name__ == "__main__":

    app.secret_key = "super secret key Super Nigga 69 jhbvfjhbkvbfduyvgueyrlybvuyrbyubverbuyuyybveiunvuibveb"
    app.run(debug=True, port=5510)
