rule extract_usearch:
    input:
        "bin/usearch.gz"
    output:
        "bin/usearch"
    shell:
        """
        zcat {input} > {output}
        chmod +x {output}
        """
