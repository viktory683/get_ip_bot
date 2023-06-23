FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG BOT_TOKEN
ENV BOT_TOKEN=$BOT_TOKEN

ARG ADMINS
ENV ADMINS=$ADMINS

CMD ["python", "bot.py"]