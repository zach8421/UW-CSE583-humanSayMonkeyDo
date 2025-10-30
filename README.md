# UW-CSE583-humanSayMonkeyDo
Fall quarter UW-CSE 583 final project

# humanSayMonkeyDo
CSE583 project

### Monkey Datasets:
https://dandiarchive.org/dandiset/000688

### Human Datasets:
https://www.kaggle.com/competitions/brain-to-text-25/data

### Project description:
Both these datasets contain neural recordings from brain regions in motor cortex in macaque and human. The monkey data is during standard center out reaching task while the human recordings are taken during attempted speech. The goal of this project is to reformat the human dataset to resemble the trial structure during the reaching task and allow parallel analysis of reaching kinematics and tongue/mouth kinematics.

### Dataset formating: 
1. Monkey -> Ready to go
2. Human -> Prep/chunk, convert phonemes to psuedokinematic measures

### Proposed Analyses:
1. Movement onset detection
2. Single neuron kinematic tuning
3. Target position decoding

### Examples/Tutorials:
1. Neuromatch Classifiers: https://compneuro.neuromatch.io/tutorials/W1D3_GeneralizedLinearModels/student/W1D3_Tutorial2.html
    a. Potentially use a logistic/linear model to classify movement aligned neural data vs motionless neural data
2. Kinematic/Direction tuning: 
    a. Example code/function to calculate tuning curves: https://analyze.readthedocs.io/en/latest/_modules/aopy/analysis/tuning.html#curve_fitting_func
    b. Explanation of tuning curve: https://openbooks.library.northwestern.edu/neuroscienceconcepts/chapter/tuning-curves/
3. Target Position Decoding:
    a. Start with the same logistic/linear models as in number 1, can move on to RNN/Deep learning classifiers if we have time/interest: https://compneuro.neuromatch.io/tutorials/W1D5_DeepLearning/student/W1D5_Tutorial1.html?highlight=decoding
    b. Example paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC3429374/

### Interesting papers:
https://pmc.ncbi.nlm.nih.gov/articles/PMC3429374/
https://www.nature.com/articles/s41467-023-38586-3

