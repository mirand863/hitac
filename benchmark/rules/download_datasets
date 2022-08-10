from snakemake.remote.HTTP import RemoteProvider as HTTPRemoteProvider

HTTP = HTTPRemoteProvider()

rule download_datasets:
    input:
        train = HTTP.remote(config["urls"]["train"], keep_local=True),
        test = HTTP.remote(config["urls"]["test"], keep_local=True)
    output:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta"
    shell:
        """
        mv {input.train} {output.train}
        mv {input.test} {output.test}
        """