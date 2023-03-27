FROM python:2.7-buster

ARG SPINGO=https://github.com/GuyAllard/SPINGO/archive/refs/tags/v1.3.zip

ENV PATH "$PATH:/usr/bin/SPINGO-1.3/"

RUN wget $SPINGO \
    -O spingo-1.3.zip && \
    unzip spingo-1.3.zip -d /usr/bin && \
    rm spingo-1.3.zip
