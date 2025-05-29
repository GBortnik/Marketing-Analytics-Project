SELECT 
    EngagementID,
    ContentID, 
	CampaignID,
    ProductID, 
    CASE -- Case capitalizing values and correcting Socialmedia to Social media
        WHEN ContentType IS NOT NULL THEN
            UPPER(LEFT(LOWER(REPLACE(ContentType, 'Socialmedia', 'Social Media')), 1)) + 
            LOWER(SUBSTRING(LOWER(REPLACE(ContentType, 'Socialmedia', 'Social Media')), 2, 1000))
        ELSE NULL
    END AS ContentType,
	LEFT(ViewsClicksCombined, CHARINDEX('-', ViewsClicksCombined) - 1) AS Views,  -- Extracts the Views part from the ViewsClicksCombined column by taking the substring before the '-' character
    RIGHT(ViewsClicksCombined, LEN(ViewsClicksCombined) - CHARINDEX('-', ViewsClicksCombined)) AS Clicks,  -- Extracts the Clicks part from the ViewsClicksCombined column by taking the substring after the '-' character
    Likes,
	EngagementDate
FROM 
    dbo.engagement_data 
WHERE 
    ContentType != 'Newsletter';  -- Filters out rows where ContentType is 'Newsletter' as these are not relevant for our analysis