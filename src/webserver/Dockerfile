FROM python:3.7.7-buster

RUN pip3 install flask && pip3 install mysql-connector-python==8.0.18 && pip3 install waitress==1.4.4

COPY webserver.py /usr/bin/dtd/
COPY static /usr/bin/dtd/static
COPY run.sh /usr/bin/dtd
COPY config.json /usr/bin/dtd/

RUN chmod +x /usr/bin/dtd/run.sh

WORKDIR /usr/bin/dtd
ENTRYPOINT ./run.sh
