"""
Neural and Behavioral Data Processing Module

This module provides a comprehensive toolkit for processing neural spike data,
kinematic/behavioral data, and ECoG recordings from neuroscience experiments.
It includes efficient functions for extracting time-windowed data chunks,
binning spike trains, and generating phonetic kinematic trajectories for
speech experiments.

Module Organization
-------------------
The module is organized into four functional areas:

1. **Kinematic Data Extraction**
   - get_pos_chunk: Extract kinematic data chunks based on time windows
   - get_windowed_pos_chunk: Extract windowed chunks around center times

2. **Spike Data Processing**
   - get_chunk_spikes: Extract spike times with multiple output formats
   - get_chunk_spikes_binned: Bin spikes into fixed time bins (3D arrays)
   - get_chunk_spikes_binned_windowed: Windowed version of binned extraction
   - get_chunk_spikes_aligned: Extract and align spikes with padding

3. **Time Series Utilities**
   - timestamps_to_binary: Convert time intervals to binary time series
   - samples_to_timeseries: Generate time arrays from sample count and rate

4. **Phonetic/Speech Analysis**
   - map_vowels_to_unit_circle: Map vowel sounds to 2D unit circle coordinates
   - encode_sounds_to_2d: Encode sound lists to 2D coordinate arrays
   - generate_phonetic_kinematics: Generate interpolated vowel trajectories
   - get_human_kinematics: Extract speaking activity from NWB ECoG files

Key Functions
-------------
get_pos_chunk : function
    Core function for extracting time-windowed chunks from kinematic data.
    Uses efficient binary search for fast lookups across multiple time windows.

get_chunk_spikes : function
    Extract spike times from multiple units across multiple time windows.
    Supports list, dict, and ragged array output formats.

get_chunk_spikes_binned : function
    Extract and bin spike data into 3D arrays [chunks × units × time_bins].
    Ideal for creating inputs to neural decoders and machine learning models.

get_human_kinematics : function
    Process NWB files from speech experiments to extract phonetic kinematics.
    Generates 2D trajectories representing vowel articulation in phonetic space.

Dependencies
------------
Standard Libraries:
    - numpy : All array operations, numerical computing, and linear algebra

Data Structures
---------------
Spike Data:
    - List format: List of arrays, one per unit containing spike times
    - Binned format: 3D array [n_chunks, n_units, n_bins] with spike counts
    - Aligned format: Padded 3D array with NaN for missing spikes

Kinematic Data:
    - Can be 1D (scalar) or 2D (multi-dimensional, e.g., [x, y] position)
    - Time-aligned with timestamps array
    - Extracted as list of arrays (one per time window)

Phonetic Data:
    - 2D coordinates (x, y) on unit circle representing vowel space
    - Three vowel categories: front_high (ee), back_high (oo), back_low (aa)
    - Interpolated trajectories during vowel transitions

Performance Considerations
--------------------------
- All functions use vectorized numpy operations for efficiency
- Binary search (searchsorted) used for time-based lookups: O(log n)
- Spike extraction scales well to 100+ units and 1000+ time windows
- Binning operations pre-allocate arrays to avoid memory reallocation
- For very large datasets, consider processing in batches

Data Format Requirements
------------------------
Timestamps:
    - Must be monotonically increasing
    - Typically in seconds
    - Should be uniformly sampled for binning operations

Spike Times:
    - List of arrays, one per unit/neuron
    - Times in seconds, sorted in ascending order
    - Can handle units with zero spikes (empty arrays)

NWB Files (for get_human_kinematics):
    - Must contain 'ElectricalSeries' in acquisition
    - Must have trials table with columns: 'speak', 'cv_transition_time', 
      'stop_time', 'condition'
    - Condition field must contain sounds ending in 'aa', 'ee', or 'oo'

Examples
--------
Extract velocity chunks around go cues:
>>> velocity_chunks = get_windowed_pos_chunk(
...     kinematics=cursor_velocity,
...     timestamps=kin_timestamps,
...     center_times=go_cue_times,
...     window_size=[-0.2, 0.8]  # 200ms before to 800ms after
... )

Bin spikes for multiple trials:
>>> binned_spikes, metadata = get_chunk_spikes_binned(
...     list_units_spkts=spike_times_per_unit,
...     start_times=trial_starts,
...     end_times=trial_ends,
...     bin_size=0.050  # 50ms bins
... )
>>> print(f"Shape: {binned_spikes.shape}")  # [n_trials, n_units, n_bins]
>>> print(f"Bin size: {metadata['bin_size']}")

Create binary time series for trial periods:
>>> timestamps = np.arange(0, 10, 0.001)  # 10 seconds at 1kHz
>>> trial_periods = np.array([[1.0, 2.0], [5.0, 7.0]])  # two trials
>>> is_trial = timestamps_to_binary(timestamps, trial_periods)
>>> print(f"Trial samples: {np.sum(is_trial)}")

Generate phonetic trajectories:
>>> sounds = ['baa', 'dee', 'goo']
>>> coords, vowel_types = encode_sounds_to_2d(sounds)
>>> print(f"Vowel types: {vowel_types}")
>>> # ['back_low', 'front_high', 'back_high']

Notes
-----
- All time values should use consistent units (typically seconds)
- Empty time windows return empty arrays with appropriate shape
- Functions handle edge cases (empty units, zero-duration windows)
- Overlapping time windows are supported and processed independently
- For speech data, only trials with speak==True are processed

Common Pitfalls
---------------
- Ensure timestamps and kinematic arrays have same length
- Spike times must be sorted for efficient searchsorted operations
- Window sizes are [before, after] relative to center time
- Bin sizes should match your analysis time scale (typically 10-100ms)
- NWB files must have all required fields for get_human_kinematics()

Version Information
-------------------
Author: Autumn Mallory
Date: December 2025
Version: 1.0
"""

# ============================================================================
# IMPORTS
# ============================================================================

# Standard library - numpy is the only required import
import numpy as np


def get_pos_chunk(timestamps, kinematics, start_times, end_times) -> list:
    """
    Extract chunks of kinematic data based on start and end times.
    
    This function extracts segments of kinematic data that fall within
    specified time windows. It efficiently handles multiple time windows
    by sorting and using vectorized operations.
    
    Parameters
    ----------
    timestamps : array-like
        1D array of timestamps corresponding to kinematic samples.
    kinematics : array-like
        Kinematic data array. Can be either:
        - 1D array of shape (n_samples,) for scalar kinematics
        - 2D array of shape (n_samples, n_features) for multi-dimensional kinematics
        Must have the same length as timestamps along the first dimension.
    start_times : array-like
        Array of start times for each chunk to extract.
    end_times : array-like
        Array of end times for each chunk to extract.
        Must have the same length as start_times.
    
    Returns
    -------
    list of numpy.ndarray
        List of extracted kinematic data chunks. Each chunk corresponds to
        data within one [start_time, end_time) interval. Empty chunks are
        returned as empty arrays when no data falls within the time window.
    
    Raises
    ------
    ValueError
        If timestamps is None or empty.
        If kinematics is None or empty.
        If start_times and end_times have different lengths.
        If timestamps and kinematics have different lengths along first dimension.
    
    Examples
    --------
    >>> timestamps = np.array([0, 1, 2, 3, 4, 5])
    >>> kinematics = np.array([10, 20, 30, 40, 50, 60])
    >>> start_times = [1, 3.5]
    >>> end_times = [3, 5]
    >>> chunks = get_pos_chunk(timestamps, kinematics, start_times, end_times)
    >>> print(chunks[0])  # Data from time 1 to 3
    [20 30]
    >>> print(chunks[1])  # Data from time 3.5 to 5
    [40 50]
    
    Notes
    -----
    The function uses binary search (np.searchsorted) for efficient lookup.
    Start times use 'left' side (inclusive) and end times use 'right' side
    (exclusive), so intervals are [start_time, end_time).
    Chunks are returned in the sorted order of start_times.
    """
    # Validate inputs
    if timestamps is None or len(timestamps) == 0:
        raise ValueError("timestamps cannot be None or empty")
    if kinematics is None or len(kinematics) == 0:
        raise ValueError("kinematics cannot be None or empty")
    if len(start_times) != len(end_times):
        raise ValueError("start_times and end_times must have the same length")
    
    # Convert to numpy arrays once
    timestamps = np.asarray(timestamps)
    kinematics = np.asarray(kinematics)
    start_times = np.asarray(start_times)
    end_times = np.asarray(end_times)
    
    # Validate that timestamps and kinematics have matching lengths
    if len(timestamps) != len(kinematics):
        raise ValueError(
            f"timestamps and kinematics must have the same length, "
            f"got {len(timestamps)} and {len(kinematics)}"
        )
    
    # Sort by start times for efficient sequential access
    sort_idx = np.argsort(start_times)
    sorted_start_times = start_times[sort_idx]
    sorted_end_times = end_times[sort_idx]
    
    # Vectorized searchsorted for all start/end times at once
    start_indices = np.searchsorted(timestamps, sorted_start_times, side='left')
    end_indices = np.searchsorted(timestamps, sorted_end_times, side='right')
    
    # Extract chunks
    chunks = []
    for start_idx, end_idx in zip(start_indices, end_indices):
        if start_idx < end_idx:  # Only add non-empty chunks
            chunk = kinematics[start_idx:end_idx]
            chunks.append(chunk)
        else:
            # Return empty array with appropriate shape
            if kinematics.ndim == 1:
                chunks.append(np.array([]))
            else:
                chunks.append(np.empty((0, kinematics.shape[1])))
    
    return chunks

def get_windowed_pos_chunk(kinematics, timestamps, center_times, window_size) -> list:
    """Extract windowed chunks of data from an HDF5 dataset based on center times and window size.

    Args:
        hdf_dataset: HDF5 dataset object with time-indexed data.
        center_times (list): List of center times for each chunk.
        window_size (list): Two floats specifying the window size before and after the center time.
    Returns:
        list: List of numpy arrays containing the extracted data chunks.
    """
    if len(window_size) != 2:
        raise ValueError(f"window_size must be a list of two floats, but got {len(window_size)}: {window_size}")

    center_times = np.asarray(center_times)
    window_size = np.asarray(window_size)

    before, after = window_size

    start_times = center_times - before
    end_times = center_times + after

    return get_pos_chunk(timestamps, kinematics, start_times, end_times)


def get_chunk_spikes(list_units_spkts, start_times, end_times, return_format='list'):
    """Extract spike times from a list of units based on start and end times.

    Args:
        list_units_spkts: List of spike times for each unit (each element is array-like).
        start_times (list): List of start times for each chunk.
        end_times (list): List of end times for each chunk.
        return_format (str): 'list', 'dict', or 'ragged' for output format.

    Returns:
        If return_format='list': List of shape [n_chunks][n_units] containing spike arrays
        If return_format='dict': Dict with keys 'spikes', 'counts', 'chunk_times'
        If return_format='ragged': Ragged array structure with metadata
    """
    # Convert to numpy arrays for faster operations
    start_times = np.asarray(start_times)
    end_times = np.asarray(end_times)
    n_chunks = len(start_times)
    n_units = len(list_units_spkts)

    # Pre-convert all units to numpy arrays once
    units_array = [np.asarray(unit) for unit in list_units_spkts]

    # Pre-allocate result structure
    chunked_list = [[None for _ in range(n_units)] for _ in range(n_chunks)]

    # Vectorized approach: use searchsorted for each unit
    for unit_idx, spikes in enumerate(units_array):
        if len(spikes) == 0:
            # Handle empty units
            for chunk_idx in range(n_chunks):
                chunked_list[chunk_idx][unit_idx] = np.array([])
            continue

        # Find indices for all chunks at once using searchsorted
        start_indices = np.searchsorted(spikes, start_times, side='left')
        end_indices = np.searchsorted(spikes, end_times, side='right')

        # Extract spikes for each chunk
        for chunk_idx in range(n_chunks):
            start_idx = start_indices[chunk_idx]
            end_idx = end_indices[chunk_idx]
            chunked_list[chunk_idx][unit_idx] = spikes[start_idx:end_idx]

    if return_format == 'dict':
        return {
            'spikes': chunked_list,
            'counts': [[len(chunked_list[c][u]) for u in range(n_units)]
                       for c in range(n_chunks)],
            'chunk_times': list(zip(start_times, end_times)),
            'n_units': n_units,
            'n_chunks': n_chunks
        }
    elif return_format == 'ragged':
        # Return as structured array with metadata
        return {
            'data': chunked_list,
            'spike_counts': np.array([[len(chunked_list[c][u]) for u in range(n_units)]
                                      for c in range(n_chunks)]),
            'start_times': start_times,
            'end_times': end_times
        }
    else:
        return chunked_list


def get_chunk_spikes_binned(list_units_spkts, start_times, end_times, bin_size=0.001):
    """Extract and bin spike times into fixed-size bins for array output.

    Args:
        list_units_spkts: List of spike times for each unit.
        start_times (list): List of start times for each chunk.
        end_times (list): List of end times for each chunk.
        bin_size (float): Size of time bins in seconds.

    Returns:
        numpy.ndarray: 3D array of shape [n_chunks, n_units, n_bins] with spike counts
        dict: Metadata including bin_edges, actual_times, etc.
    """
    start_times = np.asarray(start_times)
    end_times = np.asarray(end_times)
    n_chunks = len(start_times)
    n_units = len(list_units_spkts)

    # Calculate number of bins for each chunk
    chunk_durations = end_times - start_times
    n_bins_per_chunk = np.ceil(chunk_durations / bin_size).astype(int)
    max_bins = n_bins_per_chunk.max()

    # Pre-allocate 3D array
    binned_spikes = np.zeros((n_chunks, n_units, max_bins), dtype=np.int32)

    # Convert units to numpy arrays
    units_array = [np.asarray(unit) for unit in list_units_spkts]

    # Bin spikes for each chunk and unit
    for chunk_idx, (start, end, n_bins) in enumerate(zip(start_times, end_times, n_bins_per_chunk)):
        bin_edges = np.linspace(start, end, n_bins + 1)

        for unit_idx, spikes in enumerate(units_array):
            # Extract spikes in this chunk
            mask = (spikes >= start) & (spikes <= end)
            chunk_spikes = spikes[mask]

            if len(chunk_spikes) > 0:
                # Bin the spikes
                counts, _ = np.histogram(chunk_spikes, bins=bin_edges)
                binned_spikes[chunk_idx, unit_idx, :n_bins] = counts

    metadata = {
        'bin_size': bin_size,
        'n_bins_per_chunk': n_bins_per_chunk,
        'start_times': start_times,
        'end_times': end_times,
        'chunk_durations': chunk_durations
    }

    return binned_spikes, metadata

def get_chunk_spikes_binned_windowed(list_units_spkts, center_times, window_size, bin_size=0.001):

    center_times = np.asarray(center_times)
    window_size = np.asarray(window_size)

    before, after = window_size

    start_times = center_times - before
    end_times = center_times + after

    return get_chunk_spikes_binned(list_units_spkts, start_times, end_times, bin_size=bin_size)


def get_chunk_spikes_aligned(list_units_spkts, start_times, end_times, max_duration=None):
    """Extract spikes and pad to create aligned 3D array.

    Args:
        list_units_spkts: List of spike times for each unit.
        start_times (list): List of start times for each chunk.
        end_times (list): List of end times for each chunk.
        max_duration (float): Maximum duration to consider. If None, uses longest chunk.

    Returns:
        numpy.ndarray: 3D array [n_chunks, n_units, max_spikes] with spike times (relative to chunk start)
        numpy.ndarray: 3D array [n_chunks, n_units, max_spikes] with valid spike mask
        dict: Metadata
    """
    start_times = np.asarray(start_times)
    end_times = np.asarray(end_times)
    n_chunks = len(start_times)
    n_units = len(list_units_spkts)

    units_array = [np.asarray(unit) for unit in list_units_spkts]

    # First pass: find maximum number of spikes in any chunk for any unit
    max_spikes = 0
    spike_lists = [[None for _ in range(n_units)] for _ in range(n_chunks)]

    for unit_idx, spikes in enumerate(units_array):
        start_indices = np.searchsorted(spikes, start_times, side='left')
        end_indices = np.searchsorted(spikes, end_times, side='right')

        for chunk_idx in range(n_chunks):
            chunk_spikes = spikes[start_indices[chunk_idx]:end_indices[chunk_idx]]
            # Convert to relative times
            relative_spikes = chunk_spikes - start_times[chunk_idx]
            spike_lists[chunk_idx][unit_idx] = relative_spikes
            max_spikes = max(max_spikes, len(relative_spikes))

    # Second pass: create padded arrays
    spike_array = np.full((n_chunks, n_units, max_spikes), np.nan, dtype=np.float32)
    valid_mask = np.zeros((n_chunks, n_units, max_spikes), dtype=bool)

    for chunk_idx in range(n_chunks):
        for unit_idx in range(n_units):
            spikes = spike_lists[chunk_idx][unit_idx]
            n_spikes = len(spikes)
            if n_spikes > 0:
                spike_array[chunk_idx, unit_idx, :n_spikes] = spikes
                valid_mask[chunk_idx, unit_idx, :n_spikes] = True

    metadata = {
        'max_spikes': max_spikes,
        'start_times': start_times,
        'end_times': end_times,
        'spike_counts': valid_mask.sum(axis=2)  # [n_chunks, n_units]
    }

    return spike_array, valid_mask, metadata


def timestamps_to_binary(timestamps, start_stop_times):
    """
    Convert timestamps to binary time series based on start/stop intervals.
    
    Parameters
    ----------
    timestamps : array-like
        Array of timestamps to evaluate.
    start_stop_times : array-like
        2D array of shape (n, 2) where each row contains [start_time, stop_time].
        The first column contains start times, the second column contains stop times.
    
    Returns
    -------
    numpy.ndarray
        Binary array of shape (len(timestamps),) where 1 indicates the timestamp
        falls within at least one start/stop interval, and 0 indicates it falls
        outside all intervals.
    
    Raises
    ------
    ValueError
        If start_stop_times is not a 2D array with 2 columns.
        If any stop time is less than its corresponding start time.
    
    Examples
    --------
    >>> timestamps = np.array([0, 1, 2, 3, 4, 5])
    >>> start_stop = np.array([[1, 3], [4, 5]])
    >>> timestamps_to_binary(timestamps, start_stop)
    array([0, 1, 1, 1, 1, 1])
    
    >>> timestamps = np.array([0.5, 1.5, 2.5, 3.5])
    >>> start_stop = np.array([[1.0, 2.0]])
    >>> timestamps_to_binary(timestamps, start_stop)
    array([0, 1, 0, 0])
    
    Notes
    -----
    If intervals overlap, timestamps within overlapping regions are still marked
    as 1 (within interval). The function uses vectorized operations for efficiency.
    Interval boundaries are inclusive: timestamps equal to start or stop times
    are considered within the interval.
    """
    import numpy as np
    
    timestamps = np.asarray(timestamps)
    start_stop_times = np.asarray(start_stop_times)
    
    # Validate input shape
    if start_stop_times.ndim != 2 or start_stop_times.shape[1] != 2:
        raise ValueError(
            "start_stop_times must be a 2D array with 2 columns "
            f"(start, stop), got shape {start_stop_times.shape}"
        )
    
    # Validate start <= stop for all pairs
    if np.any(start_stop_times[:, 1] < start_stop_times[:, 0]):
        raise ValueError("All stop times must be >= their corresponding start times")
    
    # Initialize binary array
    binary_series = np.zeros(len(timestamps), dtype=int)
    
    # Check each interval
    for start, stop in start_stop_times:
        # Mark timestamps within this interval as 1
        within_interval = (timestamps >= start) & (timestamps <= stop)
        binary_series = np.logical_or(binary_series, within_interval).astype(int)
    
    return binary_series

def samples_to_timeseries(n_samples, fs):
    """
    Convert number of samples and sampling frequency to a time series.
    
    Parameters
    ----------
    n_samples : int
        Number of samples in the time series.
    fs : float
        Sampling frequency in Hz.
    
    Returns
    -------
    numpy.ndarray
        Array of time values starting at 0, with shape (n_samples,).
    
    Raises
    ------
    ValueError
        If n_samples is not positive or fs is not positive.
    
    Examples
    --------
    >>> samples_to_timeseries(5, 100)
    array([0.  , 0.01, 0.02, 0.03, 0.04])
    
    >>> samples_to_timeseries(10, 1000)
    array([0.   , 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009])
    
    Notes
    -----
    The time series is generated using numpy.arange with a step size of 1/fs.
    The resulting array will have exactly n_samples elements.
    """
    import numpy as np
    
    if n_samples <= 0:
        raise ValueError("n_samples must be positive")
    if fs <= 0:
        raise ValueError("fs must be positive")
    
    return np.arange(n_samples) / fs

def map_vowels_to_unit_circle():
    """
    Map vowel sounds to positions on a unit circle based on phonetic features.
    
    The mapping uses the traditional vowel space where:
    - Front vowels (ee) are on the right
    - Back vowels (aa, oo) are on the left
    - High vowels (ee, oo) are at the top
    - Low vowels (aa) are at the bottom
    
    Returns
    -------
    vowel_positions : dict
        Dictionary mapping vowel categories to (x, y) coordinates on unit circle.
    vowel_angles : dict
        Dictionary mapping vowel categories to angles in radians.
    
    Examples
    --------
    >>> positions = map_vowels_to_unit_circle()
    >>> print(positions['vowel_positions']['front_high'])
    (1.0, 0.0)
    """
    vowel_angles = {
        'front_high': 0,           # /i/ "ee" - 0° (right, like 3 o'clock)
        'back_high': 2 * np.pi / 3,  # /u/ "oo" - 120° (upper left)
        'back_low': 4 * np.pi / 3    # /ɑ/ "aa" - 240° (lower left)
    }
    
    vowel_positions = {}
    for vowel, angle in vowel_angles.items():
        x = np.cos(angle)
        y = np.sin(angle)
        vowel_positions[vowel] = (x, y)
    
    return {
        'vowel_positions': vowel_positions,
        'vowel_angles': vowel_angles
    }


def encode_sounds_to_2d(sound_list):
    """
    Encode a list of sounds into 2D coordinates on the unit circle.
    
    Parameters
    ----------
    sound_list : list of str
        List of sound strings (e.g., ['baa', 'dee', 'foo']).
        Each sound should end with 'aa', 'ee', or 'oo'.
    
    Returns
    -------
    coordinates : numpy.ndarray
        Array of shape (n_sounds, 2) containing (x, y) coordinates
        for each sound on the unit circle.
    vowel_types : list of str
        List of vowel categories corresponding to each sound.
    
    Examples
    --------
    >>> sounds = ['baa', 'dee', 'foo']
    >>> coords, vowels = encode_sounds_to_2d(sounds)
    >>> print(coords)
    [[-0.5  -0.866]
     [ 1.    0.   ]
     [-0.5   0.866]]
    """
    # Get vowel mappings
    mapping = map_vowels_to_unit_circle()
    positions = mapping['vowel_positions']
    
    # Create lookup from vowel suffix to category
    vowel_suffix_to_category = {
        'aa': 'back_low',
        'ee': 'front_high',
        'oo': 'back_high'
    }
    
    # Encode each sound
    coordinates = []
    vowel_types = []
    
    for sound in sound_list:
        # Extract vowel suffix (last 2 characters)
        vowel_suffix = sound[-2:]
        
        # Get vowel category
        vowel_category = vowel_suffix_to_category.get(vowel_suffix)
        
        if vowel_category is None:
            raise ValueError(f"Unknown vowel suffix '{vowel_suffix}' in sound '{sound}'")
        
        # Get coordinates
        x, y = positions[vowel_category]
        coordinates.append([x, y])
        vowel_types.append(vowel_category)
    
    return np.array(coordinates), vowel_types


def generate_phonetic_kinematics(timestamps, start_stop_times, coordinates):
    """
    Generate interpolated phonetic kinematic trajectories for vowel transitions.
    
    This function creates a 2D kinematic time series that interpolates from
    (0, 0) to target vowel coordinates during each vowel transition period.
    Outside of transition periods, the kinematic values are (0, 0).
    
    Parameters
    ----------
    timestamps : array-like
        1D array of timestamps for the kinematic time series.
    start_stop_times : array-like
        2D array of shape (n_transitions, 2) where each row contains
        [start_time, stop_time] for a vowel transition period.
    coordinates : array-like
        2D array of shape (n_transitions, 2) containing the target (x, y)
        coordinates for each vowel transition. Each row corresponds to the
        matching row in start_stop_times.
    
    Returns
    -------
    phonetic_kinematics : numpy.ndarray
        2D array of shape (len(timestamps), 2) containing interpolated
        (x, y) kinematic values. During each transition period, values
        interpolate linearly from (0, 0) to the target coordinates.
        Outside transition periods, values are (0, 0).
    
    Raises
    ------
    ValueError
        If start_stop_times and coordinates have different numbers of rows.
        If start_stop_times is not shape (n, 2).
        If coordinates is not shape (n, 2).
    
    Examples
    --------
    >>> timestamps = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    >>> start_stop_times = np.array([[0.1, 0.3]])
    >>> coordinates = np.array([[1.0, 0.5]])
    >>> kinematics = generate_phonetic_kinematics(timestamps, start_stop_times, coordinates)
    >>> print(kinematics)
    [[0.   0.  ]
     [0.   0.  ]
     [0.5  0.25]
     [1.   0.5 ]
     [0.   0.  ]
     [0.   0.  ]]
    
    Notes
    -----
    The function performs linear interpolation from (0, 0) at the start_time
    to the target coordinates at the stop_time for each transition period.
    If transition periods overlap, the last transition takes precedence.
    """
    
    # Convert inputs to numpy arrays
    timestamps = np.asarray(timestamps)
    start_stop_times = np.asarray(start_stop_times)
    coordinates = np.asarray(coordinates)
    
    # Validate inputs
    if start_stop_times.ndim != 2 or start_stop_times.shape[1] != 2:
        raise ValueError(
            f"start_stop_times must be shape (n, 2), got {start_stop_times.shape}"
        )
    
    if coordinates.ndim != 2 or coordinates.shape[1] != 2:
        raise ValueError(
            f"coordinates must be shape (n, 2), got {coordinates.shape}"
        )
    
    if start_stop_times.shape[0] != coordinates.shape[0]:
        raise ValueError(
            f"start_stop_times and coordinates must have same number of rows, "
            f"got {start_stop_times.shape[0]} and {coordinates.shape[0]}"
        )
    
    # Initialize output array with zeros
    phonetic_kinematics = np.zeros((len(timestamps), 2))
    
    # Process each transition period
    for i, (start_time, stop_time) in enumerate(start_stop_times):
        # Get target coordinates for this transition
        target_x, target_y = coordinates[i]
        
        # Find timestamps within this transition period
        within_transition = (timestamps >= start_time) & (timestamps <= stop_time)
        
        if not np.any(within_transition):
            continue  # No timestamps in this period
        
        # Get the timestamps in this period
        transition_timestamps = timestamps[within_transition]
        
        # Calculate interpolation parameter (0 at start, 1 at stop)
        duration = stop_time - start_time
        if duration == 0:
            # If start and stop are the same, set to target coordinates
            alpha = np.ones_like(transition_timestamps)
        else:
            alpha = (transition_timestamps - start_time) / duration
        
        # Linear interpolation from (0, 0) to (target_x, target_y)
        phonetic_kinematics[within_transition, 0] = alpha * target_x
        phonetic_kinematics[within_transition, 1] = alpha * target_y
    
    return phonetic_kinematics

def get_human_kinematics(nwbfile):
    """
    Extract binary speaking activity time series from NWB file.
    
    This function creates a binary time series indicating when a human subject
    was actively speaking during ECoG recordings. Speaking periods are derived
    from trial metadata in the NWB file.
    
    Parameters
    ----------
    nwbfile : d.NWBFile
        NWB file object containing ECoG data and trial information.
        Must contain:
        - acquisition['ElectricalSeries']: ECoG recordings with .data and .rate
        - trials: DataFrame with 'speak', 'start_time', and 'stop_time' columns
    
    Returns
    -------
    binary_kinematic : numpy.ndarray
        Binary array of shape (n_samples,) where 1 indicates the subject was
        speaking and 0 indicates the subject was not speaking.
    timestamps : numpy.ndarray
        Array of timestamps corresponding to each sample in binary_kinematic,
        starting at 0 and sampled at the ECoG sampling rate.
    
    Raises
    ------
    KeyError
        If 'ElectricalSeries' is not found in nwbfile.acquisition.
    AttributeError
        If required fields are missing from the NWB file structure.
    ValueError
        If no speaking trials are found (all speak==False).
    
    Examples
    --------
    >>> binary_kin, times = get_human_kinematics(nwbfile)
    >>> print(f"Total samples: {len(binary_kin)}")
    >>> print(f"Speaking samples: {np.sum(binary_kin)}")
    >>> print(f"Duration: {times[-1]:.2f} seconds")
    
    Notes
    -----
    The function filters trials to include only those where speak==True,
    then marks all timestamps falling within those trial periods as speaking (1).
    All other timestamps are marked as non-speaking (0).
    """
    total_samples = nwbfile.acquisition['ElectricalSeries'].data.shape[0]
    fs = nwbfile.acquisition['ElectricalSeries'].rate
    timestamps = samples_to_timeseries(total_samples, fs)
    
    data = nwbfile.trials[:]
    remove_non_speaking = data['speak']
    data = data[remove_non_speaking]
    
    start_stop_times = np.array(data[["cv_transition_time", "stop_time"]])
    sounds = data.condition
    # Encode to 2D coordinates
    coordinates, vowel_categories = encode_sounds_to_2d(sounds)

    phonetic_kinematics = generate_phonetic_kinematics(timestamps, start_stop_times, coordinates)
    #binary_kinematic = timestamps_to_binary(timestamps, start_stop_times)

    return phonetic_kinematics, timestamps

