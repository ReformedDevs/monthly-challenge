FROM python:alpine
MAINTAINER Ian S. Pringle <ian@dapringles.com>
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "collector.py"]
