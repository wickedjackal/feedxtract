# feedxtract
FeedXtract takes your bookmarks manager export file, searches the root domain of all your bookmarks, and extracts the RSS/Atom Feeds from them, providing a .opml file for use in RSS feed readers like Newsboat.

Detailed Explanation
This simple Python script is designed to extract URLs from an HTML file, identify RSS/Atom feeds from those URLs root domain, and then create an OPML (Outline Processor Markup Language) file containing the list of identified feeds. So far, I have only tested this in KDE Neon.

Use Case:
I use Raindrop.io as my bookmarks manager and wanted an easy way to find all the RSS feeds from all my bookmarks and feed them into the Newsboat CLI RSS Reader. So this simple script will comb through the HTML export from Raindrop (or any other bookmarks manager, so long as it's an html file), search the root domain of each URL it finds for available RSS/Atom feeds, and if it finds them, will drop them into an OPML file ready for Newsboat to import. This was mainly meant to get my RSS Reader started easily, rather than having to individually find each RSS Feed from all my bookmarks. This makes it a little bit easier to populate my reader with feeds and then curate afterwards.

Extract URLs from HTML:
extract_urls_from_html(html_content): This function uses BeautifulSoup to parse HTML content and extract all URLs from <a> tags.

Find RSS Feeds:
find_rss_feeds(url): This function takes a URL, sends a GET request to fetch its HTML content, and then uses BeautifulSoup to find RSS or Atom feed links within the <link> tags.

Create OPML:
create_opml(feeds): This function generates an OPML file from a list of feed dictionaries, each containing a title and url.
Main Function:

main(): This function reads HTML content from a file named input.html, extracts URLs using extract_urls_from_html, finds RSS feeds for each URL using find_rss_feeds, and finally creates an OPML file using create_opml.
Dependencies

FeedXtract requires the following dependencies:
requests: For making HTTP requests to fetch web pages.
beautifulsoup4: For parsing HTML content and extracting URLs and RSS feed links.

Installation
Clone the repository using the following command:
git clone https://github.com/WickedJackal/feedxtract.git

You can install the required dependencies using pip and apt.

apt install python3 python3-requests 
pip install requests beautifulsoup4 lxml

Note: lxml is optional but should speed up parsing for BeautifulSoup4


Usage Guide
Prepare the HTML File:
  Option 1 : Create New
  Create an HTML file named input.html in the same directory as FeedXtract. This file should contain the HTML content with   the URLs you want to extract.

  Option 2: Import
  Export an HTML file from your chosen bookmarks manager, rename it input.html, and place it in the same directory as FeedXtract

Run the Script:
Execute the script by running the following command in your terminal:
python feedxtract.py


Check the Output:
After running the script, an OPML file named feeds.opml will be created in the same directory. This file will contain the list of identified RSS/Atom feeds.

Notes
-Ensure the input.html file is correctly formatted (you only need to name the file input.html, anything that isn't a URL in the file will be ignored) and contains valid URLs.
-The script assumes that the root domain of each URL might contain RSS/Atom feeds. This may not always be accurate, so adjust the logic if needed for more specific use cases.
-This script will take a while to run, depending on how bit input.html is and how many bookmarks you have.
-Fetching errors are normal 
-Not every website has an RSS Feed, obviously.
-After importing feeds.opml into Newsboat for the first time, I noticed that no items were actually loaded in the feeds. I hit Shift-R to refresh all, and voila! Everything updated and items became available.


Patch Notes:

V0.4.1 - Revert
Explanation:
Removing command-line arguments functionality because I hate it. Verbose Mode remains.

v0.4.0 - Improvements
Explanation:
A few general Improvements
1. Error Log Increment: Whenever an error is logged into error_log, it will increment the error count.
2. Error Handling for File Operation: Added checks to ensure the input file exists
3. Logging Successes: Added a log_success function to log successful operations
4. Command-Line Arguments: Added command-line arguments for input and output file paths using argparse.
5. Verbose Mode: You can add a verbose mode if needed by extending the argparse options and adding conditional print statements.


v0.3.0 - Scrape All Feeds
Explanation:
Ensures that all available RSS/Atom feeds on a domain will be appended to the OPML file and removes any duplicates before finalizing the file.
1. Finding All RSS/AtomFeeds: The find_rss_feeds function now ensures that all RSS and Atom feeds on a domain are captrued by using urljoin to handle relative URLs.
2. Removing Duplicates: The remove_duplicates function removes exact duplicate feeds based on their URLs.
3. Integrating Duplicate Removal: The create_opml function calls remove_duplicates before writing the feeds to the OPML file.
4. Added a progress ticker to show the amount of sites parsed, the amount of feeds found, and the amount of errors encountered. Though the error count doesn't seem to increment, probably because it skips over them instead.

First successful test

v0.2.0 - Error Handling
Explanation:
Any errors encountered will be appended to an error_log.txt file and the script will continue to run even if some URLs cause errors, and all errors encountered will be logged into error_log.txt
1. log_error function: This function appends error messages to error_log.txt
2. Try-Except Blocks: Added try-except blocks in each function to catch and log errors.
3. Main Function: Wrapped the main logic in a try-except block to catch any unhandled exceptions
4. Error Handling in URL Processing: The try-except block inside the loop in the main function ensures that if an error occurs while processing a specific URL, it logs the error and continues with the next URL.
