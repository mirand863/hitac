rule fscore_boxplot:
    output:
        plot = "results/figures_and_tables/hierarchical_metrics/fscore.pdf"
    params:
        hierarchical_metrics = "results/hierarchical_metrics",
        datasets = expand("{dataset}", dataset=config["datasets"])
    container:
        config["containers"]["seaborn"]
    shell:
        """
        python figures_and_tables/scripts/plot_fscore.py \
            --hierarchical-metrics {params.hierarchical_metrics} \
            --datasets {params.datasets} \
            --output {output.plot}
        """
