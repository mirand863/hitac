rule install_bioautoml:
    output:
        bioautoml = "results/BioAutoML/BioAutoML-feature.py"
    conda:
        "../environments/bioautoml.yml"
    shell:
        """
        git clone https://github.com/Bonidia/BioAutoML.git results/BioAutoML
        cd results/BioAutoML
        git submodule init
        git submodule update
        """
