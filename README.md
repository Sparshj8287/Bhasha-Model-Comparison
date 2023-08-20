# <center>Bhasha Model Comparison<center>
<br>


![Alt India Image](https://github.com/Sparshj8287/Bhasha-Model-Comparison/blob/main/india.png)


The **Bhasha Model Comparison** repository is a project aimed at evaluating and comparing the performance of two different language translation models on 11 diverse Indian languages. The project focuses on translating these Indian languages into English using two distinct models: the **Indic Trans model** and the **NLLB (No language left behind)** model. The repository provides a comprehensive framework for assessing the translation quality and effectiveness of these models across various Indian languages.

- [Colab notebook](#1-colab-notebook)
- [Folder Directory Structure](#1-Folder-Directory-Structure)
- [Code files ](#2-Code-files )
- [Text Files](#3-Text-Files)
- [Cloning this repository ](#4-Cloning-this-repository)
- [Installation of Model Inference code (in Local)](#5-Installation-of-Model-Inference-code)
- [Import Dependicies](#6-Import-Dependicies)
- [README.md ](#7-README.md )
- [Usage](#8-Usage )

## Depondfi'23 notebooks {#1-Depondfi-notebooks}

You can open the notebook in Colab (there is a button directly on said pages).

| Notebook                   | Description                                                                    |                                                                                                                                                                     |
| :------------------------- | :----------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Colab Notebook | Inference on two models (indicTrans and NLLB)                           | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1tL2axVDh0-IcxksooJGaneUXUgHDRK6Z?usp=sharing) |


## 1) Folder Directory Structure {#1-Folder-Directory-Structure}

```

Bhasha Model Comparison
│
│
├── Code_files/
│ └── text_files
│     ├── as_indic_text.txt
│     ├── bn_indic_text.txt
│     ├── ground_truth_text.txt
│     ├── gu_indic_text.txt
│     ├── hi_indic_text.txt
│     ├── kn_indic_text.txt
│     ├── ml_indic_text.txt
│     ├── or_indic_text.txt
│     ├── pa_indic_text.txt
│     ├── ta_indic_text.txt
│     └── te_indic_text.txt
│
│
│ ├── english_text_scraper.py
│ ├── indic_text_scraper.py
│ ├── indic_trans_inference.py
│ ├── install_dependencies.sh
│ ├── nllb_inference.py
│ ├── preprocessing.py
│ └──web_scraper.py
│
│
├── LICENSE
│
│
└── README.md



```

## 2) Code files 

This directory contains the code files for my project.



## 3) Text Files

This directory holds the text which is extracted from [PoshanTracker](https://www.poshantracker.in/) in 11 different Indian languages.

- `as_indic_text.txt`: Assamese language text for evaluation.
- `bn_indic_text.txt`: Bengali language text for evaluation.
- `gu_indic_text.txt`: Gujarati language text for evaluation.
- `hi_indic_text.txt`: Hindi language text for evaluation.
- `kn_indic_text.txt`: Kannada language text for evaluation.
- `ml_indic_text.txt`: Malayalam language text for evaluation.
- `mr_indic_text.txt`: Marathi language text for evaluation.
- `or_indic_text.txt`: Oriya language text for evaluation.
- `pa_indic_text.txt`: Punjabi language text for evaluation.
- `ta_indic_text.txt`: Tamil language text for evaluation.
- `te_indic_text.txt`: Telugu language text for evaluation.
- `ground_truth_text.txt`: Ground truth English translations corresponding to the above Indic language texts.

### `english_text_scraper.py`

This script scrapes English text from the [PoshanTracker](https://www.poshantracker.in/) for evaluation. The scraped text will be save in text_files directory.

### `indic_text_scraper.py`

This script scrapes Indic text in 11 different languages from the [PoshanTracker](https://www.poshantracker.in/) for evaluation. The scraped text will be save in text_files directory.

### `indic_trans_inference.py`

Python script for performing inference on Indic text translation to english using **indicTrans**.

### `nllb_inference.py`

Python script for performing inference on Indic text translation to english using **NLLB**.

### `preprocessing.py`

Python script for preprocessing text data before feeding it to the models.
- The script should take the text file as the input and perform this tasks.
- a. Perform language detection
- b. Split the scraped text at a sentence level
- c. Compute the statistics of words and sentences across all the languages

### `web_scraper.py`

Python script for web scraping that can **generalize to any website.**
The scraped text will be save in a new directory named as web_scraper_text.


## 4) Cloning this repository 

- Command to clone this repository:-
```
git clone https://github.com/Sparshj8287/Bhasha-Model-Comparison.git
```
```python
cd Bhasha-Model-Comparison
```
## 5) Installation of Model Inference code (in Local) 

**Note**:- If you want to inference the models in local then run the following command:-
```python
chmod +x Code_files/install_dependencies.sh
```
```python
./Code_files/install_dependencies.sh
```
Else the **inference of both models is done in colab notebook**.
you can click the link which is given above.
**Make sure to check the path that you have provided is correct and files is placed in the right directory and connect with GPU for faster inference.**

**Make sure to put the indic_trans_inference.py in the indicTrans repository for excluding file path errors.**

Make sure to correct the indic_trans_inference.py paths according to your system paths.
```python
indic2en_model = Model(expdir='/..indic-en')
```
```python
os.environ['PYTHONPATH'] += ":/content/fairseq/"
```

## 6) Import Dependicies
 Install dependencies (only once):
```python
pip install -r requirements.txt
```
**Download the fasttext model weight file and add the file in the Code_files directory:**
[Link](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin)


## 7) README.md 

A README file providing general information about our project and its directory structure.

## 8) Usage 

In order to implement the general web scraper code which can be used for any dynamic website:-
- Command to run the `Code_files/web_scraper.py`:
 ```
 python path/to/web_scraper.py --url url/to/website
 ```

For the PoshanTracker Website:-
- Command to run the `Code_files/english_text_scraper.py`:
```
 python path/to/english_text_scraper.py
 ```
- Command to run the `Code_files/indic_text_scraper.py`:
```
 python path/to/indic_text_scraper.py
 ```
For preprocessing the text data scraped from the website:-
- Command to run the `Code_files/preprocessing.py`:
```
 python path/to/preprocessing.py --CPU no/of/cpu --text_file_paths 'path/to/text/file/1' 'path/to/text/file/2'
 ```
 **Note**:- You can also give mutiple texts file path in preprocessing.py

- If you want to inference the model in local
    - First run the commands in Installation of Model Inference code (in Local)

- Command to run the `Code_files/indic_trans_inference.py`:
```
 python indic_trans_inference.py --indic_text_file_path  'indic/text/file/path'  --english_grounded_text_file_path 'grounded/english/label/text/file/path'
 ```

 - Command to run the `Code_files/nllb_inference.py`:
```
 python nllb_inference.py --indic_text_file_path  'indic/text/file/path'  --english_grounded_text_file_path 'grounded/english/label/text/file/path'
 ```
## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.


