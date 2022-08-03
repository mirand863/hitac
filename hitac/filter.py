"""Extends the LocalClassifierPerLevel."""
from typing import List

import numpy as np
from hiclass import LocalClassifierPerLevel


class Filter(LocalClassifierPerLevel):
    """Add the predict_proba method and classes_ attribute."""

    def fit(self, X, y):
        """
        Fit a local classifier per level.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The training input samples. Internally, its dtype will be converted
            to ``dtype=np.float32``. If a sparse matrix is provided, it will be
            converted into a sparse ``csc_matrix``.
        y : array-like of shape (n_samples, n_levels)
            The target values, i.e., hierarchical class labels for classification.

        Returns
        -------
        self : object
            Fitted estimator.
        """
        super().fit(X, y)
        self.classes_ = [
            self._remove_separator(classifier.classes_)
            for classifier in self.local_classifiers_
        ]
        return self

    def predict_proba(self, X: np.ndarray) -> List:
        """
        Compute prediction probabilities.

        Parameters
        ----------
        X : np.array of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        probabilities : np.ndarray of shape (n_levels, n_samples)
            Prediction probabilities for all classes in each hierarchical level.
        """
        probabilities = []
        for classifier in self.local_classifiers_:
            probabilities.append(classifier.predict_proba(X))
        return probabilities

    def _remove_separator(self, classes: np.ndarray) -> np.ndarray:
        return np.array([value.split(self.separator_)[-1] for value in classes])
