rule extract_sensitivity:
    output:
        csv = temp("results/figures_and_tables/taxxi_metrics/sensitivity.csv")
    params:
        taxxi_metrics = "results/taxxi_metrics",
        datasets = expand("{dataset}", dataset=config["datasets"])
    container:
        config["containers"]["seaborn"]
    shell:
        """
        python figures_and_tables/scripts/extract_sensitivity.py \
            --taxxi-metrics {params.taxxi_metrics} \
            --datasets {params.datasets} \
            --output {output.csv}
        """


rule plot_sensitivity:
    input:
        csv = "results/figures_and_tables/taxxi_metrics/sensitivity.csv"
    output:
        plot = "results/figures_and_tables/taxxi_metrics/sensitivity.pdf"
    params:
        file = "sensitivity.pdf",
        path = "results/figures_and_tables/taxxi_metrics"
    container:
        config["containers"]["r_base"]
    shell:
        """
        Rscript --vanilla figures_and_tables/scripts/plot_sensitivity.R \
            --input {input.csv} \
            --path {params.path} \
            --file {params.file}
        """
