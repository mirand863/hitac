import unittest

from hitac.hitac_classify import parse_args


class TestUtils(unittest.TestCase):
    def test_parse_args(self):
        parser = parse_args(
            [
                "--reads",
                "reads.fasta",
                "--classifier",
                "classifier.pkl",
                "--kmer",
                "9",
                "--threads",
                "32",
                "--classification",
                "classification.tsv",
            ]
        )
        self.assertTrue(parser.reads)
        self.assertEqual(parser.reads, "reads.fasta")
        self.assertTrue(parser.classifier)
        self.assertEqual(parser.classifier, "classifier.pkl")
        self.assertTrue(parser.kmer)
        self.assertEqual(parser.kmer, 9)
        self.assertTrue(parser.threads)
        self.assertEqual(parser.threads, 32)
        self.assertTrue(parser.classification)
        self.assertEqual(parser.classification, "classification.tsv")
