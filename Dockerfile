FROM debian:jessie

ENV http_proxy http://16.85.88.10:8080
ENV https_proxy http://16.85.88.10:8080

RUN apt update && \
    apt install -y python python-pip python-dev build-essential gfortran libatlas-base-dev

WORKDIR /scc5920

ENTRYPOINT pip install -r requirements.txt; python -m nltk.downloader all
