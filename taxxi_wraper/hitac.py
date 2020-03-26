#!/usr/bin/env python3

from sklearn.linear_model import LogisticRegression
from itertools import product
from Bio import SeqIO
import pandas as pd
import numpy as np
import argparse

# Train and test files are required parameters
# K-mer is optional with a default value of 6-mer
parser = argparse.ArgumentParser(description='HiTaC, a hierarchical taxonomy classifier for fungal ITS sequences')
parser.add_argument('--kmer', type=int, default=6, help='Kmer size for feature extraction [default: 6]')
parser.add_argument('--threads', type=int, default=-1, help='Number of threads [default: all threads available]')
parser.add_argument('train', type=str, help='Input FASTA file containing the sequences for training')
parser.add_argument('test', type=str, help='Input FASTA file containing the sequences for taxonomy prediction')
parser.add_argument('predictions', type=str, help='Output file to write the predictions')
args = parser.parse_args()

# Computes all kmer possibilities based on alphabet ACGT
alphabet = 'ACGT'
kmers = [''.join(c) for c in product(alphabet, repeat=args.kmer)]

# Computes kmer frequencies for training and test datasets
def computeFrequencies(fasta):
    frequencies = []
    for record in SeqIO.parse(fasta, "fasta"):
        freq = []
        for kmer in kmers:
            freq.append(record.seq.count(kmer))
        frequencies.append(freq)
    frequencies = pd.DataFrame(frequencies) # kmer frequencies are stored here
    return frequencies

# Returns a list with ranks extracted from TAXXI format
def getRanks(taxxi):
    split = taxxi.split(',')
    kingdom = split[0]
    kingdom = kingdom[kingdom.find('=') + 1:]
    phylum = split[1]
    classs = split[2]
    order = split[3]
    family = split[4]
    if len(split) == 6:
        genus = split[5].replace(';', '')
        return [kingdom, phylum, classs, order, family, genus]
    elif len(split) == 7:
        genus = split[5]
        species = split[6].replace(';', '')
        return [kingdom, phylum, classs, order, family, genus, species]

# Returns taxonomy ranks from training dataset
def getTaxonomy(fasta):
    taxonomy = []
    for record in SeqIO.parse(fasta, "fasta"):
        taxonomy.append(getRanks(record.id))
    if len(taxonomy[0]) == 7:
        columns = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    else:
        columns = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus']
    taxonomy = pd.DataFrame(taxonomy, columns=columns)
    return taxonomy

# Creates dataframe that holds the IDs of the test file and predictions
def createYTest(fasta):
    if Y_train.shape[1] == 7:
        columns = ['id', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    else:
        columns = ['id', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus']
    Y_test = pd.DataFrame(np.full((X_test.shape[0], Y_train.shape[1] + 1), ''), columns=columns)
    index = 0
    for record in SeqIO.parse(fasta, "fasta"):
        Y_test.at[index, 'id'] = record.id
        index = index + 1
    return Y_test

X_train = computeFrequencies(args.train)
Y_train = getTaxonomy(args.train)

X_test = computeFrequencies(args.test)
Y_test = createYTest(args.test)

# Checks if there is only one label to predict
# This is to avoid errors thrown by Logistic Regression
# And we do not need a classifier if there is only one class to predict
unique_kingdom = Y_train.loc[:, 'kingdom'].unique()
if len(unique_kingdom) > 1:
    model = LogisticRegression(solver='lbfgs', multi_class='auto', class_weight='balanced', max_iter=1000, verbose=0, n_jobs=args.threads)
    model.fit(X_train, Y_train.loc[:, 'kingdom'])
    Y_test.at[:, 'kingdom'] = model.predict(X_test)
else:
    Y_test.at[:, 'kingdom'] = np.full(X_test.shape[0], unique_kingdom)

# Iterative approach for the hierarchical model
# Consumes less memory than the recursive version
# And we can predict right after training each local model
# Saving even more memory
ranks = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
for rank_index in range(2, Y_test.shape[1]):
    parents = Y_test.iloc[:, rank_index - 1].unique()
    for parent in parents:
        X_train_node = X_train.loc[Y_train.iloc[:, rank_index - 2] == parent]
        Y_train_node = Y_train.loc[Y_train.iloc[:, rank_index - 2] == parent].iloc[:, rank_index - 1]
        X_test_node = X_test.loc[Y_test.iloc[:, rank_index - 1] == parent]
        children = Y_train_node.unique()
        # Use logistic regression only if there is more than one class to predict
        if len(children) > 1:
            model = LogisticRegression(solver='lbfgs', multi_class='auto', class_weight='balanced', max_iter=1000, verbose=0, n_jobs=args.threads)
            model.fit(X_train_node, Y_train_node)
            Y_test.at[Y_test.iloc[:, rank_index - 1] == parent, ranks[rank_index - 1]] = model.predict(X_test_node)
        else:
            Y_test.at[Y_test.iloc[:, rank_index - 1] == parent, ranks[rank_index - 1]] = np.full(X_test_node.shape[0], children)

# Saves predictions
predictions = open(args.predictions, 'w+')
for i in range(Y_test.shape[0]):
    predictions.write(Y_test.at[i, 'id'] + '\t')
    predictions.write(Y_test.at[i, 'kingdom'] + ',')
    predictions.write(Y_test.at[i, 'phylum'] + ',')
    predictions.write(Y_test.at[i, 'class'] + ',')
    predictions.write(Y_test.at[i, 'order'] + ',')
    predictions.write(Y_test.at[i, 'family'] + ',')
    if Y_train.shape[1] == 7:
        predictions.write(Y_test.at[i, 'genus'] + ',')
        predictions.write(Y_test.at[i, 'species'] + '\n')
    else:
        predictions.write(Y_test.at[i, 'genus'] + '\n')
predictions.close()
