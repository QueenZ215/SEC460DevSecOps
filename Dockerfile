FROM python:3.12-alpine

RUN apk update && apk upgrade --no-cache libcrypto3 libssl3

RUN adduser -D -u 1001 nightwatch

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R nightwatch:nightwatch /app

USER nightwatch
EXPOSE 5000
CMD ["python", "run.py"]