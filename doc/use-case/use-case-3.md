### Use Case: Decode Movements from Neural Data

**Goal**  
Allow Mabel to run decoding models that predict movement direction or behavior from neural signals.

**User**  
Mabel

**Inputs**  
- Neural activity data
- Corresponding movement labels (e.g., target direction)

**Outputs**  
- Decoding accuracy and confusion matrix
- Optional trained model for later use

**Steps**  
1. Mabel loads a dataset from a new recording session.  
2. The tool extracts neural features for each trial.  
3. Mabel selects a decoding model (default provided).  
4. The tool trains and evaluates the model.  
5. Results are displayed for interpretation.

