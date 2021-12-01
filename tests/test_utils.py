import numpy as np
from hitac import _utils
from q2_types.feature_data import DNAIterator
from skbio.sequence._dna import DNA


class TestUtils:
    def test_compute_possible_kmers_1(self):
        ground_truth = np.array(["A", "C", "G", "T"])
        results = _utils.compute_possible_kmers(1)
        assert ground_truth.shape == results.shape
        assert np.array_equal(ground_truth, results)

    def test_compute_possible_kmers_2(self):
        ground_truth = np.array(
            [
                "AA",
                "AC",
                "AG",
                "AT",
                "CA",
                "CC",
                "CG",
                "CT",
                "GA",
                "GC",
                "GG",
                "GT",
                "TA",
                "TC",
                "TG",
                "TT",
            ]
        )
        results = _utils.compute_possible_kmers(2)
        assert ground_truth.shape == results.shape
        assert np.array_equal(ground_truth, results)

    def test_frequency_1(self):
        ground_truth = np.array([1, 1, 2, 1])
        kmers = _utils.compute_possible_kmers(1)
        results = _utils.compute_kmer_frequency("ATCGG", kmers)
        assert ground_truth.shape == results.shape
        assert np.array_equal(ground_truth, results)

    def test_frequency_2(self):
        ground_truth = np.array([0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0])
        kmers = _utils.compute_possible_kmers(2)
        results = _utils.compute_kmer_frequency("ATCGG", kmers)
        assert ground_truth.shape == results.shape
        assert np.array_equal(ground_truth, results)

    def test_grouper_1(self):
        elements = 5
        items = [1, 2, 3, 4, 5]
        ground_truth = np.array([items])
        results = _utils.grouper(elements, items)
        assert ground_truth.shape == results.shape
        assert np.array_equal(ground_truth, results)

    def test_grouper_2(self):
        elements = 3
        items = [1, 2, 3, 4, 5]
        ground_truth = np.array([[1, 2, 3], [4, 5]])
        results = _utils.grouper(elements, items)
        assert ground_truth.shape == results.shape
        assert np.array_equal(ground_truth, results)

    def test_compute_frequencies_1(self):
        sequences = (b"CCAACC", b"CGGGCC")
        kmers = _utils.compute_possible_kmers(1)
        threads = 1
        ground_truth = np.array([[2, 4, 0, 0], [0, 3, 3, 0]])
        results = _utils.compute_frequencies(sequences, kmers, threads)
        assert ground_truth.shape == results.shape
        assert np.array_equal(ground_truth, results)

    def test_computeFrequencies_2(self):
        sequences = (b"CCAACC", b"CGGGCC")
        kmers = _utils.compute_possible_kmers(2)
        threads = 2
        ground_truth = np.array(
            [
                [1, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0],
            ]
        )
        results = _utils.compute_frequencies(sequences, kmers, threads)
        assert ground_truth.shape == results.shape
        assert np.array_equal(ground_truth, results)

    def test_extract_qiime2_ranks_1(self):
        taxonomy = (
            "d__Fungi; p__Ascomycota; c__Orbiliomycetes; "
            "o__Orbiliales; f__Orbiliaceae; g__Dactylellina; "
            "s__Dactylellina_cionopaga"
        )
        ground_truth = np.array(
            [
                "d__Fungi",
                " p__Ascomycota",
                " c__Orbiliomycetes",
                " o__Orbiliales",
                " f__Orbiliaceae",
                " g__Dactylellina",
                " s__Dactylellina_cionopaga",
            ]
        )
        results = _utils.extract_qiime2_ranks(taxonomy)
        assert ground_truth.shape == results.shape
        assert np.array_equal(ground_truth, results)

    def test_extract_qiime2_ranks_2(self):
        taxonomy = (
            "d__Fungi; p__Basidiomycota; "
            "c__Agaricomycetes; o__Agaricales; "
            "f__Amanitaceae; g__Limacella; s__Limacella_illinita"
        )
        ground_truth = np.array(
            [
                "d__Fungi",
                " p__Basidiomycota",
                " c__Agaricomycetes",
                " o__Agaricales",
                " f__Amanitaceae",
                " g__Limacella",
                " s__Limacella_illinita",
            ]
        )
        results = _utils.extract_qiime2_ranks(taxonomy)
        assert ground_truth.shape == results.shape
        assert np.array_equal(ground_truth, results)

    def test_extract_qiime2_ranks_3(self):
        taxonomy = (
            "d__Fungi; p__Ascomycota; c__Sordariomycetes; "
            "o__Sordariales; f__Chaetomiaceae; g__Myceliophthora"
        )
        ground_truth = np.array(
            [
                "d__Fungi",
                " p__Ascomycota",
                " c__Sordariomycetes",
                " o__Sordariales",
                " f__Chaetomiaceae",
                " g__Myceliophthora",
            ]
        )
        results = _utils.extract_qiime2_ranks(taxonomy)
        assert ground_truth.shape == results.shape
        assert np.array_equal(ground_truth, results)

    def test_extract_qiime2_ranks_4(self):
        taxonomy = (
            "d__Fungi; p__Ascomycota; c__Sordariomycetes; "
            "o__Sordariales; f__Chaetomiaceae"
        )
        ground_truth = np.array(
            [
                "d__Fungi",
                " p__Ascomycota",
                " c__Sordariomycetes",
                " o__Sordariales",
                " f__Chaetomiaceae",
            ]
        )
        results = _utils.extract_qiime2_ranks(taxonomy)
        assert ground_truth.shape == results.shape
        assert np.array_equal(ground_truth, results)

    def test_extract_qiime2_taxonomy_1(self):
        taxonomy_1 = (
            "d__Fungi; p__Basidiomycota; "
            "c__Agaricomycetes; o__Agaricales; "
            "f__Inocybaceae; g__Inocybe"
        )
        taxonomy_2 = (
            "d__Fungi; p__Basidiomycota; "
            "c__Agaricomycetes; o__Hymenochaetales; "
            "f__Hymenochaetaceae; g__Phellinus"
        )
        taxonomy_3 = (
            "d__Fungi; p__Basidiomycota; "
            "c__Pucciniomycetes; o__Pucciniales; "
            "f__Melampsoraceae; g__Melampsora"
        )
        taxonomy = np.array([taxonomy_1, taxonomy_2, taxonomy_3])
        ground_truth = np.array(
            [
                [
                    "d__Fungi",
                    " p__Basidiomycota",
                    " c__Agaricomycetes",
                    " o__Agaricales",
                    " f__Inocybaceae",
                    " g__Inocybe",
                ],
                [
                    "d__Fungi",
                    " p__Basidiomycota",
                    " c__Agaricomycetes",
                    " o__Hymenochaetales",
                    " f__Hymenochaetaceae",
                    " g__Phellinus",
                ],
                [
                    "d__Fungi",
                    " p__Basidiomycota",
                    " c__Pucciniomycetes",
                    " o__Pucciniales",
                    " f__Melampsoraceae",
                    " g__Melampsora",
                ],
            ]
        )
        results = _utils.extract_qiime2_taxonomy(taxonomy)
        assert ground_truth.shape == results.shape
        assert np.array_equal(ground_truth, results)

    def test_extract_qiime2_taxonomy_2(self):
        taxonomy_1 = (
            "d__Fungi; p__Basidiomycota; "
            "c__Agaricomycetes; o__Agaricales; "
            "f__Mycenaceae; g__Panellus"
        )
        taxonomy_2 = (
            "d__Fungi; p__Basidiomycota; "
            "c__Agaricomycetes; o__Atheliales; "
            "f__Atheliaceae; g__Piloderma"
        )
        taxonomy_3 = (
            "d__Fungi; p__Ascomycota; c__Dothideomycetes; "
            "o__Pleosporales; f__Didymellaceae; g__Didymella"
        )
        taxonomy = np.array([taxonomy_1, taxonomy_2, taxonomy_3])
        ground_truth = np.array(
            [
                [
                    "d__Fungi",
                    " p__Basidiomycota",
                    " c__Agaricomycetes",
                    " o__Agaricales",
                    " f__Mycenaceae",
                    " g__Panellus",
                ],
                [
                    "d__Fungi",
                    " p__Basidiomycota",
                    " c__Agaricomycetes",
                    " o__Atheliales",
                    " f__Atheliaceae",
                    " g__Piloderma",
                ],
                [
                    "d__Fungi",
                    " p__Ascomycota",
                    " c__Dothideomycetes",
                    " o__Pleosporales",
                    " f__Didymellaceae",
                    " g__Didymella",
                ],
            ]
        )
        results = _utils.extract_qiime2_taxonomy(taxonomy)
        assert ground_truth.shape == results.shape
        assert np.array_equal(ground_truth, results)

    def test_extract_qiime2_taxonomy_3(self):
        taxonomy_1 = (
            "d__Fungi; p__Ascomycota; c__Lecanoromycetes; "
            "o__Lecanorales; f__Parmeliaceae; g__Usnea; s__Usnea_ceratina"
        )
        taxonomy_2 = (
            "d__Fungi; p__Basidiomycota; c__Agaricomycetes; "
            "o__Agaricales; f__Marasmiaceae; g__Gymnopus; s__Gymnopus_parvulus"
        )
        taxonomy_3 = (
            "d__Fungi; p__Basidiomycota; c__Agaricomycetes; "
            "o__Agaricales; f__Psathyrellaceae; g__Parasola; "
            "s__Parasola_leiocephala"
        )
        taxonomy = np.array([taxonomy_1, taxonomy_2, taxonomy_3])
        ground_truth = np.array(
            [
                [
                    "d__Fungi",
                    " p__Ascomycota",
                    " c__Lecanoromycetes",
                    " o__Lecanorales",
                    " f__Parmeliaceae",
                    " g__Usnea",
                    " s__Usnea_ceratina",
                ],
                [
                    "d__Fungi",
                    " p__Basidiomycota",
                    " c__Agaricomycetes",
                    " o__Agaricales",
                    " f__Marasmiaceae",
                    " g__Gymnopus",
                    " s__Gymnopus_parvulus",
                ],
                [
                    "d__Fungi",
                    " p__Basidiomycota",
                    " c__Agaricomycetes",
                    " o__Agaricales",
                    " f__Psathyrellaceae",
                    " g__Parasola",
                    " s__Parasola_leiocephala",
                ],
            ]
        )
        results = _utils.extract_qiime2_taxonomy(taxonomy)
        assert ground_truth.shape == results.shape
        assert np.array_equal(ground_truth, results)

    def test_extract_reads_1(self):
        s1 = DNA("ACGT", metadata={"id": "s1"})
        s2 = DNA("TGCA", metadata={"id": "s2"})
        it = DNAIterator([s1, s2])
        ground_truth = [
            (s1.metadata["id"], s1._string),
            (s2.metadata["id"], s2._string),
        ]
        results = list(zip(*_utils._extract_reads(it)))
        assert len(ground_truth) == len(results)
        assert all([a == b for a, b in zip(results, ground_truth)])

    def test_convert_taxonomy_to_qiime2_1(self):
        taxonomy_1 = [
            "d__Fungi",
            " p__Ascomycota",
            " c__Lecanoromycetes",
            " o__Lecanorales",
            " f__Parmeliaceae",
            " g__Parmotrema",
        ]
        taxonomy_2 = [
            "d__Fungi",
            " p__Ascomycota",
            " c__Eurotiomycetes",
            " o__Eurotiales",
            " f__Trichocomaceae",
            " g__Penicillium",
        ]
        taxonomy_3 = [
            "d__Fungi",
            " p__Ascomycota",
            " c__Dothideomycetes",
            " o__Botryosphaeriales",
            " f__Botryosphaeriaceae",
            " g__Botryosphaeria",
        ]
        taxonomy = np.array([taxonomy_1, taxonomy_2, taxonomy_3])
        ground_truth = [
            "d__Fungi; p__Ascomycota; c__Lecanoromycetes; o__Lecanorales; f__Parmeliaceae; g__Parmotrema",
            "d__Fungi; p__Ascomycota; c__Eurotiomycetes; o__Eurotiales; f__Trichocomaceae; g__Penicillium",
            "d__Fungi; p__Ascomycota; c__Dothideomycetes; o__Botryosphaeriales; f__Botryosphaeriaceae; g__Botryosphaeria",
        ]
        results = _utils.convert_taxonomy_to_qiime2(taxonomy)
        assert len(ground_truth) == len(results)
        assert all([a == b for a, b in zip(results, ground_truth)])

    def test_search_1(self):
        key = "d__Fungi"
        taxonomy = [
            "d__Fungi",
            " p__Ascomycota",
            " c__Lecanoromycetes",
            " o__Lecanorales",
            " f__Parmeliaceae",
            " g__Parmotrema",
        ]
        ground_truth = 0
        result = _utils.search(key, taxonomy)
        assert ground_truth == result

    def test_search_2(self):
        key = " o__Lecanorales"
        taxonomy = [
            "d__Fungi",
            " p__Ascomycota",
            " c__Lecanoromycetes",
            " o__Lecanorales",
            " f__Parmeliaceae",
            " g__Parmotrema",
        ]
        ground_truth = 3
        result = _utils.search(key, taxonomy)
        assert ground_truth == result
