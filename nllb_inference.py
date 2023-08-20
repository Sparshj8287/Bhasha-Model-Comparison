# Import required libraries
from indicnlp.tokenize import sentence_tokenize
import fasttext
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import argparse
import time
from sacrebleu.metrics import BLEU, CHRF
from mosestokenizer import MosesSentenceSplitter
import logging

# Function to perform language detection using FastText
def perform_language_detection(text):
    try:
        model = fasttext.load_model('Code_files/lid.176.bin')
    except Exception as e:
        print(f"Error loading FastText model: {e}")
        return

    # Predict the language of the input text
    result = model.predict([text])
    return result[0][0][0]

# Function to preprocess text by sentence tokenization
def preprocess_text(input_text, lang_code):
    # Tokenize input text into sentences
    sentences = sentence_tokenize.sentence_split(input_text, lang=str(lang_code))
    return sentences

# Function to perform translation using the NLLB model
def prediction_nllb(PATH):
    with open(PATH, 'r') as f:
        text = f.read()

    new_text = text.replace('\n', ' ')
    lang_code = perform_language_detection(new_text)
    sentences = preprocess_text(new_text, lang_code[9:])

    # Load tokenizer and model for NLLB translation
    tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

    start = time.time()
    inputs = tokenizer(sentences, return_tensors="pt", padding=True)

    # Generate translated tokens
    translated_tokens = model.generate(
        **inputs, forced_bos_token_id=tokenizer.lang_code_to_id["eng_Latn"]
    )

    # Decode translated tokens to sentences
    output_nllb = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)
    end = time.time()
    length = len(sentences)
    print(f"The total time of inference of {length} sentences on NLLB model on Tesla T4 GPU:{end - start:.2f}")
    return output_nllb, lang_code, sentences

# Function to calculate BLEU and chrF scores
def calculate_bleu_and_chrf_scores(output_nllb, english_file_path):
    bleu = BLEU()
    chrf = CHRF()

    with open(english_file_path, 'r') as f:
        text = f.read()
    new_text = text.replace('\n', ' ')

    # Split English grounded truth text into sentences
    with MosesSentenceSplitter("en") as splitter:
        ground_truth_english = splitter([new_text])

    # Calculate BLEU and chrF scores
    bleu_score_nllb = bleu.corpus_score(output_nllb, ground_truth_english).score
    chrf_score_nllb = chrf.corpus_score(output_nllb, ground_truth_english).score

    print(f"NLLB BLEU Score: {bleu_score_nllb:.2f}")
    print(f"NLLB chrF Score: {chrf_score_nllb:.2f}")

# Main function
def main():
    logging.basicConfig(level=logging.INFO)  
    parser = argparse.ArgumentParser(description='Translate text to English using NLLB model')
    parser.add_argument('--indic_text_file_path', type=str, required=True, 
                        help='Path to the input text file')
    parser.add_argument('--english_grounded_text_file_path', type=str, required=True, 
                        help='Path to the corresponding English grounded truth text file')
    args = parser.parse_args()

    PATH = args.indic_text_file_path
    ENG_PATH = args.english_grounded_text_file_path

    # Perform translation using NLLB model
    output_nllb, lang_code, sentences = prediction_nllb(PATH)

    print(f"Source sentences in {lang_code[9:]} and their translations to English:\n")
    for src_sen, tgt_sen in zip(sentences, output_nllb):
        print(f"{src_sen} -----> {tgt_sen}")

    # Calculate and display BLEU and chrF scores
    calculate_bleu_and_chrf_scores(output_nllb, ENG_PATH)

if __name__ == "__main__":
    main()
