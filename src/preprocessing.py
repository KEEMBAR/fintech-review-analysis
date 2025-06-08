import pandas as pd
import os
import re
from spellchecker import SpellChecker
from langdetect import detect
import emoji
import logging

# Set up logging
logging.basicConfig(
    filename='preprocessing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize spell checker once
spell = SpellChecker()

def contains_amharic(text):
    """
    Check if text contains Amharic characters.
    Amharic Unicode range: \u1200-\u137F (base characters) and \u1380-\u139F (supplementary characters)
    """
    if not isinstance(text, str):
        return False
    return bool(re.search(r'[\u1200-\u137F\u1380-\u139F]', text))

def is_english(text):
    """
    Returns True if the text is in English and does not contain Amharic script.
    """
    try:
        # First check for Amharic characters
        if contains_amharic(text):
            return False
        
        # Then check with langdetect
        return detect(text) == 'en'
    except:
        return False

def remove_emojis(text):
    """Remove emojis from text."""
    return emoji.replace_emoji(text, replace='')

def clean_review(text):
    """
    Clean and normalize review text:
    - Remove emojis and non-ASCII characters
    - Remove URLs, punctuation, numbers
    - Lowercase text and trim spaces
    - Correct spelling
    """
    if not isinstance(text, str):
        return ""
        
    # Remove emojis
    text = remove_emojis(text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove numbers and punctuation but keep spaces
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Normalize whitespace and lowercase
    text = re.sub(r'\s+', ' ', text).strip().lower()
    
    # Skip spell checking if text is empty after cleaning
    if not text.strip():
        return ""
    
    # Correct spelling
    corrected_words = []
    for word in text.split():
        if len(word) > 1:  # Only correct words longer than 1 character
            corrected = spell.correction(word)
            corrected_words.append(corrected if corrected else word)
    
    return ' '.join(corrected_words)

def preprocess_reviews(input_path, output_path, min_reviews=400):
    """
    Preprocess reviews:
    - Remove duplicates
    - Drop missing/empty reviews
    - Keep only English reviews
    - Normalize dates and clean text
    - Save cleaned CSV
    """
    try:
        # Load raw data
        df = pd.read_csv(input_path)
        initial_count = len(df)
        logging.info(f"Processing {input_path}: Initial review count: {initial_count}")

        # Drop duplicate reviews
        df.drop_duplicates(subset="review_text", inplace=True)
        logging.info(f"After removing duplicates: {len(df)} reviews")

        # Drop missing or empty review_text
        df.dropna(subset=["review_text"], inplace=True)
        df = df[df["review_text"].str.strip().astype(bool)]
        logging.info(f"After removing empty reviews: {len(df)} reviews")

        # Keep only English reviews (no Amharic)
        df = df[df["review_text"].apply(is_english)]
        logging.info(f"After keeping English reviews: {len(df)} reviews")

        # Clean text
        df["review"] = df["review_text"].apply(clean_review)
        
        # Remove rows where cleaning resulted in empty text
        df = df[df["review"].str.strip().astype(bool)]
        logging.info(f"After cleaning text: {len(df)} reviews")

        # Normalize date to YYYY-MM-DD
        df["date"] = pd.to_datetime(df["date"], errors='coerce').dt.strftime('%Y-%m-%d')
        df.dropna(subset=["date"], inplace=True)
        logging.info(f"After date normalization: {len(df)} reviews")

        # Keep only the required columns
        df = df[["review", "rating", "date", "bank_name", "source"]]
        df.rename(columns={"bank_name": "bank"}, inplace=True)

        # Check if we have enough reviews
        if len(df) < min_reviews:
            logging.warning(f"Warning: Only {len(df)} reviews after cleaning, minimum required is {min_reviews}")
            print(f"⚠️ Warning: Only {len(df)} reviews after cleaning, minimum required is {min_reviews}")
            
            # If we don't have enough reviews, try to be less aggressive with cleaning
            if len(df) < min_reviews:
                # Reload and try with less aggressive cleaning
                df = pd.read_csv(input_path)
                df.drop_duplicates(subset="review_text", inplace=True)
                df.dropna(subset=["review_text"], inplace=True)
                df = df[df["review_text"].str.strip().astype(bool)]
                
                # Only remove emojis and URLs, keep punctuation
                df["review"] = df["review_text"].apply(lambda x: remove_emojis(x) if isinstance(x, str) else "")
                df["review"] = df["review"].apply(lambda x: re.sub(r'http\S+|www\S+', '', x) if isinstance(x, str) else "")
                df["review"] = df["review"].str.lower().str.strip()
                
                # Still remove Amharic text even in less aggressive mode
                df = df[~df["review"].apply(contains_amharic)]
                
                df = df[df["review"].str.strip().astype(bool)]
                df["date"] = pd.to_datetime(df["date"], errors='coerce').dt.strftime('%Y-%m-%d')
                df.dropna(subset=["date"], inplace=True)
                
                df = df[["review", "rating", "date", "bank_name", "source"]]
                df.rename(columns={"bank_name": "bank"}, inplace=True)
                
                logging.info(f"After less aggressive cleaning: {len(df)} reviews")

        # Save cleaned file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)

        print(f"✅ Cleaned data saved to {output_path}")
        print(f"📊 Total cleaned reviews: {len(df)}")
        logging.info(f"Final review count: {len(df)}")

    except Exception as e:
        logging.error(f"Error processing {input_path}: {str(e)}")
        print(f"❌ Error processing {input_path}: {str(e)}")
        raise

if __name__ == "__main__":
    input_folder = "data/raw"
    output_folder = "data/cleaned"

    filenames = [
        "Commercial_Bank_of_Ethiopia_reviews_data.csv",
        "Bank_of_Abyssinia_reviews_data.csv",
        "Dashen_Bank_reviews_data.csv"
    ]

    for file in filenames:
        input_path = os.path.join(input_folder, file)
        output_filename = file.replace("reviews", "cleaned")
        output_path = os.path.join(output_folder, output_filename)

        print(f"🔄 Preprocessing: {file}")
        preprocess_reviews(input_path, output_path)
