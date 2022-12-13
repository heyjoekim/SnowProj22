# Assessing Cosmic Ray Neutron Sensing Corrections Equations to Location
## 1. Introduction
The amount of water that is stored in snow is an important resource to monitor especially with anthropogenic climate change. In the prairie, snow is heavily affected by winds [5]. We hope that cosmic ray neutron sensing, which has approximate maximum footprints ranges between 200 m to 300 m be able to get important measurements of snow water equivalence, the amount of water stored in snowpack. However, recent examinations have discussed whether the current corrections of raw CRNS data as described by Desilets (2017) [3] are extremely location derived [1, 10, 14]. From the correction factors, we know that neutron counts are related to moisture in its surrounding. Can we use a regression model to obtain a modelled neutron count given our given the atmospheric conditions (temperature, humidity, and pressure) assuming no changes in soil moisture? How accurate are SWE estimates from these modelled counting rates?

### 1.1 Dependencies
1. Anaconda
2. You need to have a NASA Earthdata Account
### 1.2 Running the Code
Before running the code, please have your username and password ready for a NASA Earthdata Account. One of the datasets required for this analysis downloads data from the NSIDC. Then, you may clone this github repo in a terminal or Anaconda Power Shell.
```
git clone https://github.com/heyjoekim/SnowProj22
```
Alternatively, you can download the zipped file. After that, change into the repo saved onto your device. We need to make the script that will run all of the code executable first
```
cd SnowProj22
chmod +x run_snowproj.sh
```
After that the code should run without any errors. The following script will create a new conda environment called `snow` which will use all the versions of the python packages that this analysis used. It will also complete all of the analysis.
```
source run_snowproj.sh <os> <uid> <password>
```
The `<uid>` and `<password>` are the username and password for NASA Earthdata Login. Delete these and add your username and password to be able to download the files. For `<os>`: Enter your os. Important for windows system.
  
## 2. Data and Methods
### 2.1 Data Sources
This analysis will use measurements from the Cosmic Ray Neutron Sensor (CRNS) manufactured by Hydroinova LLC at a field site in Moccasin, Montana. The field site is a 1 km by 1 km research site containing multiple agricultural fields managed by Central Agriculture Research Center (CARC) through Montana State University. At the CARC, winter crops may persists which helps to trap snow and change snow redistribution patterns from winds. The CRNS sensor detects low-energy or “fast” neutrons. These neutrons are produced from cosmic rays interacting in matter and are typically attenuated from water molecules[3,15]. CRNS sensors were originally developed for soil moisture detection but a method was established to determine the snow water equivalent (SWE). Our CRNS sensor collected data from November 2020 to May 2021. The CRNS also collects air temperatures, humidity, and atmospheric pressure in order to correct the effects of the interactions of cosmic rays with the atmosphere. 

Along with the atmospheric conditions that are collected by the CRNS sensor, I also used humidity, atmospheric pressure, and temperature from the Montana Mesonet network located near our study site in Moccasin. The Montana Mesonet stations are operated by the Montana Climate Office (MCO) as a part of the Montana Forest \& Conservation Experiment Station at the University of Montana. In order to support research and agriculture, the MT Mesonet stations gather data on soil moisture and meteorological conditions. Data was downloaded from [https://shiny.cfc.umt.edu/mesonet-download/](https://shiny.cfc.umt.edu/mesonet-download/). Daily Air Temperatures, Atmospheric Pressure, and Relative Humidity was downloaded from the Mocassin ARC Mesonet station from November 22, 2020 to June 1, 2021 using the url provided.

To compare and test the location effect of the correction formulas for CRNS data, another site in located west of Missoula, MT will be added. This site was chosen due to the rough colocation of a MT Mesonet station and a United States Department of Agriculture Natural Resource Conservation Service Snow Telemetry (SNOTEL) station. The SNOTEL network is a group of over 600 stations across the Western United States that was placed in high snow accumulation area, mostly colocated with a snow course site [12]. SNOTEL stations are designed to run automatically, especially in regions where snow course data is dangerous to collect. SWE is collected through a snow pillow, a pressure transducer that when snow accumulates induced a change in a monometer [12]. Occasionally, foreign debris may land on top of the snow pillow, so data needs to be checked for erroneous changes. Data will be taken for the approximate winter season for water year 2021 (October 1, 2020 to June 1, 2021) for the Moiese N MDA Mesonet station and the Sleeping Woman SNOTEL station.

To double check the magnitude of SWE, I will also use the Western United States UCLA Daily Snow Reanalyis, Version 1 dataset [4]. This data is freely available from the National Snow and Ice Data Center (NSIDC). A bash script is provided to download the currently available data. This dataset is created from a series of Landsat images that are uniquely blended in order to obtain posterior estimates of snow depth, SWE, and fractional snow cover. This analysis will only look at the SWE potion of the data. A time series of SWE at the approximate pixel location of both sites will be taken for water year 2021.

### 2.2 Data Processing and Model
This section will outline the major data processing that must be done on the CRNS measurements.
#### 2.2.1 Quality Control
CRNS measurements of neutron counts below 2000 counts per hour was removed from the dataset. CRNS measured temperature and humidity must also be quality controlled for erroneous measurements and missing data. For CRNS measured temperatures, any values below -60 was considered to be missing data and was removed Additionally, any relative humidity values that were above 100 was also removed. Similar quality controls will also be done on Montana Mesonet data if needed. 

SNOTEL daily measurements will also be quality controlled for missing and erroneous data using the following procedures [12]. Erroneous data is designated as any change in measurements that is greater than at least 5 standard deviations greater than the monthly mean. Missing data will also be flagged. Common quality control for SNOTEL stations typically involve negative measurements for SWE and snow depth. Unless precipitation is involved, most data will be filled with a value of 0 for these negative measurements.
#### 2.2.2 CRNS Processing and SWE Calculations
The main calculations for CRNS processing and SWE calculations are done based on Darin Desilet's 2017 [3] analysis which is summarized in this section. The raw neutron counting rate from the sensor first needs to be corrected from other moisture sources such as the atmosphere:

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

$f_{bar}$ is the correction factor based on barometric pressure. $\beta$ is a pressure coefficient assumed to be 0.0077 hPa $^{-1}$. $p(t)$ is the pressure and $p_0$ is a reference pressure usually some average pressure for the site. $f_{sol}$ corrects for solar activity and is based off of the Jungfraujoch neutron monitor. This correction factor will not be varied in this analysis. Finally, $f_{hum}$ is the correction for humidity, which was derived from data and simulations by Rosolem et al. (2013) [9]. H(t) can be calculated with the equation

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

#### 2.2.3 Models
In order to check if the equations from [3] will work for our site in Montana, I will first use a random forest regression to my CRNS data. Random forests are an ensemble model by creating multiple decision trees with more randomness [2].The random forest regression will be running using the version implemented in Python with the scikit-learn package[8]. In order to estimate the coefficients, I will use partial dependence plots. Introduced by [7], partial dependence plots allows us to interpret model relationships within a model, especially with machine learning models that do no take explicit assumptions. The partial dependence plots used are also from scikit-learn [8]. Additionally, another issue that needs to be brought up in multicolinearity. I calculated the VIF for my features for my random forest regression. While slightly colinear with our variables (VIF<10), pressure is highly colinear with our corrected neutron counts with the VIF being at least an order of magnitude greater than 10. While feature selection is not a major part of this analysis, using highly colinear variables may influence the results of our regression. 

Table 1: Variable Inflation Factors for each feature in the regression DataFrame. VIFs greater than 10 is set to have too much multicolinearity.
|**Feature**| **VIF**|
|-----------|--------|
|N_cor [cph]|723.05  |
|P [mb]     |676.81  |
|H $[g/m^3]$ |	9.71 |


I will specifically run random forest models using both pressure in mb/hPa and absolute humidity in $g/m^{-3}$ (Equation 6) combining temperature and relative humidity from our weather data. Using H will give us an easier linear relationship to analyze with the partial dependence plots (PDP). Additionally, to obtain a rough approximation between the relationship of neutron counts hitting the detector and our two atmospheric variables, I will compare the partial dependence plots with modeled neutron counts. The modeled neutron counts will be from the Ultra-Rapid Neutron Only Simulation (URANOS), a Monte Carlo simulation developed specifically for CRNS purposes. The Monte Carlo code can generate millions of neutrons with some randomly sampled initial conditions, while tracking their paths and interactions. URANOS also allows us to model geometries using layers to replicate important site characteristics[6]. Two sets of URANOS models runs were done: 1 set under equal pressure and variable humidity, and another set at equal humidity but variable pressures. Both runs also kept soil moisture and soil porosity constant at 12.5\% and 50\% respectively. Each model run also calculated the path and interactions of 1 million neutrons. Only the epithermal neutron counts are shown in this analysis to compare against our measurements and PDP.

From the approximations of the partial dependence plots, I will approximate the $\beta$ from the pressure correction equation (Equation 3) as well as relationships between relative humidity and temperature. For the second regression, I will estimate both y-intercept (= 1) and the slope (0.0054) from Equation 5, to see if our trained random forest regression is estimating these values. These linear regressions will be performed using the statsmodel package for python [11].

#### 2.2.4 Training/Validation
Both regression model would be trained on the processed CRNS data. The corrected neutron counting rate N will be predicted using pressure (mb) and absolute humidity ($g/m^3$). The full hourly CRNS data will be used to train the regression model. The training and testing split of the data will be done using the scikit-learn Python package and its built-in function train\_test\_split. The training/testing split will be done on 7:3 ratio. For the ridge regression, the data will be normalized before fitting, also using scikit-learn's standardization functions. Comparisons of model fit will be made using $R^2$, root mean squared error, and the Pearson correlation metric. Both $R^2$ and root mean squared error is built into scikit-learn package through the metrics module. The Pearson correlation will be used from the Python package scipy [13]. The counting rates will also be compared after going through the corrections described in Desilet (2017) as well as the modelled counting rates.

Finally, these counting rates would be used to calculate SWE values which will be compared to either both SNOTEL data and the UCLA reanalysis data or just the reanalysis data to check magnitude and correlations.
## 3 Results
![regression results](/figures/my_figs_original/rf_results.png)
*Figure 1. (a) Random Forest results shown between "observed" corrected Neutron counts against predicted corrected Neutron Counts for our CRNS sensor at the CARC in counts per hour. The dashed line shows a one to one relationship between the two entities. (b) A similar plot against our "observed" neutron counts with the residuals of the regression results. A dashed line at 0 represents where both predicted and observed values are equal. The residuals clearly have some heteroscedasticity.*

![Pressure PDP](/figures/my_figs_original/pdp_press.png)
*Figure 2. A partial dependence plot (PDP) between pressure [mb] against Corrected Neutron counts (blue dots). The black dashed line is a linear fit for pressure as the independent variable and the log Neutron Count as the depdendent variable. Modeled results from URANOS are plotted along side our regression PDP with changing pressures at a constant humidity, soil moisture, and soil porosity. The red line is a linear fit for modeled results and shows a slight difference between the RF regression and simple modeled results.*

![Abs. Humidity PDP](/figures/my_figs_original/pdp_humid.png)
*Figure 3. A partial dependence plot (PDP) between absolute humidity [g/m^3] against Corrected Neutron counts (blue dots). The black line is a linear fit for absolutre pressure as the independent variable and the Neutron Count as the depdendent variable. Modeled results from URANOS are plotted along side our regression PDP with changing humidity at a constant pressure, soil moisture, and soil porosity. The red dashed line is the linear equation for modeled humidity and neutron counts.*

![CARC SWE](/figures/my_figs_original/carc_swe_results.png)
*Figure 4: a) Corrected neutron counts for our CARC site using the Desilets (2017) equation (blue) and the RF regression (orange) for the Moccasin Mesonet station data. b) SWE calculations using the Desilets (2017) equations for neutron counts based on Desilet (2017) corrections (blue), Random Forest correction (orange). The Western United States UCLA Snow Reanalysis Data is also plotted as an additional data source (green).*

![SW SWE](/figures/my_figs_original/sw_swe_results.png)
*Figure 5: a) Corrected neutron counts for the Sleeping Woman SNOTEL site using RF regression (blue) using the Moise MD Mesonet station data. No CRNS data is available for this site b) SWE calculations using the Desilets (2017) equations for neutron counts based on Desilet (2017) for Random Forest correction (orange). SNOTEL measurements (blue) and the Western United States UCLA Snow Reanalysis Data (green) are also shown. At this site, the RF corrections does not work well.*  
## 4. Discussion

## 5. Conclusion

## References
1. Andreasen, M., Jensen, K. H., Zreda, M., Desilets, D., Bogena, H., & Looms, M. C. (2016). Modeling cosmic ray neutron field measurements: MODELING COSMIC RAY NEUTRON FIELD MEASUREMENTS. *Water Resources Research*, 52(8), 6451–6471. https://doi.org/10.1002/2015WR018236
2. Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5–32. https://doi.org/10.1023/A:1010933404324
3. Desilets, D. (2017). Calibrating A Non-Invasive Cosmic Ray Soil Moisture For Snow Water Equivalent. https://doi.org/10.5281/ZENODO.439105
4. Fang, Y., Y. L. and Margulis., S. A. (2022). Western united states ucla daily snow reanalysis,
version 1
4. Gray, D. M. (1970). Snow hydrology of the prairie environment. *Snow hydrology*, 21-34.
5. Köhli, M., Schrön, M., Zacharias, S., & Schmidt, U. (2022). URANOS v1.0 – the Ultra Rapid Adaptable Neutron-Only Simulation for Environmental Research [Preprint]. Climate and Earth system modeling. https://doi.org/10.5194/gmd-2022-93
6. Molnar, C., Freiesleben, T., König, G., Casalicchio, G., Wright, M. N., & Bischl, B. (2021). Relating the Partial Dependence Plot and Permutation Feature Importance to the Data Generating Process (arXiv:2109.01433). arXiv. http://arxiv.org/abs/2109.01433
7. Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel,
M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau,
D., Brucher, M., Perrot, M., and Duchesnay, E. (2011). Scikit-learn: Machine learning in
Python. Journal of Machine Learning Research, 12:2825–2830.
7. Rosolem, R., Shuttleworth, W. J., Zreda, M., Franz, T. E., Zeng, X., & Kurc, S. A. (2013). The Effect of Atmospheric Water Vapor on Neutron Count in the Cosmic-Ray Soil Moisture Observing System. *Journal of Hydrometeorology*, 14(5), 1659–1671. https://doi.org/10.1175/JHM-D-12-0120.1
8. Schattan, P., Köhli, M., Schrön, M., Baroni, G., & Oswald, S. E. (2019). Sensing Area‐Average Snow Water Equivalent with Cosmic‐Ray Neutrons: The Influence of Fractional Snow Cover. *Water Resources Research*, 55(12), 10796–10812. https://doi.org/10.1029/2019WR025647
9. Seabold, S. and Perktold, J. (2010). statsmodels: Econometric and statistical modeling with
python. In 9th Python in Science Conference.
9. Serreze, M. C., Clark, M. P., Armstrong, R. L., McGinnis, D. A., & Pulwarty, R. S. (1999). Characteristics of the western United States snowpack from snowpack telemetry (SNOTEL) data. *Water Resources Research*, 35(7), 2145–2160. https://doi.org/10.1029/1999WR900090
10. Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M., Reddy, T., Cournapeau, D.,
Burovski, E., Peterson, P., Weckesser, W., Bright, J., van der Walt, S. J., Brett, M.,
Wilson, J., Millman, K. J., Mayorov, N., Nelson, A. R. J., Jones, E., Kern, R., Larson,
E., Carey, C. J., Polat,  ̇I., Feng, Y., Moore, E. W., VanderPlas, J., Laxalde, D., Perktold,
J., Cimrman, R., Henriksen, I., Quintero, E. A., Harris, C. R., Archibald, A. M., Ribeiro,
A. H., Pedregosa, F., van Mulbregt, P., and SciPy 1.0 Contributors (2020). SciPy 1.0:
Fundamental Algorithms for Scientific Computing in Python. Nature Methods, 17:261–272.
10. Wallbank, J. R., Cole, S. J., Moore, R. J., Anderson, S. R., & Mellor, E. J. (2021). Estimating snow water equivalent using cosmic‐ray neutron sensors from the COSMOS‐UK network. *Hydrological Processes*, 35(5). https://doi.org/10/gq5kxc
11. Zreda, M., Shuttleworth, W. J., Zeng, X., Zweck, C., Desilets, D., Franz, T., & Rosolem, R. (2012). COSMOS: The COsmic-ray Soil Moisture Observing System. *Hydrology and Earth System Sciences*, 16(11), 4079–4099. https://doi.org/10.5194/hess-16-4079-2012
