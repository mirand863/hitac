from snakemake.remote.HTTP import RemoteProvider as HTTPRemoteProvider

HTTP = HTTPRemoteProvider()

rule download_blca:
    input:
        HTTP.remote(config["urls"]["blca"], keep_local=True)
    output:
        temp("bin/BLCA-2.3-alpha.tar.gz")
    shell:
        """
        mv {input} {output}
        """
