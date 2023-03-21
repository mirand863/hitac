FROM python:2.7-buster

ARG BLCA=https://github.com/qunfengdong/BLCA/archive/refs/tags/v2.3-alpha.tar.gz
ARG CLUSTALO=http://www.clustal.org/omega/clustalo-1.2.4-Ubuntu-x86_64
ARG BLAST=https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.10.1/ncbi-blast-2.10.1+-x64-linux.tar.gz

ENV PATH "$PATH:/usr/bin/BLCA-2.3-alpha/"
ENV PATH "$PATH:/usr/bin/ncbi-blast-2.10.1+/bin/"

RUN wget $BLCA && \
    tar -xvzf v2.3-alpha.tar.gz -C /usr/bin && \
    rm v2.3-alpha.tar.gz && \
    pip install biopython==1.72 && \
    wget $CLUSTALO -O /usr/bin/clustalo && \
    chmod +x /usr/bin/clustalo && \
    wget $BLAST && \
    tar -xvzf ncbi-blast-2.10.1+-x64-linux.tar.gz \
    -C /usr/bin && \
    rm ncbi-blast-2.10.1+-x64-linux.tar.gz
