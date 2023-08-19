import os
import concurrent.futures
from collections import Counter
from indicnlp.tokenize import sentence_tokenize, indic_tokenize
import fasttext
import re
import argparse
from mosestokenizer import MosesSentenceSplitter, MosesTokenizer


class TextProcessor:   
    def __init__(self, cpu_count):
        """Initialize TextProcessor."""

        self.cpu_count = cpu_count

    def perform_language_detection(self, text):
        """Perform language detection using FastText."""

        # Load FastText model 
        try:
            model=fasttext.load_model('lid.176.bin')
        except Exception as e:
            print(f"Error loading FastText model: {e}")
            return

        # Perform language prediction
        result = model.predict([text])
        return result[0][0][0]
    
    def preprocess_text(self, input_text,lang_code):
        """Preprocess the given text by sentence and word tokenization."""
        tokenizer = MosesTokenizer()
        # Sentence tokenization
        if lang_code == 'en':
            with MosesSentenceSplitter("en") as splitter:
                sentences = splitter([input_text])
            words=tokenizer(input_text)
            print("Using Moses Sentence Splitter for sentence tokenization and Moses Tokenizer for word tokenization")
        else:
            print("Using Indic NLP library for sentence tokenization and word tokenization")
            sentences = sentence_tokenize.sentence_split(input_text, lang=str(lang_code))  
            # Word tokenization
            words = indic_tokenize.trivial_tokenize(input_text, lang=str(lang_code))
        return sentences, words
    
    def compute_statistics(self, text_file):
        """Compute and return statistics for the given text file."""

        with open(text_file, 'r') as f:
            text = f.read()

        # Replace new line character
        new_text = text.replace('\n', ' ')
        
        # Perform language detection
        lang_code = self.perform_language_detection(new_text)
        
        # Preprocess the text
        sentences, words = self.preprocess_text(new_text, lang_code[9:])
        # Compute statistics
        sentence_count = len(sentences)
        word_count = len(words)
        unique_word_count = len(set(words))

        # Count word frequency
        word_frequency = Counter(words)

        filename = os.path.basename(text_file).split('.')[0]
        return filename, sentence_count, word_count, unique_word_count, word_frequency.most_common(10)

    def print_statistics(self, results):
        """Print computed statistics."""

        for result in results:
            filename, sentence_count, word_count, unique_word_count, word_frequency = result
            print(f"\nFile: {filename}\n"
                  f"Total Sentences: {sentence_count}\n"
                  f"Total Words: {word_count}\n"
                  f"Unique Words: {unique_word_count}\n")
            print("Top 10 Most Frequent Words:")
            for word, count in word_frequency:
                print(f"{word}: {count}")
    
    def process_files(self, file_path):
        """Process text files in parallel using multiple CPUs."""
        text_files = [file_path] if isinstance(file_path, str) else file_path
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.cpu_count) as executor:
            try:
                # call to executor.map should have list of files
                results = executor.map(self.compute_statistics, text_files) 
            except Exception as e:
                print(f"Error in parallel processing: {e}")
                return
            self.print_statistics(results)



def main():
    parser = argparse.ArgumentParser(description='Process text files using specified number of CPUs.')
    parser.add_argument('--CPU', type=int, required=True, 
                        help='an integer specifying number of CPUs to be used')
    parser.add_argument('--text_file_paths', nargs='+', required=True, help='an string specifying the path to text file')
    
    args = parser.parse_args()
    
    CPU_COUNT = args.CPU  
    PATH=args.text_file_paths


    try:
        tprocessor = TextProcessor(CPU_COUNT)
        tprocessor.process_files(PATH)
    except Exception as e:
        print(f"Error processing text files: {e}")


if __name__ == '__main__':
    main()