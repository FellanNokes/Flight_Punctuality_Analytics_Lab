-- Create warehouse schema

USE ROLE SYSADMIN;

USE DATABASE flights;

CREATE SCHEMA IF NOT EXISTS warehouse;

SHOW SCHEMAS IN DATABASE flights;

-- grant privileges to work on warehouse schema
USE ROLE SECURITYADMIN;

GRANT ROLE flights_dlt_role TO ROLE flights_dbt_role;

SHOW GRANTS TO ROLE flights_dbt_role;
SHOW GRANTS OF ROLE flights_dbt_role;

GRANT USAGE,
CREATE TABLE,
CREATE VIEW ON SCHEMA flights.warehouse TO ROLE flights_dbt_role;

-- grant CRUD and select tables and views
GRANT SELECT,
INSERT,
UPDATE,
DELETE ON ALL TABLES IN SCHEMA flights.warehouse TO ROLE flights_dbt_role;
GRANT SELECT ON ALL VIEWS IN SCHEMA flights.warehouse TO ROLE flights_dbt_role;

GRANT SELECT,
INSERT,
UPDATE,
DELETE ON FUTURE TABLES IN SCHEMA flights.warehouse TO ROLE flights_dbt_role;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA flights.warehouse TO ROLE flights_dbt_role;

-- test on the new role
USE ROLE flights_dbt_role;
SELECT * FROM flights.staging.arivals LIMIT 10;

SHOW GRANTS ON SCHEMA flights.warehouse;

USE SCHEMA flights.warehouse;
CREATE TABLE test (id INTEGER);
SHOW TABLES;
SHOW GRANTS TO ROLE flights_dbt_role;
DROP TABLE TEST;