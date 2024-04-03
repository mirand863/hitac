.PHONY: help
help: ## display this help
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: local
local:  ## Run pipeline without slurm
	-sed -i "s?workdir.*?workdir: `pwd`?" config/config.yml
	-snakemake --printshellcmds --reason --use-conda --cores 1 --conda-frontend mamba --resources mem_kb=480000000 --restart-times 2

.PHONY: delab
delab:  ## Run pipeline on delab with slurm
	-sed -i "s?workdir.*?workdir: `pwd`?" config/config.yml
	-rm -rf slurm-*.out slurm-*.err
	-sbatch -J hitac allocate_job.slurm
#	-srun -A renard -p magic --cpus-per-task 12 --mem=60G --time='5-00:00:00' --constraint 'ARCH:X86' snakemake --printshellcmds --reason --use-conda --cores 12 --conda-frontend mamba --resources mem_kb=480000000 --restart-times 3


.PHONY: clean
clean:  ## delete temporary files
	-rm -rf .snakemake slurm*.out

.PHONY: delete-results
delete-results:  ## delete results from pipeline
	-rm -rf results

.PHONY: git
git:  ## Update local repository
	-git reset --hard
	-git fetch
	-git pull
