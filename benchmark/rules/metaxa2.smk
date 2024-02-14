rule taxxi_to_metaxa2:
    input:
        train = "data/train/{dataset}.fasta",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        reference_reads = temp("results/temp/{dataset}/metaxa2/reference_reads.fasta"),
        reference_taxonomy = temp("results/temp/{dataset}/metaxa2/reference_taxonomy.txt")
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/fasta_utax2_to_metaxa2.py \
            {input.train} \
            {output.reference_reads} \
            {output.reference_taxonomy}
        """


rule train_metaxa2:
    input:
        reference_reads = "results/temp/{dataset}/metaxa2/reference_reads.fasta",
        reference_taxonomy = "results/temp/{dataset}/metaxa2/reference_taxonomy.txt"
    output:
        nhr = temp("results/temp/{dataset}/metaxa2/database/blast.nhr"),
        nin = temp("results/temp/{dataset}/metaxa2/database/blast.nin"),
        nsd = temp("results/temp/{dataset}/metaxa2/database/blast.nsd"),
        nsi = temp("results/temp/{dataset}/metaxa2/database/blast.nsi"),
        nsq = temp("results/temp/{dataset}/metaxa2/database/blast.nsq")
    params:
        database = "results/temp/{dataset}/metaxa2/database"
    benchmark:
        repeat("results/benchmark/{dataset}/train/metaxa2.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["metaxa2"]
    shell:
        """
        metaxa2_dbb \
            -b {input.reference_reads} \
            -o {params.database} \
            -t {input.reference_taxonomy} \
            --auto_rep T \
            --cpu {threads} \
            --mode divergent
        """


rule classify_metaxa2:
    input:
        test = "data/test/{dataset}.fasta",
        nhr = "results/temp/{dataset}/metaxa2/database/blast.nhr",
        nin = "results/temp/{dataset}/metaxa2/database/blast.nin",
        nsd = "results/temp/{dataset}/metaxa2/database/blast.nsd",
        nsi = "results/temp/{dataset}/metaxa2/database/blast.nsi",
        nsq = "results/temp/{dataset}/metaxa2/database/blast.nsq"
    output:
        predictions = temp("results/temp/{dataset}/metaxa2/results.taxonomy.txt"),
        archaea = temp("results/temp/{dataset}/metaxa2/results.archaea.fasta"),
        bacteria = temp("results/temp/{dataset}/metaxa2/results.bacteria.fasta"),
        chloroplast = temp("results/temp/{dataset}/metaxa2/results.chloroplast.fasta"),
        eukaryota = temp("results/temp/{dataset}/metaxa2/results.eukaryota.fasta"),
        extraction_fasta = temp("results/temp/{dataset}/metaxa2/results.extraction.fasta"),
        extraction = temp("results/temp/{dataset}/metaxa2/results.extraction.results"),
        graph = temp("results/temp/{dataset}/metaxa2/results.graph"),
        mitochondria = temp("results/temp/{dataset}/metaxa2/results.mitochondria.fasta"),
        summary = temp("results/temp/{dataset}/metaxa2/results.summary.txt"),
        uncertain = temp("results/temp/{dataset}/metaxa2/results.uncertain.fasta")
    params:
        database = "results/temp/{dataset}/metaxa2/database",
        predictions = "results/temp/{dataset}/metaxa2/results"
    benchmark:
        repeat("results/benchmark/{dataset}/classify/metaxa2.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["metaxa2"]
    shell:
        """
        metaxa2 \
            -i {input.test} \
            -d {params.database}/blast \
            -p {params.database}/HMMs \
            -o {params.predictions} \
            -cpu {threads}
        """


rule metaxa2_to_taxxi:
    input:
        predictions = "results/temp/{dataset}/metaxa2/results.taxonomy.txt",
        test = "data/test/{dataset}.fasta",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        predictions = "results/predictions/{dataset}/metaxa2.tsv"
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/metaxa2tab.py \
            {input.predictions} \
            {input.test} \
            > {output.predictions}
        """
