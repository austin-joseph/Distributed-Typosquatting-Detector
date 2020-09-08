echo "Building container dtd-urlverifier"
docker build -t dtd-urlverifier .
docker create --network dtd-network --name dtd-urlverifier dtd-urlverifier