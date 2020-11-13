docker build -t dtd-database .
docker create -p 3306:3306 --name dtd-database -e MYSQL_ROOT_PASSWORD=mysql --network dtd-network -v /var/lib/mysql:/dtd-mysql/datadir dtd-database