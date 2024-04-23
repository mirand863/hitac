#!/bin/bash
#SBATCH -A renard
#SBATCH --partition sorcery
#SBATCH --time=5-00:00:00
#SBATCH --mem=20G
#SBATCH --constraint="ARCH:X86"
#SBATCH --gpus=1
#SBATCH --container-image=/hpi/fs00/scratch/fabio.malchermiranda/snakemake.sqfs
#SBATCH --container-mounts /hpi/fs00/scratch/fabio.malchermiranda/hitac_cuml:/hitac_cuml
#SBATCH --container-remap-root
#SBATCH --container-writable
###SBATCH --constraint="GPU_SKU:A100&GPU_MEM:80GB"

root/miniforge-pypy3/bin/conda activate snakemake
cd /hitac_cuml/benchmark
export PATH=/root/miniforge-pypy3/bin:$PATH
sed -i "s?workdir.*?workdir: `pwd`?" config.yml
snakemake --unlock
snakemake --keep-going --printshellcmds --reason --use-singularity --use-conda --cores 12
