/*
 * PRODUCT NAME CORRECTION:
 * "Soccer Ball" is the American English term.
 * Using "Football" to match European English conventions.
 * This update ensures naming consistency with local terminology.
 */

-- Starting a transaction to allow rollback in case of issues
BEGIN TRANSACTION;

UPDATE dbo.products
SET ProductName = 'Football'
WHERE ProductName = 'Soccer Ball';

-- Check results before commiting
SELECT * FROM dbo.products WHERE ProductName IN ('Football', 'Soccer Ball');

-- Commit changes if everything is correct
COMMIT TRANSACTION;

-- If we want to undo (uncomment if needed):
-- ROLLBACK TRANSACTION;