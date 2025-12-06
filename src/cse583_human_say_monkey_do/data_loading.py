"""
Data Loading Module: Unified Interface for NWB Files

This module provides a unified interface for loading and extracting data from
Neurodata Without Borders (NWB) files containing both monkey (Macaca mulatta)
cursor control experiments and human (Homo sapiens) speech production experiments.
It handles species-specific data structures and returns standardized outputs.

Module Purpose
--------------
The primary goal is to abstract away species-specific data access patterns,
allowing analysis code to work seamlessly with both monkey and human datasets.
Functions automatically detect the subject species and route to appropriate
extraction methods, returning data in consistent formats with metadata
describing the data type and source.

Key Functions
-------------
get_nwbs : function
    Discover and return paths to all NWB files for a specified species.
    Entry point for batch processing multiple subjects.

get_trial_times : function
    Unified interface for extracting trial timing information.
    Routes to species-specific methods and returns standardized column names.

get_kinematics : function
    Unified interface for extracting behavioral/kinematic data.
    Returns cursor positions for monkeys or speech kinematics for humans.

get_neural_data : function
    Unified interface for extracting neural recordings.
    Returns binned spike counts for monkeys or ECoG traces for humans.

Species-Specific Functions
---------------------------
Monkey Functions:
    - get_monkey_trial_times: Extract reach task trial timing
    - get_monkey_kinematics: Extract cursor position/velocity data
    - get_monkey_neural_data: Extract and bin spike train data

Human Functions:
    - get_human_trial_times: Extract speech task trial timing
    - get_human_kinematics: Extract phonetic trajectory data (from CSE583_humanSayMonkeyDo.data_processing)
    - get_human_neural_data: Extract ECoG electrode traces

Dependencies
------------
Standard Libraries:
    - numpy : Array operations and numerical computing
    - pandas : DataFrame operations (implicit through NWB trials tables)
    - pathlib : Path handling (implicit through get_data_paths)

NWB Library:
    - pynwb : Reading and accessing NWB file structures
      Install with: pip install pynwb

Custom Module Dependencies (from CSE583_humanSayMonkeyDo package):
    - load_config.get_data_paths : Returns configured data directory paths
    - data_formatting.get_human_kinematics : Extracts phonetic kinematics
    - data_formatting.get_chunk_spikes_binned_windowed : Bins spike data

Required Imports
----------------
```python
# Standard library
import numpy as np

# NWB file handling
from pynwb import NWBHDF5IO

# Custom package imports
from CSE583_humanSayMonkeyDo.load_config import get_data_paths
from CSE583_humanSayMonkeyDo.data_processing import (
    get_human_kinematics,
    get_chunk_spikes_binned_windowed
)
```

Data Structure Overview
-----------------------
Monkey NWB Files:
    - nwbfile.trials: Contains 'start_time', 'go_cue_time', 'stop_time'
    - nwbfile.processing['behavior']: Contains Position/Velocity interfaces
    - nwbfile.units: Contains spike times for each recorded neuron

Human NWB Files:
    - nwbfile.trials: Contains 'speak', 'start_time', 'cv_transition_time', 
                      'stop_time', 'condition'
    - nwbfile.acquisition['ElectricalSeries']: Contains ECoG electrode data

Standardized Return Formats
----------------------------
Trial Times (both species):
    - DataFrame with standardized columns: ['trial_start', 'go', 'trial_end']
    - For monkeys: 'go' is the go_cue_time
    - For humans: 'go' is the cv_transition_time (consonant-vowel transition)

Kinematics:
    - Monkeys: (n_samples, 2) array of [x, y] cursor positions
    - Humans: (n_samples, 2) array of [x, y] phonetic space coordinates

Neural Data:
    - Monkeys: (n_chunks, n_units, n_bins) binned spike counts
    - Humans: (n_samples, n_channels, n_chunks) continuous ECoG traces

Metadata Dictionaries:
    All unified functions return metadata dicts with 'species' and a 
    type-specific key ('trial_type', 'kinematic_type', 'data_type')

Typical Workflows
-----------------
Loading All Subjects:
    >>> from CSE583_humanSayMonkeyDo import data_loading
    >>> nwb_paths = data_loading.get_nwbs(primate='monkey', max_subjects=5)
    >>> for nwb_path in nwb_paths:
    ...     with NWBHDF5IO(nwb_path, 'r') as io:
    ...         nwbfile = io.read()
    ...         # Process nwbfile...

Extracting Trial-Aligned Data:
    >>> # Works for both species automatically
    >>> trial_times, metadata = get_trial_times(nwbfile)
    >>> go_times = trial_times['go'].values
    >>> 
    >>> # Extract neural data around go cue
    >>> neural_data, neural_meta = get_neural_data(
    ...     nwbfile, go_times, window=[-0.5, 1.0], bin_size=0.05
    ... )
    >>> print(f"Species: {neural_meta['species']}")
    >>> print(f"Data type: {neural_meta['data_type']}")

Cross-Species Analysis:
    >>> monkey_nwbs = get_nwbs('monkey')
    >>> human_nwbs = get_nwbs('human')
    >>> 
    >>> for nwb_path in monkey_nwbs + human_nwbs:
    ...     with NWBHDF5IO(nwb_path, 'r') as io:
    ...         nwbfile = io.read()
    ...         kinematics, timestamps, meta = get_kinematics(nwbfile)
    ...         # Same interface works for both species!

Performance Considerations
--------------------------
- NWB files can be large (GBs); use NWBHDF5IO context manager
- Full neural data arrays are loaded into memory - consider chunking for very 
  long recordings
- Spike binning is vectorized and efficient for 100s of neurons
- Use max_subjects parameter to limit memory usage during batch processing

Notes and Caveats
-----------------
- All time values are in seconds
- Monkey go_cue_time can be NaN for some trials (these are filtered out)
- Human trials are filtered to include only speaking trials (speak==True)
- Neural data windowing uses [start, end) intervals (start inclusive, end exclusive)
- Monkey kinematic data has both Position and Velocity available
- Human kinematic data represents phonetic space, not physical movement

Data Quality Checks
-------------------
Before processing, verify:
    - nwbfile.subject.species is set correctly
    - Required trials columns exist and are not all NaN
    - Neural data arrays are not empty
    - Timestamps are monotonically increasing
    - Window boundaries are within the recording duration

Version Information
-------------------
Package: CSE583_humanSayMonkeyDo
Module: data_loading
Author: Autumn Mallory
Date: December 2025
Version: 1.0
Dependencies: numpy, pynwb, pandas (implicit)
"""

# ============================================================================
# IMPORTS
# ============================================================================

# Standard library
import numpy as np

# Custom package imports - configuration
from cse583_human_say_monkey_do.load_config import get_data_paths

# Custom package imports - data processing functions
from cse583_human_say_monkey_do.data_formatting import (
    get_human_kinematics,
    get_chunk_spikes_binned_windowed
)

# ============================================================================
# UNDEFINED/MISSING IMPORTS
# ============================================================================
#
# The following imports are USED but NOT CURRENTLY IMPORTED in the module:
#
# 1. NWBHDF5IO - Required for opening NWB files
#    from pynwb import NWBHDF5IO
#    
#    Usage: Users of this module need to open NWB files before passing them
#    to these functions. Add this to usage documentation/examples.
#
# 2. pandas - Implicit dependency through nwbfile.trials[:] returning DataFrames
#    import pandas as pd
#    


def get_nwbs(primate='monkey', max_subjects=None) -> list:
    """Return absolute Path objects for all data directories.

    Args:
        primate (str): 'monkey' or 'human' to specify
        max_subjects (int, optional): Maximum number of subjects to return. Defaults to None.
    Returns:
        list: a list of Path objects.
    """
    if primate not in ("monkey", "human"):
        raise ValueError("primate must be 'monkey' or 'human'")

    if max_subjects is not None:
        if not isinstance(max_subjects, int):
            raise TypeError("max_subjects must be an integer")
        if max_subjects <= 0:
            raise ValueError("max_subjects must be a positive integer")

    data_paths = get_data_paths()
    nwb = list(data_paths[primate].glob("**/*.nwb"))
    if max_subjects is not None:
        nwb = nwb[:max_subjects]

    return nwb

def get_monkey_trial_times(nwbfile):
    """
    Extract trial timing information from monkey NWB file.
    
    This function retrieves the start time, go cue time, and stop time for
    each trial in a monkey cursor control experiment. Trials with missing
    (NaN) go cue times are excluded.
    
    Parameters
    ----------
    nwbfile : pynwb.NWBFile
        NWB file object containing monkey trial data.
        Must have nwbfile.trials with 'start_time', 'go_cue_time', and
        'stop_time' columns.
    
    Returns
    -------
    trial_times : pandas.DataFrame
        DataFrame of shape (n_valid_trials, 3) with columns:
        - 'start_time': Trial start time in seconds
        - 'go_cue_time': Time when movement cue was presented in seconds
        - 'stop_time': Trial end time in seconds
        Only includes trials where go_cue_time is not NaN.
    
    Raises
    ------
    KeyError
        If required columns ('start_time', 'go_cue_time', 'stop_time') are
        not found in nwbfile.trials.
    AttributeError
        If nwbfile.trials is not accessible.
    
    Examples
    --------
    >>> trial_times = get_monkey_trial_times(nwbfile)
    >>> print(f"Number of valid trials: {len(trial_times)}")
    >>> print(f"Average trial duration: {(trial_times['stop_time'] - trial_times['start_time']).mean():.2f}s")
    
    Notes
    -----
    The go_cue_time marks when the animal receives the signal to begin
    movement towards the target. This typically occurs after the start_time
    and before the stop_time. Trials without a valid go_cue_time (NaN values)
    are filtered out and not included in the returned DataFrame.
    """
    trial_times = nwbfile.trials[:][['start_time', 'go_cue_time', 'stop_time']]
    valid_go_cue = ~np.isnan(trial_times['go_cue_time'])
    trial_times = trial_times[valid_go_cue]
    return trial_times


def get_human_trial_times(nwbfile):
    """
    Extract trial timing information from human speech NWB file.
    
    This function retrieves timing information for speaking trials only,
    filtering out non-speaking trials. Returns the start time, consonant-vowel
    transition time, and stop time for each speaking trial.
    
    Parameters
    ----------
    nwbfile : pynwb.NWBFile
        NWB file object containing human speech trial data.
        Must have nwbfile.trials with 'speak', 'start_time',
        'cv_transition_time', and 'stop_time' columns.
    
    Returns
    -------
    trial_times : pandas.DataFrame
        DataFrame of shape (n_speaking_trials, 3) with columns:
        - 'start_time': Trial start time in seconds
        - 'cv_transition_time': Consonant-vowel transition time in seconds
        - 'stop_time': Trial end time in seconds
        Only includes trials where speak==True.
    
    Raises
    ------
    KeyError
        If required columns ('speak', 'start_time', 'cv_transition_time',
        'stop_time') are not found in nwbfile.trials.
    AttributeError
        If nwbfile.trials is not accessible.
    
    Examples
    --------
    >>> trial_times = get_human_trial_times(nwbfile)
    >>> print(f"Number of speaking trials: {len(trial_times)}")
    >>> cv_delays = trial_times['cv_transition_time'] - trial_times['start_time']
    >>> print(f"Average time to CV transition: {cv_delays.mean():.3f}s")
    
    Notes
    -----
    This function filters trials to include only those where the subject was
    speaking (speak==True). The cv_transition_time marks the point during
    speech production when articulation transitions from consonant to vowel,
    which is an important landmark in speech motor control analysis.
    """
    data = nwbfile.trials[:]
    remove_non_speaking = data['speak']
    data = data[remove_non_speaking]
    trial_times = data[["start_time", "cv_transition_time", "stop_time"]]
    return trial_times

def get_trial_times(nwbfile):
    """
    Extract trial timing information from NWB file based on subject species.
    
    This function routes to species-specific trial time extraction methods
    and returns trial timing data along with metadata describing the trial
    type and subject species.
    
    Parameters
    ----------
    nwbfile : pynwb.NWBFile
        NWB file object containing subject information and trial data.
        Must have nwbfile.subject.species set to either 'Macaca mulatta'
        or 'Homo sapiens'.
    
    Returns
    -------
    trial_times : pandas.DataFrame
        DataFrame of shape (n_trials, 3) containing trial timing information.
        Columns depend on species:
        - Macaca mulatta: ['start_time', 'go_cue_time', 'stop_time']
        - Homo sapiens: ['start_time', 'cv_transition_time', 'stop_time']
    metadata : dict
        Dictionary containing trial metadata with keys:
        - 'species': Subject species name
        - 'trial_type': Type of trial ('reach' for monkey, 'speech' for human)
    
    Raises
    ------
    ValueError
        If subject species is neither 'Macaca mulatta' nor 'Homo sapiens'.
    AttributeError
        If nwbfile.subject.species is not accessible.
    
    Examples
    --------
    >>> trial_times, metadata = get_trial_times(nwbfile)
    >>> print(f"Species: {metadata['species']}")
    >>> print(f"Trial type: {metadata['trial_type']}")
    >>> print(f"Number of trials: {len(trial_times)}")
    >>> print(f"Columns: {trial_times.columns.tolist()}")
    
    Notes
    -----
    This function serves as a unified interface for extracting trial timing
    data from both monkey reach experiments and human speech experiments.
    The metadata dictionary allows downstream code to properly interpret the
    trial timing columns based on the trial type and source species.
    """
    if nwbfile.subject.species == 'Macaca mulatta':
        trial_times = get_monkey_trial_times(nwbfile)
        metadata = {
            'species': 'Macaca mulatta',
            'trial_type': 'reach'
        }
    elif nwbfile.subject.species == 'Homo sapiens':
        trial_times = get_human_trial_times(nwbfile)
        metadata = {
            'species': 'Homo sapiens',
            'trial_type': 'speech'
        }
    else:
        raise ValueError("Missing required field: NWB file does not have monkey or human species")
    
    trial_times.columns = ['trial_start', 'go', 'trial_end']
    return trial_times, metadata

def get_monkey_kinematics(nwbfile, kin_type='Position'):
    """
    Extract cursor position kinematics from monkey NWB file.
    
    This function retrieves the x/y cursor position data from a monkey
    performing a cursor control task. The cursor position represents the
    location on screen controlled by the animal's arm movements over time.
    
    Parameters
    ----------
    nwbfile : pynwb.NWBFile
        NWB file object containing behavioral data from monkey experiments.
        Must contain:
        - processing['behavior'].data_interfaces['Position']: Position data
        - spatial_series['cursor_pos']: Cursor position time series with
          .data and .timestamps attributes
    
    Returns
    -------
    kinematic : numpy.ndarray
        Array of shape (n_samples, 2) containing x/y cursor positions on screen.
        Each row represents [x_position, y_position] at a given time point.
    timestamps : numpy.ndarray
        Array of shape (n_samples,) containing the timestamp for each cursor
        position sample.
    kin_type: String- "Position" or "Velocity"
        Specifying to return either position or velocity kinematic information
    
    Raises
    ------
    KeyError
        If 'behavior' processing module, 'Position' interface, or 'cursor_pos'
        spatial series is not found in the NWB file.
    AttributeError
        If required .data or .timestamps attributes are missing.
    
    Examples
    --------
    >>> kinematic, timestamps = get_monkey_kinematics(nwbfile)
    >>> print(f"Cursor data shape: {kinematic.shape}")
    >>> print(f"Recording duration: {timestamps[-1] - timestamps[0]:.2f} seconds")
    >>> print(f"X range: [{kinematic[:, 0].min()}, {kinematic[:, 0].max()}]")
    
    Notes
    -----
    The cursor position data represents screen coordinates controlled by the
    monkey's arm movements during behavioral tasks. Timestamps are stored
    separately and may not be uniformly sampled.
    """
    assert kin_type in ("Position", "Velocity"), f"kin_type must be 'Position' or 'Velocity', got {kin_type}"
    if kin_type=="Position":
        kinematic = nwbfile.processing['behavior'].data_interfaces[kin_type].spatial_series['cursor_pos']
    elif kin_type=="Velocity":
        kinematic = nwbfile.processing['behavior'].data_interfaces[kin_type].time_series['cursor_vel']

    timestamps = kinematic.timestamps[:]
    kinematic = kinematic.data[:]
    
    
    return kinematic, timestamps



def get_kinematics(nwbfile, kin_type="Position"):
    """
    Extract kinematic data from NWB file based on subject species.
    
    This function routes to species-specific kinematic extraction methods
    and returns kinematic data along with metadata describing the data type
    and subject species.
    
    Parameters
    ----------
    nwbfile : pynwb.NWBFile
        NWB file object containing subject information and kinematic data.
        Must have nwbfile.subject.species set to either 'Macaca mulatta'
        or 'Homo sapiens'.
    kin_type: String
        Only relevant for monkey kinematics, specifies either velocity 
        or position kinematics
    Returns
    -------
    kinematic : numpy.ndarray
        Kinematic data array. Shape and content depend on species:
        - Macaca mulatta: (n_samples, 2) array of x/y cursor positions
        - Homo sapiens: (n_samples,) binary array of speaking activity
    timestamps : numpy.ndarray
        Array of shape (n_samples,) containing timestamps for each sample.
    metadata : dict
        Dictionary containing kinematic metadata with keys:
        - 'species': Subject species name
        - 'kinematic_type': Type of kinematic data ('cursor_position' or 'speech_binary')
    
    Raises
    ------
    ValueError
        If subject species is neither 'Macaca mulatta' nor 'Homo sapiens'.
    AttributeError
        If nwbfile.subject.species is not accessible.
    
    Examples
    --------
    >>> kinematic, timestamps, metadata = get_kinematics(nwbfile)
    >>> print(f"Species: {metadata['species']}")
    >>> print(f"Kinematic type: {metadata['kinematic_type']}")
    >>> print(f"Data shape: {kinematic.shape}")
    
    Notes
    -----
    This function serves as a unified interface for extracting kinematic data
    from both monkey cursor control experiments and human speech experiments.
    The metadata dictionary allows downstream code to properly interpret the
    kinematic data based on its type and source species.
    """
    if nwbfile.subject.species == 'Macaca mulatta':
        kinematic, timestamps = get_monkey_kinematics(nwbfile, kin_type)
        metadata = {
            'species': 'Macaca mulatta',
            'kinematic_type': 'cursor_position'
        }
    elif nwbfile.subject.species == 'Homo sapiens':
        kinematic, timestamps = get_human_kinematics(nwbfile)
        metadata = {
            'species': 'Homo sapiens',
            'kinematic_type': 'speech_binary'
        }
    else:
        raise ValueError("Missing required field: NWB file does not have monkey or human species")
    
    return kinematic, timestamps, metadata


def get_human_neural_data(nwbfile, times, window):
    """
    Extract neural data from NWB file at specified timestamps with a time window.
    
    This function extracts chunks of neural data from an NWB (Neurodata Without Borders)
    file's ElectricalSeries acquisition data. For each timestamp provided, it extracts
    neural data across all channels within a specified time window around that timestamp.
    
    Parameters
    ----------
    nwbfile : pynwb.NWBFile
        The NWB file object containing the neural data. The neural data should be 
        accessible via nwbfile.acquisition['ElectricalSeries'].
    times : array-like
        Array or list of timestamps (in seconds) at which to extract neural data.
        Each timestamp serves as the center reference point for the extraction window.
    window : list or tuple of length 2
        Time window [start, end] in seconds relative to each timestamp.
        - window[0]: Start of window (typically negative, e.g., -0.1 for 100ms before)
        - window[1]: End of window (typically positive, e.g., 0.1 for 100ms after)
        Must satisfy: window[0] < window[1]
    
    Returns
    -------
    numpy.ndarray
        3D array of shape (n_samples, n_channels, n_chunks) where:
        - n_samples: Number of samples within the time window
        - n_channels: Number of electrode channels
        - n_chunks: Number of timestamps (length of `times`)
    
    Raises
    ------
    AssertionError
        If window[0] >= window[1]
    KeyError
        If 'ElectricalSeries' is not found in nwbfile.acquisition
    
    Notes
    -----
    The ElectricalSeries structure contains:
    - starting_time: Initial timestamp (typically 0.0 seconds)
    - rate: Sampling rate in Hz (e.g., 3051.7578125 Hz)
    - data: 2D array of shape (n_timepoints, n_channels) in volts
    - conversion: Scaling factor (e.g., 0.001)
    - unit: Data units (e.g., 'volts')
    
    Examples
    --------
    Extract 200ms windows (±100ms) around three timestamps:
    >>> times = [1.0, 2.5, 5.0]  # seconds
    >>> window = [-0.1, 0.1]  # ±100ms window
    >>> neural_data = get_human_neural_data(nwbfile, times, window)
    >>> print(f"Data shape: {neural_data.shape}")  # (n_samples, n_channels, 3)
    >>> print(f"First chunk: {neural_data[:, :, 0].shape}")
    
    Extract asymmetric window (50ms before, 150ms after):
    >>> window = [-0.05, 0.15]
    >>> neural_data = get_human_neural_data(nwbfile, times, window)
    """
    # Validate window parameter
    assert window[0] < window[1], \
        f"window[0] must be less than window[1], got window={window}"
    
    # Access the ElectricalSeries data
    electrical_series = nwbfile.acquisition['ElectricalSeries']
    
    # Get sampling rate and starting time
    sampling_rate = electrical_series.rate
    starting_time = electrical_series.starting_time
    
    # Access the full neural data (timepoints x channels)
    full_data = electrical_series.data[:]
    
    # Get number of channels
    n_channels = full_data.shape[1]
    
    # Calculate expected number of samples per window
    window_duration = window[1] - window[0]
    n_samples = int(window_duration * sampling_rate)
    
    # Initialize 3D array to store extracted chunks (n_samples x n_channels x n_chunks)
    n_chunks = len(times)
    neural_data_array = np.zeros((n_samples, n_channels, n_chunks))
    
    # Extract data for each timestamp
    for chunk_idx, timestamp in enumerate(times):
        # Calculate absolute time boundaries for this window
        window_start_time = timestamp + window[0]
        window_end_time = timestamp + window[1]
        
        # Convert time boundaries to sample indices
        # Index = (time - starting_time) * sampling_rate
        start_idx = int((window_start_time - starting_time) * sampling_rate)
        end_idx = int((window_end_time - starting_time) * sampling_rate)
        
        # Ensure indices are within valid range
        start_idx = max(0, start_idx)
        end_idx = min(len(full_data), end_idx)
        
        # Extract the data chunk for this time window
        if start_idx < end_idx:
            data_chunk = full_data[start_idx:end_idx, :]
            # Handle cases where extracted chunk might be shorter than expected
            actual_samples = min(data_chunk.shape[0], n_samples)
            neural_data_array[:actual_samples, :, chunk_idx] = data_chunk[:actual_samples, :]
    
    return neural_data_array



def get_monkey_neural_data(nwbfile, times, window, bin_size=0.01):
    list_units_spkts = nwbfile.units[:]['spike_times']
    spike_data = get_chunk_spikes_binned_windowed(list_units_spkts, times, window, bin_size)
    return spike_data[0]


#h_nwbfile.acquisition['ElectricalSeries'].data[:]
def get_neural_data(nwbfile, times, window, bin_size=0.01):
    """
    """
    if nwbfile.subject.species == 'Macaca mulatta':
        neural_data = get_monkey_neural_data(nwbfile, times, window, bin_size)
        metadata = {
            'species': 'Macaca mulatta',
            'data_type': 'binned spike counts'
        }
    elif nwbfile.subject.species == 'Homo sapiens':
        neural_data = get_human_neural_data(nwbfile, times, window)
        metadata = {
            'species': 'Homo sapiens',
            'data_type': 'Ecog traces'
        }
    else:
        raise ValueError("Missing required field: NWB file does not have monkey or human species")
    
    return neural_data, metadata