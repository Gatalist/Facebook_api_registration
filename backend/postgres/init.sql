CREATE DATABASE postgres_drf;
CREATE USER system_01 WITH PASSWORD 'hsNd*eC5hUxE26nD';
ALTER ROLE system_01 SET client_encoding TO 'utf8';
ALTER ROLE system_01 SET default_transaction_isolation TO 'read committed';
ALTER ROLE system_01 SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE postgres_drf TO system_01;
GRANT ALL PRIVILEGES ON SCHEMA public TO system_01;
