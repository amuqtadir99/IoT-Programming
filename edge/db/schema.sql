-- Smart Room Guardian — MariaDB schema
-- SWE30011 IoT Programming — Assignment 2
--
-- IMPORTANT: change 'CHANGE_ME' below to your own password before running,
-- and use the same password in edge/config.py.
--
-- Run as:  sudo mysql -u root -p < edge/db/schema.sql

CREATE DATABASE IF NOT EXISTS iot_project;
USE iot_project;

-- One row per reading received from the Arduino IoT Node.
CREATE TABLE IF NOT EXISTS readings (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    temperature   FLOAT NOT NULL,
    door_tilt     TINYINT NOT NULL,   -- 0 = closed/level, 1 = open/tilted
    fan_state     TINYINT NOT NULL,   -- actuator state decided this cycle
    alarm_state   TINYINT NOT NULL,   -- actuator state decided this cycle
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Single-row table holding the live automation rule + manual overrides.
CREATE TABLE IF NOT EXISTS settings (
    id              INT PRIMARY KEY,
    temp_threshold  FLOAT NOT NULL DEFAULT 30.0,
    fan_override    ENUM('AUTO','ON','OFF') NOT NULL DEFAULT 'AUTO',
    alarm_override  ENUM('AUTO','ON','OFF') NOT NULL DEFAULT 'AUTO',
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO settings (id, temp_threshold, fan_override, alarm_override)
VALUES (1, 30.0, 'AUTO', 'AUTO')
ON DUPLICATE KEY UPDATE id = id;

-- Dedicated application account (don't use root from the Python scripts).
CREATE USER IF NOT EXISTS 'iot_user'@'localhost' IDENTIFIED BY 'CHANGE_ME';
GRANT ALL PRIVILEGES ON iot_project.* TO 'iot_user'@'localhost';
FLUSH PRIVILEGES;
