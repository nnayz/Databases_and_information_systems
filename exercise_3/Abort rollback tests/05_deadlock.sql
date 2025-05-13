\set AUTOCOMMIT off
BEGIN;
UPDATE sheet3 SET name = 'X1' WHERE id = 1;
-- In SESSION 2:
-- BEGIN;
-- UPDATE sheet3 SET name = 'Y1' WHERE id = 2;
-- Then back here:
-- UPDATE sheet3 SET name = 'X2' WHERE id = 2;
-- Then in SESSION 2:
-- UPDATE sheet3 SET name = 'Y2' WHERE id = 1;
