echo "Building container dtd-typogenerator"
docker build -t dtd-typogenerator .
docker create --network dtd-network --name dtd-typogenerator dtd-typogenerator