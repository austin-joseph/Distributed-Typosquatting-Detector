docker rm dtd-mysql
docker build -t dtd-mysql .
docker create --name dtd-mysql -e MYSQL_ROOT_PASSWORD=mysql --network dtd-network -v /var/lib/mysql:/dtd-mysql/datadir dtd-mysql