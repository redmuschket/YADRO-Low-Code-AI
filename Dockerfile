FROM ubuntu:latest
LABEL authors="popbo"

ENTRYPOINT ["top", "-b"]