-- Create database schema for fraud detection system

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    risk_score FLOAT DEFAULT 0.0,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    amount FLOAT NOT NULL,
    merchant VARCHAR(200) NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location VARCHAR(200),
    device_id VARCHAR(100),
    ip_address VARCHAR(45),
    is_fraudulent BOOLEAN DEFAULT FALSE,
    fraud_score FLOAT DEFAULT 0.0,
    detection_method VARCHAR(100),
    raw_features JSONB,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_timestamp (timestamp)
);

-- Anomaly detections table
CREATE TABLE IF NOT EXISTS anomaly_detections (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    anomaly_type VARCHAR(50) NOT NULL,
    anomaly_score FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    is_confirmed BOOLEAN DEFAULT FALSE,
    features JSONB,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_timestamp (timestamp)
);

-- Phishing detections table
CREATE TABLE IF NOT EXISTS phishing_detections (
    id VARCHAR(36) PRIMARY KEY,
    email_subject VARCHAR(500),
    email_body TEXT,
    sender_email VARCHAR(100),
    recipient_email VARCHAR(100),
    phishing_score FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_phishing BOOLEAN DEFAULT FALSE,
    indicators JSONB,
    action_taken VARCHAR(100),
    INDEX idx_sender (sender_email),
    INDEX idx_recipient (recipient_email),
    INDEX idx_timestamp (timestamp)
);

-- Behavioral patterns table
CREATE TABLE IF NOT EXISTS behavioral_patterns (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    pattern_type VARCHAR(50) NOT NULL,
    metric VARCHAR(100),
    value FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    baseline FLOAT,
    deviation FLOAT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_timestamp (timestamp)
);

-- Network traffic table
CREATE TABLE IF NOT EXISTS network_traffic (
    id VARCHAR(36) PRIMARY KEY,
    source_ip VARCHAR(45),
    destination_ip VARCHAR(45),
    port INTEGER,
    protocol VARCHAR(20),
    packet_count INTEGER,
    byte_count INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    anomaly_score FLOAT DEFAULT 0.0,
    is_suspicious BOOLEAN DEFAULT FALSE,
    metadata JSONB,
    INDEX idx_source_ip (source_ip),
    INDEX idx_destination_ip (destination_ip),
    INDEX idx_timestamp (timestamp)
);

-- Model metrics table
CREATE TABLE IF NOT EXISTS model_metrics (
    id VARCHAR(36) PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50),
    accuracy FLOAT,
    precision FLOAT,
    recall FLOAT,
    f1_score FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    training_samples INTEGER,
    INDEX idx_model_name (model_name),
    INDEX idx_timestamp (timestamp)
);

-- Create indices for better query performance
CREATE INDEX IF NOT EXISTS idx_transactions_created_date ON transactions(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_anomaly_score ON anomaly_detections(anomaly_score DESC);
CREATE INDEX IF NOT EXISTS idx_phishing_score ON phishing_detections(phishing_score DESC);
CREATE INDEX IF NOT EXISTS idx_user_risk_score ON users(risk_score DESC);
