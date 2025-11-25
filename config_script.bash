# ensure the script runs from the project directory
cd "$(dirname "$0")" || exit

# Function to check available storage
check_space() {
    local required_bytes=$1
    local target_path=${2:-.}
    
    local available=$(df --output=avail -B 1 "$target_path" 2>/dev/null | tail -n 1)
    
    # Fallback for macOS
    if [ -z "$available" ]; then
        available=$(df -k "$target_path" | tail -1 | awk '{print $4 * 1024}')
    fi
    
    if [ "$available" -ge "$required_bytes" ]; then
        echo "✓ Sufficient space available: $(numfmt --to=iec $available 2>/dev/null || echo "$((available / 1024 / 1024 / 1024))GB")"
        return 0
    else
        echo "✗ Insufficient space. Available: $(numfmt --to=iec $available 2>/dev/null || echo "$((available / 1024 / 1024 / 1024))GB"), Required: $(numfmt --to=iec $required_bytes 2>/dev/null || echo "$((required_bytes / 1024 / 1024 / 1024))GB")"
        return 1
    fi
}

# Function to download DANDI dataset with storage check and full/subset option
download_dandi_dataset() {
    local dataset_id=$1
    local dataset_version=$2
    local subset_filter=$3  # Optional: filter for subset (e.g., "sub-J")
    local full_size_gb=$12   # Size in GB for full dataset
    local dataset_name=${5:-"dataset"}  # Optional: name for display
    
    while true; do
        read -p "Would you like to download the full $dataset_name or a subset? (full/subset): " choice
        if [[ "$choice" == "full" ]]; then
            echo "Checking storage for full $dataset_name..."
            local required_bytes=$((full_size_gb * 1024 * 1024 * 1024))
            if check_space "$required_bytes" "."; then
                echo "Downloading full $dataset_name..."
                dandi download "DANDI:${dataset_id}/${dataset_version}"
                # Clean up the numbered folder
                if [ -d "$dataset_id" ]; then
                    mv "$dataset_id"/* .
                    rmdir "$dataset_id"
                fi
                break
            else
                echo "Not enough storage for full dataset. Please free up space or choose subset."
                exit 1
            fi
        elif [[ "$choice" == "subset" ]]; then
            echo "Downloading subset..."
            if [ -n "$subset_filter" ]; then
                #dandi download "https://dandiarchive.org/dandiset/${dataset_id}/${dataset_version}/files?location=${subset_filter}"
                dandi download -e REFRESH -f PYOUT --path-type EXACT "https://dandiarchive.org/dandiset/${dataset_id}/${dataset_version}/files?location=${subset_filter}"
                #echo "https://dandiarchive.org/dandiset/${dataset_id}/${dataset_version}/files?location=${subset_filter}"
                #dandi download --existing REFRESH "https://dandiarchive.org/dandiset/${dataset_id}/${dataset_version}/files?location=${subset_filter}"
            else
                echo "Error: No subset filter defined for this dataset"
                exit 1
            fi
            break
        else
            echo "Invalid choice. Please enter 'full' or 'subset'"
        fi
    done
}

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

#Give option of downloading full dataset or partial
# Usage examples:
echo "downloading monkey data..."
cd ./data/monkey
download_dandi_dataset "000688" "0.250122.1735" "sub-J" 12 "monkey dataset"

echo "downloading human data..."
cd ../human
download_dandi_dataset "000019" "0.220126.2148" "sub-GP33" 12 "human dataset"