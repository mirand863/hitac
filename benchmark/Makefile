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
	-srun -A renard --mem=10G --cpus-per-task=12 --time=5-00:00:00 -p magic snakemake --restart-times 5 --keep-going --printshellcmds --reason --use-conda --cores 12 --resources mem_gb=2700 --jobs 6 --cluster "sbatch -A renard -p magic --mem=16G --cpus-per-task=12 --time=5-00:00:00 -C 'ARCH:X86'"
	-rm -f slurm-*

.PHONY: git
git:  ## Update local repository
	-git reset --hard
	-git fetch
	-git pull
