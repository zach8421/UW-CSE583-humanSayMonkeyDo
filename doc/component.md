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

1. Database
    - What it does: Gives you neural and kinematic data 
    - Inputs: Subject, trial, trial type
    - Matrix that is Timestamps X Trials
2. Analysis
    - What it does: Applies standard analysis to neural/kinematic data
    - Inputs: Analysis specification, data matrix
    - Output: Data structure with analysis outputs and data
3. Visualization
    - What it does: Visualize the analysis results
    - Inputs: Analysis data structure
    - Output: Graph showing analysis results

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