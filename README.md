# HiTaC

HiTaC is an open-source hierarchical taxonomic classifier for fungal ITS sequences compatible with QIIME 2.

[![pipeline](https://github.com/mirand863/hitac/actions/workflows/deploy.yml/badge.svg?branch=main)](https://github.com/mirand863/hitac/actions/workflows/deploy.yml) [![codecov](https://codecov.io/gh/mirand863/hitac/branch/main/graph/badge.svg?token=2G05Q8PQBE)](https://codecov.io/gh/mirand863/hitac) [![Downloads PyPI](https://static.pepy.tech/personalized-badge/hitac?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=pypi)](https://pypi.org/project/hitac/) [![Downloads Conda](https://img.shields.io/conda/dn/bioconda/hitac?label=conda)](https://anaconda.org/bioconda/hitac) [![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Quick links

- [Benchmark](#benchmark)
- [Install](#install)
- [Quick start](#quick-start)
- [Support](#support)
- [Contributing](#contributing)
- [Getting the latest updates](#getting-the-latest-updates)
- [Citation](#citation)

## Benchmark

HiTaC was thoroughly evaluated with the [TAXXI benchmark](https://peerj.com/articles/4652/), consistently achieving higher accuracy and sensitivity as evidenced in the figures below.

![Accuracy](benchmark/results/images/accuracy.svg)

![True positive rate](benchmark/results/images/tpr.svg)

For reproducibility, a Snakemake pipeline was created. Instructions on how to run it and source code are available at [https://github.com/mirand863/hitac/tree/main/benchmark](https://github.com/mirand863/hitac/tree/main/benchmark).

## Install

### Option 1: Conda

HiTaC dependends on QIIME 2. We recommend using QIIME 2 version 2022.2. To install QIIME 2 in a GNU/Linux machine, run:

```shell
wget https://data.qiime2.org/distro/core/qiime2-2022.2-py38-linux-conda.yml
conda env create -n hitac --file qiime2-2022.2-py38-linux-conda.yml
# OPTIONAL CLEANUP
rm qiime2-2022.2-py38-linux-conda.yml
```

**Note:** Instructions on how to install on Windows and macOS are available at [QIIME 2 docs](https://docs.qiime2.org/2022.2/install/native/#install-qiime-2-within-a-conda-environment).

Afterwards, the new conda environment created in the last step can be activated and HiTaC can be installed:

```shell
conda activate hitac
conda install -c conda-forge -c bioconda hitac
```

For conda installation instructions, we refer the reader to [Conda's user guide](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).

### Option 2: Pip

Alternatively, HiTaC can be installed with pip in an environment where QIIME 2 was previously installed:

```shell
pip install hitac
```

### Option 3: Docker

Lastly, HiTaC and all its dependencies can be download as a docker image:

```shell
docker pull mirand863/hitac:latest
```

The downloaded image can then be started with:

```shell
docker run -it mirand863/hitac:latest /bin/bash
```

## Quick start

For an interactive tutorial, we refer the reader to our [Google Colabs notebook](https://colab.research.google.com/drive/12XicbyNhUQB2eVaiJG2b-0HMsOqvQTNs).

To see the usage run `qiime hitac --help` or `qiime hitac [command] --help` if you want further help with a specific command.

```shell
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

### Input Files

HiTaC accepts taxonomy in TSV format and training and test files in FASTA format. All these files must be previously imported by QIIME 2, for example:

```shell
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

### Training and predicting taxonomies

To train the model and classify, simply run:

```shell
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

```shell
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

### Output File

The predictions can be exported from QIIME 2 to a TSV file:

```shell
qiime tools export \
--input-path classifier_output.qza \
--output-path output_dir
```

or alternativelly if the filter was used:

```shell
qiime tools export \
--input-path filter_output.qza \
--output-path output_dir
```

The first column in the TSV file contains the identifier of the test sequence and the second column holds the predictions made by HiTaC. For example:

```shell
Feature ID	Taxon	Confidence
EU254776;tax=d:Fungi,p:Ascomycota,c:Sordariomycetes,o:Diaporthales,f:Gnomoniaceae,g:Gnomonia;	d__Fungi; p__Ascomycota; c__Sordariomycetes; o__Diaporthales; f__Valsaceae; g__Cryptosporella	-1
FJ711636;tax=d:Fungi,p:Basidiomycota,c:Agaricomycetes,o:Agaricales,f:Marasmiaceae,g:Armillaria;	d__Fungi; p__Basidiomycota; c__Agaricomycetes; o__Agaricales; f__Marasmiaceae; g__Armillaria	-1
UDB016040;tax=d:Fungi,p:Basidiomycota,c:Agaricomycetes,o:Russulales,f:Russulaceae,g:Russula;	d__Fungi; p__Basidiomycota; c__Agaricomycetes; o__Russulales; f__Russulaceae; g__Russula	-1
GU827310;tax=d:Fungi,p:Ascomycota,c:Lecanoromycetes,o:Lecanorales,f:Ramalinaceae,g:Ramalina;	d__Fungi; p__Ascomycota; c__Lecanoromycetes; o__Lecanorales; f__Ramalinaceae; g__Ramalina	-1
JN943699;tax=d:Fungi,p:Ascomycota,c:Lecanoromycetes,o:Lecanorales,f:Parmeliaceae,g:Melanohalea;	d__Fungi; p__Ascomycota; c__Lecanoromycetes; o__Lecanorales; f__Parmeliaceae; g__Punctelia	-1
```

## Support

If you run into any problems or issues, please create a [GitHub issue](https://github.com/mirand863/hitac/issues) and we will try our best to help.

We strive to provide good support through our issue tracker on GitLab. However, if you'd like to receive private support with:

- Phone / video calls to discuss your specific use case and get recommendations
- Private discussions over Slack or Mattermost

Please reach out to fabio.malchermiranda@hpi.de.

## Contributing

We are a small team on a mission to improve ITS taxonomic classification, and we will take all the help we can get! If you would like to get involved, here is information on [contribution guidelines and how to test the code locally](CONTRIBUTING.md).

You can contribute in multiple ways, e.g., reporting bugs, writing or translating documentation, reviewing or refactoring code, requesting or implementing new features, etc.

## Getting the latest updates

If you'd like to get updates when we release new versions, please click on the "Watch" button on the top and select "Releases only". GitLab will then send you notifications along with a changelog with each new release.

## Citation

If you use HiTaC, please cite:

>Miranda, Fábio M., et al. "HiTaC: Hierarchical Taxonomic Classification of Fungal ITS Sequences." bioRxiv (2020).

```latex
@article{miranda2020hitac,
  title={HiTaC: Hierarchical Taxonomic Classification of Fungal ITS Sequences},
  author={Miranda, F{\'a}bio M and Azevedo, Vasco AC and Renard, Bernhard Y and Piro, Vitor C and Ramos, Rommel TJ},
  journal={bioRxiv},
  year={2020},
  publisher={Cold Spring Harbor Laboratory}
}
```
