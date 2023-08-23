FROM continuumio/miniconda3:22.11.1-alpine

COPY BioAutoML /BioAutoML

ENV PATH "$PATH:/BioAutoML"

RUN conda env update --name base --file /BioAutoML/BioAutoML-env.yml --prune
