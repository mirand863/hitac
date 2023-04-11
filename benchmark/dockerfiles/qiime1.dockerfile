FROM python:2.7-buster

ENV PATH "$PATH:/qiime_software/sourcetracker-1.0.0-release/."
ENV PATH "$PATH:/qiime_software/qiime-galaxy-0.0.1-repository-de3646d3/scripts"
ENV PATH "$PATH:/qiime_software/SeqPrep-v1.1-release/."
ENV PATH "$PATH:/qiime_software/cdhit-3.1-release/."
ENV PATH "$PATH:/qiime_software/rdpclassifier-2.2-release/."
ENV PATH "$PATH:/qiime_software/muscle-3.8.31-release/."
ENV PATH "$PATH:/qiime_software/infernal-1.0.2-release/bin"
ENV PATH "$PATH:/qiime_software/blast-2.2.22-release/bin"
ENV PATH "$PATH:/qiime_software/bwa-0.6.2-release/."
ENV PATH "$PATH:/qiime_software/mothur-1.25.0-release/."
ENV PATH "$PATH:/qiime_software/ea-utils-1.1.2-537-release/."
ENV PATH "$PATH:/qiime_software/vienna-1.8.4-release/."
ENV PATH "$PATH:/qiime_software/drisee-1.2-release/."
ENV PATH "$PATH:/qiime_software/raxml-7.3.0-release/."
ENV PATH "$PATH:/qiime_software/chimeraslayer-4.29.2010-release/ChimeraSlayer"
ENV PATH "$PATH:/qiime_software/chimeraslayer-4.29.2010-release/NAST-iEr"
ENV PATH "$PATH:/qiime_software/cytoscape-2.7.0-release/."
ENV PATH "$PATH:/qiime_software/rtax-0.984-release/."
ENV PATH "$PATH:/qiime_software/cdbtools-10.11.2010-release/."
ENV PATH "$PATH:/qiime_software/ampliconnoise-1.27-release/Scripts"
ENV PATH "$PATH:/qiime_software/ampliconnoise-1.27-release/bin"
ENV PATH "$PATH:/qiime_software/blat-34-release/."
ENV PATH "$PATH:/qiime_software/tax2tree-1.0-release/bin"
ENV PATH "$PATH:/qiime_software/pprospector-1.0.1-release/bin"
ENV PATH "$PATH:/qiime_software/clearcut-1.0.9-release/."

COPY qiime_software /qiime_software
COPY bin /usr/local/bin

RUN pip install numpy>=1.10 && \
    pip install qiime==1.9 \
    biom-format==2.1.7
