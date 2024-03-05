from snakemake.remote.HTTP import RemoteProvider as HTTPRemoteProvider

HTTP = HTTPRemoteProvider()

rule download_unite:
    input:
        unite = HTTP.remote(config["urls"]["unite"], keep_local=True)
    output:
        unite = "data/unite.tgz"
    shell:
        """
        mv {input.unite} {output.unite}
        """
