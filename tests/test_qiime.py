import itertools
import os
import tarfile
import unittest
from io import StringIO
from pathlib import Path
from typing import TextIO

import pandas as pd
import skbio
import sklearn
from hiclass import LocalClassifierPerParentNode
from pyfakefs.fake_filesystem_unittest import Patcher
from q2_types.feature_data import DNAIterator
from sklearn.linear_model import LogisticRegression

from hitac import qiime
from hitac._qiime import (
    PickleFormat,
    JSONFormat,
    HierarchicalTaxonomicClassifierDirFmt,
    _8,
    _3,
    _2,
    HierarchicalTaxonomicClassiferTemporaryPickleDirFmt,
    _1,
    _7,
    _6,
)
from hitac.filter import Filter

fixtures_loc = os.path.join(os.path.dirname(__file__), "fixtures")


class TestUtils(unittest.TestCase):
    def test_pickle_format(self):
        with Patcher() as patcher:
            content = "asdf"
            patcher.fs.create_file("not_tar.txt", contents=content)
            pickle_format = PickleFormat
            self.assertFalse(pickle_format.sniff("not_tar.txt"))
            with tarfile.open("file.tar", "w:gz") as tar:
                tar.add("not_tar.txt")
            self.assertTrue(pickle_format.sniff("file.tar"))

    def test_json_format_1(self):
        with Patcher() as patcher:
            content = "not json content"
            patcher.fs.create_file("not_json.txt", contents=content)
            json_format = JSONFormat
            path = Path("not_json.txt")
            self.assertFalse(json_format.sniff(path))

    def test_json_format_2(self):
        with Patcher() as patcher:
            content = '{"domain": "fungi"}'
            patcher.fs.create_file("file.json", contents=content)
            json_format = JSONFormat
            path = Path("file.json")
            self.assertTrue(json_format.sniff(path))

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
        hierarchical_classifier = qiime.fit(reference_reads, reference_taxonomy)
        predictions = qiime.classify(query_reads, hierarchical_classifier)[
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
        hierarchical_classifier = qiime.fit(reference_reads_1, reference_taxonomy)
        classification = qiime.classify(query_reads, hierarchical_classifier)
        hierarchical_filter = qiime.fit_filter(reference_reads_2, reference_taxonomy)
        predictions = qiime.filter(query_reads, hierarchical_filter, classification)[
            "Taxon"
        ].values.tolist()
        predictions.sort()
        assert len(ground_truth) == len(predictions)
        assert all([a == b for a, b in zip(predictions, ground_truth)])

    def test_1_and_2(self):
        lr = LogisticRegression()
        lcpn = LocalClassifierPerParentNode(local_classifier=lr)
        dirfmt = _2(lcpn)
        self.assertIsInstance(
            dirfmt, HierarchicalTaxonomicClassiferTemporaryPickleDirFmt
        )
        model = _1(dirfmt)
        self.assertIsInstance(model, LocalClassifierPerParentNode)
        with self.assertRaises(ValueError):
            version = sklearn.__version__
            sklearn.__version__ = -1
            _1(dirfmt)
            sklearn.__version__ = version

    def test_3(self):
        dirfmt = HierarchicalTaxonomicClassifierDirFmt
        with self.assertRaises(ValueError):
            _3(dirfmt)

    def test_6_and_7(self):
        lr = LogisticRegression()
        filter = Filter(local_classifier=lr)
        dirfmt = _7(filter)
        self.assertIsInstance(
            dirfmt, HierarchicalTaxonomicClassiferTemporaryPickleDirFmt
        )
        model = _6(dirfmt)
        self.assertIsInstance(model, Filter)
        with self.assertRaises(ValueError):
            version = sklearn.__version__
            sklearn.__version__ = -2
            _6(dirfmt)
            sklearn.__version__ = version

    def test_8(self):
        dirfmt = HierarchicalTaxonomicClassifierDirFmt
        with self.assertRaises(ValueError):
            _8(dirfmt)
