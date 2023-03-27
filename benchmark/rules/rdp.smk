rule taxxi2rdp:
    input:
        train="data/train/{dataset}.fasta",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        reference_taxonomy = temp("results/temp/{dataset}/rdp/reference_taxonomy.txt"),
        reference_reads = temp("results/temp/{dataset}/rdp/reference_reads.fasta")
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/fasta_utax2rdp.py \
            {input.train} \
            {output.reference_taxonomy} \
            > {output.reference_reads}
        """


rule rdp:
    input:
        reference_taxonomy = "results/temp/{dataset}/rdp/reference_taxonomy.txt",
        reference_reads = "results/temp/{dataset}/rdp/reference_reads.fasta",
        test = "data/test/{dataset}.fasta",
    output:
        properties = temp("results/temp/{dataset}/rdp/rRNAClassifier.properties"),
        predictions = temp("results/temp/{dataset}/rdp/predictions.tsv")
    params:
        tmpdir = temp(directory("results/temp/{dataset}/rdp"))
    benchmark:
        repeat("results/benchmark/{dataset}/rdp.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["rdp"]
    shell:
        """
        workdir=`echo /usr/bin/rdp_classifier_2.13/dist/classifier.jar | sed "-es/e:/\/e/"`

        rd=`dirname $workdir | sed "-es/\/dist//"`

        props=$(find $rd | grep rRNAClassifier.properties | head -1)

        cp $props {output.properties}

        java \
            -Xmx8g \
            -cp /usr/bin/rdp_classifier_2.13/dist/classifier.jar \
            edu/msu/cme/rdp/classifier/train/ClassifierTraineeMaker \
            train \
            -t {input.reference_taxonomy} \
            -s {input.reference_reads} \
            -o {params.tmpdir}

        java \
            -Xmx1g \
            -jar /usr/bin/rdp_classifier_2.13/dist/classifier.jar \
            -t {output.properties} \
            -q {input.test} \
            -o {output.predictions}
        """


# rule rdp:
#     input:
#         train="data/train/{dataset}.fasta",
#         test="data/test/{dataset}.fasta",
#         rdp = "bin/rdp_classifier_2.13/dist/classifier.jar",
#         scripts = expand("scripts/{script}",script=config["scripts"])
#     output:
#         rdp50 = "results/predictions/{dataset}/rdp50.tsv",
#         rdp80 = "results/predictions/{dataset}/rdp80.tsv",
#         tmpdir = temp(directory("results/temp/{dataset}/rdp"))
#     benchmark:
#         repeat("results/benchmark/{dataset}/rdp.tsv",config["benchmark"]["repeat"])
#     threads:
#         config["threads"]
#     conda:
#         "../envs/rdp.yml"
#     shell:
#         """
#         mkdir -p {output.tmpdir}
#
#         python scripts/fasta_utax2rdp.py \
#             {input.train} \
#             {output.tmpdir}/rdp_tree.txt \
#             > {output.tmpdir}/rdp_db.fa
#
#         workdir=`echo {input.rdp} | sed "-es/e:/\/e/"`
#
#         rd=`dirname $workdir | sed "-es/\/dist//"`
#
#         props=$(find $rd | grep rRNAClassifier.properties | head -1)
#
#         cp $props {output.tmpdir}
#
#         java \
#             -Xmx8g \
#             -cp {input.rdp} \
#             edu/msu/cme/rdp/classifier/train/ClassifierTraineeMaker \
#             train \
#             -t {output.tmpdir}/rdp_tree.txt \
#             -s {output.tmpdir}/rdp_db.fa \
#             -o {output.tmpdir}
#
#         java \
#             -Xmx1g \
#             -jar {input.rdp} \
#             -t {output.tmpdir}/rRNAClassifier.properties \
#             -q {input.test} \
#             -o {output.tmpdir}/raw
#
#         python scripts/rdpc2tab3.py \
#             {output.tmpdir}/raw 50 \
#             > {output.rdp50}
#
#         python scripts/rdpc2tab3.py \
#             {output.tmpdir}/raw 80 \
#             > {output.rdp80}
#         """
