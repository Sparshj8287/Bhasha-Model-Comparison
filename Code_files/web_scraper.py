from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import argparse
import time
import locale
import os
from trafilatura import bare_extraction

# Modified getpreferredencoding function to always return UTF-8


def getpreferredencoding(do_setlocale=True):
    """Returns the preferred encoding - set to 'UTF-8' for this script."""
    return "UTF-8"


def get_soup(target_url):
    """Returns the formatted text from the HTML contents of the target URL."""

    # Override the default locale.getpreferredencoding method
    locale.getpreferredencoding = getpreferredencoding
    link_list = []

    try:
        # Initialize the driver and load the webpage
        options = Options()
        options.add_argument("log-level=3")
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(target_url)
        driver.maximize_window()

        # Wait for elements to load
        driver.implicitly_wait(220)
        # Fetch the page source and parse it with BeautifulSoup
        # Use can reduce the timer for faster scraping of the website
        time.sleep(5)
        resp = driver.page_source
        # iterate over the elements
        pdf_link_found = False
        count=[]
        soup = BeautifulSoup(resp, 'lxml')

        # Get formatted text by separating elements with a newline character
        formatted_text = soup.get_text(separator='\n')
        formatted_text = "\n".join(
            line.strip() for line in formatted_text.splitlines() if line.strip())
        

        text_dict = bare_extraction(resp)
        trafil_text=text_dict['text']
        # print(trafil_text)

        links_second_method = driver.find_elements(By.TAG_NAME, 'a')
        for link in links_second_method:
            href = link.get_attribute('href')
            if href is not None and href != '' and not href.startswith(('javascript:', 'tel:', 'mailto:', 'ftp:', 'irc:', 'news:', 'data:')) and not href.endswith(('main-content')):
                if href.endswith('.pdf'): # check if the url ends with .pdf
                    pdf_link_found = True
                    break

                if pdf_link_found:
                    count.append(1)
                else:
                    count.append(0)

                link_list.append(href)
        link_list = list(set(link_list))
        if 1 in count:
            print("PDF link found")
        else:
            print("PDF link not found")
        # print(trafil_text)
        return trafil_text,link_list

    except WebDriverException as e:
        print(f"An error occurred while interacting with WebDriver: {e}")
    except TimeoutException as e:
        print(f"Timeout occurred: {e}")
    except ConnectionRefusedError:
        print("The connection was refused by the server.")
    except NoSuchWindowException:
        print("Attempted to interact with a window that does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        # Regardless of exception, always close the driver
        driver.close()



def write_to_file(formatted_text, links, output_file, links_output_file):
    """Writes the formatted text to the output file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(formatted_text)
    with open(links_output_file, 'w', encoding='utf-8') as f:
        f.write(links)


def main():
    """Note:- You can scraped any dynamic website using this code. You can change manually in the web driver and scrape the website according to your need."""
    parser = argparse.ArgumentParser(
        description='Translate Indic text to English using IndicTrans model')
    parser.add_argument('--url', type=str, required=True,
                        help='Path to the input Indic text file')
    args = parser.parse_args()

    target_url = args.url
    formatted_text, links = get_soup(target_url)
    print(formatted_text)
    # print(links)
    link_text = '\n'.join(i for i in links)
    print(link_text)
    # Create output directory (if it doesn't exist) to store result files
    os.makedirs(f'Code_files/web_scraper_text', exist_ok=True)

    # Paths for output files
    PATH = f'Code_files/web_scraper_text/website_text.txt'
    LINKS = f'Code_files/web_scraper_text/links.txt'
    # Write the results into corresponding files
    write_to_file(formatted_text, link_text, PATH, LINKS)


if __name__ == '__main__':
    main()
