SCRAPPER
========

This script is a web scraper and report generator that scrapes web pages and generates a report about the scraped content in HTML, PDF, or CSV format.

Features
--------

*   Scrapes web pages using asynchronous requests for better performance
*   Generates reports in HTML, PDF, or CSV format
*   Extracts internal and external links, images, and HTML tag count
*   Uses a list of user agent headers for scraping
*   Supports concurrent requests

Requirements
------------

*   Python 3.7+
*   aiohttp
*   aiofiles
*   beautifulsoup4
*   WeasyPrint
*   argparse

To install the required libraries, run:

    pip install aiohttp aiofiles beautifulsoup4 WeasyPrint argparse
    

Usage
-----

    python webscraper.py -u <urls> [-hf <headers_file>] [-c <concurrent_requests>] [-o <output_dir>] [-rf <report_format>]
    

Arguments
---------

*   \-u, --urls: List of URLs to scrape (required)
*   \-hf, --headers\_file: File containing user agent headers (default: user\_agents.txt)
*   \-c, --concurrent\_requests: Number of concurrent requests (default: 10)
*   \-o, --output\_dir: Directory to save scraped pages and reports (default: scraped\_pages)
*   \-rf, --report\_format: Format of the report (default: csv). Accepted formats: html, pdf, csv

Example
-------

    python webscraper.py -u https://example.com https://example.org -hf user_agents.txt -c 10 -o scraped_pages -rf html
    

This command will scrape the web pages at https://example.com and https://example.org, save the scraped pages in the scraped\_pages directory, and generate HTML reports for each page.