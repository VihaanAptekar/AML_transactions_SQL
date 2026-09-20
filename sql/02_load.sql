-- do this first for local file very very important
-- Locate your MySQL connection.

-- Right-click it, or click the wrench icon.

-- Choose Edit Connection.

-- Open the Advanced tab.

-- Find the Others text box.

-- Add this line:

-- text
-- OPT_LOCAL_INFILE=1
-- If other options already exist, put it on a new line. This enables local file loading for the Workbench client.

-- Click Test Connection.

-- Click Close or OK.

-- Reopen the connection in Workbench.


SET GLOBAL local_infile = 1;

SHOW GLOBAL VARIABLES LIKE 'local_infile';

USE aml_database;

SHOW COLUMNS FROM staging_transactions;

SET autocommit = 0;
SET unique_checks = 0;
SET foreign_key_checks = 0;

LOAD DATA LOCAL INFILE
'C:\dev\aml-mysql-analytics\data\sample\SAML-D_1M_sample.csv'
INTO TABLE staging_transactions
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(
    `Date`,
    `Time`,
    Sender_account,
    Receiver_account,
    Amount,
    Payment_currency,
    Received_currency,
    Sender_bank_location,
    Receiver_bank_location,
    Payment_type,
    Is_laundering,
    Laundering_type
);

SET unique_checks = 1;
SET foreign_key_checks = 1;
COMMIT;