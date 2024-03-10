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


rule train_rdp:
    input:
        reference_taxonomy = "results/temp/{dataset}/rdp/reference_taxonomy.txt",
        reference_reads = "results/temp/{dataset}/rdp/reference_reads.fasta"
    output:
        tree = temp("results/temp/{dataset}/rdp/bergeyTrainingTree.xml"),
        probabilities = temp("results/temp/{dataset}/rdp/genus_wordConditionalProbList.txt"),
        prior = temp("results/temp/{dataset}/rdp/logWordPrior.txt"),
        array = temp("results/temp/{dataset}/rdp/wordConditionalProbIndexArr.txt")
    params:
        tmpdir = temp(directory("results/temp/{dataset}/rdp"))
    benchmark:
        repeat("results/benchmark/{dataset}/train/rdp.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["rdp"]
    shell:
        """
        java \
            -Xmx8g \
            -cp /usr/bin/rdp_classifier_2.13/dist/classifier.jar \
            edu/msu/cme/rdp/classifier/train/ClassifierTraineeMaker \
            train \
            -t {input.reference_taxonomy} \
            -s {input.reference_reads} \
            -o {params.tmpdir}
        """


rule classify_rdp:
    input:
        test = "data/test/{dataset}.fasta",
        tree = "results/temp/{dataset}/rdp/bergeyTrainingTree.xml",
        probabilities = "results/temp/{dataset}/rdp/genus_wordConditionalProbList.txt",
        prior = "results/temp/{dataset}/rdp/logWordPrior.txt",
        array = "results/temp/{dataset}/rdp/wordConditionalProbIndexArr.txt"
    output:
        properties = temp("results/temp/{dataset}/rdp/rRNAClassifier.properties"),
        predictions = temp("results/temp/{dataset}/rdp/predictions.tsv")
    params:
        tmpdir = temp(directory("results/temp/{dataset}/rdp"))
    benchmark:
        repeat("results/benchmark/{dataset}/classify/rdp.tsv", config["benchmark"]["repeat"])
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
            -Xmx1g \
            -jar /usr/bin/rdp_classifier_2.13/dist/classifier.jar \
            -t {output.properties} \
            -q {input.test} \
            -o {output.predictions}
        """


rule rdp50:
    input:
        predictions = "results/temp/{dataset}/rdp/predictions.tsv",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        predictions = "results/predictions/{dataset}/rdp50.tsv"
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/rdpc2tab3.py \
            {input.predictions} \
            50 \
            > {output.predictions}
        """


rule rdp80:
    input:
        predictions = "results/temp/{dataset}/rdp/predictions.tsv",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        predictions = "results/predictions/{dataset}/rdp80.tsv"
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/rdpc2tab3.py \
            {input.predictions} \
            80 \
            > {output.predictions}
        """
