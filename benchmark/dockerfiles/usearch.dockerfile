FROM python:2.7-buster

ARG USEARCH=https://www.drive5.com/downloads/usearch11.0.667_i86linux32.gz

RUN wget $USEARCH && \
    zcat usearch11.0.667_i86linux32.gz \
    > /usr/bin/usearch && \
    chmod +x /usr/bin/usearch \
