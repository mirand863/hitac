FROM python:3.8-slim

RUN pip install pandas==1.4 && \
    pip install seaborn==0.13.2 && \
    pip install matplotlib==3.8.3
