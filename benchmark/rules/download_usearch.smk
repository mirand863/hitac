from snakemake.remote.HTTP import RemoteProvider as HTTPRemoteProvider

HTTP = HTTPRemoteProvider()

rule download_usearch:
    input:
        HTTP.remote(config["urls"]["usearch"], keep_local=True)
    output:
        temp("bin/usearch.gz")
    shell:
        """
        mv {input} {output}
        """
