docker build -t dtd-webserver .
docker create --network dtd-network -p 4000:8080 --name dtd-webserver dtd-webserver
