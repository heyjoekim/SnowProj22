# Data Directory README:
Most files for the analysis are provided in the necessary folders. The only data that is not included due to space on GitHub in the UCLA SWE reanalyis
## Directory for the data directory
1. RAW DATA
    1. `/crns`
    2. `/mesonet`
    3. `/snow`
        -  `/snotel`
        - `/ucla_swe`
2. ANALYSIS
3. MODEL OUTPUTS

### `/crns`
This directory contains the Cosmic Ray Neutron Sensor (CRNS) data for 11-22-2020 to 5-2021 at our CARC site in Montana. The .txt file is provided. From Sam Tuttle. This data will eventually be published to the NSIDC.

### `/mesonet`
This directory contains the Montana Mesonet data. This data was downloaded from the [Mesonet Downloader](https://shiny.cfc.umt.edu/mesonet-download/). I downloaded data from 2 stations. A screenshot of the data downloader is provided.

![Mesonet Downloader](../figures/readme_figs/mesonet_downloader.png)

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
1. Mocassin N 
    - 2018-10-01 to 2019-06-01
    - 2019-10-01 to 2020-06-01
    - 2020-11-21 to 2021-06-02
2. Moiese N MDA
    - 2020-10-01 to 2021-06-01

### `/snow/snotel`
This data was downloaded from the [Sleeping Woman Snotel site](https://wcc.sc.egov.usda.gov/nwcc/site?sitenum=783). The following file(s) was downloaded using the menus. Refer to the screenshot:

![SNOTEL Downloader](../figures/readme_figs/snotel_downloader.png)
Options for downloading SNOTEL data:
- Select Report Content: "Standard SNOTEL"
- Select Time Series: "Daily"
- Select Format: "csv"
- Skip View Current
- For Date (under green header), I selected:
    - Years: 2020
    - "Water Year"
    - "All days"
- Click on "View Historic" to download the csv file

### `/snow/ucla_swe`
This directory is left empty. A shell script is provided to download the Western United States UCLA Snow Reanalysis (WUS_UCLA_SR) v1 from the National Snow and Ice Data Center (NSIDC).

### `/processed`
This directory will hold all the processed data that will be used for the rest of the analysis. They will be in csv format that is saved to this directory with the Data_Process.py code.
