-- NOTE: you should place the create user part 
-- in a separate file and .gitignore it as it contains credentials


-- create dlt user and dlt role 
USE ROLE USERADMIN;

CREATE ROLE IF NOT EXISTS flights_dlt_role;

-- grant role to user
USE ROLE SECURITYADMIN;

GRANT ROLE flights_dlt_role TO USER extract_loader;


-- grant privileges to role
GRANT USAGE ON WAREHOUSE flights_wh TO ROLE flights_dlt_role;
GRANT USAGE ON DATABASE flights TO ROLE flights_dlt_role;
GRANT USAGE ON SCHEMA flights.staging TO ROLE flights_dlt_role;
GRANT CREATE SCHEMA ON DATABASE flights TO ROLE flights_dlt_role;
GRANT CREATE TABLE ON SCHEMA flights.staging TO ROLE flights_dlt_role;

-- gran CRUD operations to role
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA flights.staging TO ROLE flights_dlt_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA flights.staging TO ROLE flights_dlt_role;


-- check grants
SHOW GRANTS ON SCHEMA flights.staging;
SHOW FUTURE GRANTS IN SCHEMA flights.staging;
SHOW GRANTS TO ROLE flights_dlt_role;
SHOW GRANTS TO USER extract_loader;

GRANT ROLE flights_dlt_role TO USER nokes;
GRANT ROLE flights_dlt_role TO USER anja;
GRANT ROLE flights_dlt_role TO USER rikard;