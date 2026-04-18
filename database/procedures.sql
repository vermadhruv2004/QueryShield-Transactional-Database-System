-- =========================================
-- QueryShield Stored Procedures
-- =========================================

USE queryshield;

DELIMITER $$

-- =========================================
-- 1. Deposit Money
-- =========================================
CREATE PROCEDURE deposit_money (
    IN p_account_id INT,
    IN p_amount DECIMAL(12,2)
)
BEGIN
    -- Update balance
    UPDATE accounts
    SET balance = balance + p_amount
    WHERE account_id = p_account_id;

    -- Insert transaction
    INSERT INTO transactions (account_id, transaction_type, amount)
    VALUES (p_account_id, 'DEPOSIT', p_amount);
END$$


-- =========================================
-- 2. Withdraw Money
-- =========================================
CREATE PROCEDURE withdraw_money (
    IN p_account_id INT,
    IN p_amount DECIMAL(12,2)
)
BEGIN
    DECLARE current_balance DECIMAL(12,2);

    SELECT balance INTO current_balance
    FROM accounts
    WHERE account_id = p_account_id;

    IF current_balance >= p_amount THEN
        
        -- Deduct balance
        UPDATE accounts
        SET balance = balance - p_amount
        WHERE account_id = p_account_id;

        -- Insert transaction
        INSERT INTO transactions (account_id, transaction_type, amount)
        VALUES (p_account_id, 'WITHDRAWAL', p_amount);

    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Insufficient Balance';
    END IF;
END$$


-- =========================================
-- 3. Transfer Money
-- =========================================
CREATE PROCEDURE transfer_money (
    IN p_from_account INT,
    IN p_to_account INT,
    IN p_amount DECIMAL(12,2)
)
BEGIN
    DECLARE sender_balance DECIMAL(12,2);

    SELECT balance INTO sender_balance
    FROM accounts
    WHERE account_id = p_from_account;

    IF sender_balance >= p_amount THEN
        
        -- Deduct from sender
        UPDATE accounts
        SET balance = balance - p_amount
        WHERE account_id = p_from_account;

        -- Add to receiver
        UPDATE accounts
        SET balance = balance + p_amount
        WHERE account_id = p_to_account;

        -- Record transactions
        INSERT INTO transactions (account_id, transaction_type, amount)
        VALUES (p_from_account, 'TRANSFER', p_amount);

        INSERT INTO transactions (account_id, transaction_type, amount)
        VALUES (p_to_account, 'DEPOSIT', p_amount);

    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Transfer Failed: Insufficient Balance';
    END IF;
END$$


-- =========================================
-- 4. Get Account Details
-- =========================================
CREATE PROCEDURE get_account_details (
    IN p_account_id INT
)
BEGIN
    SELECT a.account_id, c.name, a.account_type, a.balance, a.status
    FROM accounts a
    JOIN customers c ON a.customer_id = c.customer_id
    WHERE a.account_id = p_account_id;
END$$


-- =========================================
-- 5. Get Fraud Alerts for an Account
-- =========================================
CREATE PROCEDURE get_alerts_by_account (
    IN p_account_id INT
)
BEGIN
    SELECT *
    FROM alerts
    WHERE account_id = p_account_id
    ORDER BY created_at DESC;
END$$


-- =========================================
-- 6. Resolve Alert
-- =========================================
CREATE PROCEDURE resolve_alert (
    IN p_alert_id INT
)
BEGIN
    UPDATE alerts
    SET status = 'RESOLVED'
    WHERE alert_id = p_alert_id;
END$$

DELIMITER ;