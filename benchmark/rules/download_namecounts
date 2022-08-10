from snakemake.remote.HTTP import RemoteProvider as HTTPRemoteProvider

HTTP = HTTPRemoteProvider()

rule download_namecounts:
    input:
        HTTP.remote(config["urls"]["namecounts"], keep_local=True)
    output:
        "namecounts/{dataset}"
    shell:
        """
        mv {input} {output}
        """