FROM python:3.7.4

RUN python -m pip install --upgrade pip

COPY ./requirements.txt /workout_manager/requirements.txt

WORKDIR /workout_manager

RUN pip3 install -r requirements.txt

COPY . /workout_manager

ENTRYPOINT [ "python3" ]

CMD [ "workout_manager/app.py" ]
