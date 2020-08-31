FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3.7 && apt-get install -y python3-pip

RUN pip3 install flask && pip3 install mysql-connector-python==8.0.18 && pip3 install waitress

COPY webserver.py /usr/bin/dtd/
COPY static /usr/bin/dtd/static
COPY run.sh /usr/bin/dtd
COPY config.json /usr/bin/dtd/

RUN chmod +x /usr/bin/dtd/run.sh

WORKDIR /usr/bin/dtd
ENTRYPOINT ./run.sh
