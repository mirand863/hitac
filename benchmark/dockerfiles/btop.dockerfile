FROM python:3.8-buster

ARG BLAST=https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.10.1/ncbi-blast-2.10.1+-x64-linux.tar.gz

ENV PATH "$PATH:/usr/bin/ncbi-blast-2.10.1+/bin/"

RUN wget $BLAST && \
    tar -xvzf ncbi-blast-2.10.1+-x64-linux.tar.gz \
    -C /usr/bin && \
    rm ncbi-blast-2.10.1+-x64-linux.tar.gz && \
    pip install biopython==1.72 \
    pandas==1.4.3
