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

Navigate to the monkey data directory:

```bash
cd data/monkey
```

You have two options for downloading the dataset:

#### Option A: Download Full Monkey Dataset

> Note: DANDI downloads usually create a directory named after the dataset
(e.g., 000688/). The commands below flatten that structure by moving
the files directly into `data/monkey` and removing the extra folder.

**Warning:** If .nwb files already exist in `data/monkey`, the `mv` command may overwrite files. Use with caution.

```bash
dandi download DANDI:000688/0.250122.1735
mv 000688/* .
rmdir 000688
```

#### Option B: Download Monkey Subset (Recommended for Testing)

```bash
dandi download -e refresh -f pyout --path-type exact \
  --output-dir data/monkey \
  "https://dandiarchive.org/dandiset/000688/0.250122.1735/files?location=sub-J"
```

This downloads only the subset containing subject J data, which is sufficient for most development and testing tasks.

### 6. Download the Human Dataset

> **Dataset Size Note**
> Full human datasets each exceed **tens of gigabytes**. Subset downloads are typically only a few GB and are recommended for most users.

Verify that the DANDI CLI is installed:

```bash
dandi --version
```

If the DANDI CLI is not found, ensure your conda environment is activated.

Navigate to the human data directory:

```bash
cd data/human
```

You have two options for downloading the dataset:

#### Option A: Download Full Human Dataset

As with the monkey dataset, DANDI will create a directory matching the
dataset ID (e.g., 000019/). The commands below flatten that structure so
all .nwb files live directly in data/human.

**Warning:** If .nwb files already exist in `data/human`, the `mv` command may overwrite files. Use with caution.

```bash
dandi download DANDI:000019/0.220126.2148
mv 000019/* .
rmdir 000019
```

#### Option B: Download Human Subset (Recommended for Testing)

```bash
dandi download -e refresh -f pyout --path-type exact \
  --output-dir data/human \
  "https://dandiarchive.org/dandiset/000019/0.220126.2148/files?location=sub-GP33"
```

This downloads a small subset for subject GP33, which is sufficient for most development and testing tasks.

### 7. Verify Datasets

From the project root, list the contents of each data directory.

#### Expected monkey subset output

```bash
ls data/monkey
```

You should see files similar to:

```plaintext
sub-J_session1.nwb
sub-J_session2.nwb
sub-J_session3.nwb
```

#### Human subset example

```bash
ls data/human
```

Expected output:

```plaintext
sub-GP33_session1.nwb
sub-GP33_session2.nwb
```

If the expected .nwb files appear, your datasets downloaded correctly.

### 8. Verify Installation

Return to the project root:

```bash
cd ../..
```

Verify that the data structure looks correct:

```bash
ls -la data/monkey/
```

You should see `.nwb` files in this directory.

Run a quick test to ensure everything is working:

```bash
python - << 'EOF'
from pynwb import NWBHDF5IO
print("Imports successful. NWB IO ready.")
EOF
```

If this runs without errors, your environment is set up correctly!

## Directory Structure

After setup, your project should look like this:

```plaintext
humanSayMonkeyDo/
├── environment.yaml
├── config.yaml
├── data/
│   ├── monkey/
│   │   ├── sub-J_*.nwb
│   │   └── ...
│   └── human/
│       ├── sub-*.nwb
│       └── ...
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
