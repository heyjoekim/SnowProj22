#!/bin/bash

# Run script to get data from NSIDC
echo "obtaining Data from NSIDC"
./nsidc_download.sh
echo "finished"

echo "Running Python Script for Data Processing"
python ./code/Data_Process.py
echo "finished"
