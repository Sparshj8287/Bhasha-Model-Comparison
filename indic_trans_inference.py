import os
from indicnlp.tokenize import sentence_tokenize
import fasttext
import time
from inference.engine import Model
import argparse
from mosestokenizer import MosesSentenceSplitter
from sacrebleu.metrics import BLEU, CHRF
from fairseq import checkpoint_utils, distributed_utils, options, tasks, utils
import logging

os.environ['PYTHONPATH'] += ":/content/fairseq/"

# Initialize the IndicTrans model
indic2en_model = Model(expdir='/content/indicTrans/indic-en')

def perform_language_detection(text):
    try:
        model = fasttext.load_model('Code_files/lid.176.bin')
    except Exception as e:
        print(f"Error loading FastText model: {e}")
        return

    # Predict the language of the input text
    result = model.predict([text])
    return result[0][0][0]

def preprocess_text(input_text, lang_code):
    # Tokenize input text into sentences
    sentences = sentence_tokenize.sentence_split(input_text, lang=str(lang_code))
    return sentences

def predict_indic_translations(input_path):
    # Read input text from file
    with open(input_path, 'r') as f:
        text = f.read()

    # Preprocess the text and detect language
    new_text = text.replace('\n', ' ')
    lang_code = perform_language_detection(new_text)
    sentences = preprocess_text(new_text, lang_code[9:])
    
    # Translate sentences using IndicTrans model
    start = time.time()
    output_indic_trans = indic2en_model.batch_translate(sentences, lang_code[9:], 'en')
    end = time.time()
    
    print(f"Total time taken to translate {len(sentences)} sentences with IndicTrans: {end - start:.2f} seconds")
    return output_indic_trans, lang_code, sentences

def calculate_bleu_and_chrf_scores(output_indic_trans, english_file_path):
    # Initialize BLEU and chrF scorers
    bleu = BLEU()
    chrf = CHRF()

    # Read ground truth English text from file
    with open(english_file_path, 'r') as f:
        text = f.read()
    new_text = text.replace('\n', ' ')
    
    # Tokenize ground truth English text into sentences
    with MosesSentenceSplitter("en") as splitter:
        ground_truth_english = splitter([new_text])
    # Calculate BLEU and chrF scores
    bleu_score_indic_trans = bleu.corpus_score(output_indic_trans, ground_truth_english).score
    chrf_score_indic_trans = chrf.corpus_score(output_indic_trans, ground_truth_english).score

    print(f"Indic Trans BLEU Score: {bleu_score_indic_trans:.2f}")
    print(f"Indic Trans chrF Score: {chrf_score_indic_trans:.2f}")

def main():
    logging.basicConfig(level=logging.INFO)  

    parser = argparse.ArgumentParser(description='Translate Indic text to English using IndicTrans model')
    parser.add_argument('--indic_text_file_path', type=str, required=True, 
                        help='Path to the input Indic text file')
    parser.add_argument('--english_grounded_text_file_path', type=str, required=True, 
                        help='Path to the corresponding English grounded truth text file')
    args = parser.parse_args()

    input_path = args.indic_text_file_path
    english_path = args.english_grounded_text_file_path

    output_indic_trans, lang_code, sentences = predict_indic_translations(input_path)

    print(f"Source sentences in {lang_code[9:]} and their translations to English:\n")
    for src_sen, tgt_sen in zip(sentences, output_indic_trans):
        print(f"{src_sen} -----> {tgt_sen}")

    calculate_bleu_and_chrf_scores(output_indic_trans, english_path)

if __name__ == "__main__":
    main()
