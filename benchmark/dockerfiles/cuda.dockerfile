FROM nvidia/cuda:11.2.2-runtime-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive
ARG MINIFORGE=https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge-pypy3-Linux-x86_64.sh

RUN apt-get update -y && \
    apt-get install snakemake wget -y && \
    wget $MINIFORGE && \
    bash Miniforge-pypy3-Linux-x86_64.sh -b && \
    /root/miniforge-pypy3/bin/conda init