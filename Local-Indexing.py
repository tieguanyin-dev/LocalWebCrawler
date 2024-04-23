import requests  # Import the requests library for making HTTP requests
from bs4 import BeautifulSoup  # Import BeautifulSoup for HTML parsing
from urllib.parse import urlparse, urljoin  # Import urlparse and urljoin for URL manipulation
import certifi  # Import certifi for SSL certificate handling
import warnings  # Import warnings module to suppress warnings
import urllib3  # Import urllib3 for HTTP connection pooling
from urllib3.exceptions import InsecureRequestWarning  # Import InsecureRequestWarning for SSL warnings suppression

def crawl_website(url):
    visited_urls = set()  # Initialize a set to store visited URLs
    queue = [url]  # Initialize a queue with the starting URL
    
    while queue:
        current_url = queue.pop(0)  # Get the next URL from the queue
        if current_url in visited_urls:
            continue  # Skip if URL has already been visited
        
        try:            
            # Suppress InsecureRequestWarning
            urllib3.disable_warnings(InsecureRequestWarning)
            # Send a GET request to the current URL and retrieve the response
            response = requests.get(current_url, verify=False)

            if response.status_code == 200:  # If the response is successful
                visited_urls.add(current_url)  # Add the URL to the set of visited URLs
                soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content of the response
                for link in soup.find_all('a', href=True):  # Find all <a> elements with href attribute
                    next_url = urljoin(current_url, link['href'])  # Construct the absolute URL of the next page
                    if is_internal_url(url, next_url):  # Check if the next URL is internal
                        queue.append(next_url)  # Add the next URL to the queue for crawling
        except Exception as e:
            print(f"Error crawling {current_url}: {str(e)}")  # Print error message if crawling fails

    return visited_urls  # Return the set of visited URLs

def is_internal_url(base_url, url):
    base_domain = urlparse(base_url).netloc  # Extract the domain from the base URL
    next_domain = urlparse(url).netloc  # Extract the domain from the next URL
    return base_domain == next_domain  # Check if both URLs have the same domain

if __name__ == "__main__":
    # Prompt the user to insert a URL
    website_url = input("Please enter the URL: ")
    # Call the crawl_website function with the provided URL
    discovered_urls = crawl_website(website_url)
    # Print all discovered URLs
    for url in discovered_urls:
        print(url)
