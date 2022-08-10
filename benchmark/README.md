# Benchmark

This is a reproducible Snakemake pipeline to compare HiTaC using the [TAXXI benchmark](https://peerj.com/articles/4652/).

## Installation

The main requirement to run this pipeline is Anaconda 3. Please, install the latest version of [Anaconda 3](https://www.anaconda.com/products/distribution) on your machine beforehand.

With Anaconda installed, install mamba to manage dependencies:

```shell
conda install -n base -c conda-forge mamba
conda activate base
```

Create a new environment with snakemake by running the following commands:

```shell
mamba create -c conda-forge -c bioconda -n snakemake snakemake
```

The file `config.yml` holds configuration information to run the pipeline, e.g., working directory, number of threads to run tasks in parallel, number of times to repeat the benchmark, datasets, methods, taxonomic ranks, etc. For the purpose of this tutorial, we will keep most parameters intact and modify only the working directory. In order to do that, run the command:

```shell
sed -i "s?workdir.*?workdir: `pwd`?" config.yml
```

## Running

After a successful installation, you can activate the newly created environment and run the pipelines (please don't forget to modify the config file with your working directory as described in the last section).

```
conda activate snakemake
snakemake --keep-going --printshellcmds --reason --use-conda --cores 12 --conda-frontend mamba -s workflows/methods
snakemake --keep-going --printshellcmds --reason --use-conda --cores 12 --conda-frontend mamba -s workflows/metrics
```

The parameter --keep-going forces Snakemake to keep executing independent tasks if an unrelated one fails, while the parameter --printshellcmds enables printing the commands that will be executed, the parameter --reason makes Snakemake print the reason for each executed rule, the parameter --use-conda is necessary to indicate that conda will be used to manage the software dependencies of the pipeline, the parameter --cores tells Snakemake how many cpus can be used overall (the more cpus you can spare, the faster the pipeline will finish), the parameter --conda-frontend switches from conda to mamba for faster dependency management, and the parameter -s selects the workflow to be executed.

The benchmarks, predictions and metrics for each model are saved in the results folder.
