FROM python:3.8.7-slim

EXPOSE 8000
# set work directory
WORKDIR /app/

# set environment variables
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /app/requirements.txt

# copy project
COPY . /app/
RUN pip install -e .