"""
Neural Data Visualization Module: Firing Rates and Classification Results

This module provides visualization tools for neural data analysis and machine learning
results. It includes functions for creating heatmaps of neural firing rates and
comprehensive visualizations of Linear Discriminant Analysis (LDA) classification
performance.

Key Functions
-------------
plot_firing_rate_heatmap : function
    Creates a heatmap visualization of neural population firing rates over time.
    Displays activity patterns across multiple units/neurons with optional time
    axis and automatic rate conversion from spike counts.

plot_lda_results : function
    Generates a comprehensive 4-panel visualization of LDA classification results,
    including confusion matrix, prediction probabilities, LDA projections, and
    cross-validation performance. Useful for evaluating classifier performance
    and understanding classification boundaries.

Dependencies
------------
Standard Libraries:
    - numpy : Array operations and numerical computing
    - matplotlib.pyplot : Core plotting functionality

Visualization Features
----------------------
Firing Rate Heatmap:
    - Automatic spike count to firing rate conversion
    - Flexible time axis (indices or actual time values)
    - Customizable colormaps and color scaling
    - Proper axis labels based on data type

LDA Results Visualization:
    - Confusion matrix with accuracy annotation
    - Prediction probability distributions by true class
    - 1D LDA projection showing class separation
    - Cross-validation scores across folds with mean line

Example Usage
-------------
>>> # Plot neural firing rates
>>> fig, ax = plot_firing_rate_heatmap(
...     firing_rates_2d=spike_counts,  # [96 units × 200 time bins]
...     time_axis=np.linspace(-0.5, 1.5, 200),
...     bin_size=0.01,  # 10ms bins
...     cmap='viridis',
...     title='Motor Cortex Activity During Reaching'
... )
>>> plt.savefig('firing_rates.png', dpi=300)
>>>
>>> # Visualize LDA classification results
>>> lda, results = train_lda_classifier(neural_data, labels)
>>> fig = plot_lda_results(results)
>>> plt.savefig('lda_performance.png', dpi=300)

Design Considerations
---------------------
- Heatmaps use 'nearest' interpolation to preserve discrete time bins
- Color scales default to data range but can be fixed for comparisons
- LDA visualizations assume binary classification (2 classes)
- All plots use tight_layout() for optimal spacing
- Figures are returned to allow further customization

Notes
-----
- Firing rate heatmaps work best with 20-200 units (more may be hard to see)
- Time axes should match the number of time points in the data
- LDA results require output from train_lda_classifier() function
- Cross-validation plots assume 5-fold CV (adjustable in source)

Common Use Cases
----------------
1. Neural Population Analysis:
   - Compare firing patterns across experimental conditions
   - Identify temporal structure in population activity
   - Visualize tuning curves across multiple neurons

2. Classifier Evaluation:
   - Assess classification accuracy and confusion patterns
   - Identify misclassification biases (false positives vs negatives)
   - Evaluate model confidence through probability distributions
   - Verify consistent performance across CV folds

Author: Autumn Mallory
Date: December 2025
Version: 1.0
"""

# Standard library imports
import numpy as np
from matplotlib import pyplot as plt

# Machine learning metrics import
# The confusion_matrix function is needed for plot_lda_results
from sklearn.metrics import confusion_matrix
import seaborn as sns

def plot_firing_rate_heatmap(firing_rates_2d, time_axis=None, bin_size=None,
                              figsize=(12, 8), cmap='viridis',
                              vmin=None, vmax=None, title=None):
    """Plot firing rate heatmap for a 2D matrix.

    Args:
        firing_rates_2d: 2D array [n_units, n_timepoints] - spike counts or firing rates
        time_axis: Array of time values for x-axis. If None, uses indices.
        bin_size: Time bin size in seconds. If provided, converts counts to rates (Hz)
        figsize: Figure size tuple
        cmap: Colormap name ('viridis', 'hot', 'plasma', etc.)
        vmin, vmax: Color scale limits (None = auto)
        title: Plot title (None = default title)

    Returns:
        fig, ax: Figure and axis objects
    """
    # Convert to numpy array if needed
    firing_rates_2d = np.asarray(firing_rates_2d)
    n_units, n_timepoints = firing_rates_2d.shape

    # Convert spike counts to firing rates if bin_size provided
    if bin_size is not None:
        data_to_plot = firing_rates_2d / bin_size
        rate_label = 'Firing Rate (Hz)'
    else:
        data_to_plot = firing_rates_2d
        rate_label = 'Spike Count'

    # Create time axis if not provided
    if time_axis is None:
        time_axis = np.arange(n_timepoints)
        xlabel = 'Time Bin'
    else:
        time_axis = np.asarray(time_axis)
        xlabel = 'Time (s)'

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Plot heatmap
    im = ax.imshow(data_to_plot,
                   aspect='auto',
                   cmap=cmap,
                   interpolation='nearest',
                   extent=[time_axis[0], time_axis[-1], n_units, 0],
                   vmin=vmin, vmax=vmax)

    # Add colorbar
    plt.colorbar(im, ax=ax, label=rate_label)

    # Labels and title
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel('Unit Number', fontsize=12)

    if title is None:
        title = 'Neural Population Firing Rate'
    ax.set_title(title, fontsize=14)

    plt.tight_layout()
    return fig, ax

def plot_lda_results(results):
    """Visualize LDA classification results."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Confusion Matrix
    ax = axes[0, 0]
    cm = confusion_matrix(results['y_test'], results['y_test_pred'])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_xlabel('Predicted Label')
    ax.set_ylabel('True Label')
    ax.set_title(f'Confusion Matrix\nTest Accuracy: {results["test_accuracy"]:.3f}')

    # 2. Prediction Probabilities
    ax = axes[0, 1]
    for class_label in [0, 1]:
        mask = results['y_test'] == class_label
        proba = results['y_test_proba'][mask, 1]  # Probability of class 1
        ax.hist(proba, bins=20, alpha=0.6, label=f'True Class {class_label}')
    ax.set_xlabel('Predicted Probability (Class 1)')
    ax.set_ylabel('Count')
    ax.set_title('Prediction Probability Distribution')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 3. LDA Projection (1D)
    ax = axes[1, 0]
    lda = results['lda']
    X_test_lda = lda.transform(results['X_test'])

    for class_label in [0, 1]:
        mask = results['y_test'] == class_label
        ax.hist(X_test_lda[mask, 0], bins=20, alpha=0.6, label=f'Class {class_label}')
    ax.set_xlabel('LDA Component')
    ax.set_ylabel('Count')
    ax.set_title('LDA Projection')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 4. Cross-validation scores
    ax = axes[1, 1]
    cv_scores = results['cv_scores']
    ax.bar(range(len(cv_scores)), cv_scores, color='skyblue', edgecolor='black')
    ax.axhline(y=cv_scores.mean(), color='r', linestyle='--',
               label=f'Mean: {cv_scores.mean():.3f}')
    ax.set_xlabel('Fold')
    ax.set_ylabel('Accuracy')
    ax.set_title('Cross-Validation Scores')
    ax.set_ylim([0, 1])
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
    return fig