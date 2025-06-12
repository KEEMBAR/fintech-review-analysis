"""
Database schema definitions for the fintech review analysis project.
"""

# SQL statements for creating tables
CREATE_TABLES = {
    'reviews': """
        CREATE TABLE IF NOT EXISTS reviews (
            id SERIAL PRIMARY KEY,
            review_text TEXT NOT NULL,
            rating INTEGER CHECK (rating >= 1 AND rating <= 5),
            review_date TIMESTAMP,
            bank_name VARCHAR(50) NOT NULL,
            sentiment_label VARCHAR(20),
            sentiment_score FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """,
    
    'themes': """
        CREATE TABLE IF NOT EXISTS themes (
            id SERIAL PRIMARY KEY,
            review_id INTEGER REFERENCES reviews(id) ON DELETE CASCADE,
            theme_name VARCHAR(50) NOT NULL,
            confidence_score FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """,
    
    'analysis_summary': """
        CREATE TABLE IF NOT EXISTS analysis_summary (
            id SERIAL PRIMARY KEY,
            bank_name VARCHAR(50) NOT NULL,
            total_reviews INTEGER NOT NULL,
            avg_sentiment_score FLOAT,
            theme_distribution JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(bank_name)
        );
    """
}

# Indexes for better query performance
CREATE_INDEXES = {
    'reviews_bank_name_idx': """
        CREATE INDEX IF NOT EXISTS reviews_bank_name_idx ON reviews(bank_name);
    """,
    'reviews_sentiment_label_idx': """
        CREATE INDEX IF NOT EXISTS reviews_sentiment_label_idx ON reviews(sentiment_label);
    """,
    'themes_review_id_idx': """
        CREATE INDEX IF NOT EXISTS themes_review_id_idx ON themes(review_id);
    """,
    'themes_theme_name_idx': """
        CREATE INDEX IF NOT EXISTS themes_theme_name_idx ON themes(theme_name);
    """
} 