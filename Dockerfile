# pull official base image
FROM python:3.7-alpine

# set work directory
WORKDIR /usr/src/Datefix

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add --no-cache libressl-dev musl-dev libffi-dev

RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

RUN python manage.py collectstatic --noinput