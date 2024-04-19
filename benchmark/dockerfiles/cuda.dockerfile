FROM nvidia/cuda:11.2.2-runtime-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive
ARG MINIFORGE=https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge-pypy3-Linux-x86_64.sh
ARG SINGULARITY=https://github.com/sylabs/singularity.git
ARG GO=https://dl.google.com/go/go1.21.9.linux-amd64.tar.gz

RUN apt-get update -y && \
    apt-get install wget -y && \
    wget $MINIFORGE && \
    bash Miniforge-pypy3-Linux-x86_64.sh -b && \
    /root/miniforge-pypy3/bin/conda init && \
    /root/miniforge-pypy3/bin/conda create \
        -c conda-forge -c bioconda -n snakemake \
        snakemake=5.32.2 -y && \
    /root/miniforge-pypy3/bin/conda config --set channel_priority flexible && \
    echo "conda activate snakemake" >> ~/.bashrc && \
    apt-get update && \
    apt-get install -y \
        autoconf \
        automake \
        cryptsetup \
        fuse2fs \
        git \
        fuse \
        libfuse-dev \
        libglib2.0-dev \
        libseccomp-dev \
        libtool \
        pkg-config \
        runc \
        squashfs-tools \
        squashfs-tools-ng \
        uidmap \
        wget \
        zlib1g-dev \
        build-essential && \
    wget -O /tmp/go.tar.gz $GO && \
    tar -C /usr/local -xzf /tmp/go.tar.gz && \
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc && \
    git clone --recurse-submodules $SINGULARITY /tmp/singularity && \
    export PATH=$PATH:/usr/local/go/bin && \
    cd /tmp/singularity && \
    git checkout --recurse-submodules v4.1.2 && \
    ./mconfig && \
    make -C builddir && \
    make -C builddir install
