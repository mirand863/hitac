FROM r-base:4.3.2

RUN apt-get update && \
    apt-get install -y curl \
    libssl-dev \
    libcurl4-openssl-dev \
    libfontconfig1-dev \
    libxml2 \
    libxml2-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libfreetype6 \
    libfreetype6-dev \
    libpng-dev \
    libtiff-dev \
    libjpeg-dev \
    cmake && \
    R -e "install.packages('tidyverse', dependencies=TRUE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('optparse', dependencies=TRUE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('ggpubr', dependencies=TRUE, repos='http://cran.rstudio.com/')"
