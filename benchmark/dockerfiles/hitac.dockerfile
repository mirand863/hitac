FROM quay.io/qiime2/core:2023.2

COPY ./ ./

RUN python -m pip install . --ignore-installed --no-deps -vv && \
pip install hiclass && \
pip install torch && \
pip install transformers && \
qiime dev refresh-cache
