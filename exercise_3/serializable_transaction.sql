-- Serializable Transaction
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

BEGIN;
SELECT * FROM sheet3 WHERE id = 1;