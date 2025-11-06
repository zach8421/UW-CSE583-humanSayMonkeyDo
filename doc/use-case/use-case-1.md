### Use Case Name
Load and Preprocess Human Attempted Speech Dataset

### Goal
Allow Alice to load the human dataset and automatically convert phoneme labels into pseudo-kinematic time series aligned to trials.

### Actors / Users
Alice (non-technical neuroscience researcher)

### Inputs
- Human neural recordings (e.g., NWB / NumPy arrays)
- Phoneme annotation file (timestamps + labels)

### Outputs
- Trial-aligned pseudo-kinematic human dataset (continuous signals suitable for tuning/decoding)

### Preconditions
- Human dataset has been downloaded to local system

### Basic Flow
1. Alice selects “Load Human Dataset” in the interface.
2. The tool reads the neural time series.
3. The tool converts phoneme labels into continuous pseudo-kinematic features.
4. The tool windows the data into trial-aligned segments.
5. The preprocessed dataset is stored and shown as “Ready for Analysis.”

### Notes / Rationale
This allows comparison with monkey reach trials without requiring Alice to write preprocessing code.

