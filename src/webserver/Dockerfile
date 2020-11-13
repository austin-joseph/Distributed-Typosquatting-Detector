FROM python:3.7.7-buster

RUN pip3 install flask==1.1.2 && pip3 install mysql-connector-python==8.0.18 && pip3 install waitress==1.4.4 && pip3 install python-json-logger==2.0.1

RUN mkdir -p /usr/bin/dtd/logs

COPY run.sh /usr/bin/dtd
RUN chmod +x /usr/bin/dtd/run.sh

COPY config.json /usr/bin/dtd/
COPY static /usr/bin/dtd/static
COPY webserver.py /usr/bin/dtd/


WORKDIR /usr/bin/dtd
ENTRYPOINT ./run.sh
