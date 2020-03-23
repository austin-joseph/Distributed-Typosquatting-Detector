docker rm dtd-webserver
docker build -t dtd-webserver .
docker create --publish 80:80 --name dtd-webserver dtd-webserver
