FROM quay.io/qiime2/core:2023.2

COPY ./ src

RUN cd src && \
python -m pip install . --ignore-installed --no-deps -vv && \
pip install hiclass
