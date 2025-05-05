-- Drop all tables from the estate database
-- Using CASCADE to also drop any dependent objects (views, constraints, etc.)

-- First try to drop the views explicitly
DROP VIEW IF EXISTS contract_type CASCADE;
DROP VIEW IF EXISTS estate_type CASCADE;

-- Then drop the tables
DROP TABLE IF EXISTS purchase_contract CASCADE;
DROP TABLE IF EXISTS tenancy_contract CASCADE;
DROP TABLE IF EXISTS house CASCADE;
DROP TABLE IF EXISTS apartment CASCADE;
DROP TABLE IF EXISTS estate CASCADE;
DROP TABLE IF EXISTS contract CASCADE;
DROP TABLE IF EXISTS person CASCADE;
DROP TABLE IF EXISTS estate_agent CASCADE; 