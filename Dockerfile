FROM python:3.12-slim

RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /postify-app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY postify-app/ .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]