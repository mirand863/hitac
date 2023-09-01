import unittest

from hitac.hitac_fit import parse_args


class TestUtils(unittest.TestCase):
    def test_parse_args(self):
        parser = parse_args(
            [
                "--reference",
                "reference.fasta",
                "--classifier",
                "classifier.pkl",
                "--kmer",
                "9",
                "--threads",
                "32",
            ]
        )
        self.assertTrue(parser.reference)
        self.assertEqual(parser.reference, "reference.fasta")
        self.assertTrue(parser.kmer)
        self.assertEqual(parser.kmer, 9)
        self.assertTrue(parser.threads)
        self.assertEqual(parser.threads, 32)
        self.assertTrue(parser.classifier)
        self.assertEqual(parser.classifier, "classifier.pkl")
