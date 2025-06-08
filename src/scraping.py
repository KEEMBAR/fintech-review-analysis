from google_play_scraper import Sort, reviews
from datetime import datetime
import csv
import logging
import os

# Set up logging
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Bank App IDs
BANK_APPS = {
    'Commercial Bank of Ethiopia': 'com.combanketh.mobilebanking',
    'Bank of Abyssinia': 'com.boa.boaMobileBanking',
    'Dashen Bank': 'com.dashen.dashensuperapp'
}

def scrape_reviews(app_id, bank_name, output_dir="data/raw", count=2000):
    logging.info(f"🔄 Fetching reviews for {bank_name}...")

    try:
        results, _ = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=count,
            filter_score_with=None
        )

        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(output_dir, f"{bank_name.replace(' ', '_')}_reviews_{timestamp}.csv")

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['review_text', 'rating', 'date', 'bank_name', 'source'])
            writer.writeheader()

            for entry in results:
                writer.writerow({
                    'review_text': entry['content'],
                    'rating': entry['score'],
                    'date': entry['at'].strftime('%Y-%m-%d'),
                    'bank_name': bank_name,
                    'source': 'Google Play'
                })

        logging.info(f"✅ Saved {len(results)} reviews for {bank_name} to {filename}")
        print(f"✅ Done: {bank_name} -> {filename}")

    except Exception as e:
        logging.error(f"❌ Error while scraping {bank_name}: {e}")
        print(f"❌ Failed: {bank_name} - {e}")

def main():
    for bank_name, app_id in BANK_APPS.items():
        scrape_reviews(app_id, bank_name)

if __name__ == "__main__":
    main()
