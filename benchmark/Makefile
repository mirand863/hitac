.PHONY: help
help: ## display this help
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: mamba
mamba:  ## install mamba
	conda install -n base -c conda-forge mamba

.PHONY: snakemake
snakemake:  ## install snakemake
	-mamba remove -n snakemake --all -y
	-mamba create -c conda-forge -c bioconda -n snakemake snakemake -y

.PHONY: laptop
laptop:  ## Run methods pipeline on laptop
	-sed -i "s?workdir.*?workdir: `pwd`?" config.yml
	-snakemake --keep-going --printshellcmds --reason --use-conda --cores 12 --conda-frontend mamba -s workflows/methods.smk

.PHONY: delab
delab:  ## Run methods pipeline on delab
	-sed -i "s?workdir.*?workdir: `pwd`?" config.yml
	-srun -A renard --mem=450G --cpus-per-task=250 --time=168:0:0 -p cauldron snakemake --keep-going --printshellcmds --reason --use-conda --cores 256 --restart-times 20 --conda-frontend mamba -s workflows/methods

.PHONY: metrics
metrics:  ## Compute metrics
	-sed -i "s?workdir.*?workdir: `pwd`?" config.yml
	-snakemake --keep-going --printshellcmds --reason --use-conda --cores 12 --conda-frontend mamba -s workflows/metrics

.PHONY: clean
clean:  ## delete temporary files from pipeline
	-rm -rf .snakemake
	-rm -rf raw.githubusercontent.com/
	-rm -rf github.com/
	-rm -rf drive5.com/
	-rm -rf bin
	-rm -rf data
	-rm -rf scripts
	-rm -rf namecounts

.PHONY: delete-results
delete-results:  ## delete results from pipeline
	-rm -rf results
