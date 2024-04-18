FROM nvidia/cuda:11.2.2-runtime-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

COPY ./ ./

RUN apt-get update -y && \
    apt-get install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install python3.9 python3.9-distutils snakemake curl -y && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.9 get-pip.py
