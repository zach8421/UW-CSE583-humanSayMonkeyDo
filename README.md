# humanSayMonkeyDo Setup Guide

This guide will walk you through setting up the conda environment and downloading the required datasets for the humanSayMonkeyDo project.

## Prerequisites

- **Conda**: You must have Conda installed on your system
  - Download from: [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
  - Verify installation: `conda --version`

- **DANDI CLI**: For downloading datasets
  - Will be installed automatically with the conda environment

## Setup Instructions

### 1. Clone or Navigate to the Project Directory
```bash
cd /path/to/humanSayMonkeyDo
```

Make sure you're in the main project directory that contains the `environment.yaml` file.

### 2. Create the Conda Environment

Check if the environment already exists:
```bash
conda env list | grep humanSayMonkeyDo
```

If it doesn't exist, create it from the environment file:
```bash
conda env create -f environment.yaml
```

This will:
- Create a new conda environment named `humanSayMonkeyDo`
- Install all required Python packages and dependencies
- Install the DANDI CLI tool for data download

### 3. Activate the Environment
```bash
conda activate humanSayMonkeyDo
```

You should see `(humanSayMonkeyDo)` prepended to your command prompt.

**Note**: If you get an error about `conda activate` not working, first run:
```bash
conda init bash  # or conda init zsh if using zsh
```

Then restart your terminal and try activating again.

### 4. Create Data Directory Structure

From the project root directory:
```bash
mkdir -p data/monkey
mkdir -p data/human
```

### 5. Download the Monkey Dataset

Navigate to the monkey data directory:
```bash
cd data/monkey
```

You have two options for downloading the dataset:

#### Option A: Download Full Dataset
```bash
dandi download DANDI:000688/0.250122.1735
mv 000688/* .
rmdir 000688
```

**Warning**: The full dataset is large and may take significant time and storage space.

#### Option B: Download Subset (Recommended for Testing)
```bash
dandi download "https://dandiarchive.org/dandiset/000688/0.250122.1735/files?location=sub-J"
```

This downloads only the subset containing subject J data, which is sufficient for testing and development.

### 6. Verify Installation

Return to the project root:
```bash
cd ../..
```

Verify that the data structure looks correct:
```bash
ls -la data/monkey/
```

You should see `.nwb` files in this directory.

### 7. Test Your Setup

Run a quick test to ensure everything is working:
```bash
python -c "import pynwb; import numpy; import matplotlib; print('All imports successful!')"
```

If this runs without errors, your environment is set up correctly!

## Directory Structure

After setup, your project should look like this:
```
humanSayMonkeyDo/
├── environment.yaml
├── config.yaml
├── data/
│   ├── monkey/
│   │   ├── sub-J_*.nwb
│   │   └── ...
│   └── human/
│       └── (TODO: human data will go here)
├── src/
│   └── ...
├── notebooks/
│   └── ...
└── tests/
    └── ...
```

## Troubleshooting

### Conda Environment Creation Fails

- Make sure you're in the correct directory containing `environment.yaml`
- Try updating conda: `conda update conda`
- Check that the environment.yaml file is properly formatted

### DANDI Download Fails

- Check your internet connection
- Verify you have sufficient disk space
- Try downloading a smaller subset first
- Check DANDI archive status: https://dandiarchive.org

### "Command not found: conda activate"

Run these commands:
```bash
conda init bash  # or your shell (zsh, fish, etc.)
source ~/.bashrc  # or ~/.zshrc
```

### Permission Errors

If you get permission errors when creating directories:
```bash
sudo mkdir -p data/monkey data/human
sudo chown -R $USER:$USER data/
```

## Deactivating the Environment

When you're done working:
```bash
conda deactivate
```

## Updating the Environment

If the `environment.yaml` file is updated:
```bash
conda env update -f environment.yaml --prune
```

## Removing the Environment

If you need to start fresh:
```bash
conda deactivate
conda env remove -n humanSayMonkeyDo
```

Then follow the setup instructions again.

## Additional Resources

- **DANDI Archive**: https://dandiarchive.org
- **Dataset Documentation**: https://dandiarchive.org/dandiset/000688
- **Project Repository**: [Add your repo URL here]
- **Conda Documentation**: https://docs.conda.io

## Human Dataset (Coming Soon)

Instructions for downloading and setting up the human dataset will be added here when available.

---

**Need Help?**

If you encounter issues not covered in this guide, please:
1. Check the troubleshooting section above
2. Search existing issues in the project repository
3. Open a new issue with details about your problem

# humanSayMonkeyDo
CSE583 project

### Setup

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

