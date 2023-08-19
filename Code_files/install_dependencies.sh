git clone https://github.com/AI4Bharat/indicTrans.git
cd indicTrans
pip install fasttext selenium bs4 
pip install transformers
pip install sacremoses pandas mock sacrebleu tensorboardX pyarrow indic-nlp-library
pip install mosestokenizer subword-nmt

# Install fairseq from source
git clone https://github.com/pytorch/fairseq.git
cd fairseq
# !git checkout da9eaba12d82b9bfc1442f0e2c6fc1b895f4d35d
pip install ./
pip install xformers
cd ..
wget https://ai4b-public-nlu-nlg.objectstore.e2enetworks.net/indic2en.zip
unzip indic2en.zip