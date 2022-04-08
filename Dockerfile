FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN pip install django
RUN pip install Pillow

ENDPOINT ["python3", "manage.py", "runserver"]