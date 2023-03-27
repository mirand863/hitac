FROM r-base:4.1.0

RUN R -e "install.packages('microseq', repos='http://cran.rstudio.com/', dependencies = TRUE)" && \
    R -e "install.packages('microclass', repos='http://cran.rstudio.com/', dependencies = TRUE)"
