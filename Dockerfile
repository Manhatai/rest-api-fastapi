FROM python:3.12

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /logs

COPY . .

CMD ["fastapi", "run", "main.py", "--port", "8000"]