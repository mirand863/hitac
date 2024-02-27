rule benchmark_table:
    output:
        table = "results/figures_and_tables/benchmarks/{dataset}.csv"
    params:
        benchmark_folder = "results/benchmark",
        dataset = "{dataset}"
    container:
        config["containers"]["pandas"]
    shell:
        """
        python figures_and_tables/scripts/create_benchmark_table.py \
            --benchmark {params.benchmark_folder} \
            --dataset {params.dataset} \
            --output {output.table}
        """
