SELECT 
    c.CustomerID,
    c.CustomerName, 
    c.Email, 
    c.Gender,
    c.Age,
    g.Country, 
    g.City, 
	CASE -- Grouping customers by Age
    WHEN Age < 30 THEN 'Young Adult (18-29)'
    WHEN Age BETWEEN 30 AND 39 THEN 'Adult (30-39)'
    WHEN Age BETWEEN 40 AND 59 THEN 'Middle Age (40-59)'
    WHEN Age >= 60 THEN 'Senior (60 and above)'
	END AS AgeGroup

FROM
    dbo.customers as c
LEFT JOIN
    dbo.geography g 
ON 
    c.GeographyID = g.GeographyID