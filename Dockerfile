FROM python:3.11.1

# ENV PYTHONUNBUFFERED=1 # logs immediately incase of crash

WORKDIR /home/django_js

RUN addgroup --system developers \
	&& adduser --system --no-create-home --ingroup developers backend \
	&& chown -R backend:developers /home

RUN apt-get update \
	&& apt-get install -y nano

COPY requirements.txt ./

RUN pip install -r requirements.txt

USER backend

COPY . .