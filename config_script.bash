cat "checking conda install..."
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
    echo "Environment does not exist, initializign conda environment"

    #check that we are usign the correct environment file
    if [[ -f "environment.yaml" ]] && head -n 1 environment.yaml | grep -q "humanSayMonkeyDo"; then
        echo "Identified correct environment file, creating environment..."
        if conda env create -f environment.yaml; then
            echo "Environment successfully created"
        else
            echo "Error: Failed to create environment"
            exit 1
    else
        echo "Unable to identify correct environment file. Ensure that current folder is in the main humanSayMonkeyDo folder..."
    fi
fi


#activate environemnt
conda activate humanSayMonkeyDo

#create file structure
echo "creating data folder structure" 
mkdir data
mkdir data/monkey
mkdir data/human

echo "downloading monkey data..."
cd ./data/monkey

#Give option of downloading full dataset or partial
read -p "Would you like to download the full dataset or a subset? (full/subset): " choice

if [[ "$choice" == "full" ]]; then
    echo "Downloading full dataset..."
    dandi download DANDI:000688/0.250122.1735
    mv 000688/* .
elif [[ "$choice" == "subset" ]]; then
    echo "Downloading subset..."
    dandi download "https://dandiarchive.org/dandiset/000688/0.250122.1735/files?location=sub-J"
else
    echo "Invalid choice. Please enter 'full' or 'subset'"
    exit 1
fi

echo "TODO: download human dataset"