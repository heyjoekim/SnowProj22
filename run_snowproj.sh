#!/bin/bash

# Create environment to run my project
conda env create -f myenv.yml
conda activate snow

# Run script to get data from NSIDC
echo "obtaining Data from NSIDC"
# make sure script is executable
chmod +x ./code/nsidc_download.sh
chmod +x ./code/nsidc_download_win.sh
# execute nsidc download script
sh ./code/nsidc_download.sh $1 $2
echo "finished"

echo "Running Python Script for Data Processing"
python ./code/Data_Process.py
echo "Finished"

echo " "
echo "Running and Training Models"
python ./code/model_code_validation.py
echo "Finished"

echo " "
echo "Generating Figures"
python ./code/figures.py
echo "Finished"
