FROM continuumio/miniconda3:22.11.1-alpine

RUN conda install \
    -c conda-forge \
    -c bioconda \
    -y \
    mothur=1.48.0
