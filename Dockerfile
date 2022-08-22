FROM python:3.7.4

RUN python -m pip install --upgrade pip

COPY ./requirements.txt /workout_manager/requirements.txt

WORKDIR /workout_manager

RUN pip3 install -r requirements.txt

COPY . /workout_manager

CMD [ "python3", "workout_manager/app.py" ]
