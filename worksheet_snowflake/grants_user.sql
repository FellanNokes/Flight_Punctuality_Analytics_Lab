-- grant role to user
USE ROLE SECURITYADMIN;

-- grant dlt role
GRANT ROLE flights_dlt_role TO USER extract_loader;

GRANT ROLE flights_dlt_role TO USER nokes;
GRANT ROLE flights_dlt_role TO USER anja;
GRANT ROLE flights_dlt_role TO USER rikard;

-- grant dbt role
GRANT ROLE flights_dbt_role TO USER transformer;

GRANT ROLE flights_dbt_role TO USER nokes;
GRANT ROLE flights_dbt_role TO USER anja;
GRANT ROLE flights_dbt_role TO USER rikard;