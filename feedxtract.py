import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import xml.etree.ElementTree as ET
import threading
import time
import faulthandler
import signal
import os

faulthandler.register(signal.SIGUSR1)

# Global counters
success_count = 0
error_count = 0
feed_count = 0

def log_error(message):
    global error_count
    with open('error_log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(message + '\n')
    error_count += 1

def log_success(message):
    with open('success_log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(message + '\n')

def extract_urls_from_html(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        urls = [a['href'] for a in soup.find_all('a', href=True)]
        return urls
    except Exception as e:
        log_error(f"Error extracting URLs from HTML: {e}")
        return []

def find_rss_feeds(url):
    rss_feeds = []  # Initialize the list
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('link', type='application/rss+xml'):
            rss_feeds.append(urljoin(url, link['href']))
        for link in soup.find_all('link', type='application/atom+xml'):
            rss_feeds.append(urljoin(url, link['href']))
    except requests.RequestException as e:
        log_error(f"Error fetching {url}: {e}")
    except Exception as e:
        log_error(f"Error parsing RSS feeds from {url}: {e}")
    return rss_feeds

def remove_duplicates(feeds):
    seen = set()
    unique_feeds = []
    for feed in feeds:
        if feed['url'] not in seen:
            unique_feeds.append(feed)
            seen.add(feed['url'])
    return unique_feeds

def create_opml(feeds, output_file):
    try:
        feeds = remove_duplicates(feeds)
        opml = ET.Element('opml', version='1.0')
        head = ET.SubElement(opml, 'head')
        title = ET.SubElement(head, 'title')
        title.text = 'RSS Feeds'
        body = ET.SubElement(opml, 'body')

        for feed in feeds:
            outline = ET.SubElement(body, 'outline', type='rss', text=feed['title'], title=feed['title'], xmlUrl=feed['url'])

        tree = ET.ElementTree(opml)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
    except Exception as e:
        log_error(f"Error creating OPML file: {e}")

def ticker():
    while True:
        print(f"\rURLs Processed: {success_count}, Errors: {error_count}, Feeds Identified: {feed_count}", end="")
        time.sleep(1)

def main():
    global success_count, error_count, feed_count

    input_file = 'input.html'
    output_file = 'feeds.opml'

    if not os.path.exists(input_file):
        log_error(f"Input file {input_file} does not exist.")
        return

    # Start the ticker thread
    ticker_thread = threading.Thread(target=ticker)
    ticker_thread.daemon = True
    ticker_thread.start()

    try:
        # Read the HTML content from the input file
        with open(input_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Extract URLs from the HTML content
        urls = extract_urls_from_html(html_content)

        # Find RSS feeds for each URL
        feeds = []
        for url in urls:
            try:
                parsed_url = urlparse(url)
                root_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
                rss_feeds = find_rss_feeds(root_domain)
                for rss_feed in rss_feeds:
                    feeds.append({'title': root_domain, 'url': rss_feed})
                    feed_count += 1
                success_count += 1
                log_success(f"Successfully processed URL {url}")
            except Exception as e:
                log_error(f"Error processing URL {url}: {e}")

        # Create OPML file
        create_opml(feeds, output_file)
        print(f"\nOPML file '{output_file}' created successfully.")
    except Exception as e:
        log_error(f"Error in main function: {e}")

if __name__ == '__main__':
    main()

