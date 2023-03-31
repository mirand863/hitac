FROM python:2.7-buster

ARG METAXA2=https://microbiology.se/sw/Metaxa2_2.2.3.tar.gz
ARG BLAST=https://ftp.ncbi.nlm.nih.gov/blast/executables/legacy.NOTSUPPORTED/2.2.26/blast-2.2.26-x64-linux.tar.gz

ENV PATH "$PATH:/usr/bin/Metaxa2_2.2.3/"
ENV PATH "$PATH:/usr/bin/blast-2.2.26/bin/"

RUN wget --no-check-certificate $METAXA2 && \
    tar -xvzf Metaxa2_2.2.3.tar.gz -C /usr/bin && \
    wget $BLAST && \
    tar -xvzf blast-2.2.26-x64-linux.tar.gz -C /usr/bin
