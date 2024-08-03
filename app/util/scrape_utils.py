from bs4 import BeautifulSoup
import requests
import fitz
from app.config.config import settings
from urllib.parse import urljoin, urlparse
import time
from app.model.extracted_document import ExtractedDocument
from app.config.config import settings

class ScrapeUtils(): # type: ignore
    
    def __init__(self):
        self.new_paper_urls = []
        self.extracted_urls = set()
        self.load_urls_into_set()
        self.crawl_site_for_pdfs(site_url=settings.BASE_SOURCE_URL)
    
    def load_urls_into_set(self):
        filename = settings.INGESTED_LIST_FILE
        try:
            with open(filename, 'r') as file:
                for line in file:
                    url = line.strip()
                    if url:
                        self.extracted_urls.add(url)
        except FileNotFoundError:
            print(f"The file {filename} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def append_urls_to_file(self, new_urls):
        """
        Appends a list of new URLs to the bottom of the file.

        Args:
        new_urls (list): A list of URLs to append to the file.
        """
        try:
            with open(settings.INGESTED_LIST_FILE, 'a') as file:
                for url in new_urls:
                    file.write(url + '\n')
        except FileNotFoundError:
            print(f"The file {filename} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def crawl_site_for_pdfs(self, site_url, visited=None):
        """
        Crawls a website and all its subpages to find URLs of PDF files.

        Args:
        site_url (str): The URL of the website to crawl.
        visited (set): A set to keep track of visited URLs.

        Returns:
        list: A list of URLs pointing to PDF files on the website and its subpages.
        """
        if visited is None:
            visited = set()
            
        # if site_url[-4] == '.pdf':
        #     if site_url not in self.extracted_urls:
        #         self.new_paper_urls.append(full_url)
        #         self.extracted_urls.add(full_url)
        #     return

        try:
            response = requests.get(site_url)
            response.raise_for_status()  # Check if the request was successful

            soup = BeautifulSoup(response.text, 'html.parser')
            visited.add(site_url)

            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(site_url, href)
                parsed_url = urlparse(full_url)

                if parsed_url.path.lower().endswith('.bib'):
                    continue
                # Skip if the URL is already visited or if it points to a different domain
                if full_url in visited or parsed_url.netloc != urlparse(site_url).netloc:
                    continue

                if parsed_url.path.lower().endswith('.pdf'):
                    if full_url not in self.extracted_urls:
                        self.new_paper_urls.append(full_url)
                        self.extracted_urls.add(full_url)
                    continue
                elif parsed_url.scheme in ('http', 'https') and parsed_url.path.lower().endswith('.html'):
                    time.sleep(0.5)  # Delay to avoid overloading the server
                    self.crawl_site_for_pdfs(full_url, visited)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def extract_text_from_html(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        return soup.get_text()

    def extract_text_from_pdf(self, content):
        # Use PyMuPDF to read and extract text from the PDF content
        pdf_document = fitz.open(stream=content, filetype="pdf")
        text = ''
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text
    
    def extract_text_from_url(self, url):
        # Fetch the document from the URL
        response = requests.get(url)
        
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()

        content_type = response.headers.get('Content-Type')

        if 'text/html' in content_type:
            # If the content is HTML
            return self.extract_text_from_html(response.content)
        elif 'application/pdf' in content_type:
            # If the content is PDF
            return self.extract_text_from_pdf(response.content)
        elif 'text/plain' in content_type:
            # If the content is plain text
            return response.text
        else:
            raise ValueError(f'Unsupported content type: {content_type}')

    def get_docs(self):
        docs = []
        for url in self.new_paper_urls:
            try:
                text = extract_text_from_url(url)
                docs.append(ExtractedDocument(text, url))
                print(text)
            except Exception as e:
                print(f'An error occurred: {e}')
        return docs

    
    