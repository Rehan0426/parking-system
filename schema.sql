CREATE DATABASE IF NOT EXISTS parking_system;
USE parking_system;

CREATE TABLE IF NOT EXISTS slots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    number VARCHAR(10) NOT NULL,
    type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'Available'
);

CREATE TABLE IF NOT EXISTS records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plate VARCHAR(20) NOT NULL,
    slot_id INT,
    slot_number VARCHAR(10),
    type VARCHAR(20),
    owner VARCHAR(100),
    phone VARCHAR(20),
    entry_time DATETIME,
    exit_time DATETIME NULL,
    hours INT,
    amount INT,
    FOREIGN KEY (slot_id) REFERENCES slots(id)
);

CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    record_id INT,
    plate VARCHAR(20),
    amount INT,
    method VARCHAR(20),
    time DATETIME,
    FOREIGN KEY (record_id) REFERENCES records(id)
);
