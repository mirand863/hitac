FROM qiime2/core:2020.2

COPY hitac.tar.gz hitac.tar.gz

RUN pip install tqdm && \
tar -xvzf hitac.tar.gz && \
cd hitac && \
python setup.py install && \
cd .. && \
rm -rf hitac.tar.gz hitac
