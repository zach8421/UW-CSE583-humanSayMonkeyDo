# Contributions:
Autumn (AJ) Mallory: Data loading and Analysis

Yici Chen: Functional specifications and tests writing 


# humanSayMonkeyDo Setup Guide

This project analyzes human and monkey neural recordings using NWB-formatted datasets from the DANDI Archive.

This guide will walk you through setting up the conda environment and downloading the required datasets for the humanSayMonkeyDo project.

## Prerequisites

- **Conda**: You must have Conda installed on your system
  - Download from: [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
  - Verify installation: `conda --version`

- **DANDI CLI**: For downloading datasets
  - Will be installed automatically with the conda environment

## Quick Start (Experienced Users)

If you’re already familiar with Conda and the DANDI CLI, you can set up the project with:

```bash
# Create and activate environment
conda env create -f environment.yaml
conda activate humanSayMonkeyDo

# Create data directories
mkdir -p data/{monkey,human}

# Download subsets (recommended)

# Verify DANDI CLI installation
dandi --version

# Monkey subset (subject J)
dandi download -e refresh -f pyout --path-type exact \
  --output-dir data/monkey \
  "https://dandiarchive.org/dandiset/000688/0.250122.1735/files?location=sub-J"

# Human subset (subject GP33)
dandi download -e refresh -f pyout --path-type exact \
  --output-dir data/human \
  "https://dandiarchive.org/dandiset/000019/0.220126.2148/files?location=sub-GP33"
```

These subset downloads are much smaller than the full datasets (a few GB instead of tens of GB) and are usually sufficient for local development and testing.

For detailed steps, see the full setup guide below.

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

If it already exists and you want to update it (e.g., after pulling new changes):

```bash
conda env update -f environment.yaml --prune
```

> **Note**: The `--prune` flag removes packages that are no longer in `environment.yaml`, ensuring your environment matches exactly what's specified.

This will:

- Create a new conda environment named `humanSayMonkeyDo` (if creating)
- Update an existing environment to match the latest `environment.yaml` (if updating)
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
mkdir -p data/{monkey,human}
```

### 5. Download the Monkey Dataset

> **Dataset Size Note**
> Full monkey datasets each exceed **tens of gigabytes**. Subset downloads are typically only a few GB and are recommended for most users.

Verify that the DANDI CLI is installed:

```bash
dandi --version
```

If the DANDI CLI is not found, ensure your conda environment is activated.

#### Option A: Download Monkey Subset (Recommended)

This downloads only the subset containing subject J data, which is sufficient for most development and testing tasks.

From the project root directory:

```bash
dandi download -e refresh -f pyout --path-type exact \
  --output-dir data/monkey \
  "https://dandiarchive.org/dandiset/000688/0.250122.1735/files?location=sub-J"
```

#### Option B: Download Full Monkey Dataset (Advanced)

> **Warning:** Full dataset is much larger (tens of GB). Only use if you need all subjects.

From the project root directory:

```bash
dandi download -e refresh -f pyout --path-type exact \
  --output-dir data/monkey \
  DANDI:000688/0.250122.1735
```

> Note: The full download will create subject subdirectories (e.g., `sub-J/`, `sub-L/`, etc.) inside `data/monkey/`.

### 6. Download the Human Dataset

> **Dataset Size Note**
> Full human datasets each exceed **tens of gigabytes**. Subset downloads are typically only a few GB and are recommended for most users.

Verify that the DANDI CLI is installed:

```bash
dandi --version
```

If the DANDI CLI is not found, ensure your conda environment is activated.

#### Option A: Download Human Subset (Recommended)

This downloads a small subset for subject GP33, which is sufficient for most development and testing tasks.

From the project root directory:

```bash
dandi download -e refresh -f pyout --path-type exact \
  --output-dir data/human \
  "https://dandiarchive.org/dandiset/000019/0.220126.2148/files?location=sub-GP33"
```

#### Option B: Download Full Human Dataset (Advanced)

> **Warning:** Full dataset is much larger (tens of GB). Only use if you need all subjects.

From the project root directory:

```bash
dandi download -e refresh -f pyout --path-type exact \
  --output-dir data/human \
  DANDI:000019/0.220126.2148
```

> Note: The full download will create subject subdirectories (e.g., `sub-GP33/`, `sub-GP31/`, etc.) inside `data/human/`.

### 7. Verify Installation

From the project root directory, verify your downloads:

#### Verify Monkey Dataset

Check the monkey data directory structure:

```bash
ls data/monkey/sub-J/
```

Expected output for **Option A (subset download)**:

```plaintext
sub-J_ses-CO-20160405_behavior+ecephys.nwb
sub-J_ses-CO-20160406_behavior+ecephys.nwb
sub-J_ses-CO-20160407_behavior+ecephys.nwb
```

#### Verify Human Dataset

Check the human data directory structure:

```bash
ls data/human/sub-GP33/
```

Expected output for **Option A (subset download)**:

```plaintext
sub-GP33_ses-GP33-B1.nwb
sub-GP33_ses-GP33-B30.nwb
sub-GP33_ses-GP33-B5.nwb
```

> **Note**: If you used Option B (full dataset download), you may see additional subject directories and files.

#### Test Python Environment

Verify that your conda environment is activated and the required packages are available:

```bash
python -c "from pynwb import NWBHDF5IO; print('Success: NWB environment ready!')"
```

If you see `Success: NWB environment ready!`, your setup is complete!

**Troubleshooting**: If you get `command not found: python`, make sure the conda environment is activated. You should see `(humanSayMonkeyDo)` at the start of your command prompt.

## Directory Structure

After completing the setup, your key project structure should look like this:

```plaintext
humanSayMonkeyDo/
├── environment.yaml         # Conda environment configuration
├── config.yaml              # Project configuration
├── pyproject.toml           # Python project metadata
├── data/                    # Downloaded datasets
│   ├── monkey/
│   │   └── sub-J/
│   │       ├── sub-J_ses-CO-20160405_behavior+ecephys.nwb
│   │       ├── sub-J_ses-CO-20160406_behavior+ecephys.nwb
│   │       └── sub-J_ses-CO-20160407_behavior+ecephys.nwb
│   └── human/
│       └── sub-GP33/
│           ├── sub-GP33_ses-GP33-B1.nwb
│           ├── sub-GP33_ses-GP33-B30.nwb
│           └── sub-GP33_ses-GP33-B5.nwb
├── src/                     # Source code
│   └── cse583_human_say_monkey_do/
│       ├── __init__.py
│       ├── core.py
│       ├── data_loading.py
│       └── ...
├── examples/                # Example notebooks and scripts
│   ├── human_example.ipynb
│   ├── monkey_example.ipynb
│   └── example_usage.py
├── tests/                   # Test files
└── doc/                     # Documentation
```

> **Note**: This shows the essential structure after recommended subset downloads (Option A). Full dataset downloads (Option B) may contain additional subject directories. Additional project files and documentation not shown here may also be present.

## Troubleshooting

### Conda Environment Creation Fails

- Make sure you're in the correct directory containing `environment.yaml`
- Try updating conda: `conda update conda`
- Check that the `environment.yaml` file is properly formatted

### DANDI Download Fails

- Check your internet connection
- Verify you have sufficient disk space
- Try downloading a smaller subset first
- Check DANDI archive status: <https://dandiarchive.org>

### "Command not found: conda activate"

If you see errors such as `command not found: conda` or `conda activate`:

```bash
# Initialize Conda for your shell
conda init bash     # or: conda init zsh

# Reload your shell config
source ~/.bashrc    # or: source ~/.zshrc
```

Then close and reopen your terminal (or open a new tab) and try:

```bash
conda activate humanSayMonkeyDo
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

- **DANDI Archive**: <https://dandiarchive.org>
- **Dataset Documentation**: <https://dandiarchive.org/dandiset/000688>
- **Project Repository**: <https://github.com/zach8421/UW-CSE583-humanSayMonkeyDo>
- **Conda Documentation**: <https://docs.conda.io>

---

**Need Help?**

If you encounter issues not covered in this guide, please:

1. Check the troubleshooting section above
2. Search existing issues in the project repository
3. Open a new issue with details about your problem

Happy coding!
