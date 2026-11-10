-- Issue Tracker schema (MySQL 8.0.13+)
-- Usage:
--   mysql -u <user> -p -e "CREATE DATABASE issue_tracker_db"
--   mysql -u <user> -p issue_tracker_db < schema.sql

CREATE TABLE developer (
  developer_id INT NOT NULL AUTO_INCREMENT,
  username     VARCHAR(20) NOT NULL,
  first_name   VARCHAR(20) NOT NULL,
  last_name    VARCHAR(20) DEFAULT NULL,
  PRIMARY KEY (developer_id),
  UNIQUE KEY username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE issue (
  issue_id      INT NOT NULL AUTO_INCREMENT,
  title         VARCHAR(255) NOT NULL,
  posible_cause VARCHAR(255) DEFAULT NULL,
  creation_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  close_date    DATETIME DEFAULT NULL,
  status        VARCHAR(20) NOT NULL DEFAULT 'open',
  priority      INT NOT NULL,
  developer_id  INT DEFAULT NULL,
  PRIMARY KEY (issue_id),
  KEY developer_id (developer_id),
  CONSTRAINT issue_ibfk_1 FOREIGN KEY (developer_id) REFERENCES developer (developer_id),
  CONSTRAINT issue_chk_status CHECK (status IN ('open', 'in_progress', 'closed')),
  CONSTRAINT issue_chk_priority CHECK (priority BETWEEN 1 AND 3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
