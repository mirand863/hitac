FROM quay.io/qiime2/core:2023.2

COPY ./ ./

RUN python -m pip install . --ignore-installed --no-deps -vv && \
pip install hiclass
