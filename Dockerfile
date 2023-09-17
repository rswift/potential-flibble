FROM python:3.11.5-alpine

RUN apk update && apk upgrade && apk add curl

RUN addgroup user && adduser -G user -D user user

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./app /app
RUN mkdir -p /usr/local/var/log && chown user:user /usr/local/var/log

EXPOSE 8080
USER user

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--log-config", "/app/logging.ini"]
