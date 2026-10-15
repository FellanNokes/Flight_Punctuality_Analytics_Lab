USE ROLE SYSADMIN;

USE DATABASE flights;

CREATE SCHEMA IF NOT EXISTS marts;

USE ROLE SECURITYADMIN;

GRANT USAGE,
CREATE TABLE,
CREATE VIEW ON SCHEMA flights.marts TO ROLE flights_dbt_role;

-- grant CRUD and select tables and views
GRANT SELECT,
INSERT,
UPDATE,
DELETE ON ALL TABLES IN SCHEMA flights.marts TO ROLE flights_dbt_role;
GRANT SELECT ON ALL VIEWS IN SCHEMA flights.marts TO ROLE flights_dbt_role;

-- grant CRUD andselect on future tables and views in schema
GRANT SELECT,
INSERT,
UPDATE,
DELETE ON FUTURE TABLES IN SCHEMA flights.marts TO ROLE flights_dbt_role;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA flights.marts TO ROLE flights_dbt_role;

-- tests
USE ROLE flights_dbt_role;

SHOW GRANTS ON SCHEMA flights.marts;

USE SCHEMA flights.marts;
CREATE TABLE test (id INTEGER);
SHOW TABLES;
DROP TABLE TEST;