FROM python:3.11.1

WORKDIR /home/django_js

RUN addgroup --system developers \
	&& adduser --system --no-create-home --ingroup developers backend \
	&& chown -R backend:developers /home/django_js

RUN apt-get update \
	&& apt-get install -y nano

COPY requirements.txt ./

RUN pip install -r requirements.txt

USER backend

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]