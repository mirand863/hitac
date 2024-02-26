rule extract_accuracy:
    output:
        csv = temp("results/figures_and_tables/taxxi_metrics/accuracy.csv")
    params:
        taxxi_metrics = "results/taxxi_metrics",
        datasets = expand("{dataset}", dataset=config["datasets"])
    container:
        config["containers"]["seaborn"]
    shell:
        """
        python figures_and_tables/scripts/extract_accuracy.py \
            --taxxi-metrics {params.taxxi_metrics} \
            --datasets {params.datasets} \
            --output {output.csv}
        """


rule plot_accuracy:
    input:
        csv = "results/figures_and_tables/taxxi_metrics/accuracy.csv"
    output:
        plot = "results/figures_and_tables/taxxi_metrics/accuracy.pdf"
    params:
        file = "accuracy.pdf",
        path = "results/figures_and_tables/taxxi_metrics"
    container:
        config["containers"]["r_base"]
    shell:
        """
        Rscript --vanilla figures_and_tables/scripts/plot_accuracy.R \
            --input {input.csv} \
            --path {params.path} \
            --file {params.file}
        """
