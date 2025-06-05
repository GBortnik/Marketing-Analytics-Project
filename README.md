# Marketing Analytics Project
This project focuses on analyzing marketing datasets. It includes:
- **SQL** database preparation
- Data cleaning and transformation
- Additional **Sentiment Analysis** in **Python**
- Final **Power BI** report creation

Static PDF export of the dashboards is available [here](/Marketing%20Analysis%20Report.pdf). Please note that the PDF version does not retain interactive features.

🇵🇱 Polish version of the document can be found [here](/README-PL.md)/Polską wersję dokumentu można znaleźć [tutaj](/README-PL.md). 🇵🇱
## Contents
- [SQL Data Preparation](#sql-data-preparation)
- [Python Sentiment Analysis](#python-sentiment-analysis)
- [Model Relationship](#model-relationship)
- [Additional DAX Measures](#additional-dax-measures)
- [Power BI Report](#power-bi-report)
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
The data model incorporates:
- All tables previously prepared in SQL and Python
- An additional **`dim_calendar`** dimension table created via DAX measure. Measure can be found in [Additional DAX Measures](#additional-dax-measures) section.

**Relationship Configuration:**
- Dimension Tables ↔ Fact Tables:  
  🔗 **One-to-many** relationships  
  🔄 **Single-direction** cross-filtering (from dimensions to facts)

![Model Relationship](/images/Model%20Relationships.png)

## Additional DAX Measures
The project utilizes supplemental **DAX measures**, including creation of the dimension table `dim_calendar` and the `Conversion Rate` metric. Details below:

- Calendar Dimension Table

Centralized date reference for time-based analysis in Power BI. 
``` 
dim_calendar = 
ADDCOLUMNS (
    CALENDAR ( DATE ( 2023, 1, 1 ), DATE ( 2025, 12, 31 ) ),
    "DateAsInteger", FORMAT ( [Date], "YYYYMMDD" ),
    "Year", YEAR ( [Date] ),
    "Monthnumber", FORMAT ( [Date], "MM" ),
    "YearMonthnumber", FORMAT ( [Date], "YYYY/MM" ),
    "YearMonthShort", FORMAT ( [Date], "YYYY/mmm" ),
    "MonthNameShort", FORMAT ( [Date], "mmm" ),
    "MonthNameLong", FORMAT ( [Date], "mmmm" ),
    "DayOfWeekNumber", WEEKDAY ( [Date] ),
    "DayOfWeek", FORMAT ( [Date], "dddd" ),
    "DayOfWeekShort", FORMAT ( [Date], "ddd" ),
    "Quarter", "Q" & FORMAT ( [Date], "Q" ),
    "YearQuarter",
        FORMAT ( [Date], "YYYY" ) & "/Q"
            & FORMAT ( [Date], "Q" )
)
```

- Conversion Rate

Calculates the percentage of visitors who made a purchase (Views → Purchases).

```
Conversion Rate = 
VAR TotalVisitors = 
    CALCULATE(
        COUNT(fact_customer_journey[JourneyID]),
        fact_customer_journey[Action] = "View"
    )
VAR TotalPurchases = 
    CALCULATE(
        COUNT(fact_customer_journey[JourneyID]),
        fact_customer_journey[Action] = "Purchase"
    )
RETURN
    IF(
        TotalVisitors = 0,
        0,
        DIVIDE(TotalPurchases, TotalVisitors)
    )
```

- Positive Reviews Percentage

Calculates the percentage of positive reviews (Positive or Mixed Positive Category)

```
PositiveReviewsPercentage = 
VAR TotalReviews = COUNTROWS(fact_reviews_sentiment)
VAR PositiveReviews =
    CALCULATE(
        COUNTROWS(fact_reviews_sentiment),
        fact_reviews_sentiment[SentimentCategory] IN { "Mixed Positive", "Positive" }
    )
RETURN
DIVIDE(PositiveReviews, TotalReviews, 0)
```

## Power BI Report

- **Overview**

Main report page summarizing the key aspects of the analysis. It includes crucial insights related to Social Media, Customer Reviews, and Conversion. The page also offers time-based analysis and interactive slicers to enhance user engagement with the report.

![Overview Page](/images/Overview%20Page.png)

- **Social Media Details**

Detailed breakdown of customer reach and engagement with products. This page provides advanced insights into performance metrics, content effectiveness, and audience interactions across social platforms, enabling data-driven optimization of campaigns.

![Social Media Details](/images/Social%20Media%20Details.png)

- **Customer Reviews Details**

This page provides key insights into customer feedback, including the percentage of positive reviews and average product ratings. Interactive visuals, such as the decomposition tree and treemap, allow users to explore sentiment distribution and uncover trends or drivers behind customer opinions. The high level of interactivity empowers users to analyze the data from multiple perspectives.



![Customer Reviews Details](/images/Customer%20Reviews%20Details.png)

- **Conversion Details**

This page provides key insights into conversion performance, showing important KPIs like conversion rates and visitor metrics. Interactive visualizations help users identify bottlenecks and understand how visitors progress through the funnel to optimize sales outcomes.

![Conversion Details](/images/Conversion%20Details.png)

## Credit
**Project Inspiration & Dataset**

This project was inspired by [Data Analyst Project](https://github.com/aliahmad-1987/DataAnalystPortfolioProject_PBI_SQL_Python_MarketingAnalytics) and utilizes a dataset provided by the author.
