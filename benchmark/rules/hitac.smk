rule hitac:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta",
        reference_sequences = "results/temp/{dataset}/dbq.fa",
        reference_taxonomy = "results/temp/{dataset}/db-tax.txt",
    output:
        predictions = "results/predictions/{dataset}/hitac.tsv",
        tmpdir = temp(directory("results/temp/{dataset}/hitac"))
    benchmark:
        # repeat("results/benchmark/{dataset}/hitac.tsv", config["benchmark"]["repeat"])
        "results/benchmark/{dataset}/hitac.tsv"
    threads:
        config["threads"]
    conda:
        "../envs/hitac.yml"
    shell:
        """
        mkdir -p {output.tmpdir}

        export LC_ALL=C.UTF-8
        export LANG=C.UTF-8

        qiime tools import \
            --input-path {input.test} \
            --output-path {output.tmpdir}/q-seqs.qza \
            --type 'FeatureData[Sequence]'

        qiime tools import \
            --input-path {input.reference_sequences} \
            --output-path {output.tmpdir}/db-seqs.qza \
            --type 'FeatureData[Sequence]'

        qiime tools import \
            --type 'FeatureData[Taxonomy]' \
            --input-format HeaderlessTSVTaxonomyFormat \
            --input-path {input.reference_taxonomy} \
            --output-path {output.tmpdir}/db-tax.qza

        qiime hitac fit \
            --i-reference-reads {output.tmpdir}/db-seqs.qza \
            --i-reference-taxonomy {output.tmpdir}/db-tax.qza \
            --p-kmer 6 \
            --p-threads {threads} \
            --o-classifier {output.tmpdir}/classifier.qza

        qiime hitac classify \
            --i-reads {output.tmpdir}/q-seqs.qza \
            --i-classifier {output.tmpdir}/classifier.qza \
            --p-kmer 6 \
            --p-threads {threads} \
            --o-classification {output.tmpdir}/classifier_output.qza

        qiime tools export \
            --input-path {output.tmpdir}/classifier_output.qza \
            --output-path {output.tmpdir}/output_dir

        python2 scripts/qiime2tax2tab.py \
            {output.tmpdir}/output_dir/taxonomy.tsv \
            > {output.predictions}
        """
