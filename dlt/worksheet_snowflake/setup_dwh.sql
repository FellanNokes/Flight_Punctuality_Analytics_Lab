USE ROLE SYSADMIN;

CREATE WAREHOUSE flights_wh
WITH
    WAREHOUSE_SIZE = 'X-Small'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Warehouse for dlt loads and analysis in the flight punctuality lab';

SHOW WAREHOUSES;
