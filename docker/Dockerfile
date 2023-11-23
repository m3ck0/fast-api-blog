FROM python:3.12.0-alpine3.18

WORKDIR /app

COPY ./src/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./src/db.py db.py
COPY ./src/main.py main.py
COPY ./src/models.py models.py
COPY ./src/worker worker

CMD uvicorn main:app --host 0.0.0.0

# docker build -f docker/Dockerfile -t fast_api_blog:latest .
# docker run -e "MONGODB_CS=<mongodb_cs>" fast_api_blog:latest
