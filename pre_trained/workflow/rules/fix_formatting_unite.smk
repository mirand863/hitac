rule fix_formatting_unite:
    input:
        fasta = "results/data/unite/{dataset}/developer/sh_refs_qiime_{filename}.fasta"
    output:
        fasta = "results/fix_formatting/unite/{dataset}/developer/sh_refs_qiime_{filename}.fasta"
    shell:
        """
        awk "/^>/ {{print(\$0)}}; /^[^>]/ {{print(toupper(\$0))}}" {input.fasta} | tr -d " " > {output.fasta}
        """
