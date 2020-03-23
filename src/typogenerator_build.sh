docker rm dtd
docker build -t dtd .
docker create --publish 80:80 --name dtd dtd
