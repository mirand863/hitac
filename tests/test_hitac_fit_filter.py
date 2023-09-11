import unittest

from hitac.hitac_fit_filter import parse_args


class TestUtils(unittest.TestCase):
    def test_parse_args(self):
        parser = parse_args(
            [
                "--reference",
                "reference.fasta",
                "--filter",
                "classifier.pkl",
                "--kmer",
                "8",
                "--threads",
                "1",
            ]
        )
        self.assertTrue(parser.reference)
        self.assertEqual(parser.reference, "reference.fasta")
        self.assertTrue(parser.kmer)
        self.assertEqual(parser.kmer, 8)
        self.assertTrue(parser.threads)
        self.assertEqual(parser.threads, 1)
        self.assertTrue(parser.filter)
        self.assertEqual(parser.filter, "classifier.pkl")
