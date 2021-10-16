# pull base image
FROM python:3.8

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work dir
WORKDIR /code

# install dependencies
COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system

# copy over files
COPY . /code/

# collect static files
RUN python manage.py collectstatic --noinput