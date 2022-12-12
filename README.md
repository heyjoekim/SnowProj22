# SnowProj22 - Final Project for CEE609 EnvDatSci
## 1. Introduction
The amount of water that is stored in snow is an important resource to monitor especially with anthropogenic climate change. In the prairie, snow is heavily affected by winds \citep{pomeroy_prairie_1993}. We hope that cosmic ray neutron sensing, which has approximate maximum footprints ranges between 200 m to 300 m be able to get important measurements of snow water equivalence, the amount of water stored in snowpack. However, recent examinations have discussed whether the current corrections of raw CRNS data as described by \citet{desilets_calibrating_2017} are extremely location derived \citep{schattan_sensing_2019, andreasen_cosmic_2020, wallbank_estimating_2021}. From the correction factors, we know that neutron counts are related to moisture in its surrounding. Can we use a regression model to obtain a modelled neutron count given our given the atmospheric conditions (temperature, humidity, and pressure) assuming no changes in soil moisture? How accurate are SWE estimates from these modelled counting rates?

### 1.1 Dependencies
1. Anaconda
2. You need to have a NASA Earthdata Account
### 1.2 Running the Code
To run the code should be easy to do. First, clone the github repo in a terminal or Anaconda Power Shell.
```
git clone https://github.com/heyjoekim/SnowProj22
```
Alternatively, you can download the zipped file. After that, change into the repo saved onto your device. We need to make the script that will run all of the code executable first
```
cd SnowProj22
chmod +x run_snowproj.sh
```
After that the code should run without any errors
```
source run_snowproj.sh <os> <uid> <password>
```
The `<uid>` and `<password>` are the username and password for NASA Earthdata Login. Delete these and add your username and password to be able to download the files. For `<os>`: Enter your os. Important for windows system.
  
## 2. Data and Methods
### 2.1 Data Sources
This analysis will use measurements from the Cosmic Ray Neutron Sensor (CRNS) manufactured by Hydroinova LLC at a field site in Moccasin, Montana. The field site is a 1 km by 1 km research site containing multiple agricultural fields managed by Central Agriculture Research Center (CARC) through Montana State University. At the CARC, winter crops may persists which helps to trap snow and change snow redistribution patterns from winds. The CRNS sensor detects low-energy or “fast” neutrons. These neutrons are produced from cosmic rays interacting in matter and are typically attenuated from water molecules\citep{zreda_cosmos_2012, desilets_calibrating_2017}. CRNS sensors were originally developed for soil moisture detection but a method was established to determine the snow water equivalent (SWE). Our CRNS sensor collected data from November 2020 to May 2021. The CRNS also collects air temperatures, humidity, and atmospheric pressure in order to differentiate the effects of the interactions of cosmic rays with the atmosphere. 

Along with the atmospheric conditions that are collected by the CRNS sensor, I plan to also use humidity, atmospheric pressure, and temperature from the Montana Mesonet network located near our study site in Moccasin. The Montana Mesonet stations are operated by the Montana Climate Office (MCO) as a part of the Montana Forest \& Conservation Experiment Station at the University of Montana. In order to support research and agriculture, the MT Mesonet stations gather data on soil moisture and meteorological conditions. Data was downloaded from [https://shiny.cfc.umt.edu/mesonet-download/](https://shiny.cfc.umt.edu/mesonet-download/). Daily Air Temperatures, Atmospheric Pressure, and Relative Humidity was downloaded from the Mocassin ARC Mesonet station from November 22, 2020 to June 1, 2021 using the url provided.

To compare and test the location effect of the correction formulas for CRNS data, another site in Montana will be added. The location chosen is a site located west of Missoula, MT. This site was chosen due to the rough colocation of a MT Mesonet station and a United States Department of Agriculture Natural Resource Conservation Service Snow Telemetry (SNOTEL) station. The SNOTEL network is a group of over 600 stations across the Western United States that was placed in high snow accumulation area, mostly colocated with a snow course site \citep{serreze_characteristics_1999}. SNOTEL stations are designed to run automatically, especially in regions where obtain snow course data is dangerous to collect. SWE is collected through a snow pillow, a pressure transducer that when snow accumulates induced a change in a monometer \citep{serreze_characteristics_1999}. Occasionally, foreign debris may land on top of the snow pillow, so data needs to be checked for erroneous changes. Data will be taken for the approximate winter season for water year 2021 (October 1, 2020 to June 1, 2021) for the Moiese N MDA Mesonet station and the Sleeping Woman SNOTEL station. This was limited due to data availability for download of the Moiese N MDA Mesonet station.

To double check the magnitude of SWE, I will also use the Western United States UCLA Daily Snow Reanalyis, Version 1 dataset \citep{ucla_snow}. This data is freely available from the National Snow and Ice Data Center (NSIDC). A bash script is provided to download the currently available data. This dataset is created from a series of Landsat images that are uniquely blended in order to obtain posterior estimates of snow depth, SWE, and fractional snow cover. This analysis will only look at the SWE potion of the data. A time series of SWE at the approximate pixel location of both sites will be taken for water year 2021.

### 2.2 Data Processing
This section will outline the major data processing that must be done on the CRNS measurements.
### 2.2.1 Quality Control
CRNS measurements of neutron counts below 2000 counts per hour was removed from the dataset. CRNS measured temperature and humidity must also be quality controlled for erroneous measurements and missing data. For CRNS measured temperatures, any values below -60 was considered to be missing data and was removed from the data. Additionally, any relative humidity values that were above 100 was also removed from the data. Similar quality controls will also be done on Montana Mesonet data if needed. 

SNOTEL daily measurements will also be quality controlled for missing and erroneous data following procedures from \citet{serreze_characteristics_1999}. Erroneous data is designated as any change in measurements that is greater than at least 5 standard deviations greater than the monthly mean. Missing data will also be flagged. Common quality control for SNOTEL stations typically involve negative measurements for SWE and snow depth. Unless precipitation is involved, most data will be filled with a value of 0 for these negative measurements. However, if significant
### 2.2.2 CRNS Processing and SWE Calculations
The main calculations for CRNS processing and SWE calculations are done based on \citet{desilets_calibrating_2017} which is summarized in this section. The raw neutron counting rate from the sensor first needs to be corrected from other moisture sources such as the atmosphere:

$$
    N=N_{raw}F(t) \tag{1}
$$

$F(t)$ is the correction factor which is then decomposed into the following components

$$
    F(t)=f_{bar}f_{sol}f_{hum} \tag{2}
$$

$$
    f_{bar}=\exp[\beta(p(t)-p_0)]\tag{3}
$$

$$
    f_{sol}=\frac{M_0}{M(t)}\tag{4}
$$

$$
    f_{hum}=1+0.0054H(t)\tag{5}
$$

$f_{bar}$ is the correction factor based on barometric pressure. $\beta$ is a pressure coefficient assumed to be 0.0077 hPa $^{-1}$. p(t) is the pressure and $p_0$ is a reference pressure usually some average pressure for the site. $f_{sol}$ corrects for solar activity and is based off of the Jungfraujoch neutron monitor. This correction factor will not be varied in this analysis. Finally, $f_{hum}$ is the correction for humidity, which was derived from data and simulations by \citet{rosolem_effect_2013}. H(t) can be calculated with the equation

$$
    H(t) = \frac{U}{100}(\frac{e_wk}{T+273.13})\tag{6}
$$

$U$ is relative humidity expressed as a percentage and $k$ is a constant equal to 216.68 $g k J^{-1}$. $e_w$ is the saturation vapor pressure calculated by

$$
    e_w = 6.112 \exp(\frac{17.62T}{243.12+T})\tag{7}
$$

for temperature T in $^{\circ}C$ . The final equations that are also needed are

$$
    N_{wat}=0.24N_0\tag{8}
$$

$$
    N_0 = \frac{F(t)N_\theta}{\frac{a_0}{\theta_g\rho_{bd}+a_2}+a_1}\tag{9}
$$

where $a_0$, $a_1$, and $a_2$ are all derived from simulations. Using all of these corrections, we can invert equations and derive an expression for the SWE. The SWE function is

$$
    SWE = -\Lambda\ln(\frac{N-N_{wat}}{N_\theta-N_{wat}})\tag{10}
$$

where $\Lambda$ is an attenuation length and $N_{wat}$ is the counting rate over deep water, $N_\theta$ is the zero-snow counting rate, and N is the counting rate.

### 2.2.3 Models
In order to check if the equations from \citet{desilets_calibrating_2017} work for our site in Montana, I will first use a random forest regression to my CRNS data. Random forests are an ensemble model by creating multiple decision trees with more randomness \citep{breiman2001random}. In order to estimate the coefficients, I will use partial dependence plots. Introduced by \citet{molnar_relating_2021}, partial dependence plots allows us to interpret model relationships within a model, especially with machine learning models that do no take explicit assumptions. Additionally, another issue that needs to be brought up in multicolinearity. I calculated the VIF for my features for my random forest regression. While slightly colinear with our variables (VIF<10), pressure is highly colinear with our corrected neutron counts with the VIF being at least an order of magnitude greater than 10. While feature selection is not a major part of this analysis, using highly colinear variables may influence the results of our regression. 

Table 1: Variable Inflation Factors for each feature in the regression DataFrame. VIFs greater than 10 is set to have too much multicolinearity.
|**Feature**| **VIF**|
|-----------|--------|
|N_cor [cph]|723.05  |
|P [mb]     |676.81  |
|H [$gm^3$] |	9.71 |


I will specifically run random forest models using both pressure in mb/hPa and absolute humidity in $g/m^{-3}$ (Equation 6) combining temperature and relative humidity from our weather data. Using H will give us an easier linear relationship to analyze with the partial dependence plots. 

From the approximations of the partial dependence plots, I will approximate the $\beta$ from the pressure correction equation (Equation 3) as well as relationships between relative humidity and temperature. For the second regression, I will estimate both y-intercept (= 1) and the slope (0.0054) from Equation 5, to see if our trained random forest regression is estimating these values. These linear regressions will be performed using the statsmodel package for python \citep{seabold2010statsmodels}.

### 2.2.4 Training/Validation
Both regression model would be trained on the processed CRNS data. The corrected neutron counting rate N will be predicted using pressure (mb) and absolute humidity (). The full hourly CRNS data will be used to train the regression model. The training and testing split of the data will be done using the scikit-learn Python package and its built-in function train\_test\_split. The training/testing split will be done on 7:3 ratio. For the ridge regression, the data will be normalized before fitting, also using scikit-learn's standardization functions. Comparisons of model fit will be made using $R^2$, root mean squared error, and the Pearson correlation metric. Both $R^2$ and root mean squared error is built into scikit-learn package through the metrics module. The Pearson correlation will be used from the Python package scipy \citep{2020SciPy-NMeth}. The counting rates will also be compared after going through the corrections described in \citet{desilets_calibrating_2017} as well as the modelled counting rates.

Finally, these counting rates would be used to calculate SWE values which will be compared to either both SNOTEL data and the UCLA reanalysis data or just the reanalysis data to check magnitude and correlations.
## 3 Results
## 4.
