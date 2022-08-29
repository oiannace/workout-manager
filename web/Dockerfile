FROM python:3.7.4

WORKDIR /web

RUN apt-get update && apt-get install -y netcat

RUN python -m pip install --upgrade pip
COPY ./requirements.txt /web/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /web

ENTRYPOINT ["/web/db_wait.sh"]

