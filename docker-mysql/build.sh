docker build -t dtd-mysql .
docker create -p 3306:3306 --name dtd-mysql -e MYSQL_ROOT_PASSWORD=mysql --network dtd-network -v /var/lib/mysql:/dtd-mysql/datadir dtd-mysql