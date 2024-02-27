rule extract_ocr_ucr:
    output:
        csv = temp("results/figures_and_tables/taxxi_metrics/ocr_ucr_{dataset}.csv")
    params:
        taxxi_metrics = "results/taxxi_metrics"
    container:
        config["containers"]["seaborn"]
    shell:
        """
        python figures_and_tables/scripts/extract_ocr_ucr.py \
            --taxxi-metrics {params.taxxi_metrics} \
            --dataset {wildcards.dataset} \
            --output {output.csv}
        """


rule plot_ocr_ucr:
    input:
        csv = "results/figures_and_tables/taxxi_metrics/ocr_ucr_{dataset}.csv"
    output:
        plot = "results/figures_and_tables/taxxi_metrics/{dataset}.pdf"
    params:
        dataset = "{dataset}",
        path = "results/figures_and_tables/taxxi_metrics"
    container:
        config["containers"]["r_base"]
    shell:
        """
        Rscript --vanilla figures_and_tables/scripts/plot_ocr_ucr.R \
            --input {input.csv} \
            --path {params.path} \
            --dataset {params.dataset}
        """
