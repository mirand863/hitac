# Benchmark

This is a reproducible Snakemake pipeline to compare HiTaC using the [TAXXI benchmark](https://peerj.com/articles/4652/).

## Installation

The main requirements to run this pipeline are Anaconda 3 and Singularity. Please, install the latest version of [Anaconda 3](https://www.anaconda.com/products/distribution) and [Singularity](https://docs.sylabs.io/guides/2.6/user-guide/installation.html) on your machine beforehand.

With Anaconda installed, install mamba to manage dependencies:

```shell
conda install -n base -c conda-forge mamba
conda activate base
```

Create a new environment with snakemake by running the following command:

```shell
mamba env create --name snakemake --file snakemake.yml
```

The file `config.yml` holds configuration information to run the pipeline, e.g., working directory, number of threads to run tasks in parallel, number of times to repeat the benchmark, datasets, methods, taxonomic ranks, etc. For the purpose of this tutorial, we will keep most parameters intact and modify only the working directory. In order to do that, run the command:

```shell
sed -i "s?workdir.*?workdir: `pwd`?" config.yml
```

## Running

After a successful installation, you can activate the newly created environment and run the pipeline (please don't forget to modify the config file with your working directory as described in the last section).

```shell
conda activate snakemake
snakemake \
    --keep-going \
    --printshellcmds \
    --reason \
    --use-singularity \
    --cores 12
```

Each parameter has the following meaning:

- `--keep-going` forces Snakemake to keep executing independent tasks if an unrelated one fails;
- `--printshellcmds` enables printing the commands that will be executed;
- `--reason` makes Snakemake print the reason for each executed rule;
- `--use-singularity` is necessary to indicate that Singularity will be used to manage the software dependencies of the pipeline;
- `--cores` tells Snakemake how many cpus can be used overall (the more cpus you can spare, the faster the pipeline will finish).

The benchmarks, predictions and metrics for each model are saved in the results folder.

After running the previous pipeline, you can optionally recreate the tables and figures by running the command:

```shell
snakemake \
    --snakefile figures_and_tables/Snakefile \
    --keep-going \
    --printshellcmds \
    --reason \
    --use-singularity \
    --cores 12
```
