# HiTaC [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A hierarchical taxonomy classifier for fungal ITS sequences.

## Installation

[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/hitac/README.html)

HiTaC can be easily installed with conda:

```
conda install -c bioconda hitac
```

## Running

To see the usage run `hitac -h`

~~~
usage: hitac [-h] [--kmer KMER] [--threads THREADS] train test predictions

HiTaC, a hierarchical taxonomy classifier for fungal ITS sequences

positional arguments:
  train              Input FASTA file containing the sequences for training
  test               Input FASTA file containing the sequences for taxonomy
                     prediction
  predictions        Output file to write the predictions

optional arguments:
  -h, --help         show this help message and exit
  --kmer KMER        Kmer size for feature extraction [default: 6]
  --threads THREADS  Number of threads [default: all threads available]
~~~
