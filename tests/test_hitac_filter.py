import unittest

from hitac.hitac_filter import parse_args


class TestUtils(unittest.TestCase):
    def test_parse_args(self):
        parser = parse_args(
            [
                "--filter",
                "filter.pkl",
                "--reads",
                "reads.fasta",
                "--classification",
                "classification.tsv",
                "--threshold",
                "0.7",
                "--kmer",
                "128",
                "--threads",
                "256",
                "--filtered-classification",
                "filtered_classification.tsv",
            ]
        )
        self.assertTrue(parser.filter)
        self.assertEqual(parser.filter, "filter.pkl")
        self.assertTrue(parser.reads)
        self.assertEqual(parser.reads, "reads.fasta")
        self.assertTrue(parser.classification)
        self.assertEqual(parser.classification, "classification.tsv")
        self.assertTrue(parser.threshold)
        self.assertEqual(parser.threshold, 0.7)
        self.assertTrue(parser.kmer)
        self.assertEqual(parser.kmer, 128)
        self.assertTrue(parser.threads)
        self.assertEqual(parser.threads, 256)
        self.assertTrue(parser.filtered_classification)
        self.assertEqual(parser.filtered_classification, "filtered_classification.tsv")
