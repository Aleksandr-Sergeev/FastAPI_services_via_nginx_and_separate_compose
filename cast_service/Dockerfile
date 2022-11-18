FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

#RUN pip install --upgrade pip && pip install -r /app/requirements.txt \
#    && rm -rf /root/.cache/pip
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
RUN rm -rf /root/.cache/pip

COPY . /app/