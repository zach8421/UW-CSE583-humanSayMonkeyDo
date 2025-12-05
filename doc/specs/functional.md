## 1. Background

This project aims to build a unified and accessible analysis pipeline that helps neuroscientists relate neural activity to behavior. We work with two publicly available NWB datasets hosted on the DANDI Archive: a monkey center-out reaching dataset containing spike-sorted units and behavioral kinematics, and a human speech production dataset containing high-density ECoG recordings with speech-onset labels.

We initially planned to explore three classic analytical directions:

- Decoding movement onset with a classifier  
- Tuning curve analysis for directional preference of single neurons  
- Target decoding from neural population activity  

After evaluating the datasets and their documentation, several practical constraints emerged:

- Differences in trial structure and available behavioral signals make tuning curve analysis and target decoding difficult to parallelize across the two datasets.  
- Neural modalities differ substantially (spike trains versus continuous ECoG), requiring separate preprocessing pipelines rather than a single unified workflow.  
- The project timeline does not allow building a fully generalized cross-dataset pipeline.

Given these constraints, we focused on a single feasible and well defined direction:  
**decoding movement onset with a classifier**, implemented on the monkey dataset as the primary foundation for the analysis pipeline.

Once this pipeline is established, we then consider which components may generalize to the human dataset in future work.

---

## 2. User Profile

The system is designed for neuroscientists who want to analyze NWB datasets without implementing low-level loading, preprocessing, or modeling themselves.

### 2.1 Summary of users

- **Primary users:** neuroscientists with domain expertise but limited coding experience  
- **Secondary users:**  
  - Researchers with moderate Python familiarity who want quick decoding tools  
  - Advanced programmers who may extend the pipeline  

### 2.2 Primary user description

The primary users:

- Understand experimental paradigms such as center-out reaching and speech production  
- Can run Python notebooks but do not want to manage NWB internals  
- Want to load datasets, inspect trial-aligned neural activity, and run decoding with minimal code  
- Prefer clear visualizations, simple function calls, and exportable results  

Their goals include:

- Loading neural–behavioral data in a standardized structure and selecting sessions for analysis  
- Running movement-onset decoding without implementing preprocessing steps
- Visualizing neural activity or classifier outputs using built-in plotting functions  
- Reusing the pipeline on additional sessions with minimal changes  
- Optionally extending the workflow once the basic pipeline is understood  

The system prioritizes clarity, consistency, and ease of use.

---

## 3. Data Sources

Both datasets come from the DANDI Archive, which supports structured NWB files, stable metadata, and reproducible access.  
Because the full datasets are large, we use one representative **sub-dataset** from each collection.  
This does not reduce generalizability, because the workflow depends on NWB schema elements rather than file-specific structures.

### 3.1 Monkey dataset (primary dataset used to build the pipeline)

- **Dataset:** DANDI:000688  
- **Subset used:** sub-J  

**Key components**

- **Units (spike trains):** spike-sorted activity used for feature extraction and decoding  
- **Behavioral signals:** position and related kinematic traces used to determine movement onset  
- **Trials table:** includes start_time, stop_time, target_on_time, go_cue_time, target direction, and trial result  

**Usage**

- Serves as the primary dataset for building the movement-onset decoding pipeline  
- Provides the structures needed for event alignment, feature construction, and classifier training/testing  

### 3.2 Human dataset (used to assess extensibility)

- **Dataset:** DANDI:000019  
- **Subset used:** sub-GP33  

**Key components**

- **ElectricalSeries:** continuous 256-channel ECoG  
- **Trials table:** includes cv_transition_time (speech onset), a speak flag, and syllable labels  
- **Electrode metadata:** spatial distribution of recording sites  

**Usage**
 
- Used to evaluate how well the pipeline design may generalize to different NWB modalities  

### 3.3 Subset selection and generalizability

Because the dataset collections are large, we use one representative sub-dataset from each. This approach:

- Keeps computation manageable  
- Enables rapid iteration during development  
- Preserves generalizability because processing depends on NWB schema rather than specific files  

Additional NWB sessions can be analyzed simply by supplying a new file path.

---

## 4. Use Cases

Use cases are framed for the primary users: neuroscientists who want to analyze neural–behavioral datasets without writing low-level code.

### Use Case 1: Load and inspect available NWB files

**Objective**  
Enable neuroscientists to identify which NWB files are available for analysis and confirm that the dataset loads correctly.

**Interaction**

1. Users run a command such as:
   ```python
   get_nwbs("monkey")
   ```
2. The system retrieves root paths via `get_data_paths()`.  
3. The system scans directories recursively for `.nwb` files.  
4. A list of valid NWB session paths is returned.  
5. Users select a session path and open it in the tutorial notebook for further inspection.

**Outcome**  
Neuroscientists obtain a clean list of available NWB files and select which session to analyze next.

### Use Case 2: Extract neural or behavioral chunks aligned to events

**Objective**  
Allow neuroscientists to extract trial-aligned segments of velocity traces or spike trains, which will later serve as features for movement-onset decoding.

**Interaction**

1. Users load an NWB session and access datasets such as velocity or unit spike times.  
2. They call helper functions such as:
   ```python
   get_windowed_pos_chunk(...)
   get_pos_chunk(...)
   get_chunk_spikes(...)
   get_chunk_spikes_binned(...)
   ```
3. The system reads timestamps, identifies start/end indices, and extracts aligned windows.  
4. Users optionally visualize extracted chunks using matplotlib.

**Outcome**  
Neuroscientists receive structured, trial-aligned neural or behavioral data that can be directly used for decoding.

### Use Case 3: Detect movement onset from velocity signals

**Objective**  
Enable neuroscientists to automatically detect movement-onset timestamps after the go cue, producing labels required for classifier training.

**Interaction**

1. Users call:
   ```python
   get_movement_onset_times(velocity_dataset, go_cue_times)
   ```
2. The system:
   - Extracts velocity windows around each go cue  
   - Computes velocity magnitude  
   - Detects the first threshold crossing per trial  
   - Converts window indices into absolute timestamps  
3. Detected onset times and indices are returned.

**Outcome**  
Reliable movement-onset labels are generated for use in downstream classifier training.

### Use Case 4: Train and visualize a movement-onset classifier

**Objective**  
Allow neuroscientists to evaluate whether neural population activity predicts movement onset.

**Interaction**

1. Users prepare spike-binned neural matrices using earlier extraction functions.  
2. They call:
   ```python
   lda, results = train_lda_classifier(data_matrices, labels)
   ```
3. The system:
   - Flattens neural matrices  
   - Splits into train/test sets  
   - Fits an LDA classifier  
   - Computes accuracy, cross-validation scores, and confusion matrices  
4. Users visualize results using:
   ```python
   plot_lda_results(results)
   ```

**Outcome**  
Neuroscientists obtain decoding metrics and clear visualizations summarizing classifier performance.

### Use Case 5: Apply the pipeline to a new session

**Objective**  
Enable neuroscientists to reuse the entire preprocessing and decoding pipeline on additional NWB sessions with minimal changes.

**Interaction**

1. Users load another NWB file (e.g., a different sub-J session) using:
   ```python
   sessions = get_nwbs("monkey")
   new_file = sessions[1]
   ```
2. They rerun the same feature-extraction code:
   ```python
   binned_spikes, meta = get_chunk_spikes_binned(list_units_spkts, start_times, end_times)
   ```
3. They run the classifier again:
   ```python
   lda, results = train_lda_classifier(data_matrices, labels)
   ```
4. The system produces decoding accuracy, confusion matrices, and visualizations in exactly the same format as previous sessions.
5. Users compare decoding performance across sessions.

**Outcome**  
Neuroscientists can reuse the workflow across multiple recording sessions without modifying the pipeline, ensuring consistency and facilitating cross-session comparisons.

### Use Case 6: Visualize neural population activity or decoding results

**Objective**  
Allow neuroscientists to generate interpretable visualizations of neural population activity or classifier outputs without writing plotting code.

**Interaction**

1. Users compute neural features using:
   ```python
   binned_spikes, meta = get_chunk_spikes_binned(list_units_spkts, start_times, end_times)
   ```
2. They visualize population firing-rate activity:
   ```python
   fig, ax = plot_firing_rate_heatmap(
       firing_rates_2d=binned_spikes.mean(axis=0),
       bin_size=meta["bin_size"]
   )
   ```
3. After training the classifier, they visualize decoding metrics using:
   ```python
   fig = plot_lda_results(results)
   ```
4. The system automatically generates figures such as:
   - Firing-rate heatmaps  
   - Confusion matrices  
   - Prediction-probability histograms  
   - LDA projection histograms  
   - Cross-validation accuracy plots  
5. Users inspect these figures and may optionally save them:
   ```python
   fig.savefig("results.png")
   ```

**Outcome**  
Neuroscientists can rapidly interpret neural dynamics and classifier performance using built-in visualization tools, without manually writing Matplotlib or Seaborn code.


