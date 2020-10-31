echo "Building container dtd-webserver"
docker build -t dtd-webserver .
docker create --network dtd-network -p 4001:8080 --name dtd-webserver dtd-webserver