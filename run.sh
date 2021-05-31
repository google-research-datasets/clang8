#!/bin/bash
set -e
set -x

# Download the Lang-8 raw corpus from:
# https://docs.google.com/forms/d/17gZZsC_rnaACMXmPiab3kjqBEtRHPMz0UG9Dk-x_F0k/viewform?edit_requested=true
# and provide the directory here.
readonly LANG8_DIR='<INSERT LANG8 DIRECTORY HERE>'

echo "Installing required packages..."
virtualenv -p python3 .
source ./bin/activate

pip install -r requirements.txt

python -m spacy download en_core_web_sm
python -m spacy download de_core_news_sm
python -m spacy download ru_core_news_sm

echo "Running a test..."
python -m prepare_clang8_dataset_test

echo "Generating the cLang-8 dataset for three languages: ru, de, and en"
python -m prepare_clang8_dataset \
  --lang8_dir="${LANG8_DIR}" \
  --tokenize_text='True' \
  --languages='ru,de,en'
