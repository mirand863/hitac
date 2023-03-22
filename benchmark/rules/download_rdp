from snakemake.remote.HTTP import RemoteProvider as HTTPRemoteProvider

HTTP = HTTPRemoteProvider()

rule download_rdp:
    input:
        HTTP.remote(config["urls"]["rdp"], keep_local=True)
    output:
        temp("bin/rdp_classifier_2.13.zip")
    shell:
        """
        mv {input} {output}
        """
