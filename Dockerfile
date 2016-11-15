FROM debian:jessie

RUN apt update && \
    apt install -y python python-pip python-dev build-essential gfortran libatlas-base-dev

WORKDIR /scc5920

COPY requirements.txt /scc5920

RUN pip install -r requirements.txt #&& \
	#   	python -m nltk.downloader all
