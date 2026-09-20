use aml_database;
-- Dimension tables

CREATE TABLE locations (
    location_id   INT AUTO_INCREMENT PRIMARY KEY,
    location_name VARCHAR(50) NOT NULL UNIQUE,
    is_high_risk  TINYINT DEFAULT 0
);    
CREATE TABLE currencies (
	currency_code CHAR(3) PRIMARY KEY,
    currency_name VARCHAR(50)
);

CREATE TABLE payment_types (
    payment_type_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    payment_type    VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE typologies (
	typology_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    typology_name VARCHAR(60) not null UNIQUE,
    is_suspicious TINYINT(1) not NULL
);

CREATE TABLE accounts (
    account_id      BIGINT PRIMARY KEY,
    first_txn_date  DATE,
    n_sent          INT DEFAULT 0,
    n_received      INT DEFAULT 0
) ENGINE=InnoDB;

CREATE TABLE staging_transactions (
    Date VARCHAR(20),
    Time VARCHAR(20),
    Sender_account  BIGINT,
    Receiver_account  BIGINT,
    Amount  VARCHAR(30),
    Payment_currency  VARCHAR(10),
    Received_currency VARCHAR(10),
    Sender_bank_location VARCHAR(50),
    Receiver_bank_location VARCHAR(50),
    Payment_type VARCHAR(30),
    Is_laundering TINYINT,
    Laundering_type  VARCHAR(60)
) ENGINE=InnoDB;

select COUNT(*) as t 
from staging_transactions;

select * from staging_transactions
limit 20;