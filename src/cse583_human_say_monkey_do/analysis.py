"""
Neural Data Analysis Module: Movement Detection and LDA Classification

This module provides tools for analyzing neural and behavioral data from brain-computer
interface (BCI) experiments. It includes functions for detecting movement onsets from
velocity data and training Linear Discriminant Analysis (LDA) classifiers on neural
activity patterns.

Key Functions
-------------
get_movement_onset_times : function
    Detects movement onset times when cursor velocity exceeds a threshold after go cues.
    Uses time-windowed velocity data to identify when movement begins in each trial.

train_lda_classifier : function
    Trains and evaluates an LDA classifier on matrix-structured data (e.g., neural
    activity patterns). Performs train/test split, cross-validation, and provides
    comprehensive performance metrics.

Dependencies
------------
Standard Libraries:
    - numpy : Array operations and numerical computing
    - sklearn : Machine learning tools (LDA, train/test split, metrics)

Custom Module Dependencies:
    The following functions must be imported from your local data processing module:
    - get_windowed_pos_chunk : Extracts time-windowed chunks from position/velocity data

Typical Workflow
----------------
1. Load behavioral data (velocity, timestamps) and experimental events (go cue times)
2. Use get_movement_onset_times() to identify when movements begin
3. Extract neural data around movement onsets using time windows
4. Train LDA classifier with train_lda_classifier() to decode movement direction/type
5. Evaluate classifier performance using returned metrics and visualizations

Example Usage
-------------
>>> # Detect movement onsets
>>> movement_times, movement_indices = get_movement_onset_times(
...     velocity, timestamps, go_cue_times, threshold=5.0, window=[-0.1, 1.0]
... )
>>>
>>> # Extract neural data around movement onsets
>>> neural_data = get_windowed_neural_data(neural_array, timestamps, movement_times)
>>>
>>> # Train classifier (e.g., to decode left vs right movements)
>>> labels = [0, 1, 0, 1, ...]  # 0=left, 1=right
>>> lda, results = train_lda_classifier(neural_data, labels)
>>>
>>> # Access results
>>> print(f"Test accuracy: {results['test_accuracy']:.2%}")
>>> print(f"CV accuracy: {results['cv_mean']:.2%} ± {results['cv_std']:.2%}")

Notes
-----
- Movement onset detection assumes velocity data is in physical units (e.g., cm/s)
- LDA classifier flattens multi-dimensional neural data (e.g., channels × time) into
  feature vectors for classification
- Cross-validation uses stratified 5-fold splits to ensure balanced class representation
- All temporal windowing operations assume uniformly sampled data

Author: Autumn Mallory
Date: December 2025
Version: 1.0
"""
# Standard library imports
import numpy as np

# Third-party imports
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Local module imports
# Replace 'your_module_name' with the actual name of your local module
from cse583_human_say_monkey_do.data_formatting import get_windowed_pos_chunk

def get_movement_onset_times(velocity, timestamps, go_cue_times, threshold=5.0,
                             window=[-0.1, 1.0]):
    """Find movement onset times when velocity exceeds threshold after go cues.

    Args:
        velocity_dataset: HDF5 dataset with velocity data and timestamps
        go_cue_times (array): Times of go cues
        threshold (float): Velocity magnitude threshold for movement onset
        window (list): Time window [start, end] relative to go cue (seconds)

    Returns:
        movement_onset_times (array): Timestamps of movement onsets
        movement_onset_indices (array): Indices into velocity_dataset where movement starts
    """
    # Get velocity chunks around go cues
    cursor_moving = get_windowed_pos_chunk(velocity, timestamps, go_cue_times, window)

    # Find first index exceeding threshold for each trial
    first_idx = []
    for chunk in cursor_moving:
        magnitudes = np.linalg.norm(chunk, axis=1)
        idx = np.argmax(magnitudes > threshold)

        # Verify threshold was actually exceeded
        if magnitudes[idx] > threshold:
            first_idx.append(idx)
        else:
            first_idx.append(np.nan)  # No movement detected

    first_idx = np.array(first_idx)

    # Convert to absolute timestamps
    start_indices = np.searchsorted(timestamps, go_cue_times, side='left')

    # Calculate window start offset in indices
    window_start_offset = int(window[0] / np.median(np.diff(timestamps)))
    
    # Adjust for window offset
    movement_onset_indices = start_indices + window_start_offset + first_idx

    # Get actual timestamps (handle NaN cases)
    movement_onset_times = np.full(len(movement_onset_indices), np.nan)
    valid_mask = ~np.isnan(first_idx)
    movement_onset_times[valid_mask] = timestamps[movement_onset_indices[valid_mask].astype(int)]

    return movement_onset_times, movement_onset_indices


def train_lda_classifier(data_matrices, labels):
    """Train LDA classifier on matrix data.

    Args:
        data_matrices: List or array of shape [n_trials, n_features_1, n_features_2]
                      e.g., [n_trials, 18, 21]
        labels: Array of shape [n_trials] with values 0 or 1

    Returns:
        lda: Trained LDA classifier
        results: Dict with performance metrics
    """
    # Flatten each matrix into a vector
    # Shape: [n_trials, 18*21] = [n_trials, 378]
    X = np.array([matrix.flatten() for matrix in data_matrices])
    y = np.array(labels)

    print(f"Data shape: {X.shape}")
    print(f"Labels shape: {y.shape}")
    print(f"Class distribution: 0={np.sum(y==0)}, 1={np.sum(y==1)}")

    # Split into train and test sets (80/20 split)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.4, random_state=42, stratify=y
    )

    # Train LDA classifier
    lda = LinearDiscriminantAnalysis()
    lda.fit(X_train, y_train)

    # Make predictions
    y_train_pred = lda.predict(X_train)
    y_test_pred = lda.predict(X_test)

    # Get prediction probabilities
    y_train_proba = lda.predict_proba(X_train)
    y_test_proba = lda.predict_proba(X_test)

    # Calculate metrics
    train_accuracy = accuracy_score(y_train, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)

    # Cross-validation score (5-fold)
    cv_scores = cross_val_score(lda, X, y, cv=5)

    results = {
        'lda': lda,
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'y_train_pred': y_train_pred,
        'y_test_pred': y_test_pred,
        'y_train_proba': y_train_proba,
        'y_test_proba': y_test_proba,
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'cv_scores': cv_scores,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std()
    }

    # Print results
    print("\n=== LDA Classification Results ===")
    print(f"Training Accuracy: {train_accuracy:.3f}")
    print(f"Test Accuracy: {test_accuracy:.3f}")
    print(f"Cross-validation Accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
    print(f"\nCV Scores: {cv_scores}")

    # Confusion matrix
    print("\n=== Test Set Confusion Matrix ===")
    cm = confusion_matrix(y_test, y_test_pred)
    print(cm)

    # Classification report
    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_test_pred, target_names=['Class 0', 'Class 1']))

    return lda, results
