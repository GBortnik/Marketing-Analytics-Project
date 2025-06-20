# Projekt Analizy Marketingowej

Projekt koncentruje się na analizie danych marketingowych. Obejmuje:
- Przygotowanie bazy danych w SQL
- Czyszczenie i transformację danych
- Dodatkową analizę sentymentu w Pythonie
- Utworzenie końcowego raportu w Power BI

Statyczny eksport dashboardów w formacie PDF jest dostępny [tutaj](/Marketing%20Analysis%20Report.pdf). Należy pamiętać, że wersja PDF nie obsługuje elementów interaktywnych.

🇬🇧 English version of the document can be found [here](/README.md)/Angielską wersję dokumentu można znaleźć [tutaj](/README.md). 🇬🇧

## Zawartość
- [Przygotowanie danych w SQL](#przygotowanie-danych-w-sql)
- [Analiza Nastrojów w Pythonie](#analiza-nastrojów-w-pythonie)
- [Model Semantyczny](#model-semantyczny)
- [Raport w Power BI](#raport-w-power-bi)
- [Dodatkowe Miary DAX](#dodatkowe-miary-dax)
- [Credit](#credit)

## Przygotowanie danych w SQL

Czyszczenie i transformacja danych przeprowadzone głównie przy użyciu zapytań **SQL**, w tym procesy jak normalizacja danych, kategoryzowanie wartości czy usuwanie duplikatów.

**Wstępne przetwarzanie:**
- [Korekta nazwy produktu](/Product%20Name%20Correction.sql)
- [Weryfikacja duplikatów w tabeli Customer Journey](/Checking%20Duplicates%20in%20Customer_Journey.sql)

**Przygotowanie Fact Tables:**
- [Customer Journey](/fact%20Customer%20Journey%20Query.sql)
- [Engagement Data](/fact%20Engagement%20Data%20Query.sql)

**Przygotowanie Dimension Tables:**
- [Products catalog](/dim%20Products%20Query.sql)
- [Customers & Geography](/dim%20Customers,%20Geography%20Query.sql)

*Uwaga: Tabela Customer Reviews została dodatkowo przetworzona w Pythonie pod kątem [analizy nastrojów](#analiza-nastrojów-w-pythonie).*

## Analiza Nastrojów w Pythonie

Proces analizy nastrojów dla recenzji klientów:
1. **Połączenie z bazą danych**: Zrealizowane przez SQLAlchemy
2. **Wczytywanie danych**: Import do Pandas DataFrame
3. **Przetwarzanie analizy nastrojów**:
   - Wykorzystanie modelu VADER z NLTK
   - Dodane kolumny: `SentimentScore`, `SentimentCategory`, `SentimentBucket`
4. **Eksport wyników**: Zapis wzbogaconych danych do pliku CSV dla Power BI

*Pełny kod dostępny [tutaj](/sentiment_analysis.py).*

## Model Semantyczny
Model zawiera:
- Wszystkie tabele przygotowane wcześniej w SQL i Pythonie
- Dodatkową Dimension Table **`dim_calendar`** utworzoną miarą DAX. Miarę można znaleźć w sekcji [Dodatkowe Miary DAX](#dodatkowe-miary-dax)

**Konfiguracja relacji:**
- Dimension Tables ↔ Fact Tables:  
  🔗 Relacja **One-to-many**  
  🔄 Filtrowanie krzyżowe **jednokierunkowe** (z Dimension do Fact)

![Model Relationship](/images/Model%20Relationships.png)

## Raport w Power BI

- **Overview**

Główna strona raportu podsumowująca kluczowe aspekty analizy. Zawiera istotne informacje dotyczące mediów społecznościowych, opinii klientów oraz konwersji. Oferuje również analizę czasową oraz slicery, które ułatwiają interakcję użytkownika z raportem.

![Overview Page](/images/Overview%20Page.png)

- **Social Media Details**

Analiza mediów społecznościowych: Szczegółowy przegląd zasięgu i zaangażowania klientów z produktami. Strona oferuje metryki efektywności treści, interakcji odbiorców oraz wyników kampanii, umożliwiając optymalizację działań w oparciu o dane.

![Social Media Details](/images/Social%20Media%20Details.png)

- **Customer Reviews Details**

Strona prezentuje kluczowe wskaźniki dotyczące opinii klientów, w tym procent pozytywnych recenzji i średnią ocenę produktów. Interaktywne wizualizacje, takie jak *decomposition tree* i *treemap*, umożliwiają analizę rozkładu nastrojów oraz odkrywanie trendów i czynników wpływających na opinie. Wysoki poziom interaktywności pozwala użytkownikom analizować dane z różnych perspektyw.

![Customer Reviews Details](/images/Customer%20Reviews%20Details.png)

- **Conversion Details**

Strona prezentuje kluczowe wskaźniki efektywności konwersji, takie jak współczynnik konwersji i metryki odwiedzin. Interaktywne wizualizacje pozwalają użytkownikom zidentyfikować wąskie gardła i zrozumieć przebieg ścieżki zakupowej, co pomaga optymalizować wyniki sprzedaży.

![Conversion Details](/images/Conversion%20Details.png)

## Dodatkowe Miary DAX
Projekt wykorzystuje dodatkowe miary **DAX**, w tym np. utworzenie dimension table `dim_calendar` czy metryki `Conversion Rate`. Szczegóły poniżej:

- Calendar Dimension Table

Centralna referencja dat dla analiz czasowych w Power BI. 
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

- Współczynnik konwersji

Oblicza procent użytkowników, którzy dokonali zakupu (Wyświetlenie → Zakup).

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

- Procent pozytywnych recenzji

Oblicza udział procentowy recenzji zaklasyfikowanych jako pozytywne lub częściowo pozytywne

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

## Credit
**Inspiracja i źródło danych**  
Projekt powstał w oparciu o zainspirowanie przez [Data Analyst Project](https://github.com/aliahmad-1987/DataAnalystPortfolioProject_PBI_SQL_Python_MarketingAnalytics), wykorzystując dataset udostępniony przez autora.