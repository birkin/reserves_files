## syntax=docker/dockerfile:1

FROM python:3.8.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /container_project_stuff/code
RUN mkdir /container_project_stuff/logs
RUN mkdir /container_project_stuff/DB

## set up the python environment
COPY ./config/requirements.txt /container_project_stuff/code/
RUN pip install -r ./requirements.txt  
