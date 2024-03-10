rule convert_taxxi:
    input:
        fasta = "results/fix_formatting/unite/{dataset}/developer/sh_refs_qiime_{filename}.fasta",
        taxonomy = "results/data/unite/{dataset}/developer/sh_taxonomy_qiime_{filename}.txt"
    output:
        fasta = "results/converted_taxxi/unite/{dataset}/developer/sh_refs_qiime_{filename}.fasta"
    conda:
        "../envs/convert_taxxi.yml"
    shell:
        """
        python workflow/scripts/convert_taxxi.py \
            --fasta {input.fasta} \
            --taxonomy {input.taxonomy} \
            --output {output.fasta}
        """
