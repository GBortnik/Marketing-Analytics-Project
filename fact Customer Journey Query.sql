/*
DATA NOTE: Duration NULLs
- Occur ONLY with 'Drop-off' actions
- Intentional (unmeasurable time for abandoned sessions)
- Keep NULLs - imputing would distort:
  * Conversion metrics
  * Funnel drop-off points
*/

SELECT 
    JourneyID, 
    CustomerID,
    ProductID,  
    VisitDate,  
    Stage, 
    Action,  
    Duration 
FROM 
    (
        -- Using subquery to clean and transform data
        SELECT 
            JourneyID,  
            CustomerID,  
            ProductID,  
            VisitDate, 
            UPPER(REPLACE(Stage, 'ProductPage', 'Product Page')) AS Stage, -- Fixing ProductPage value and inconsistent capitalization
            Action,
            Duration,
            ROW_NUMBER() OVER (
                PARTITION BY CustomerID, ProductID, VisitDate, UPPER(REPLACE(Stage, 'ProductPage', 'Product Page')), Action  -- Groups by these columns to identify duplicate records
                ORDER BY JourneyID  -- Orders by JourneyID to keep the first occurrence of each duplicate
            ) AS row_num  -- Assigns a row number to each row within the partition to identify duplicates
        FROM 
            dbo.customer_journey
    ) AS subquery 
WHERE 
    row_num = 1;  -- Keeps only the first occurrence of each duplicate group identified in the subquery