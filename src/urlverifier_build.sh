docker rm dtd-urlverifier
docker build -t dtd-urlverifier .
docker create --name dtd-urlverifier dtd-urlverifier
