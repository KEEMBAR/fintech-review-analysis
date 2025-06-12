"""
Data loading module for populating the database with analyzed review data.
"""
import pandas as pd
import logging
from datetime import datetime
from database import DatabaseConnection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_reviews(csv_path='data/analyzed/final_sentiment_analysis.csv'):
    """
    Load review data from CSV file into the reviews table.
    
    Args:
        csv_path (str): Path to the CSV file containing review data
    
    Returns:
        bool: True if loading was successful, False otherwise
    """
    try:
        # Read the CSV file
        logger.info(f"Reading review data from {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Prepare the data for insertion
        with DatabaseConnection.get_connection() as conn:
            with conn.cursor() as cur:
                inserted_count = 0
                
                for _, row in df.iterrows():
                    review_text = row.get('review')
                    rating = row.get('rating')
                    bank_name = row.get('bank')
                    sentiment_label = row.get('sentiment_label')
                    sentiment_score = row.get('sentiment_score')
                    
                    # Convert date safely; coerce invalid formats to NaT
                    review_date = pd.to_datetime(row.get('date'), errors='coerce')
                    if pd.isnull(review_date):
                        review_date = None
                    
                    # Skip rows missing critical data
                    if not review_text or pd.isnull(rating) or not bank_name:
                        logger.warning("Skipping row due to missing required fields.")
                        continue
                    
                    cur.execute("""
                        INSERT INTO reviews 
                        (review_text, rating, review_date, bank_name, sentiment_label, sentiment_score)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING id;
                    """, (
                        review_text,
                        int(rating),
                        review_date,
                        bank_name,
                        sentiment_label,
                        sentiment_score
                    ))
                    inserted_count += 1
                
                conn.commit()
                logger.info(f"Successfully loaded {inserted_count} reviews into the database")
                return True
                
    except Exception as e:
        logger.error(f"Error loading review data: {e}")
        return False

if __name__ == "__main__":
    load_reviews()
