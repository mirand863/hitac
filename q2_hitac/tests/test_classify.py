"""
Unit tests for the classify library
"""

from q2_types.feature_data import (DNAIterator, DNAFASTAFormat)
import pandas as pd
import numpy as np
import _classify
import pickle
import skbio


class TestClassify:

    def test_calculatePossibleKmers_1(self):
        ground_truth = ['A', 'C', 'G', 'T']
        result = _classify.calculatePossibleKmers(1)
        assert len(ground_truth) == len(result)
        assert all([a == b for a, b in zip(result, ground_truth)])

    def test_calculatePossibleKmers_2(self):
        ground_truth = ['AA', 'AC', 'AG', 'AT', 'CA', 'CC', 'CG', 'CT',
                        'GA', 'GC', 'GG', 'GT', 'TA', 'TC', 'TG', 'TT']
        result = _classify.calculatePossibleKmers(2)
        assert len(ground_truth) == len(result)
        assert all([a == b for a, b in zip(result, ground_truth)])

    def test_calculatePossibleKmers_3(self):
        ground_truth = ['AAA', 'AAC', 'AAG', 'AAT', 'ACA', 'ACC', 'ACG',
                        'ACT', 'AGA', 'AGC', 'AGG', 'AGT', 'ATA', 'ATC',
                        'ATG', 'ATT', 'CAA', 'CAC', 'CAG', 'CAT', 'CCA',
                        'CCC', 'CCG', 'CCT', 'CGA', 'CGC', 'CGG', 'CGT',
                        'CTA', 'CTC', 'CTG', 'CTT', 'GAA', 'GAC', 'GAG',
                        'GAT', 'GCA', 'GCC', 'GCG', 'GCT', 'GGA', 'GGC',
                        'GGG', 'GGT', 'GTA', 'GTC', 'GTG', 'GTT', 'TAA',
                        'TAC', 'TAG', 'TAT', 'TCA', 'TCC', 'TCG', 'TCT',
                        'TGA', 'TGC', 'TGG', 'TGT', 'TTA', 'TTC', 'TTG',
                        'TTT']
        result = _classify.calculatePossibleKmers(3)
        assert len(ground_truth) == len(result)
        assert all([a == b for a, b in zip(result, ground_truth)])

    def test_frequency_1(self):
        ground_truth = [1, 1, 2, 1]
        kmers = _classify.calculatePossibleKmers(1)
        result = _classify.frequency('ATCGG', kmers)
        assert len(ground_truth) == len(result)
        assert all([a == b for a, b in zip(result, ground_truth)])

    def test_frequency_2(self):
        ground_truth = [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        kmers = _classify.calculatePossibleKmers(2)
        result = _classify.frequency('ATCGG', kmers)
        assert len(ground_truth) == len(result)
        assert all([a == b for a, b in zip(result, ground_truth)])

    def test_frequency_3(self):
        ground_truth = [0, 2, 0, 0, 1, 2, 1, 1, 0, 0, 2, 1, 0, 1, 0, 0,
                        1, 2, 0, 1, 3, 4, 4, 2, 2, 1, 2, 2, 1, 1, 1, 1,
                        1, 0, 3, 0, 0, 3, 1, 1, 0, 3, 2, 2, 0, 1, 3, 3,
                        0, 1, 0, 0, 1, 3, 1, 0, 2, 1, 1, 2, 0, 2, 2, 0]
        kmers = _classify.calculatePossibleKmers(3)
        sequence = "CCGAGTGAGGGTCCCACGAGGCCCAACCTCCCATCCGTGT" \
            "TGAACTACACCTGTTGCTTCGGCGGGCCCGCCGTGGTTCA"
        result = _classify.frequency(sequence, kmers)
        assert len(ground_truth) == len(result)
        assert all([a == b for a, b in zip(result, ground_truth)])

    def test_grouper_1(self):
        elements = 5
        items = [1, 2, 3, 4, 5]
        ground_truth = [items]
        groups = _classify.grouper(elements, items)
        assert len(ground_truth) == len(groups)
        assert all([a == b for a, b in zip(ground_truth, groups)])

    def test_grouper_2(self):
        elements = 3
        items = [1, 2, 3, 4, 5]
        ground_truth = [items[0:3], items[3:5]]
        groups = _classify.grouper(elements, items)
        assert len(ground_truth) == len(groups)
        assert all([a == b for a, b in zip(ground_truth, groups)])

    def test_computeFrequencies_1(self):
        sequences = (b"CCAACC", b"CGGGCC")
        kmers = _classify.calculatePossibleKmers(1)
        ground_truth = [[2, 4, 0, 0], [0, 3, 3, 0]]
        results = _classify.computeFrequencies(sequences, kmers, 1)
        for i in range(len(results)):
            assert len(
                ground_truth[i]
            ) == len(
                results.loc[i, :].values.tolist()
            )
            assert all(
                [a == b for a, b in zip(
                    results.loc[i, :].values.tolist(), ground_truth[i]
                )]
            )

    def test_computeFrequencies_2(self):
        sequences = (b"CCAACC", b"CGGGCC")
        kmers = _classify.calculatePossibleKmers(2)
        ground_truth = [[1, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0]]
        results = _classify.computeFrequencies(sequences, kmers, 1)
        for i in range(len(results)):
            assert len(
                ground_truth[i]
            ) == len(
                results.loc[i, :].values.tolist()
            )
            for j in range(len(kmers)):
                assert ground_truth[i][j] == results.iloc[i, j]

    def test_computeFrequencies_3(self):
        sequences = (b"CCAACC", b"CGGGCC")
        kmers = _classify.calculatePossibleKmers(3)
        ground_truth = [[0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                        0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        results = _classify.computeFrequencies(sequences, kmers, 1)
        for i in range(len(results)):
            assert len(
                ground_truth[i]
            ) == len(
                results.loc[i, :].values.tolist()
            )
            for j in range(len(kmers)):
                assert ground_truth[i][j] == results.iloc[i, j]

    def test_getRanks_1(self):
        taxxi = "d__Fungi; p__Ascomycota; c__Orbiliomycetes; " \
            "o__Orbiliales; f__Orbiliaceae; g__Dactylellina; " \
            "s__Dactylellina_cionopaga"
        ground_truth = ['d__Fungi', ' p__Ascomycota',
                        ' c__Orbiliomycetes', ' o__Orbiliales',
                        ' f__Orbiliaceae', ' g__Dactylellina',
                        ' s__Dactylellina_cionopaga']
        results = _classify.getRanks(taxxi)
        assert len(ground_truth) == len(results)
        assert all([a == b for a, b in zip(results, ground_truth)])

    def test_getRanks_2(self):
        taxxi = "d__Fungi; p__Basidiomycota; " \
            "c__Agaricomycetes; o__Agaricales; " \
            "f__Amanitaceae; g__Limacella; s__Limacella_illinita"
        ground_truth = ['d__Fungi', ' p__Basidiomycota',
                        ' c__Agaricomycetes', ' o__Agaricales',
                        ' f__Amanitaceae', ' g__Limacella',
                        ' s__Limacella_illinita']
        results = _classify.getRanks(taxxi)
        assert len(ground_truth) == len(results)
        assert all([a == b for a, b in zip(results, ground_truth)])

    def test_getRanks_3(self):
        taxxi = "d__Fungi; p__Ascomycota; c__Sordariomycetes; " \
            "o__Sordariales; f__Chaetomiaceae; g__Myceliophthora"
        ground_truth = ['d__Fungi', ' p__Ascomycota',
                        ' c__Sordariomycetes', ' o__Sordariales',
                        ' f__Chaetomiaceae', ' g__Myceliophthora']
        results = _classify.getRanks(taxxi)
        assert len(ground_truth) == len(results)
        assert all([a == b for a, b in zip(results, ground_truth)])

    def test_getTaxonomy_1(self):
        taxonomy_1 = "d__Fungi; p__Basidiomycota; " \
            "c__Agaricomycetes; o__Agaricales; " \
            "f__Inocybaceae; g__Inocybe"
        taxonomy_2 = "d__Fungi; p__Basidiomycota; " \
            "c__Agaricomycetes; o__Hymenochaetales; " \
            "f__Hymenochaetaceae; g__Phellinus"
        taxonomy_3 = "d__Fungi; p__Basidiomycota; " \
            "c__Pucciniomycetes; o__Pucciniales; " \
            "f__Melampsoraceae; g__Melampsora"
        reference_taxonomy = pd.Series([taxonomy_1,
                                        taxonomy_2,
                                        taxonomy_3])
        ground_truth = [['d__Fungi', ' p__Basidiomycota',
                         ' c__Agaricomycetes', ' o__Agaricales',
                         ' f__Inocybaceae', ' g__Inocybe'],
                        ['d__Fungi', ' p__Basidiomycota',
                         ' c__Agaricomycetes',
                         ' o__Hymenochaetales',
                         ' f__Hymenochaetaceae', ' g__Phellinus'],
                        ['d__Fungi', ' p__Basidiomycota',
                         ' c__Pucciniomycetes', ' o__Pucciniales',
                         ' f__Melampsoraceae', ' g__Melampsora']]
        results = _classify.getTaxonomy(reference_taxonomy)
        assert len(ground_truth) == len(results)
        assert all(
            [a == b for a, b in zip(results.values.tolist(), ground_truth)]
        )

    def test_getTaxonomy_2(self):
        taxonomy_1 = "d__Fungi; p__Basidiomycota; " \
            "c__Agaricomycetes; o__Agaricales; " \
            "f__Mycenaceae; g__Panellus"
        taxonomy_2 = "d__Fungi; p__Basidiomycota; " \
            "c__Agaricomycetes; o__Atheliales; " \
            "f__Atheliaceae; g__Piloderma"
        taxonomy_3 = "d__Fungi; p__Ascomycota; c__Dothideomycetes; " \
            "o__Pleosporales; f__Didymellaceae; g__Didymella"
        reference_taxonomy = pd.Series([taxonomy_1,
                                        taxonomy_2,
                                        taxonomy_3])
        ground_truth = [['d__Fungi', ' p__Basidiomycota',
                         ' c__Agaricomycetes', ' o__Agaricales',
                         ' f__Mycenaceae', ' g__Panellus'],
                        ['d__Fungi', ' p__Basidiomycota',
                         ' c__Agaricomycetes', ' o__Atheliales',
                         ' f__Atheliaceae', ' g__Piloderma'],
                        ['d__Fungi', ' p__Ascomycota',
                         ' c__Dothideomycetes', ' o__Pleosporales',
                         ' f__Didymellaceae', ' g__Didymella']]
        results = _classify.getTaxonomy(reference_taxonomy)
        assert len(ground_truth) == len(results)
        assert all(
            [a == b for a, b in zip(results.values.tolist(), ground_truth)]
        )

    def test_getTaxonomy_3(self):
        taxonomy_1 = "d__Fungi; p__Ascomycota; c__Lecanoromycetes; " \
            "o__Lecanorales; f__Parmeliaceae; g__Usnea; s__Usnea_ceratina"
        taxonomy_2 = "d__Fungi; p__Basidiomycota; c__Agaricomycetes; " \
            "o__Agaricales; f__Marasmiaceae; g__Gymnopus; s__Gymnopus_parvulus"
        taxonomy_3 = "d__Fungi; p__Basidiomycota; c__Agaricomycetes; " \
            "o__Agaricales; f__Psathyrellaceae; g__Parasola; " \
            "s__Parasola_leiocephala"
        reference_taxonomy = pd.Series([taxonomy_1,
                                        taxonomy_2,
                                        taxonomy_3])
        ground_truth = [['d__Fungi', ' p__Ascomycota', ' c__Lecanoromycetes',
                         ' o__Lecanorales', ' f__Parmeliaceae', ' g__Usnea',
                         ' s__Usnea_ceratina'],
                        ['d__Fungi', ' p__Basidiomycota', ' c__Agaricomycetes',
                         ' o__Agaricales', ' f__Marasmiaceae', ' g__Gymnopus',
                         ' s__Gymnopus_parvulus'],
                        ['d__Fungi', ' p__Basidiomycota', ' c__Agaricomycetes',
                         ' o__Agaricales', ' f__Psathyrellaceae',
                         ' g__Parasola', ' s__Parasola_leiocephala']]
        results = _classify.getTaxonomy(reference_taxonomy)
        assert len(ground_truth) == len(results)
        assert all(
            [a == b for a, b in zip(results.values.tolist(), ground_truth)]
        )

    def test_createYTest_1(self):
        ids = tuple(np.full((1935, 1), ''))
        X_test = pd.DataFrame(np.full((1935, 4096), ''))
        Y_train = pd.DataFrame(np.full((9336, 6), ''))
        assert _classify.createYTest(ids, X_test, Y_train).shape == (1935, 7)

    def test_createYTest_2(self):
        ids = ('id_1', 'id_2', 'id_3')
        X_test = pd.DataFrame(np.full((3, 4), ''))
        Y_train = pd.DataFrame(np.full((100, 7), ''))
        result = _classify.createYTest(ids, X_test, Y_train)
        columns = ['id', 'kingdom', 'phylum', 'class',
                   'order', 'family', 'genus', 'species']
        assert result.shape == (3, 8)
        assert all(
            [a == b for a, b in zip(tuple(result['id'].values.tolist()), ids)]
        )
        assert all(
            [a == b for a, b in zip(columns, result.columns)]
        )
        assert len(columns) == len(result.columns)

    def test_createYTest_3(self):
        ids = ('id_1', 'id_2', 'id_3', 'id_4')
        X_test = pd.DataFrame(np.full((4, 256), ''))
        Y_train = pd.DataFrame(np.full((1000, 6), ''))
        result = _classify.createYTest(ids, X_test, Y_train)
        columns = ['id', 'kingdom', 'phylum', 'class',
                   'order', 'family', 'genus']
        assert result.shape == (4, 7)
        assert all(
            [a == b for a, b in zip(tuple(result['id'].values.tolist()), ids)]
        )
        assert all(
            [a == b for a, b in zip(columns, result.columns)]
        )
        assert len(columns) == len(result.columns)

    def test_extract_reads_1(self):
        ground_truth_ids = ('seq1', 'seq2', 'seq3')
        ground_truth_seq = (b'TTGCGGGGAAAGGCCCANATGGGCCGCTGAGAGAGGAGCCCG',
                            b'TCTGTTGCTCGGGGAGAGCGGCATGGGGAGTGGAAAGTCCCA',
                            b'GAATTCCACGTGTAGCGGTGAAATGCGTAGAGATGTGGAGGA')
        sequences = []
        for i, j in zip(ground_truth_ids, ground_truth_seq):
            sequences.append('>' + i + '\n')
            sequences.append(j.decode('utf-8') + '\n')
        print(sequences)
        reads = DNAIterator(
            skbio.read(sequences, format='fasta', constructor=skbio.DNA))
        result_ids, result_seq = _classify._extract_reads(reads)
        assert len(result_ids) == len(ground_truth_ids)
        assert all(
            [a == b for a, b in zip(ground_truth_ids, result_ids)]
        )
        assert len(result_seq) == len(ground_truth_seq)
        assert all(
            [a == b for a, b in zip(ground_truth_seq, result_seq)]
        )

    def test_predict_1(self):
        with open('q2_hitac/tests/predict_1.pkl', 'rb') as f:
            X_train, Y_train, X_test, Y_test, ground_truth = pickle.load(f)
            predicted = _classify.predict(X_train, Y_train, X_test, Y_test, -1)
        assert len(predicted) == len(ground_truth)
        assert all(
            [a == b for a, b in zip(predicted, ground_truth)]
        )

    def test_predict_2(self):
        with open('q2_hitac/tests/predict_2.pkl', 'rb') as f:
            X_train, Y_train, X_test, Y_test, ground_truth = pickle.load(f)
            predicted = _classify.predict(X_train, Y_train, X_test, Y_test, -1)
        assert len(predicted) == len(ground_truth)
        assert all(
            [a == b for a, b in zip(predicted, ground_truth)]
        )

    def test_classify_1(self):
        with open('q2_hitac/tests/classify1_reference.pkl', 'rb') as f:
            reference_reads, reference_taxonomy = pickle.load(f)
            query = DNAFASTAFormat('q2_hitac/tests/classify1_query.fasta',
                                   mode='r')
            predicted = _classify.classify(reference_reads,
                                           reference_taxonomy,
                                           query)
        with open('q2_hitac/tests/classify1_ground_truth.pkl', 'rb') as f:
            ground_truth = pickle.load(f)
            assert len(predicted) == len(ground_truth)
            assert all(
                [a == b for a, b in zip(predicted, ground_truth)]
            )
