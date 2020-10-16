# HiTaC

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A hierarchical taxonomy classifier for fungal ITS sequences.

## Installation

HiTaC dependends on QIIME 2. We recommend using QIIME 2 version 2020.2. To install it, please run:

```
wget https://data.qiime2.org/distro/core/qiime2-2020.2-py36-linux-conda.yml
conda env create -n qiime2-2020.2 --file qiime2-2020.2-py36-linux-conda.yml
```

Now you can activate the new environment and install HiTaC using pip:

```
conda activate qiime2-2020.2
conda install tqdm -y
pip install q2-hitac
```

## Running

To see the usage run `qiime hitac --help`

```
Usage: qiime hitac [OPTIONS] COMMAND [ARGS]...

  Description: This QIIME 2 plugin wraps HiTaC and supports hierarchical
  taxonomic classification.

  Plugin website: https://gitlab.com/dacs-hpi/hitac

  Getting user support: Please post to the QIIME 2 forum for help with this
  plugin: https://forum.qiime2.org

Options:
  --version    Show the version and exit.
  --citations  Show citations and exit.
  --help       Show this message and exit.

Commands:
  classify  HiTaC
```

## Input Files

HiTaC accepts taxonomy in TSV format and training and test files in FASTA format. All these files must be previously imported by QIIME 2. For example:

```
qiime tools import \
--input-path $qfa \
--output-path q-seqs.qza \
--type 'FeatureData[Sequence]'

qiime tools import \
--input-path dbq.fa \
--output-path db-seqs.qza \
--type 'FeatureData[Sequence]'

qiime tools import \
--type 'FeatureData[Taxonomy]' \
--input-format HeaderlessTSVTaxonomyFormat \
--input-path db-tax.txt \
--output-path db-tax.qza
```

To train the model and classify, simply run:

```
qiime hitac classify \
--i-reference-reads db-seqs.qza \
--i-reference-taxonomy db-tax.qza \
--i-query q-seqs.qza \
--o-classification classifier_output.qza --verbose
```

## Output File

The predictions can be exported from QIIME 2 to a TSV file:

```
qiime tools export \
--input-path classifier_output.qza \
--output-path output_dir
```

The first column in the TSV file contains the identifier of the test sequence and the second column holds the predictions made by HiTaC. For example:

```
Feature ID	Taxon	Confidence
EU254776;tax=d:Fungi,p:Ascomycota,c:Sordariomycetes,o:Diaporthales,f:Gnomoniaceae,g:Gnomonia;	d__Fungi; p__Ascomycota; c__Sordariomycetes; o__Diaporthales; f__Valsaceae; g__Cryptosporella	-1
FJ711636;tax=d:Fungi,p:Basidiomycota,c:Agaricomycetes,o:Agaricales,f:Marasmiaceae,g:Armillaria;	d__Fungi; p__Basidiomycota; c__Agaricomycetes; o__Agaricales; f__Marasmiaceae; g__Armillaria	-1
UDB016040;tax=d:Fungi,p:Basidiomycota,c:Agaricomycetes,o:Russulales,f:Russulaceae,g:Russula;	d__Fungi; p__Basidiomycota; c__Agaricomycetes; o__Russulales; f__Russulaceae; g__Russula	-1
GU827310;tax=d:Fungi,p:Ascomycota,c:Lecanoromycetes,o:Lecanorales,f:Ramalinaceae,g:Ramalina;	d__Fungi; p__Ascomycota; c__Lecanoromycetes; o__Lecanorales; f__Ramalinaceae; g__Ramalina	-1
JN943699;tax=d:Fungi,p:Ascomycota,c:Lecanoromycetes,o:Lecanorales,f:Parmeliaceae,g:Melanohalea;	d__Fungi; p__Ascomycota; c__Lecanoromycetes; o__Lecanorales; f__Parmeliaceae; g__Punctelia	-1
```