# ensure the script runs from the project directory
cd "$(dirname "$0")" || exit

echo "checking conda install..."
#check if the user has conda installed
if command -v conda &> /dev/null
then
    echo "Conda is installed"
    conda --version
else
    echo "Conda is not installed, please install and retry"
    echo "Installation cancelled"
    exit 1
fi

#check if they have already initialized the appropriate environment
if conda env list | grep -q "^humanSayMonkeyDo "; then
    echo "Environment 'humanSayMonkeyDo' already exists, continuing to data"
else
    echo "Environment does not exist, initializing conda environment"

    #check that we are usign the correct environment file
    if [[ -f "environment.yaml" ]] && head -n 1 environment.yaml | grep -q "humanSayMonkeyDo"; then
        echo "Identified correct environment file, creating environment..."
        if conda env create -f environment.yaml; then
            echo "Environment successfully created"
        else
            echo "Error: Failed to create environment"
            exit 1
        fi
    else
        echo "Unable to identify correct environment file. Ensure that current folder is in the main humanSayMonkeyDo folder..."
    fi
fi


#activate environemnt
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate humanSayMonkeyDo

#create file structure
echo "creating data folder structure" 
mkdir -p data/monkey
mkdir -p data/human

echo "downloading monkey data..."
cd ./data/monkey

#Give option of downloading full dataset or partial
while true; do
    read -p "Would you like to download the full dataset or a subset? (full/subset): " choice

    if [[ "$choice" == "full" ]]; then
        echo "Downloading full dataset..."
        dandi download DANDI:000688/0.250122.1735
        mv 000688/* .
        rmdir 000688 # clean up the empty folder
        break
    elif [[ "$choice" == "subset" ]]; then
        echo "Downloading subset..."
        dandi download "https://dandiarchive.org/dandiset/000688/0.250122.1735/files?location=sub-J"
        break
    else
        echo "Invalid choice. Please enter 'full' or 'subset'"
    fi
done

echo "TODO: download human dataset"