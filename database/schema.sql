-- =========================================
-- QueryShield Database Schema
-- =========================================

CREATE DATABASE IF NOT EXISTS queryshield;
USE queryshield;

-- =========================================
-- 1. Customers Table
-- =========================================
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- 2. Accounts Table
-- =========================================
CREATE TABLE accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    account_type ENUM('SAVINGS', 'CURRENT') NOT NULL,
    balance DECIMAL(12,2) DEFAULT 0.00,
    status ENUM('ACTIVE', 'BLOCKED') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE CASCADE
);

-- =========================================
-- 3. Transactions Table
-- =========================================
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    transaction_type ENUM('DEPOSIT', 'WITHDRAWAL', 'TRANSFER') NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    transaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location VARCHAR(100),
    status ENUM('SUCCESS', 'FAILED') DEFAULT 'SUCCESS',
    
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
        ON DELETE CASCADE
);

-- =========================================
-- 4. Alerts Table (Fraud Detection)
-- =========================================
CREATE TABLE alerts (
    alert_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT,
    account_id INT,
    alert_type VARCHAR(100),
    severity ENUM('LOW', 'MEDIUM', 'HIGH') DEFAULT 'LOW',
    status ENUM('PENDING', 'RESOLVED') DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
        ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
        ON DELETE CASCADE
);

-- =========================================
-- 5. Indexes (Performance Optimization)
-- =========================================
CREATE INDEX idx_transaction_account ON transactions(account_id);
CREATE INDEX idx_transaction_time ON transactions(transaction_time);
CREATE INDEX idx_alert_account ON alerts(account_id);

-- =========================================
-- 6. Sample View (For Dashboard)
-- =========================================
CREATE VIEW transaction_summary AS
SELECT 
    transaction_type,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_amount
FROM transactions
GROUP BY transaction_type;

-- =========================================
-- 7. Sample View (Fraud Summary)
-- =========================================
CREATE VIEW fraud_summary AS
SELECT 
    alert_type,
    COUNT(*) AS total_alerts,
    SUM(CASE WHEN status = 'RESOLVED' THEN 1 ELSE 0 END) AS resolved_alerts
FROM alerts
GROUP BY alert_type;