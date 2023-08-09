.PHONY: help
help: ## display this help
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: local
local:  ## Run pipeline without slurm
	-sed -i "s?workdir.*?workdir: `pwd`?" config/config.yml
	-sed -i "s?threads.*?threads: 8?" config/config.yml
	-snakemake --printshellcmds --reason --use-conda --cores 8 --conda-frontend mamba

.PHONY: delab
delab:  ## Run pipeline on delab with slurm
	-sed -i "s?workdir.*?workdir: `pwd`?" config/config.yml
	-sed -i "s?threads.*?threads: 12?" config/config.yml
	-rm -rf slurm-*.out
	-sbatch -J hitac allocate_job.slurm

.PHONY: git
git:  ## Update local repository
	-git reset --hard
	-git fetch
	-git pull
