Additional processing was not done. Figure Captions

Figure 1 File: rf_results.png
Figure 1: (a) Random Forest results shown between "observed" corrected Neutron counts against predicted corrected Neutron Counts for our CRNS sensor at the CARC in counts per hour. The dashed line shows a one to one relationship between the two entities. (b) A similar plot against our "observed" neutron counts with the residuals of the regression results. A dashed line at 0 represents where both predicted and observed values are equal. The residuals clearly have some heteroscedasticity.

Figure 2 File: pdp_press
Figure 2. A partial dependence plot (PDP) between pressure [mb] against Corrected Neutron counts (blue dots). The black dashed line is a linear fit for pressure as the independent variable and the log Neutron Count as the depdendent variable. Modeled results from URANOS are plotted along side our regression PDP with changing pressures at a constant humidity, soil moisture, and soil porosity. The red line is a linear fit for modeled results and shows a slight difference between the RF regression and simple modeled results.

Figure 3 File: pdp_humid
Figure 3. A partial dependence plot (PDP) between absolute humidity [g/m^3] against Corrected Neutron counts (blue dots). The black line is a linear fit for absolutre pressure as the independent variable and the Neutron Count as the depdendent variable. Modeled results from URANOS are plotted along side our regression PDP with changing humidity at a constant pressure, soil moisture, and soil porosity. The red dashed line is the linear equation for modeled humidity and neutron counts.

Figure 4 File: carc_swe_results
Figure 4: a) Corrected neutron counts for our CARC site using the Desilets (2017) equation (blue) and the RF regression (orange) for the Moccasin Mesonet station data. b) SWE calculations using the Desilets (2017) equations for neutron counts based on Desilet (2017) corrections (blue), Random Forest correction (orange). The Western United States UCLA Snow Reanalysis Data is also plotted as an additional data source (green).

Figure 5 File: sw_swe_results
Figure 5: a) Corrected neutron counts for the Sleeping Woman SNOTEL site using RF regression (blue) using the Moise MD Mesonet station data. No CRNS data is available for this site b) SWE calculations using the Desilets (2017) equations for neutron counts based on Desilet (2017) for Random Forest correction (orange). SNOTEL measurements (blue) and the Western United States UCLA Snow Reanalysis Data (green) are also shown. At this site, the RF corrections does not work well.  
