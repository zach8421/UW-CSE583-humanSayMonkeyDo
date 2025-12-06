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


## Software Components:

1. NWB Loader 
    What it does: 
        - Loads in neural and kinematic data for a NWB data file
    Inputs (with type information): 
        - NWB file path
        - Primate (str) - specify which data type to load in
    Outputs (with type information):
        - Data file (NWBFile Object)
        - Trial time in seconds (numpy.ndarray)
        - Time of go cues (numpy.ndarray)
    Components used:

2. Trial Chunker
    What it does:
        - Chunks the neural activity and kinematic datasets into equal sized trials at a given time window
    Inputs: 
        - Trial time in seconds (numpy.ndarray)
        - Time of go cues (numpy.ndarray)
    Outputs: 
        - All trial chunks (list)
        - 2D position during each trial (array)
        - Spiking data of all recording units during trial (array)
    Components Used: 
        - NWB Loader

3. Visualization Manager
    What it does: 
        - Displays kinematic and neural data during the duration of a trial. 
    Inputs: 
        - Trial Chunks (list) - output from Trial chunker
        - 2D position during each trial (array)
        - Spiking data timeseries of all recording units (array)
    Output: 
        - Plot of cursor movement in x/y position 
        - Plot of neural population firing rates of all recording units
    Components Used: 
        - NWB Loader
        - Trial Chunker

4. Movement Detector
    What it does: 
        - Uses position timeseries to calculate movement velocity following a go cue. 
    Inputs: 
        - Trial chunks (list)
        - 2D position timeseries during each trial (array)
        - Spiking data timeseries of all recording units (array)
        - Speed threshold (int)
    Outputs: 
        - Movement times (array)
        - Movement velocity (array)
        - Spike data during stationary and movement periods (array)
    Components Used: 
        - NWB Loader
        - Trial chunker
        
5. Movement Decoder
    What it does: 
    - Trains an LDA classifier on spike data during movements
    Inputs: 
    - Movement times (array)
    - Spike data timeseries (array)
    Outputs:
    - Accuracy of model on training and test data (float)
    - Plots of LDA model performance
    Components Used:
    - Trial Chunker
    - Movement Detector

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