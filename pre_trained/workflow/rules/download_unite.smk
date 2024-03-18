rule download_unite:
    params:
        url = lambda wildcards: config["urls"]["unite"][wildcards.dataset]
    output:
        dataset = "data/unite/{dataset}.tgz"
    shell:
        """
        while [ 1 ]; do
            wget \
                --retry-connrefused \
                --waitretry=1 \
                --read-timeout=20 \
                --timeout=15 \
                -t 0 \
                --continue \
                -O {output.dataset} \
                {params.url}
            if [ $? = 0 ]; then break; fi; # check return value, break if successful (0)
            sleep 10s;
        done;
        """
