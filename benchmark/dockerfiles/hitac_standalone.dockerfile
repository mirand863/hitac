FROM python:3.8-buster

COPY ./ ./

RUN python -m pip install . --ignore-installed --no-deps -vv && \
pip install hiclass
