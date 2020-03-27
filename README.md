# HiTaC

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A hierarchical taxonomy classifier for fungal ITS sequences.

## Installation

[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/hitac/README.html)

HiTaC can be easily installed with conda:

```
conda install -c bioconda hitac
```

## Input Files

HiTaC accepts training and test files in FASTA format. However, the taxonomy in the training file must be specified in the header in TAXXI format. For example:

```
>DQ286276;tax=d:Fungi,p:Ascomycota,c:Sordariomycetes,o:Diaporthales,f:Diaporthaceae,g:Diaporthe,s:Diaporthe_aspalathi;
GGATCATTGCTGGAACGCGCCCCAGGCGCACCCAGAAACCCTTTGTGAACTCATACCTTACTGTTGCCTCGGCGCAGGCC
GGCCCCCCAGGGGGCCCCTCGGAGACGAGGAGCAGGCCCGCCGGCGGCCAAGCCAACTCTTGTTTTTACACCGAAACTCT
GAGCAAAAAACACAAATGAATCAAAACTTTCAACAACGGATCTCTTGGTTCTGGCATCGATGAAGAACGCAGCGAAATGC
GATAAGTAATGTGAATTGCAGAATTCAGTGAATCATCGAATCTTTGAACGCACATTGCGCCCTCTGGTATTCCGGAGGGC
ATGCCTGTTCGAGCGTCATTTCAACCCTCAAGCCTGGCTTGGTGTTGGGGCACTGCCTGTAGAAGGGCAGGCCCTGAAAT
CTAGTGGCGGGCTCGCCAGGACCCCGAGCGCAGTAGTTAAACCCTCGCTCGGGAGGCCCTGGCGGTGCCCTGCCGTTAAA
CCCCCAACTTCTGAAAAT
>EU272527;tax=d:Fungi,p:Ascomycota,c:Eurotiomycetes,o:Eurotiales,f:Trichocomaceae,g:Paecilomyces,s:Paecilomyces_sinensis;
CCGAGTGAGGGTCCCACGAGGCCCAACCTCCCATCCGTGTTGAACTACACCTGTTGCTTCGGCGGGCCCGCCGTGGTTCA
CGCCCGGCCGCCGGGGGGCCTTGTGCTCCCGGGCCCGCGCCCGCCGAAGACCCCTCGAACGCTGCCCTGAAGGTTGCCGT
CTGAGTATAAAATCAATCATTAAAACTTTCAACAACGGATCTCTTGGTTCCGGCATCGATGAAGAACGCAGCGAAATGCG
ATAAGTAATGTGAATTGCAGAATTCCGTGAATCATCGAATCTTTGAACGCACATTGCGCCCCCTGGCATTCCGGGGGGCA
TGCCTGTCCGAGCGTCATTGCTAACCCTCCAGCCCGGCTGGTGTGTTGGGTCGACGTCCCCCCCGGGGGACGGGCCCGAA
AGGCAGCGGCGGCGCCGCGTCCGATCCTCGAGCGTATGGGGCTTTGTCACGCGCTCTGGTAGGGTCGGCCGGCTGGCCAG
CCAGCGACCTCACGGTCACCTATTTTTTCTCTTAGG
```

## Output File

The predictions are written in a TSV file, where the first column contains the identifier of the test sequence and the second column holds the predictions made by HiTaC. For example:

```
EF535685	d:Fungi,p:Ascomycota,c:Dothideomycetes,o:Capnodiales,f:Mycosphaerellaceae,g:Pseudocercospora,s:Pseudocercospora_basitruncata
JN943699	d:Fungi,p:Ascomycota,c:Lecanoromycetes,o:Lecanorales,f:Parmeliaceae,g:Melanohalea,s:Melanohalea_elegantula
FJ596843	d:Fungi,p:Basidiomycota,c:Agaricomycetes,o:Agaricales,f:Agaricaceae,g:Agaricus,s:Agaricus_pseudopratensis
HM017845	d:Fungi,p:Basidiomycota,c:Agaricomycetes,o:Agaricales,f:Cortinariaceae,g:Cortinarius,s:Cortinarius_biformis
AF398455	d:Fungi,p:Basidiomycota,c:Exobasidiomycetes,o:Tilletiales,f:Tilletiaceae,g:Tilletia,s:Tilletia_bromi
```

## Running

To see the usage run `hitac -h`

```
usage: hitac.py [-h] [--kmer KMER] [--threads THREADS] train test predictions

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
```

To test the installation, run the following commands:

```
wget -O train_sp_rdp_its.100.fasta https://drive5.com/taxxi/benchmark/trainfa/sp_rdp_its.100
wget -O test_sp_rdp_its.100.fasta https://drive5.com/taxxi/benchmark/testfa/sp_rdp_its.100
hitac.py --kmer 6 train_sp_rdp_its.100.fasta test_sp_rdp_its.100.fasta predictions_sp_rdp_its.100.tsv
```

If everything is OK, a file called `predictions_sp_rdp_its.100.tsv` will be created.
