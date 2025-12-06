# tests/test_plotting.py
import numpy as np
from cse583_human_say_monkey_do.visualization import (
    plot_firing_rate_heatmap,
    plot_lda_results
)


def test_plot_firing_rate_heatmap_smoke():
    data = np.random.rand(5, 10)
    fig, ax = plot_firing_rate_heatmap(data)
    assert fig is not None


def test_plot_lda_results_smoke():
    # minimal fake results
    results = {
        'y_test': np.array([0,1,0,1]),
        'y_test_pred': np.array([0,1,0,1]),
        'y_test_proba': np.random.rand(4,2),
        'lda': None,  # plot_lda_results won't use transform if None
        'X_test': np.random.rand(4, 3),
        'cv_scores': np.array([0.8, 0.9, 0.85, 0.88]),
        'test_accuracy': 0.85
    }

    # prevent error: supply lda with transform
    class DummyLDA:
        def transform(self, X): return np.random.rand(len(X), 1)
    results['lda'] = DummyLDA()

    fig = plot_lda_results(results)
    assert fig is not None
