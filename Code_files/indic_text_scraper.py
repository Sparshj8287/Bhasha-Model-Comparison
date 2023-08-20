import os
import fasttext
import concurrent.futures
from collections import OrderedDict
import warnings
from web_scraper import get_soup
from collections import Counter


class WebScraper:
    def __init__(self, model_path):
        try:
            self.model = fasttext.load_model(model_path)
        except Exception as e:
            print(f'Error while loading the FastText Model: {e}')
            raise
        self.max_label = ""

    def get_text_predictions(self, line):
        """Predict language of line in a thread-safe manner"""
        try:
            result = self.model.predict([line])
            return result[0][0][0]
        except Exception as e:
            print(f'Error while predicting language: {e}')
            return None


    def get_text(self, target_url):
        """Scrape and return website text"""
        try:
            text = get_soup(target_url).split('\n')[31:]  # We start from the 31th line to skip headers
            return text
        except Exception as e:
            print(f'Error while scraping website: {e}')
            return []

    def process_url(self, target_url):
        """Scrape website, make language predictions for every line and return indic text and English lines"""
        lines = self.get_text(target_url)
        # Using ThreadPoolExecutor for multiprocessing, get predictions for all lines
        with concurrent.futures.ThreadPoolExecutor() as executor:
            language_predictions = list(executor.map(self.get_text_predictions, lines))
        
        label_counts = Counter(language_predictions)  # Count occurences of each label
        sorted_labels = sorted(label_counts.items(), key=lambda x: x[1], reverse=True)  # Sort labels based on counts
        sorted_filtered_labels=[]
        for i in sorted_labels:
            if i[0]!='__label__en':
                sorted_filtered_labels.append(i)
        
        if len(sorted_filtered_labels) >= 2:  # If there are at least two labels
            self.max_label, _ = sorted_filtered_labels[0]  # Get the most common label
            print(f"Website will be scraped in this language: {self.max_label[9:]}")
        
        indic_indices = [i for i, lang in enumerate(language_predictions) if lang == self.max_label]  # Get indices of Indic texts
        indic_text = [lines[i] for i in indic_indices]  # Get indic texts

        return indic_text, self.max_label

    @staticmethod
    def write_to_file(file_path, content):
        """Write specified content into a file at the file_path"""
        try:
            with open(file_path, 'w') as file:
                file.write(content)
        except Exception as e:
            print(f'Error while writing to file: {e}')

    def main(self, urls):
        warnings.filterwarnings("ignore")  # Ignore all warnings
        
        # For each URL, process it (scrape, predict and get texts) and gather results
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(self.process_url, urls))
        
        # Iterate through results to merge extracted indic texts and English lines
        final_indic_text = []
        lang_code = ''
        for _, (indic_text,lang_code) in enumerate(results):
            final_indic_text.extend(indic_text)
            
        final_indic_result = '\n'.join(list(OrderedDict.fromkeys(final_indic_text)))  # Remove duplicates and join sentences
        
        os.makedirs(f'Code_files/text_files', exist_ok=True)  # Create output directory (if it doesn't exist) to store result files

        # Paths for output files
        indic_path = f'Code_files/text_files/{lang_code[9:]}_indic_text.txt'

        # Write the results into corresponding files
        self.write_to_file(indic_path, final_indic_result)
        # self.write_to_file(eng_path, final_eng_result)


if __name__ == '__main__':
    """Only these urls texts are changed for different languages
    Note:- You can manually change the languages of the webpages open by the webdriver.
    """
    URLS = ['https://www.poshantracker.in/',
            'https://www.poshantracker.in/career',
            'https://www.poshantracker.in/termsofservice',
            'https://www.poshantracker.in/privacypolicy', 
            'https://www.poshantracker.in/statistics',
            'https://www.poshantracker.in/resources',
            'https://www.poshantracker.in/support',
            'https://www.poshantracker.in/PTCalculator'
            ]
    
    MODEL_PATH = 'Code_files/lid.176.bin'
    scraper = WebScraper(MODEL_PATH)
    scraper.main(URLS)