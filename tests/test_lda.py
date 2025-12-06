# tests/test_lda.py
import numpy as np
from src.cse583_human_say_monkey_do.analysis import train_lda_classifier


def test_train_lda_classifier_smoke():
    X = np.random.rand(10, 5, 3)  # 10 trials, 5x3 features
    y = np.array([0,1]*5)

    lda, results = train_lda_classifier(X, y)

    assert 'train_accuracy' in results
    assert 'test_accuracy' in results
    assert 'cv_scores' in results
    assert 0 <= results['train_accuracy'] <= 1
