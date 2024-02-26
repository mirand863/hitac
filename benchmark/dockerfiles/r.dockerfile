FROM r-base:4.3.2

RUN R -e "install.packages('tidyverse', dependencies=TRUE, repos='http://cran.rstudio.com/')"
