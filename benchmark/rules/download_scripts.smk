from snakemake.remote.HTTP import RemoteProvider as HTTPRemoteProvider

HTTP = HTTPRemoteProvider()

rule download_scripts:
    input:
        HTTP.remote(config["urls"]["scripts"], keep_local=True)
    output:
        "scripts/{script}"
    shell:
        """
        mv {input} {output}
        """