CREATE USER 'dtd-webserver'@'%' IDENTIFIED BY 'dtd-webserver';
GRANT ALL PRIVILEGES ON dtd.* TO 'dtd-webserver'@'%';

CREATE USER 'dtd-typogenerator'@'%' IDENTIFIED BY 'dtd-typogenerator';
GRANT ALL PRIVILEGES ON dtd.* TO 'dtd-typogenerator'@'%';

CREATE USER 'dtd-urlverifier'@'%' IDENTIFIED BY 'dtd-urlverifier';
GRANT ALL PRIVILEGES ON dtd.* TO 'dtd-urlverifier'@'%';

FLUSH PRIVILEGES;
