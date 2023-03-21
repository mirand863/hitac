FROM python:2.7-buster

ARG BLCA=https://github.com/qunfengdong/BLCA/archive/refs/tags/v2.3-alpha.tar.gz

RUN wget $BLCA && \
tar -xvzf v2.3-alpha.tar.gz
