# Marketing Analytics Project
This project focuses on analyzing marketing datasets. It includes:
- **SQL** database preparation
- Data cleaning and transformation
- Additional **Sentiment Analysis** in **Python**
- Final **Power BI** report creation

Project is based on the Hotel Revenue Dataset. A static PDF export of the dashboards is available here. Please note that the PDF version does not retain interactive features.
## Contents
- [SQL Data Preparation](#sql-data-preparation)
- [Python Sentiment Analysis](#python-sentiment-analysis)
- [Model Relationship](#model-relationship)
- [Additional DAX Measures](#additional-dax-measures)
- [Credit](#credit)

## SQL Data Preparation

Data cleaning and transformation were performed primarily in **SQL** using dedicated queries, including processes such as data normalization, value categorization and duplicates removal.

**Initial Data Processing:**
- [Product name correction](/Product%20Name%20Correction.sql)
- [Duplicate verification in Customer Journey table](/Checking%20Duplicates%20in%20Customer_Journey.sql)

**Fact Tables Preparation:**
- [Customer Journey](/fact%20Customer%20Journey%20Query.sql)
- [Engagement Data](/fact%20Engagement%20Data%20Query.sql)

**Dimension Tables Preparation:**
- [Products catalog](/dim%20Products%20Query.sql)
- [Customers & Geography](/dim%20Customers,%20Geography%20Query.sql)

*Note: Customer Reviews table was additionally processed using Python for [sentiment analysis](#python-sentiment-analysis).*

## Python Sentiment Analysis

The Customer Reviews sentiment analysis was performed in Python using following workflow:
1. **Database Connection**: Established via SQLAlchemy
2. **Data Loading**: Imported into Pandas DataFrame
3. **Sentiment Processing**:
   - NLTK's VADER for sentiment scoring
   - Added columns: `SentimentScore`, `SentimentCategory`, `SentimentBucket`
4. **Results Export**: Saved enhanced dataset to CSV for Power BI integration

*Full code is available [here](/sentiment_analysis.py).*

## Model Relationship

## Additional DAX Measures

## Credit
