# HiTaC

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A hierarchical taxonomy classifier for fungal ITS sequences.

## Installation

[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/hitac/README.html)

HiTaC can be easily installed with conda:

```
conda install -c bioconda hitac
```

Alternatively, if you already have qiime2 installed, HiTaC can be installed with pip:

```
pip install hitac
```

## Input Files

HiTaC accepts taxonomy in TSV format and training and test files in FASTA format. All these files must be previously imported by qiime2. For example:

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

The predictions can be exported from qiime2 to a TSV file, where the first column contains the identifier of the test sequence and the second column holds the predictions made by HiTaC. For example:

```
qiime tools export \
--input-path classifier_output.qza \
--output-path output_dir
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
