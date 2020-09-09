FROM mysql/mysql-server:8.0.3
COPY 00_setup_tables.sql /docker-entrypoint-initdb.d/
COPY 01_setup_auth.sql /docker-entrypoint-initdb.d/