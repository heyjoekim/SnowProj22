#!/bin/bash

# Run script to get data from NSIDC
echo "obtaining Data from NSIDC"
# make sure script is executable
chmod +x ./code/nsidc_download_win.sh
# execute nsidc download script

sh ./code/nsidc_download_win.sh $1 $2

echo "Running Python Script for Data Processing"
conda run -n snow python ./code/Data_Process.py
echo "Finished"

echo " "
echo "Running and Training Models"
conda run -n snow python ./code/model_code_validation.py
echo "Finished"

echo " "
echo "Generating Figures"
conda run -n snow python ./code/figures.py
echo "Finished"
