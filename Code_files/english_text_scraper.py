from indic_text_scraper import WebScraper
import concurrent.futures
from collections import OrderedDict
from collections import Counter

class EnglishTextScraper(WebScraper):
    def english_text_batch(self, target_url, index):
        """Retrieve batch of English text by scraping"""
        try:
            # Extract website text and retrieve lines at the indices specified

            lines = self.get_text(target_url)
            return [lines[i] for i in index]
        except Exception as e:
            print(f'Error while retrieving English text: {e}')
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
            english_lines = self.english_text_batch(target_url, indic_indices)  # Get corresponding English lines

            return  english_lines



    def main(self, urls):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results  = list(executor.map(self.process_url, urls))
        final_english_text = []
        for _, english_text in enumerate(results):
            final_english_text.extend(english_text)
        final_eng_result = '\n'.join(list(OrderedDict.fromkeys(final_english_text)))

        # Paths for output files
        eng_path = f'text_files/ground_truth_text.txt'
        self.write_to_file(eng_path, final_eng_result)

    # Main function remains similar to the one in indic_text.py

if __name__ == '__main__':
    URLS = ['https://www.poshantracker.in/',
            'https://www.poshantracker.in/career',
            'https://www.poshantracker.in/termsofservice',
            'https://www.poshantracker.in/privacypolicy',
            'https://www.poshantracker.in/statistics',
            'https://www.poshantracker.in/resources', 
            'https://www.poshantracker.in/support',
            'https://www.poshantracker.in/PTCalculator'
            ]
    
    MODEL_PATH = 'lid.176.bin'
    scraper = EnglishTextScraper(MODEL_PATH)
    scraper.main(URLS)
