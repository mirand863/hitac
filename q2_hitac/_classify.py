#!/usr/bin/env python3

from joblib import Parallel, delayed, parallel_backend
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from itertools import product
import multiprocessing
from tqdm import tqdm
import pandas as pd
import numpy as np
import skbio
import biom

from q2_types.feature_data import (FeatureData, Taxonomy, Sequence, DNAIterator, DNAFASTAFormat)

# Computes all kmer possibilities based on alphabet ACGT
def calculatePossibleKmers(kmerSize):
    alphabet = 'ACGT'
    kmers = [''.join(c) for c in product(alphabet, repeat=kmerSize)]
    return kmers

def frequency(sequence, kmers):
    freq = []
    for kmer in kmers:
        freq.append(sequence.count(kmer))
    return freq

# Computes kmer frequencies for training and test datasets
def computeFrequencies(sequences, kmers, threads):
    sequences = list(sequences)
    sequences = [s.decode('utf-8') for s in sequences]
    frequencies = Parallel(n_jobs=threads)(delayed(frequency)(sequences[i], kmers) for i in tqdm(range(len(sequences))))
    frequencies = preprocessing.scale(frequencies)
    frequencies = pd.DataFrame(frequencies, columns=kmers)
    return frequencies

# Returns a list with ranks extracted from TAXXI format
def getRanks(taxxi):
    split = taxxi.split(';')
    kingdom = split[0]
    phylum = split[1]
    classs = split[2]
    order = split[3]
    family = split[4]
    genus = split[5]
    if len(split) == 6:
        return [kingdom, phylum, classs, order, family, genus]
    elif len(split) == 7:
        species = split[6]
        return [kingdom, phylum, classs, order, family, genus, species]

# Returns taxonomy ranks from training dataset
def getTaxonomy(reference_taxonomy):
    taxonomy = []
    for record in reference_taxonomy:
        taxonomy.append(getRanks(record))
    if len(taxonomy[0]) == 7:
        columns = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    else:
        columns = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus']
    taxonomy = pd.DataFrame(taxonomy, columns=columns)
    return taxonomy

# Creates dataframe that holds the IDs of the test file and predictions
def createYTest(sequences, X_test, Y_train):
    if Y_train.shape[1] == 7:
        columns = ['id', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    else:
        columns = ['id', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus']
    Y_test = pd.DataFrame(np.full((X_test.shape[0], Y_train.shape[1] + 1), ''), columns=columns)
    index = 0
    for record in sequences:
        Y_test.at[index, 'id'] = record
        index = index + 1
    return Y_test

def classify(reference_reads: DNAIterator, reference_taxonomy: pd.Series, query: DNAFASTAFormat, kmer: int = 6, threads: int = -1) -> pd.DataFrame:
    print("Computing k-mer frequencies")
    kmers = calculatePossibleKmers(kmer)
    if threads == -1:
        threads = multiprocessing.cpu_count()
    ########################## Train ##########################
    training_ids, training_sequences = _extract_reads(reference_reads)
    X_train = computeFrequencies(training_sequences, kmers, threads)
    Y_train = getTaxonomy(reference_taxonomy)
    ########################## Test ##########################
    query = DNAIterator(skbio.read(str(query), format='fasta', constructor=skbio.DNA))
    test_ids, test_sequences = _extract_reads(query)
    X_test = computeFrequencies(test_sequences, kmers, threads)
    Y_test = createYTest(test_ids, X_test, Y_train)
    ########################## Predict ##########################
    taxonomy = predict(X_train, Y_train, X_test, Y_test, threads)
    confidence = [-1] * len(test_ids)
    result = pd.DataFrame({'Taxon': taxonomy, 'Confidence': confidence}, index=test_ids, columns=['Taxon', 'Confidence'])
    result.index.name = 'Feature ID'
    return result

def _extract_reads(reads):
    return zip(*[(r.metadata['id'], r._string) for r in reads])

def predict(X_train, Y_train, X_test, Y_test, threads):
    # Checks if there is only one label to predict
    # This is to avoid errors thrown by Logistic Regression
    # And we do not need a classifier if there is only one class to predict
    unique_kingdom = Y_train.loc[:, 'kingdom'].unique()
    if len(unique_kingdom) > 1:
        with parallel_backend('loky', n_jobs=threads, inner_max_num_threads=threads):
            model = LogisticRegression(solver='lbfgs', multi_class='auto', class_weight='balanced', max_iter=1000, verbose=0)
            model.fit(X_train, Y_train.loc[:, 'kingdom'])
            Y_test.at[:, 'kingdom'] = model.predict(X_test)
    else:
        Y_test.at[:, 'kingdom'] = np.full(X_test.shape[0], unique_kingdom)

    def classify(parent_index):
        parent = parents[parent_index]
        X_train_node = X_train.loc[Y_train.iloc[:, rank_index - 2] == parent]
        Y_train_node = Y_train.loc[Y_train.iloc[:, rank_index - 2] == parent].iloc[:, rank_index - 1]
        X_test_node = X_test.loc[Y_test.iloc[:, rank_index - 1] == parent]
        children = Y_train_node.unique()
        # Use logistic regression only if there is more than one class to predict
        if len(children) > 1:
            with parallel_backend('loky', n_jobs=threads, inner_max_num_threads=threads):
                model = LogisticRegression(solver='lbfgs', multi_class='auto', class_weight='balanced', max_iter=1000, verbose=0)
                model.fit(X_train_node, Y_train_node)
                Y_test.at[Y_test.iloc[:, rank_index - 1] == parent, ranks[rank_index - 1]] = model.predict(X_test_node)
        else:
            Y_test.at[Y_test.iloc[:, rank_index - 1] == parent, ranks[rank_index - 1]] = np.full(X_test_node.shape[0], children)

    # Iterative approach for the hierarchical model
    # Consumes less memory than the recursive version
    # And we can predict right after training each local model
    # Saving even more memory
    ranks = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    for rank_index in range(2, Y_test.shape[1]):
        print("Predicting labels for %s" % (ranks[rank_index - 1]))
        parents = Y_test.iloc[:, rank_index - 1].unique()
        for i in tqdm(range(len(parents))):
            classify(i)
    #    Parallel(n_jobs=min(args.threads, len(parents)), backend="threading")(delayed(classify)(i) for i in tqdm(range(len(parents))))

    # Saves predictions
    print("Saving predictions")
    predictions = []
    for i in tqdm(range(Y_test.shape[0])):
        taxonomy = Y_test.at[i, 'kingdom'] + ';'
        taxonomy = taxonomy + Y_test.at[i, 'phylum'] + ';'
        taxonomy = taxonomy + Y_test.at[i, 'class'] + ';'
        taxonomy = taxonomy + Y_test.at[i, 'order'] + ';'
        taxonomy = taxonomy + Y_test.at[i, 'family'] + ';'
        if Y_train.shape[1] == 7:
            taxonomy = taxonomy + Y_test.at[i, 'genus'] + ';'
            taxonomy = taxonomy + Y_test.at[i, 'species']
        else:
            taxonomy = taxonomy + Y_test.at[i, 'genus']
        predictions.append(taxonomy)
    return predictions
