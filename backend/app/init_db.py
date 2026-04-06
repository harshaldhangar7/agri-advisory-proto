#!/usr/bin/env python3
"""
init_db.py

Simple MySQL initialization script for the Agri Advisory prototype.
- Creates database `agri` if missing
- Creates a dedicated DB user (optional)
- Creates core tables if missing
- Inserts a small seed row for quick testing

Usage (PowerShell / CMD):
    python init_db.py
Or set env vars first:
    set DATABASE_HOST=localhost
    set DATABASE_PORT=3306
    set DATABASE_ROOT_USER=root
    set DATABASE_ROOT_PASS=your_root_pass
    python init_db.py
"""

import os
import getpass
import pymysql
from pymysql.constants import CLIENT

# Read connection info from environment or prompt
DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_PORT = int(os.getenv("DATABASE_PORT", "3306"))
ROOT_USER = os.getenv("DATABASE_ROOT_USER", "root")
ROOT_PASS = os.getenv("DATABASE_ROOT_PASS") or None

APP_DB = os.getenv("APP_DB", "agri")
APP_USER = os.getenv("APP_DB_USER", "agriuser")
APP_PASS = os.getenv("APP_DB_PASS", "your_password")  # change before running in production

if ROOT_PASS is None:
    try:
        ROOT_PASS = getpass.getpass(f"Enter MySQL password for user '{ROOT_USER}': ")
    except Exception:
        ROOT_PASS = ""

# SQL statements to run (safe: IF NOT EXISTS checks)
SQL_STATEMENTS = f"""
-- Create database
CREATE DATABASE IF NOT EXISTS `{APP_DB}`
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- Create app user (if not exists) and grant privileges
CREATE USER IF NOT EXISTS '{APP_USER}'@'localhost' IDENTIFIED BY '{APP_PASS}';
GRANT ALL PRIVILEGES ON `{APP_DB}`.* TO '{APP_USER}'@'localhost';
FLUSH PRIVILEGES;

USE `{APP_DB}`;

-- Farmers table
CREATE TABLE IF NOT EXISTS farmers (
  id CHAR(36) NOT NULL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  phone VARCHAR(32),
  language VARCHAR(8) DEFAULT 'mr',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Plots table
CREATE TABLE IF NOT EXISTS plots (
  id CHAR(36) NOT NULL PRIMARY KEY,
  farmer_id CHAR(36) NOT NULL,
  name VARCHAR(200) NOT NULL,
  area_hectares DECIMAL(8,3) DEFAULT 0.0,
  crop VARCHAR(100),
  sowing_date DATE NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_plots_farmer FOREIGN KEY (farmer_id) REFERENCES farmers(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Advisory requests
CREATE TABLE IF NOT EXISTS advisory_requests (
  id CHAR(36) NOT NULL PRIMARY KEY,
  farmer_id CHAR(36) NULL,
  plot_id CHAR(36) NULL,
  source ENUM('ivr','whatsapp','agent','web','other') DEFAULT 'web',
  transcript TEXT,
  symptoms TEXT,
  weather_json JSON NULL,
  status ENUM('new','processed','review','rejected') DEFAULT 'new',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  processed_at TIMESTAMP NULL,
  CONSTRAINT fk_advisory_farmer FOREIGN KEY (farmer_id) REFERENCES farmers(id) ON DELETE SET NULL,
  CONSTRAINT fk_advisory_plot FOREIGN KEY (plot_id) REFERENCES plots(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Advisory responses
CREATE TABLE IF NOT EXISTS advisory_responses (
  id CHAR(36) NOT NULL PRIMARY KEY,
  request_id CHAR(36) NOT NULL,
  responder ENUM('system','agent','expert') DEFAULT 'system',
  response_text TEXT,
  response_json JSON NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_response_request FOREIGN KEY (request_id) REFERENCES advisory_requests(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Audit log
CREATE TABLE IF NOT EXISTS audit_log (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  entity_type VARCHAR(50),
  entity_id VARCHAR(64),
  action VARCHAR(100),
  payload JSON NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Indexes
CREATE INDEX IF NOT EXISTS idx_farmers_phone ON farmers(phone);
CREATE INDEX IF NOT EXISTS idx_plots_farmer ON plots(farmer_id);
CREATE INDEX IF NOT EXISTS idx_advisory_status ON advisory_requests(status);
CREATE INDEX IF NOT EXISTS idx_advisory_created ON advisory_requests(created_at);
"""

SEED_SQL = """
-- Insert a sample farmer if none exists
INSERT INTO farmers (id, name, phone, language)
SELECT UUID(), 'Ram', '+9198xxxxxx', 'mr'
WHERE NOT EXISTS (SELECT 1 FROM farmers LIMIT 1);

-- Insert a sample plot for the first farmer if none exists
SET @first_farmer = (SELECT id FROM farmers LIMIT 1);
INSERT INTO plots (id, farmer_id, name, area_hectares, crop)
SELECT UUID(), @first_farmer, 'Sample Plot', 1.0, 'tomato'
WHERE @first_farmer IS NOT NULL
  AND NOT EXISTS (SELECT 1 FROM plots WHERE farmer_id = @first_farmer LIMIT 1);
"""

def run_sql(connection, sql):
    """Execute multiple SQL statements safely."""
    # pymysql's cursor.execute can only run one statement at a time unless multi=True is used.
    # We'll split by semicolon while preserving JSON/ENUM content (simple approach).
    # Use connection.cursor().execute for each statement.
    statements = [s.strip() for s in sql.split(';') if s.strip()]
    with connection.cursor() as cur:
        for stmt in statements:
            try:
                cur.execute(stmt)
            except Exception as e:
                # Some statements (like CREATE INDEX IF NOT EXISTS) may not be supported by older MySQL versions.
                # Print and continue.
                print(f"[WARN] Statement failed (continuing): {e}\nStatement: {stmt[:120]}...")
        connection.commit()

def main():
    print("Connecting to MySQL as root user...")
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=ROOT_USER,
            password=ROOT_PASS,
            charset='utf8mb4',
            client_flag=CLIENT.MULTI_STATEMENTS
        )
    except Exception as e:
        print("Failed to connect to MySQL:", e)
        return

    try:
        print("Running initialization SQL...")
        run_sql(conn, SQL_STATEMENTS)
        print("Creating seed data...")
        # Need to switch to the app DB before running seed
        conn.select_db(APP_DB)
        run_sql(conn, SEED_SQL)
        print("Initialization complete. Database:", APP_DB)
        print(f"App DB user: {APP_USER} (password: {APP_PASS})")
    finally:
        conn.close()

if __name__ == "__main__":
    main()