# Data Directory README:
## Directory for the data directory
1. `/crns`
2. `/mesonet`
3. `/snow`
    -  `/snotel`
    - `/ucla_swe`
4. `/processed`

### `/crns`
This directory contains the Cosmic Ray Neutron Sensor (CRNS) data for 11-22-2020 to 5-2021 at our CARC site in Montana. The .txt file is provided. From Sam Tuttle. This data will eventually be published to the NSIDC.

### `/mesonet`
This directory contains the Montana Mesonet data. This data was downloaded from the link: <>. I downloaded data from 2 stations. A screenshot of the data downloader is provided.

![Mesonet Downloader](/readme_figs/mesonet_downloader.png)

Stations:
1. Moccasin N ARC
2. Moiese N

Variables:
1. Air Temperature
2. Atmospheric Pressure
3. Relative Humidity

Aggregation Interval:
- Daily

Dates:
- 

### `/snow/snotel`
This data was downloaded from <>. 

### `/snow/ucla_swe`
This directory is left empty. A shell script is provided to download the Western United States UCLA Snow Reanalysis (WUS_UCLA_SR) v1 from the National Snow and Ice Data Center (NSIDC).

### `/processed`
This directory will hold all the processed data that will be used for the rest of the analysis. They will be in csv format that is saved to this directory with the Data_Process.py code.