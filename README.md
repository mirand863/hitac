# HiTaC

[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause) [![pipeline status](https://gitlab.com/dacs-hpi/hitac/badges/master/pipeline.svg)](https://gitlab.com/dacs-hpi/hitac/-/commits/master) [![coverage report](https://gitlab.com/dacs-hpi/hitac/badges/master/coverage.svg)](https://gitlab.com/dacs-hpi/hitac/-/commits/master)

A hierarchical taxonomic classifier for fungal ITS sequences.

## Installation

[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/hitac/README.html)

HiTaC dependends on QIIME 2. We recommend using QIIME 2 version 2021.8. To install QIIME 2 in a new conda environment and activate it, please run:

```
wget https://data.qiime2.org/distro/core/qiime2-2021.8-py38-linux-conda.yml
conda env create -n qiime2-2021.8 --file qiime2-2021.8-py38-linux-conda.yml
# OPTIONAL CLEANUP
rm qiime2-2021.8-py38-linux-conda.yml
conda activate qiime2-2020.2
```

Afterwards, HiTaC can also be installed with conda:

```
conda install -c conda-forge -c bioconda hitac
```

For conda installation instructions, we refer the reader to [https://conda.io/projects/conda/en/latest/user-guide/install/index.html](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).

[![install with pip](https://gitlab.com/dacs-hpi/hitac/-/raw/master/resources/pip.svg)](https://pypi.org/project/hitac/)

Alternatively, HiTaC can be installed with pip in an environment where QIIME 2 was previously installed:

```
pip install hitac
```

[![install with docker](https://gitlab.com/dacs-hpi/hitac/-/raw/master/resources/docker.svg)](https://hub.docker.com/r/mirand863/hitac)

Lastly, HiTaC and all its dependencies can be download as a docker image:

```
docker pull mirand863/hitac:latest
```

The downloaded image can then be started with:

```
docker run -it mirand863/hitac:latest /bin/bash
```

## Running

For an interactive tutorial, we refer the reader to our [Google Colabs notebook](https://colab.research.google.com/drive/12XicbyNhUQB2eVaiJG2b-0HMsOqvQTNs).

To see the usage run `qiime hitac --help` or `qiime hitac [command] --help` if you want further help with a specific command.

```
Usage: qiime hitac [OPTIONS] COMMAND [ARGS]...

  Description: This QIIME 2 plugin wraps HiTaC for hierarchical taxonomic
  classification.

  Plugin website: https://gitlab.com/dacs-hpi/hitac

  Getting user support: Please post to the QIIME 2 forum for help with this
  plugin: https://forum.qiime2.org

Options:
  --version    Show the version and exit.
  --citations  Show citations and exit.
  --help       Show this message and exit.

Commands:
  classify    Hierarchical classification with HiTaC's pre-fitted model
  filter      Hierarchical classification filtering with HiTaC's pre-fitted
              model

  fit         Train HiTaC's hierarchical classifier
  fit-filter  Train HiTaC's hierarchical filter
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

## Training and predicting taxonomies

To train the model and classify, simply run:

```
qiime hitac fit \
--i-reference-reads db-seqs.qza \
--i-reference-taxonomy db-tax.qza \
--o-classifier classifier.qza

qiime hitac classify \
--i-classifier classifier.qza \
--i-reads q-seqs.qza \
--o-classification classifier_output.qza
```

Additionally, a filter can be trained to remove ranks where the predictions might be inaccurate and to compute the confidence score:

```
qiime hitac fit-filter \
--i-reference-reads db-seqs.qza \
--i-reference-taxonomy db-tax.qza \
--o-filter filter.qza

qiime hitac filter \
--i-filter filter.qza \
--i-reads q-seqs.qza \
--i-classification classifier_output.qza \
--o-filtered-classification filter_output.qza
```

## Output File

The predictions can be exported from QIIME 2 to a TSV file:

```
qiime tools export \
--input-path classifier_output.qza \
--output-path output_dir
```

or alternativelly if the filter was used:

```
qiime tools export \
--input-path filter_output.qza \
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

## Citation

If you use HiTaC, please cite:

>Miranda, Fábio M., et al. "HiTaC: Hierarchical Taxonomic Classification of Fungal ITS Sequences." bioRxiv (2020).

```
@article{miranda2020hitac,
  title={HiTaC: Hierarchical Taxonomic Classification of Fungal ITS Sequences},
  author={Miranda, F{\'a}bio M and Azevedo, Vasco AC and Renard, Bernhard Y and Piro, Vitor C and Ramos, Rommel TJ},
  journal={bioRxiv},
  year={2020},
  publisher={Cold Spring Harbor Laboratory}
}
```
