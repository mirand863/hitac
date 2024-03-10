FROM python:3.8-buster

RUN pip install scikit-learn && \
    pip install pandas && \
    pip install hiclass
