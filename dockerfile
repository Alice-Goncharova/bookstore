FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERD = 1

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
