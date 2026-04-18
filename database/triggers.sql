-- =========================================
-- QueryShield Fraud Detection Triggers
-- =========================================

USE queryshield;

DELIMITER $$

-- =========================================
-- 1. High Amount Transaction Trigger
-- =========================================
CREATE TRIGGER trg_high_amount
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    IF NEW.amount > 50000 THEN
        INSERT INTO alerts (transaction_id, account_id, alert_type, severity)
        VALUES (NEW.transaction_id, NEW.account_id, 'High Amount Transaction', 'HIGH');
    END IF;
END$$


-- =========================================
-- 2. Odd Hour Transaction Trigger
-- =========================================
CREATE TRIGGER trg_odd_hour
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    IF HOUR(NEW.transaction_time) < 6 OR HOUR(NEW.transaction_time) > 23 THEN
        INSERT INTO alerts (transaction_id, account_id, alert_type, severity)
        VALUES (NEW.transaction_id, NEW.account_id, 'Odd Hour Transaction', 'MEDIUM');
    END IF;
END$$


-- =========================================
-- 3. Frequent Transactions Trigger
-- (More than 3 transactions in 1 minute)
-- =========================================
CREATE TRIGGER trg_frequent_txn
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    DECLARE txn_count INT;

    SELECT COUNT(*) INTO txn_count
    FROM transactions
    WHERE account_id = NEW.account_id
      AND transaction_time >= NOW() - INTERVAL 1 MINUTE;

    IF txn_count > 3 THEN
        INSERT INTO alerts (transaction_id, account_id, alert_type, severity)
        VALUES (NEW.transaction_id, NEW.account_id, 'Frequent Transactions', 'MEDIUM');
    END IF;
END$$


-- =========================================
-- 4. Low Balance After Withdrawal Trigger
-- =========================================
CREATE TRIGGER trg_low_balance
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    DECLARE current_balance DECIMAL(12,2);

    IF NEW.transaction_type = 'WITHDRAWAL' THEN
        SELECT balance INTO current_balance
        FROM accounts
        WHERE account_id = NEW.account_id;

        IF current_balance < 1000 THEN
            INSERT INTO alerts (transaction_id, account_id, alert_type, severity)
            VALUES (NEW.transaction_id, NEW.account_id, 'Low Balance After Withdrawal', 'LOW');
        END IF;
    END IF;
END$$


-- =========================================
-- 5. Auto Block Account for High Risk
-- =========================================
CREATE TRIGGER trg_block_account
AFTER INSERT ON alerts
FOR EACH ROW
BEGIN
    IF NEW.severity = 'HIGH' THEN
        UPDATE accounts
        SET status = 'BLOCKED'
        WHERE account_id = NEW.account_id;
    END IF;
END$$

DELIMITER ;