## Instructions:

-   **Component Specification**. The document should have sections for.
    -   Software components. High level description of the software
        components such as: *data manager*, which provides a simplified
        interface to your data and provides application specific
        features (e.g., querying data subsets); and *visualization
        manager*, which displays data frames as a plot. Describe at
        least 3 components specifying: what it does, inputs it requires,
        and outputs it provides.
    -   Interactions to accomplish use cases. Describe how the above
        software components interact to accomplish at least one of your
        use cases.
    -   Preliminary plan. A list of tasks in priority order.


### Software Components:

1. Data Loader
    - What it does: 
        - Loads in neural and kinematic data for a NWB data file from the DANDI database. 
        - Specifies which dataset to load in
        - Pulls relevant trial information 
    - Inputs (with type information): 
        - NWB file path (str)
        - Primate (str) - specify which data type to load in (human or monkey)
    - Outputs (with type information):
        - Data file (NWBFile Object)
        - Trial time in seconds (numpy.ndarray)
        - Time of go cues (numpy.ndarray)
    - Components used:
        - None

2. Data Formatter
    - What it does:
        - Splits the experiment timeseries into equal sized trials at a given time window. 
        - Creates time-aligned chunks of neural activity and kinematic data.
    - Inputs: 
        - Trial time in seconds (numpy.ndarray)
        - Time of go cues (numpy.ndarray)
    - Outputs: 
        - All trial chunks (list)
        - Neural data within a trial chunk (array)
            - Spiking data of all recording units for monkey data
            - ECoG electrode data for human data 
        - Kinematic data during trial (array)
            - 2D cursor position for monkey data
            - Phonetic trajectory data for human data
    - Components Used: 
        - Data Loader - To make trial time chunks, this component needs the full timeseries and trial information pulled from the original dataset.

3. Visualization Manager
    - What it does: 
        - Generates plot of kinematic and neural data of the full time series - to quality check the data loaded in.
        - Generates plots of the positional and neural data throughout the duration of a trial.
    - Inputs: 
        - Trial Chunks (list) - output from Trial chunker
        - 2D position during each trial (array)
        - Spiking data timeseries of all recording units (array)
    - Output: 
        - Plot of cursor movement in x/y position 
        - Plot of neural population firing rates of all recording units
    - Components Used: 
        - Data Loader - this component needs the original time stamps to plot the full timeseries
        - Data Formatter - to make single trial plots, this component needs to pull the chunked behavior and neural data from Data Formatter

4. Movement Detector
    - What it does: 
        - Calculates the movement velocity as change in behavior kinematics
        - For monkey data, calculates the velocity as change in cursor position following a go cue.
        - For human data, calculate that onset of speech during a trial. 
    - Inputs: 
        - Trial chunks (list) - output from Data Formatter
        - Kinematic data (array)
            - 2D position timeseries during each trial for monkey data
            - Binary array of speech times for human data
        - Neural data (array) 
            - Spiking data timeseries of all recording units for monkey data
            - Phonetic trajectory array for human data
        - Speed threshold (int) - above this value, the change in position is equal to a movement
    - Outputs: 
        - Movement times (array)
        - Movement velocity (array)
        - Spike data during stationary and movement periods (array)
    - Components Used: 
        - Data Formatter - to calculate behavior onset within a trial, this component needs to run within trial time chunks
        - Visualizer - to quality check movement detection, the visualizer is used to change in behavior over time of trials

5. Movement Decoder
    - What it does: 
        - Trains an LDA classifier on spike data during behavior.
        - Calculates how well the neural data can be used to predict motor movements.
        - Generates plots of model performance .
    - Inputs: 
        - Movement times (array) - output from Movement Detector
        - Neural Spike data timeseries (array) 
        - Trial time chunks (array)
    - Outputs:
        - Accuracy of model on training and test data (float)
        - Plots of Model performance
    - Components Used:
        - Data Formatter - this decoder component must run on the neural activity and behavior within trials, since the neural activity corresponds to one motor movement
        - Movement Detector - this component uses the movement detector to determine neural activity that is related to the onset of movement


### Interactions:

General Workflow:
1. Query database for subset of data
2. Apply analysis to data subset
3. Visualize analysis

### Preliminary Plan, Primary Pipeline:

1. Establish data format
2. Monkey database
        - Downloading data
        - Formatting
3. Analysis
    - Movement onset detection
4. Visualization
    - Kinematic/task variables
    - Neural traces/spike rasters
    - Analysis accuracy
5. Analysis
    - Tuning curves
6. Visualization
    - Tuning Curves
7. Analysis
    - Target position decoding
8. Visualisation
    - Decoding Accuracy
9. Database
    - Integrate human database with analysis pipeline

#### Parallel Pipeline:
2. Human Database
    - Downloading data
    - Chunking data
    - Converting phonemes to kinematics
    - Formatting
3. Test Movement onset detection