rule extract_spingo:
    input:
        "bin/spingo-1.3.zip"
    output:
        "bin/SPINGO-1.3/dist/64bit/spingo"
    params:
        output_dir = "bin"
    shell:
        """
        unzip {input} -d {params.output_dir}
        """
