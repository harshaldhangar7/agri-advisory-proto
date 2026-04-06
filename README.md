# Agri Advisory Prototype

## Overview
Prototype with:
- Backend: FastAPI + SQLModel (MySQL)
- Frontend: React (Vite)

## Prerequisites (Windows)
- Python 3.10+ (in PATH)
- Node 18+ and npm
- MySQL Server installed and running
- PowerShell

## Setup steps (PowerShell)

1. Create database and user in MySQL (use MySQL Shell or Workbench):
   ```sql
   CREATE DATABASE agri CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'agriuser'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON agri.* TO 'agriuser'@'localhost';
   FLUSH PRIVILEGES;