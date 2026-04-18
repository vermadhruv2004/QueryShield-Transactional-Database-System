-- =========================================
-- QueryShield Sample Data
-- =========================================

USE queryshield;

-- =========================================
-- 1. Insert Customers
-- =========================================
INSERT INTO customers (name, email, phone, address) VALUES
('Rahul Sharma', 'rahul@gmail.com', '9876543210', 'Delhi'),
('Anita Verma', 'anita@gmail.com', '9876543211', 'Mumbai'),
('Rohit Kumar', 'rohit@gmail.com', '9876543212', 'Bangalore'),
('Sneha Singh', 'sneha@gmail.com', '9876543213', 'Lucknow');

-- =========================================
-- 2. Insert Accounts
-- =========================================
INSERT INTO accounts (customer_id, account_type, balance) VALUES
(1, 'SAVINGS', 100000),
(2, 'SAVINGS', 50000),
(3, 'CURRENT', 200000),
(4, 'SAVINGS', 30000);

-- =========================================
-- 3. Normal Transactions
-- =========================================
INSERT INTO transactions (account_id, transaction_type, amount, location)
VALUES
(1, 'DEPOSIT', 10000, 'Delhi'),
(1, 'WITHDRAWAL', 5000, 'Delhi'),
(2, 'TRANSFER', 2000, 'Mumbai'),
(3, 'DEPOSIT', 15000, 'Bangalore'),
(4, 'WITHDRAWAL', 3000, 'Lucknow');

-- =========================================
-- 4. High Amount Fraud Transaction
-- (Should trigger HIGH alert)
-- =========================================
INSERT INTO transactions (account_id, transaction_type, amount, location)
VALUES
(1, 'WITHDRAWAL', 120000, 'Delhi');

-- =========================================
-- 5. Odd Hour Transaction
-- (Force odd time manually)
-- =========================================
INSERT INTO transactions (account_id, transaction_type, amount, transaction_time, location)
VALUES
(2, 'WITHDRAWAL', 20000, '2026-04-13 02:30:00', 'Mumbai');

-- =========================================
-- 6. Frequent Transactions (Spam)
-- (Run multiple quickly)
-- =========================================
INSERT INTO transactions (account_id, transaction_type, amount, location)
VALUES
(3, 'WITHDRAWAL', 1000, 'Bangalore'),
(3, 'WITHDRAWAL', 1200, 'Bangalore'),
(3, 'WITHDRAWAL', 1500, 'Bangalore'),
(3, 'WITHDRAWAL', 1800, 'Bangalore');

-- =========================================
-- 7. Low Balance Case
-- =========================================
UPDATE accounts SET balance = 800 WHERE account_id = 4;

INSERT INTO transactions (account_id, transaction_type, amount, location)
VALUES
(4, 'WITHDRAWAL', 500, 'Lucknow');

-- =========================================
-- 8. Check Alerts
-- =========================================
SELECT * FROM alerts;

-- =========================================
-- 9. Check Accounts Status
-- =========================================
SELECT * FROM accounts;

-- =========================================
-- 10. Check Transactions
-- =========================================
SELECT * FROM transactions;