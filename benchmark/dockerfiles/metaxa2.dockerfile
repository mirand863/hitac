FROM python:2.7-buster

ARG METAXA2=https://microbiology.se/sw/Metaxa2_2.2.3.tar.gz

ENV PATH "$PATH:/usr/bin/Metaxa2_2.2.3/"

RUN wget --no-check-certificate $METAXA2 && \
    tar -xvzf Metaxa2_2.2.3.tar.gz -C /usr/bin
