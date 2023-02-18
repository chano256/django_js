FROM python:3.11.1

WORKDIR /home/django_js

RUN addgroup --system developers \
	&& adduser --system --no-create-home --ingroup developers backend

# Copy permissions 777
COPY --chown=backend:developers . /home/django_js
RUN chown -R backend:developers /home/django_js 

RUN apt-get update \
	&& apt-get install -y nano

COPY requirements.txt ./

RUN pip install -r requirements.txt

USER backend

COPY . .

# ENTRYPOINT [ "entrypoint.sh" ]