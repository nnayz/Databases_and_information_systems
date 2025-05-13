
-- In SESSION 1
\set AUTOCOMMIT off
BEGIN;
UPDATE sheet3 SET name = 'X1' WHERE id = 1;
-- In SESSION 2:
BEGIN;
UPDATE sheet3 SET name = 'Y1' WHERE id = 2;
-- In SESSION 1
UPDATE sheet3 SET name = 'X2' WHERE id = 2;

-- In SESSION 2:
UPDATE sheet3 SET name = 'Y2' WHERE id = 1;
