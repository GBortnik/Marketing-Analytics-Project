# pip install pandas nltk pyodbc sqlalchemy

import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import urllib
from sqlalchemy import create_engine

# Download sentiment analysis tool VADER Lexicon
nltk.download('vader_lexicon')


# ANALYSIS NOTE:
# Since our dataset contains cleaned reviews, we will not apply preprocessors such as tokenization, stopwords removal, or lemmatization in this case.
# Using these techniques could negatively affect the results of the Sentiment Intensity Analyzer.


server = 'GB'  # Variable for your Server name
database = 'MarketingAnalytics' # Variable for your Database name

# Define a function to fetch data from a SQL database using a SQL query
def fetch_data_from_sql():
    connection_string = (
        "Driver={ODBC Driver 18 for SQL Server};" #using recommended drivers
        f"Server={server};"
        f"Database={database};"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    params = urllib.parse.quote_plus(connection_string)

    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    
    query = "SELECT ReviewID, CustomerID, ProductID, ReviewDate, Rating, ReviewText FROM dbo.customer_reviews"
    
    # Creating pandas dataframe using our engine and query
    df = pd.read_sql(query, engine)
    
    # You don't need to manually close the connection; SQLAlchemy handles It for you.
    
    return df


df_reviews = fetch_data_from_sql()

# If It's not possible to clean whitespace (like double space) from ReviewText colum using SQL Query, then we can do that by using Python, for example:
df_reviews['ReviewText'] = df_reviews['ReviewText'].str.replace(r'\s+', ' ', regex=True).str.strip()

# Initialize the VADER sentiment intensity analyzer for analyzing the sentiment of text data
sia = SentimentIntensityAnalyzer()

# Define a function to calculate sentiment scores using VADER
def calculate_sentiment(review):
    # Get the sentiment scores for the review text
    sentiment = sia.polarity_scores(review)
    # Return the compound score, which is a normalized score between -1 (most negative) and 1 (most positive)
    return sentiment['compound']

# Define a function to categorize sentiment using both the sentiment score and the review rating
def categorize_sentiment(score, rating):
    # Use both the text sentiment score and the numerical rating to determine sentiment category
    if score > 0.05:  # Positive sentiment score
        if rating >= 4:
            return 'Positive'  # High rating and positive sentiment
        elif rating == 3:
            return 'Mixed Positive'  # Neutral rating but positive sentiment
        else:
            return 'Mixed Negative'  # Low rating but positive sentiment
    elif score < -0.05:  # Negative sentiment score
        if rating <= 2:
            return 'Negative'  # Low rating and negative sentiment
        elif rating == 3:
            return 'Mixed Negative'  # Neutral rating but negative sentiment
        else:
            return 'Mixed Positive'  # High rating but negative sentiment
    else:  # Neutral sentiment score
        if rating >= 4:
            return 'Positive'  # High rating with neutral sentiment
        elif rating <= 2:
            return 'Negative'  # Low rating with neutral sentiment
        else:
            return 'Neutral'  # Neutral rating and neutral sentiment

# Define a function to bucket sentiment scores into text ranges
def sentiment_bucket(score):
    if score >= 0.5:
        return '0.5 to 1.0'  # Strongly positive sentiment
    elif 0.0 <= score < 0.5:
        return '0.0 to 0.49'  # Mildly positive sentiment
    elif -0.5 <= score < 0.0:
        return '-0.49 to 0.0'  # Mildly negative sentiment
    else:
        return '-1.0 to -0.5'  # Strongly negative sentiment

# Apply sentiment analysis to calculate sentiment scores for each review
df_reviews['SentimentScore'] = df_reviews['ReviewText'].apply(calculate_sentiment)

# Apply sentiment categorization using both text and rating
df_reviews['SentimentCategory'] = df_reviews.apply(
    lambda row: categorize_sentiment(row['SentimentScore'], row['Rating']), axis=1)

# Apply sentiment bucketing to categorize scores into defined ranges
df_reviews['SentimentBucket'] = df_reviews['SentimentScore'].apply(sentiment_bucket)

# Display the first few rows of the DataFrame with sentiment scores, categories, and buckets
print(df_reviews.head())

# Save the DataFrame with sentiment scores, categories, and buckets to a new CSV file
df_reviews.to_csv('fact_reviews_sentiment.csv', index=False)