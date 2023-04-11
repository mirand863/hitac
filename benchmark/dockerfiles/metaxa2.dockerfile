FROM python:2.7-buster

ARG METAXA2=https://microbiology.se/sw/Metaxa2_2.2.3.tar.gz
ARG BLAST=https://ftp.ncbi.nlm.nih.gov/blast/executables/legacy.NOTSUPPORTED/2.2.26/blast-2.2.26-x64-linux.tar.gz
ARG HMMER=http://eddylab.org/software/hmmer/hmmer-3.1b2.tar.gz
ARG MAFFT=https://mafft.cbrc.jp/alignment/software/mafft-7.505-with-extensions-src.tgz
ARG USEARCH=https://www.drive5.com/downloads/usearch11.0.667_i86linux32.gz

ENV PATH "$PATH:/usr/bin/Metaxa2_2.2.3/"
ENV PATH "$PATH:/usr/bin/blast-2.2.26/bin/"

RUN wget --no-check-certificate $METAXA2 && \
    tar -xvzf Metaxa2_2.2.3.tar.gz -C /usr/bin && \
    rm Metaxa2_2.2.3.tar.gz && \
    wget $BLAST && \
    tar -xvzf blast-2.2.26-x64-linux.tar.gz -C /usr/bin && \
    rm blast-2.2.26-x64-linux.tar.gz && \
    wget $HMMER && \
    tar -xvzf hmmer-3.1b2.tar.gz && \
    rm hmmer-3.1b2.tar.gz && \
    cd hmmer-3.1b2 && \
    ./configure && \
    make && \
    make check && \
    make install && \
    cd .. && \
    rm -rf hmmer-3.1b2 && \
    wget --no-check-certificate $MAFFT && \
    tar -xvf mafft-7.505-with-extensions-src.tgz && \
    rm mafft-7.505-with-extensions-src.tgz && \
    cd mafft-7.505-with-extensions && \
    cd core && make clean && make && cd .. && \
    cd extensions && make clean && make && cd .. && \
    cd core && make install && cd .. && \
    cd extensions && make install && cd ../.. && \
    rm -rf mafft-7.505-with-extensions && \
    wget $USEARCH && \
    zcat usearch11.0.667_i86linux32.gz \
    > /usr/bin/usearch && \
    chmod +x /usr/bin/usearch && \
    rm usearch11.0.667_i86linux32.gz
