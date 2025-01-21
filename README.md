<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
</head>
<body>
<header>
     <img src="https://th.bing.com/th/id/OIG3.f.dxp0XXBWifyj6UVfdK?pid=ImgGn" alt="Web Crawler" style="max-width: 100%; display: block; margin: 0 auto;">
    <h1>Web Crawler and Content Analyzer</h1>
    <h1> DarkWeb Crawler and Content Analyzer</h1>
    <p>This is a web crawler and content analyzer application built with Python. It allows users to input a URL, crawl the website, and analyze various aspects such as keyword occurrences, text sentiment, meta tags, links, images, and more.</p>
</header>

<section id="features">
    <h2>Features</h2>
    <ul>
        <li><strong>Web Crawling:</strong> Crawls the provided URL to extract HTML content, title, meta tags, links, and images.</li>
        <li><strong>Keyword Occurrences:</strong> Counts the occurrences of specified keywords in the HTML content.</li>
        <li><strong>Text Sentiment Analysis:</strong> Analyzes the sentiment (polarity and subjectivity) of the text content using TextBlob.</li>
        <li><strong>Social Media Tags Extraction:</strong> Extracts Open Graph and Twitter Card meta tags for social media sharing.</li>
        <li><strong>Multi-threaded Crawling:</strong> Utilizes ThreadPoolExecutor for concurrent crawling of multiple URLs.</li>
        <li><strong>Flask Web Interface:</strong> Provides a user-friendly web interface for interacting with the application.</li>
    </ul>
</section>

<section id="prerequisites">
    <h2>Prerequisites</h2>
    <ul>
        <li>Python 3.11</li>
        <li>Flask</li>
        <li>Requests</li>
        <li>BeautifulSoup4</li>
        <li>TextBlob</li>
    </ul>
</section>

<section id="installation">
    <h2>Installation</h2>
    <ol>
        <li>Clone the repository:</li>
    </ol>
    <code>
        <pre>
            git clone https://github.com/thisisdakshasoni/dark-web-crawler.git
            cd web-crawler
        </pre>
    </code>
    <ol start="2">
        <li>Install dependencies:</li>
    </ol>
    <code>
        <pre>
            pip install -r requirements.txt
        </pre>
    </code>
</section>

<section id="usage">
    <h2>Usage</h2>
    <ol>
        <li>Run the Flask application:</li>
    </ol>
    <code>python app.py</code>
    <p>Access the application in your web browser at <a href="http://localhost:5511">http://localhost:5511</a>.</p>
    <p>Enter a URL in the provided form and submit to start crawling and analysis.</p>
</section>

<section id="configuration">
    <h2>Configuration</h2>
    <ul>
        <li><strong>TOR Proxy:</strong> The application uses a TOR proxy for anonymous web crawling. Make sure TOR is installed and running on your system, or modify the <code>TOR_PROXY</code> variable in <code>app.py</code> to suit your needs.</li>
        <li><strong>Keywords:</strong> Adjust the <code>KEYWORDS</code> variable in <code>app.py</code> to specify the keywords you want to track.</li>
    </ul>
</section>


<section id="acknowledgments">
    <h2>Acknowledgments</h2>
    <ul>
        <li>This project is inspired by the need for web crawling and content analysis in various applications.</li>
        <li>Special thanks to the developers of Flask, Requests, BeautifulSoup, and TextBlob for their invaluable contributions.</li>
    </ul>
</section>

 <h2>Contact</h2>
    <p>For inquiries and collaborations, you can reach out to me on <a href="https://www.linkedin.com/in/daksha-soni-14052224b/">LinkedIn</a>.</p>
</body>
</html>

# darkwebcrawler
# darkwebcrawler
# darkwebcrawler
# darkwebcrawler
# darkwebcrawler
