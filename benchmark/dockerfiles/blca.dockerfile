FROM python:2.7-buster

ARG BLCA=https://github.com/qunfengdong/BLCA/archive/refs/tags/v2.3-alpha.tar.gz

RUN wget $BLCA && \
    tar -xvzf v2.3-alpha.tar.gz && \
    pip install biopython==1.72 && \
    wget http://www.clustal.org/omega/clustalo-1.2.4-Ubuntu-x86_64 \
    -O /usr/bin/clustalo && \
    chmod +x /usr/bin/clustalo \
