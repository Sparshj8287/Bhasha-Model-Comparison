from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException,NoSuchWindowException
from selenium.webdriver.chrome.options import Options
import argparse
import time
import locale

# Modified getpreferredencoding function to always return UTF-8
def getpreferredencoding(do_setlocale = True):
    """Returns the preferred encoding - set to 'UTF-8' for this script."""
    return "UTF-8"

def get_soup(target_url):
    """Returns the formatted text from the HTML contents of the target URL."""
    
    # Override the default locale.getpreferredencoding method
    locale.getpreferredencoding = getpreferredencoding

    try:
        # Initialize the driver and load the webpage
        options = Options()
        options.add_argument("log-level=3")
        driver = webdriver.Chrome(options=options)
        driver.get(target_url)
        driver.maximize_window()

        # Wait for elements to load
        driver.implicitly_wait(220)
        # Fetch the page source and parse it with BeautifulSoup
        time.sleep(60)
        resp = driver.page_source
        soup = BeautifulSoup(resp, 'lxml')

        # Get formatted text by separating elements with a newline character
        formatted_text = soup.get_text(separator='\n')

        return formatted_text

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

    return None

def main():
    parser = argparse.ArgumentParser(description='Translate Indic text to English using IndicTrans model')
    parser.add_argument('--url', type=str, required=True, 
                        help='Path to the input Indic text file')
    args = parser.parse_args()

    target_url = args.url
    formatted_text = get_soup(target_url)
    print(formatted_text)
    return formatted_text


if __name__ == '__main__':
    main()

