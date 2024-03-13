#!/bin/bash
#SBATCH -A renard
#SBATCH --partition magic
#SBATCH --time=5-00:00:00
#SBATCH --mem=10G
#SBATCH --constraint="ARCH:X86"
###SBATCH --gpus=0
###SBATCH --constraint="GPU_SKU:A100&GPU_MEM:80GB"

snakemake --unlock
snakemake --profile slurm
