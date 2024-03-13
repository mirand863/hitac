rule hierarchical_barplot:
    output:
        plot = "results/figures_and_tables/hierarchical_metrics/{dataset}.pdf"
    params:
        hierarchical_metrics = "results/hierarchical_metrics",
        dataset = "{dataset}"
    container:
        config["containers"]["seaborn"]
    shell:
        """
        python figures_and_tables/scripts/plot_hierarchical_barplot.py \
            --hierarchical-metrics {params.hierarchical_metrics} \
            --dataset {params.dataset} \
            --output {output.plot}
        """
