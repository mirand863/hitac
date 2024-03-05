from snakemake.remote.HTTP import RemoteProvider as HTTPRemoteProvider

HTTP = HTTPRemoteProvider()

rule download_unite:
    input:
        fungi_refs = lambda wildcards: HTTP.remote(config["urls"]["unite"][wildcards.dataset], keep_local=True)
    output:
        dataset = "data/unite/{dataset}.tgz"
    shell:
        """
        mv {input.fungi_refs} {output.dataset}
        """
