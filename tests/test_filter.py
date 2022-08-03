import numpy as np
from sklearn.ensemble import RandomForestClassifier

from hitac.filter import Filter


def test_predict_proba_default():
    X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
    Y = np.array([[1, 2, 3], [1, 4, 5], [1, 6, 7], [1, 2, 8]])
    filter = Filter(
        local_classifier=RandomForestClassifier(random_state=0),
        replace_classifiers=False,
        n_jobs=2,
    )
    filter.fit(X, Y)
    result = filter.predict_proba(X)
    ground_truth = [
        np.array([[1.0], [1.0], [1.0], [1.0]]),
        np.array(
            [
                [0.64, 0.32, 0.04],
                [0.27, 0.69, 0.04],
                [0.07, 0.3, 0.63],
                [0.75, 0.08, 0.17],
            ]
        ),
        np.array(
            [
                [0.64, 0.0, 0.32, 0.04],
                [0.27, 0.0, 0.69, 0.04],
                [0.01, 0.06, 0.3, 0.63],
                [0.01, 0.74, 0.08, 0.17],
            ]
        ),
    ]
    for i in range(max(len(result), len(ground_truth))):
        assert np.array_equal(result[i], ground_truth[i])
