-- NOTE: you should place the create user part 
-- in a separate file and .gitignore it as it contains credentials


-- create dlt user and dlt role 
USE ROLE USERADMIN;

CREATE ROLE IF NOT EXISTS flights_dlt_role;

CREATE ROLE IF NOT EXISTS flights_dbt_role;

CREATE ROLE IF NOT EXISTS flights_reporter_role;


-- grant privileges to role
GRANT USAGE ON WAREHOUSE flights_wh TO ROLE flights_dlt_role;
GRANT USAGE ON DATABASE flights TO ROLE flights_dlt_role;
GRANT USAGE ON SCHEMA flights.staging TO ROLE flights_dlt_role;
GRANT CREATE SCHEMA ON DATABASE flights TO ROLE flights_dlt_role;
GRANT CREATE TABLE ON SCHEMA flights.staging TO ROLE flights_dlt_role;

-- grant CRUD operations to role
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA flights.staging TO ROLE flights_dlt_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA flights.staging TO ROLE flights_dlt_role;

-- grant privlages to reporter role 
GRANT USAGE ON WAREHOUSE flights_wh TO ROLE flights_reporter_role;
GRANT USAGE ON DATABASE flights TO ROLE flights_reporter_role;
GRANT USAGE ON SCHEMA flights.marts TO ROLE flights_reporter_role;

GRANT SELECT ON ALL TABLES IN SCHEMA flights.marts TO ROLE flights_reporter_role;
GRANT SELECT ON FUTURE TABLES IN SCHEMA flights.marts TO ROLE flights_reporter_role;
GRANT SELECT ON ALL VIEWS IN SCHEMA flights.marts TO ROLE flights_reporter_role;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA flights.marts TO ROLE flights_reporter_role;

USE ROLE SECURITYADMIN;
-- check grants
SHOW GRANTS ON SCHEMA flights.staging;
SHOW FUTURE GRANTS IN SCHEMA flights.staging;
SHOW GRANTS TO ROLE flights_dlt_role;
SHOW GRANTS TO USER extract_loader;

-- What the role is allowed to do (warehouse, database, schema, tables)
SHOW GRANTS TO ROLE flights_reporter_role;

-- Future grants in the marts schema (new tables dbt creates)
SHOW FUTURE GRANTS IN SCHEMA flights.marts;

-- Which users and roles have the role
SHOW GRANTS OF ROLE flights_reporter_role;

-- Which roles the reporter user has
SHOW GRANTS TO USER reporter;

