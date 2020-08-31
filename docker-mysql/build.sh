docker build -t dtd-mysql .
docker rm dtd-mysql
docker create --name dtd-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=mysql --network dtd-network -v /var/lib/mysql:/home/austin/mysql/dtd-mysql/datadir dtd-mysql
