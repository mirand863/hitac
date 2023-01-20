from snakemake.remote.HTTP import RemoteProvider as HTTPRemoteProvider

HTTP = HTTPRemoteProvider()

rule download_spingo:
    input:
        HTTP.remote(config["urls"]["spingo"], keep_local=True)
    output:
        temp("bin/spingo-1.3.zip")
    shell:
        """
        mv {input} {output}
        """
