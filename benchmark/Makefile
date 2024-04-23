.PHONY: help
help: ## display this help
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

#.PHONY: mamba
#mamba:  ## install mamba
#	-curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-$(uname)-$(uname -m).sh"
#        -bash Mambaforge-$(uname)-$(uname -m).sh

.PHONY: snakemake
snakemake:  ## install snakemake
	-mamba create -c conda-forge -c bioconda -n snakemake snakemake

.PHONY: local
local:  ## Run pipeline without slurm
	-sed -i "s?workdir.*?workdir: `pwd`?" config/config.yml
	-sed -i "s?#nrows.*?nrows: 10?" config/config.yml
	-snakemake --printshellcmds --reason --use-conda --cores 1 --conda-frontend mamba
	-sed -i "s?nrows.*?#nrows: 10?" config/config.yml

.PHONY: delab
delab:  ## Run pipeline on delab with slurm
	-sbatch -J cuml allocate_job.slurm

.PHONY: clean
clean:  ## delete temporary files from Snakemake
	-rm -rf .snakemake resources/test/test_sequences.fasta resources/train/train_sequences.fasta resources/train/train_terms.tsv slurm*.out

.PHONY: delete-results
delete-results:  ## delete results from pipeline
	-rm -rf results

.PHONY: git
git:  ## Update local repository
	-git reset --hard
	-git fetch
	-git pull
