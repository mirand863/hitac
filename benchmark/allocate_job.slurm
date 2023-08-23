#!/bin/bash
#SBATCH -A renard
#SBATCH --partition magic
#SBATCH --time=5-00:00:00
#SBATCH --mem=10G
#SBATCH --constraint="ARCH:X86"
#SBATCH --exclude node-21

snakemake --unlock
snakemake --profile slurm
