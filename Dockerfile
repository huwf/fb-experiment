FROM tiangolo/uwsgi-nginx-flask:flask-python3.5


ADD requirements.txt /requirements.txt
ADD app /app

RUN pip install -r /requirements.txt
