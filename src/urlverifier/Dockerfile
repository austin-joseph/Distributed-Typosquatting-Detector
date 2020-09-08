FROM python:3.7.7-buster

RUN pip3 install mysql-connector-python==8.0.18 && pip3 install requests==2.22.0 && pip3 install selenium==3.141.0

COPY urlverifier.py /usr/bin/dtd/

COPY run.sh /usr/bin/dtd/
RUN chmod +x /usr/bin/dtd/run.sh

COPY config.json /usr/bin/dtd/

WORKDIR /usr/bin/dtd
ENTRYPOINT ./run.sh
