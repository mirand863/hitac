import itertools
import os
import tarfile
import unittest
from io import StringIO
from pathlib import Path
from typing import TextIO

import pandas as pd
import skbio
from pyfakefs.fake_filesystem_unittest import Patcher
from q2_types.feature_data import DNAIterator

from hitac import qiime
from hitac._qiime import PickleFormat, JSONFormat


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
