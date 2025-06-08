# Fintech Review Analysis

## 📊 Project Overview

This project analyzes user reviews of mobile banking apps from three major Ethiopian banks — **Commercial Bank of Ethiopia (CBE)**, **Bank of Abyssinia (BOA)**, and **Dashen Bank** — to uncover key satisfaction drivers and pain points. It simulates the role of a Data Analyst at Omega Consultancy advising fintech clients.

## 🔍 Objectives

- Scrape and clean Google Play Store reviews for each bank (400+ reviews each).
- Perform sentiment analysis using NLP techniques (VADER / BERT).
- Extract themes such as UI issues, bugs, and feature requests.
- Store cleaned data in an Oracle database.
- Visualize insights and propose actionable recommendations.

## �� Project Structure

```
fintech-review-analysis/
├── data/
│   ├── raw/          # Raw scraped reviews
│   └── cleaned/      # Preprocessed reviews
├── src/
│   ├── scraping.py   # Review scraping script
│   ├── preprocessing.py  # Data cleaning script
│   ├── sentiment.py  # Sentiment analysis
│   ├── themes.py     # Theme extraction
│   └── db.py         # Database operations
├── tests/            # Unit tests
├── notebooks/        # Jupyter notebooks for analysis
└── outputs/          # Generated visualizations and reports
```

## 📋 Methodology

### 1. Data Collection

The project uses the `google-play-scraper` library to collect reviews from the Google Play Store. The scraping process:

- Targets three banking apps:
  - Commercial Bank of Ethiopia (CBE)
  - Bank of Abyssinia (BOA)
  - Dashen Bank
- Collects the following data points:
  - Review text
  - Rating (1-5 stars)
  - Date
  - Bank name
  - Source (Google Play)
- Implements error handling and logging
- Saves raw data in CSV format

### 2. Data Preprocessing

The preprocessing pipeline ensures data quality and consistency:

#### Text Cleaning

- Removes emojis using the `emoji` library
- Removes URLs and special characters
- Converts text to lowercase
- Normalizes whitespace
- Corrects spelling using `pyspellchecker`

#### Language Filtering

- Detects and removes non-English reviews using `langdetect`
- Specifically filters out Amharic text using Unicode ranges
- Maintains minimum of 400 reviews per bank

#### Data Quality Checks

- Removes duplicate reviews
- Handles missing values
- Normalizes dates to YYYY-MM-DD format
- Validates data integrity

#### Fallback Strategy

If cleaning results in fewer than 400 reviews:

- Applies less aggressive cleaning
- Keeps punctuation
- Still removes Amharic text
- Maintains minimum review count requirement

### 3. Data Storage

- Raw data stored in `data/raw/`
- Cleaned data stored in `data/cleaned/`
- CSV format with columns:
  - review: Cleaned review text
  - rating: 1-5 star rating
  - date: YYYY-MM-DD format
  - bank: Bank name
  - source: Data source

## 🛠️ Dependencies

```
google-play-scraper==1.2.7
langdetect==1.0.9
numpy==2.2.6
pandas==2.3.0
pyspellchecker==0.8.3
python-dateutil==2.9.0.post0
pytz==2025.2
schedule==1.2.2
six==1.17.0
tzdata==2025.2
emoji==2.10.1
```

## 📈 Results

- Successfully collected and cleaned reviews for all three banks
- Maintained minimum of 400 reviews per bank
- Removed non-English and Amharic text
- Prepared clean dataset for sentiment analysis and theme extraction
