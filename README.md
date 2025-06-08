# Fintech Review Analysis

## 📊 Project Overview

This project analyzes user reviews of mobile banking apps from three major Ethiopian banks — **Commercial Bank of Ethiopia (CBE)**, **Bank of Abyssinia (BOA)**, and **Dashen Bank** — to uncover key satisfaction drivers and pain points. It simulates the role of a Data Analyst at Omega Consultancy advising fintech clients.

## 🔍 Objectives

- Scrape and clean Google Play Store reviews for each bank (400+ reviews each).
- Perform sentiment analysis using NLP techniques (VADER / BERT).
- Extract themes such as UI issues, bugs, and feature requests.
- Store cleaned data in an Oracle database.
- Visualize insights and propose actionable recommendations.

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

## Task 2: Sentiment and Thematic Analysis

This task focuses on analyzing user reviews to understand sentiment and identify key themes in the feedback for different banks.

### Implementation Details

#### 1. Sentiment Analysis

- Uses DistilBERT model (distilbert-base-uncased-finetuned-sst-2-english) for sentiment analysis
- Processes each review to determine sentiment (positive/negative) and confidence score
- Results are saved in the analyzed data files

#### 2. Thematic Analysis

- Implements keyword extraction using spaCy
- Identifies themes based on predefined categories:
  - Account Access
  - Transaction Performance
  - User Interface
  - Customer Support
  - Technical Issues
- Generates detailed reports with theme statistics and example reviews

### Project Structure

```
fintech-review-analysis/
├── data/
│   ├── raw/              # Raw review data
│   ├── cleaned/          # Preprocessed review data
│   └── analyzed/         # Sentiment analysis results
├── reports/
│   └── themes/          # Theme analysis reports
├── src/
│   ├── scraping.py       # Review scraping script
│   ├── preprocessing.py  # Data cleaning script
│   ├── sentiment_analysis.py  # Sentiment analysis
│   └── theme_analysis.py # Theme analysis
└── outputs/              # Generated visualizations and reports
```

### Setup and Installation

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Download spaCy model:

```bash
python -m spacy download en_core_web_sm
```

### Usage

1. Run sentiment analysis:

```bash
python src/sentiment_analysis.py
```

2. Generate theme reports:

```bash
python src/theme_analysis.py
```

### Output

1. Analyzed Data (`data/analyzed/`):

   - CSV files containing original reviews with sentiment scores and extracted keywords
   - Columns: review, rating, date, bank, source, sentiment_label, sentiment_score, keywords

2. Theme Reports (`reports/themes/`):
   - Text files containing detailed theme analysis for each bank
   - Includes theme statistics, sentiment scores, and example reviews

### Dependencies

- transformers==4.37.2
- torch==2.2.0
- scikit-learn==1.4.0
- spacy==3.7.2
- pandas==2.3.0
- numpy==2.2.6

### Notes

- The sentiment analysis uses DistilBERT for accurate sentiment classification
- Theme analysis is based on predefined categories and keyword matching
- All analysis results are logged for debugging and monitoring
