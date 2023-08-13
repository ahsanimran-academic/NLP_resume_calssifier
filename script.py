# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 01:35:09 2023

@author: Ahsan Imran
"""

import os
import fitz
import argparse
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from transformers import AutoTokenizer, TFDistilBertForSequenceClassification
import wget

wget.download("https://raw.githubusercontent.com/yogawicaksana/helper_prabowo/main/helper_prabowo_ml.py",out="helper_prabowo_ml.py")
from helper_prabowo_ml import clean_html, remove_links, remove_special_characters, removeStopWords, remove_, remove_digits, lower, email_address, non_ascii, punct

def preprocess(text):
    text = clean_html(text)
    text = remove_(text)
    text = removeStopWords(text)
    text = remove_digits(text)
    text = remove_links(text)
    text = remove_special_characters(text)
    text = punct(text)
    text = non_ascii(text)
    text = email_address(text)
    text = lower(text)
    return text

labels_dict = {'HR': 0,
 'DESIGNER': 1,
 'INFORMATION-TECHNOLOGY': 2,
 'TEACHER': 3,
 'ADVOCATE': 4,
 'BUSINESS-DEVELOPMENT': 5,
 'HEALTHCARE': 6,
 'FITNESS': 7,
 'AGRICULTURE': 8,
 'BPO': 9,
 'SALES': 10,
 'CONSULTANT': 11,
 'DIGITAL-MEDIA': 12,
 'AUTOMOBILE': 13,
 'CHEF': 14,
 'FINANCE': 15,
 'APPAREL': 16,
 'ENGINEERING': 17,
 'ACCOUNTANT': 18,
 'CONSTRUCTION': 19,
 'PUBLIC-RELATIONS': 20,
 'BANKING': 21,
 'ARTS': 22,
 'AVIATION': 23
  }


def main():
    parser = argparse.ArgumentParser(description='Categorize and organize resumes based on predictions.')
    parser.add_argument('resume_dir', type=str, help='Directory containing resume PDFs')
    args = parser.parse_args()

    # Load the pre-trained model
    model = load_model('./resume_parser.h5', custom_objects={'TFDistilBertForSequenceClassification': TFDistilBertForSequenceClassification})

    tokenizer = AutoTokenizer.from_pretrained("manishiitg/distilbert-resume-parts-classify")
    
    categorized_resumes = []
    
    for filename in os.listdir(args.resume_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(args.resume_dir, filename)

            # Read PDF and extract text
            doc = fitz.open(pdf_path)
            pdf_text = ""
            for page in doc:
                pdf_text += page.get_text()
            doc.close()  # Close the PDF document
            # Preprocess extracted text
            preprocessed_text = preprocess(pdf_text)

            # Tokenize the preprocessed text
            encoded_input = tokenizer(text=preprocessed_text,
                                      add_special_tokens=True,
                                      padding=True,
                                      truncation=True,
                                      max_length=200,
                                      return_tensors='tf',
                                      return_attention_mask=True,
                                      return_token_type_ids=False,
                                      verbose=1)

            # Make predictions
            predictions = model.predict({'input_ids': encoded_input['input_ids'],
                                          'attention_mask': encoded_input['attention_mask']})

            # Convert the predicted category index to the original category label
            predicted_category_index = np.argmax(predictions, axis=1)
            predicted_category_label = list(labels_dict.keys())[predicted_category_index[0]]

            print("Predicted Category:", predicted_category_label)

            # Create a folder for the category if it doesn't exist
            category_dir = os.path.join(args.resume_dir, predicted_category_label)
            if not os.path.exists(category_dir):
                os.makedirs(category_dir)

            # Move the PDF to the corresponding category folder
            os.rename(pdf_path, os.path.join(category_dir, filename))
            
            # Add to categorized_resumes list
            categorized_resumes.append({'filename': filename, 'category': predicted_category_label})
    
    # Save categorized_resumes to CSV
    categorized_resumes_df = pd.DataFrame(categorized_resumes)
    csv_path = os.path.join(args.resume_dir, 'categorized_resumes.csv')
    categorized_resumes_df.to_csv(csv_path, index=False)
    print("Categorized resumes information saved to categorized_resumes.csv")


if __name__ == "__main__":
    main()
