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
        cutoffs = temp("results/temp/{dataset}/metaxa2/database/blast.cutoffs.txt"),
        fasta = temp("results/temp/{dataset}/metaxa2/database/blast.fasta"),
        nhr = temp("results/temp/{dataset}/metaxa2/database/blast.nhr"),
        nin = temp("results/temp/{dataset}/metaxa2/database/blast.nin"),
        nsd = temp("results/temp/{dataset}/metaxa2/database/blast.nsd"),
        nsi = temp("results/temp/{dataset}/metaxa2/database/blast.nsi"),
        nsq = temp("results/temp/{dataset}/metaxa2/database/blast.nsq"),
        taxonomy = temp("results/temp/{dataset}/metaxa2/database/blast.taxonomy.txt"),
        hmm = temp("results/temp/{dataset}/metaxa2/database/HMMs/B.hmm"),
        h3f = temp("results/temp/{dataset}/metaxa2/database/HMMs/B.hmm.h3f"),
        h3i = temp("results/temp/{dataset}/metaxa2/database/HMMs/B.hmm.h3i"),
        h3m = temp("results/temp/{dataset}/metaxa2/database/HMMs/B.hmm.h3m"),
        h3p = temp("results/temp/{dataset}/metaxa2/database/HMMs/B.hmm.h3p"),
        hmm_names = temp("results/temp/{dataset}/metaxa2/database/HMMs/hmm_names.txt"),
        clusters = temp("results/temp/{dataset}/metaxa2/database/HMMs/raw_data/B.clusters"),
        usearch = temp("results/temp/{dataset}/metaxa2/database/HMMs/raw_data/B.divergent.usearch.uc"),
        be1_hmm = temp("results/temp/{dataset}/metaxa2/database/HMMs/raw_data/Be1.hmm"),
        b_fasta = temp("results/temp/{dataset}/metaxa2/database/HMMs/raw_data/B.fasta"),
        b_full_results = temp("results/temp/{dataset}/metaxa2/database/HMMs/raw_data/B.full-length-matching-models.extraction.results"),
        b_full_fasta = temp("results/temp/{dataset}/metaxa2/database/HMMs/raw_data/B.full-length-matching-models.fasta"),
        b_full_graph = temp("results/temp/{dataset}/metaxa2/database/HMMs/raw_data/B.full-length-matching-models.graph"),
        b_full_summary = temp("results/temp/{dataset}/metaxa2/database/HMMs/raw_data/B.full-length-matching-models.summary.txt"),
        b_full_dump = temp("results/temp/{dataset}/metaxa2/database/HMMs/raw_data/B.id_dump.txt"),
        bs1 = temp("results/temp/{dataset}/metaxa2/database/HMMs/raw_data/Bs1.hmm"),
        identities = temp("results/temp/{dataset}/metaxa2/database/HMMs/raw_data/cutoff_identities.txt"),
        afa = temp("results/temp/{dataset}/metaxa2/database/HMMs/raw_data/final_blast_aligned.afa"),
        log = temp("results/temp/{dataset}/metaxa2/database/HMMs/raw_data/metaxa2_x_log.txt"),
        preblast = temp("results/temp/{dataset}/metaxa2/database/HMMs/raw_data/preblast.fasta"),
        taxonomy_dump = temp("results/temp/{dataset}/metaxa2/database/HMMs/raw_data/taxonomy.id_dump.txt")
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
        cutoffs = "results/temp/{dataset}/metaxa2/database/blast.cutoffs.txt",
        fasta = "results/temp/{dataset}/metaxa2/database/blast.fasta",
        nhr = "results/temp/{dataset}/metaxa2/database/blast.nhr",
        nin = "results/temp/{dataset}/metaxa2/database/blast.nin",
        nsd = "results/temp/{dataset}/metaxa2/database/blast.nsd",
        nsi = "results/temp/{dataset}/metaxa2/database/blast.nsi",
        nsq = "results/temp/{dataset}/metaxa2/database/blast.nsq",
        taxonomy = "results/temp/{dataset}/metaxa2/database/blast.taxonomy.txt",
        hmm = "results/temp/{dataset}/metaxa2/database/HMMs/B.hmm",
        h3f = "results/temp/{dataset}/metaxa2/database/HMMs/B.hmm.h3f",
        h3i = "results/temp/{dataset}/metaxa2/database/HMMs/B.hmm.h3i",
        h3m = "results/temp/{dataset}/metaxa2/database/HMMs/B.hmm.h3m",
        h3p = "results/temp/{dataset}/metaxa2/database/HMMs/B.hmm.h3p",
        hmm_names = "results/temp/{dataset}/metaxa2/database/HMMs/hmm_names.txt",
        clusters = "results/temp/{dataset}/metaxa2/database/HMMs/raw_data/B.clusters",
        usearch = "results/temp/{dataset}/metaxa2/database/HMMs/raw_data/B.divergent.usearch.uc",
        be1_hmm = "results/temp/{dataset}/metaxa2/database/HMMs/raw_data/Be1.hmm",
        b_fasta = "results/temp/{dataset}/metaxa2/database/HMMs/raw_data/B.fasta",
        b_full_results = "results/temp/{dataset}/metaxa2/database/HMMs/raw_data/B.full-length-matching-models.extraction.results",
        b_full_fasta = "results/temp/{dataset}/metaxa2/database/HMMs/raw_data/B.full-length-matching-models.fasta",
        b_full_graph = "results/temp/{dataset}/metaxa2/database/HMMs/raw_data/B.full-length-matching-models.graph",
        b_full_summary = "results/temp/{dataset}/metaxa2/database/HMMs/raw_data/B.full-length-matching-models.summary.txt",
        b_full_dump = "results/temp/{dataset}/metaxa2/database/HMMs/raw_data/B.id_dump.txt",
        bs1 = "results/temp/{dataset}/metaxa2/database/HMMs/raw_data/Bs1.hmm",
        identities = "results/temp/{dataset}/metaxa2/database/HMMs/raw_data/cutoff_identities.txt",
        afa = "results/temp/{dataset}/metaxa2/database/HMMs/raw_data/final_blast_aligned.afa",
        log = "results/temp/{dataset}/metaxa2/database/HMMs/raw_data/metaxa2_x_log.txt",
        preblast = "results/temp/{dataset}/metaxa2/database/HMMs/raw_data/preblast.fasta",
        taxonomy_dump = "results/temp/{dataset}/metaxa2/database/HMMs/raw_data/taxonomy.id_dump.txt"
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
