import itertools
import os

import pandas as pd
import skbio
from hitac import classifier
from q2_types.feature_data import DNAIterator

fixtures_loc = os.path.join(os.path.dirname(__file__), "fixtures")


class TestClassifier:
    def test_classify_1(self):
        reference_reads = DNAIterator(
            skbio.read(
                os.path.join(fixtures_loc, "classify_1_reference_reads.fasta"),
                format="fasta",
                constructor=skbio.DNA,
            )
        )
        reference_taxonomy = list(
            itertools.chain(
                *pd.read_csv(
                    os.path.join(fixtures_loc, "classify_1_reference_taxonomy.tsv"),
                    sep="\t",
                    usecols=["Taxon"],
                ).values.tolist()
            )
        )
        query_reads = os.path.join(fixtures_loc, "classify_1_query_reads.fasta")
        ground_truth = list(
            itertools.chain(
                *pd.read_csv(
                    os.path.join(fixtures_loc, "classify_1_ground_truth.tsv"),
                    sep="\t",
                    usecols=["Taxon"],
                ).values.tolist()
            )
        )
        ground_truth.sort()
        hierarchical_classifier = classifier.fit(reference_reads, reference_taxonomy)
        predictions = classifier.classify(query_reads, hierarchical_classifier)[
            "Taxon"
        ].values.tolist()
        predictions.sort()
        assert len(ground_truth) == len(predictions)
        assert all([a == b for a, b in zip(predictions, ground_truth)])

    def test_filter_1(self):
        reference_reads_1 = DNAIterator(
            skbio.read(
                os.path.join(fixtures_loc, "classify_1_reference_reads.fasta"),
                format="fasta",
                constructor=skbio.DNA,
            )
        )
        reference_reads_2 = DNAIterator(
            skbio.read(
                os.path.join(fixtures_loc, "classify_1_reference_reads.fasta"),
                format="fasta",
                constructor=skbio.DNA,
            )
        )
        reference_taxonomy = list(
            itertools.chain(
                *pd.read_csv(
                    os.path.join(fixtures_loc, "classify_1_reference_taxonomy.tsv"),
                    sep="\t",
                    usecols=["Taxon"],
                ).values.tolist()
            )
        )
        query_reads = os.path.join(fixtures_loc, "classify_1_query_reads.fasta")
        ground_truth = list(
            itertools.chain(
                *pd.read_csv(
                    os.path.join(fixtures_loc, "classify_1_ground_truth.tsv"),
                    sep="\t",
                    usecols=["Taxon"],
                ).values.tolist()
            )
        )
        ground_truth.sort()
        hierarchical_classifier = classifier.fit(reference_reads_1, reference_taxonomy)
        classification = classifier.classify(query_reads, hierarchical_classifier)
        hierarchical_filter = classifier.fit_filter(
            reference_reads_2, reference_taxonomy
        )
        predictions = classifier.filter(
            query_reads, hierarchical_filter, classification
        )["Taxon"].values.tolist()
        predictions.sort()
        assert len(ground_truth) == len(predictions)
        assert all([a == b for a, b in zip(predictions, ground_truth)])
