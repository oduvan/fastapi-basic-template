-- Create test database if it doesn't exist
SELECT 'CREATE DATABASE fastapi_db_test'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'fastapi_db_test')\gexec
