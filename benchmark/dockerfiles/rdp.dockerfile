FROM openjdk:21-buster

ARG RDP=https://zenodo.org/record/6950218/files/rdp_classifier_2.13.zip?download=1

RUN wget $RDP \
    -O rdp_classifier_2.13.zip && \
    unzip rdp_classifier_2.13.zip \
    -d /usr/bin && \
    rm rdp_classifier_2.13.zip
