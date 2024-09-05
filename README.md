# Scrappers

A collection of web scraping tools for processing and analyzing data from web pages. This repository contains two main scripts:

## Scripts

### 1. OLX Page Scraper with GUI

- **Description**: This script downloads multiple pages from OLX, extracts offer URLs, and opens them in the Brave browser based on a keyword entered by the user.
- **Technologies**: Python, BeautifulSoup, Requests, Tkinter, Threading, WebBrowser
- **Usage**:
  - Run the script to launch a GUI application.
  - Enter a keyword and click "Search" to start the process.

### 2. Advanced Web Scraper with Cloudflare Bypass

- **Description**: This script scrapes links from a webpage while handling Cloudflare protection. It also filters and processes the scraped links based on a given pattern.
- **Technologies**: Python, Selenium, Undetected ChromeDriver, Tkinter
- **Usage**:
  - Run the script to launch a GUI application.
  - Provide the URL to scrape, the link pattern to filter, and the output file location.
  - Click "Start" to begin scraping and processing.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/Scrappers.git
   cd Scrappers

2. Install the required packages:
   ```sh
   pip install requests beautifulsoup4 selenium undetected-chromedriver

3. Ensure you have Brave Browser installed at the default path.

## Dependencies
  - requests
  - beautifulsoup4
  - selenium
  - undetected-chromedriver
  - tkinter (typically included with Python)
