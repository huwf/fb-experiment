FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

RUN wget https://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-2.1.6.tar.gz
RUN tar -zxvf mysql-connector-python-2.1.6.tar.gz
WORKDIR mysql-connector-python-2.1.6
RUN ls -al

RUN python3 setup.py build
RUN python3 setup.py install

ADD requirements.txt /requirements.txt
ADD app /app
WORKDIR /app
RUN pip install -r /requirements.txt

WORKDIR /
ADD wait-for-it.sh ./wait-for-it
