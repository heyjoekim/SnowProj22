import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import scipy.stats as stats
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
from sklearn import linear_model
from sklearn.model_selection import train_test_split, cross_val_score, RepeatedKFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.inspection import PartialDependenceDisplay, partial_dependence
from pathlib import Path

from model_code_validation import *

# First Figure: Show results of testing datasets -----------------------------------------------------
rmse = np.sqrt(mean_squared_error(y_test2, y_pred2))
oob = RF2.oob_score_
r, p = stats.pearsonr(y_test2, y_pred2)

fig, ax = plt.subplots(1,2, figsize=(10,5))
ax[0].plot(y_test2, y_pred2,'o')
ax[0].set_xlabel('Observed Neutron Counts')
ax[0].set_ylabel('Predicted Neutron Counts')
ax[0].plot(np.arange(4200,5300), np.arange(4200,5300),'k--', alpha=0.6)
ax[0].axis([4200,5300,4200,5300])
ax[1].plot(y_test2, y_test2-y_pred2,'o')
ax[1].hlines(0, 4200,5300, color='k', ls='--')
ax[1].axis([4200,5300,-650,600])
ax[1].set_ylabel('Residuals')
ax[1].set_xlabel('Observed')

ax[0].text(4950,4350,'RMSE = {:.3f}'.format(rmse))
ax[0].text(4950,4300,'OOB = {:.3f}'.format(oob))
ax[0].text(4950,4250,'r = {:.3f}'.format(r))

ax[0].set_title('A) RF Regression Results', loc='left')
ax[1].set_title('B) RF Regression Residuals (OBS-PRED)', loc='left')
plt.tight_layout()
plt.savefig('./figures/rf_results.png', bbox_inches='tight', facecolor='w')
#plt.show()
# ----------------------------------------------------------------------------------------------

# PDP Plots
# read in URANOS model results
mod_h = pd.read_csv('./data/analysis/models/modeled_h.csv')
mod_p = pd.read_csv('./data/analysis/models/modeled_p.csv')
# Figure 2: PDP plot with pressure -------------------------------------------------------------
ps = np.arange(860,885)
ps = sm.add_constant(ps)
ys = mod_RF2_P.predict(ps)

xmod = mod_p['P [mb]'].to_numpy()
xmod = sm.add_constant(xmod)
ymod = mod_p['Epithermal'].to_numpy()
model = sm.OLS(np.log(ymod), xmod)
results = model.fit()
y_uranos = results.predict(xmod)

fig, ax = plt.subplots()
pdp_RF2_P.plot(x='P [mb]', y='y0', marker='o', linestyle='None', ax=ax, legend=False)
ax.plot(ps[:,1], np.exp(ys), 'k--')
ax1 = ax.twinx()
ax1.plot(mod_p['P [mb]'], mod_p['Epithermal'], 'rs', alpha=0.4)
ax1.plot(xmod[:,1], np.exp(y_uranos),'r--')
ax.set_xlabel(r'P [mb]')
ax.set_ylabel('Corrected Neutron Count [cph]', color='tab:blue')
ax1.set_ylabel('Modeled Neutron Count', color='red')
ax1.spines['left'].set_color('tab:blue')
ax.tick_params(axis='y', color='tab:blue', labelcolor='tab:blue')
ax1.spines['right'].set_color('red')
ax1.tick_params(axis='y',color='red', labelcolor='red')
plt.savefig('./figures/pdp_press.png', bbox_inches='tight', facecolor='w')
#plt.show()
# -----------------------------------------------------------------------------------------

# Figure 2: PDP plot with H -------------------------------------------------------------
Hs = np.arange(0,6)
Hs = sm.add_constant(Hs)
ys = mod_RF2_H.predict(Hs)

xmod = mod_h['H'].to_numpy()
xmod = sm.add_constant(xmod)
ymod = mod_h['Epithermal'].to_numpy()
model = sm.OLS(ymod, xmod)
results = model.fit()
y_uranos = results.predict(xmod)

fig, ax = plt.subplots()
pdp_RF2_H.plot(x='H [gm3]', y='y1', marker='o',
               linestyle='None', ax=ax, legend=False)
ax.plot(Hs[:,1], ys,'k--')
ax1 = ax.twinx()
ax1.plot(mod_h['H'], mod_h['Epithermal'], 'rs', alpha=0.4)
ax1.plot(xmod[:,1], y_uranos,'r--')

ax.set_xlabel(r'H [$g/m^3$]')
ax.set_ylabel('Corrected Neutron Count [cph]', color='tab:blue')
ax1.set_ylabel('Modeled Neutron Count', color='red')

ax1.spines['left'].set_color('tab:blue')
ax.tick_params(axis='y', color='tab:blue', labelcolor='tab:blue')
ax1.spines['right'].set_color('red')
ax1.tick_params(axis='y',color='red', labelcolor='red')
plt.savefig('./figures/pdp_humid.png', bbox_inches='tight', facecolor='w')
#plt.show()
# -----------------------------------------------------------------------------------------

# Results -----------------------------------------------------------------------------------
crns_swe.set_index('UTC', inplace=True)
re_swe = pd.read_csv('./data/analysis/swe/re_carc21.csv', parse_dates=['dates'])

fig, ax = plt.subplots(2,1, sharex=True)
crns_daily_avg = crns_swe.resample('D').mean()
crns_daily_avg.plot(y='N_cor [cph]', ax=ax[0], label='Obs')
moc21.plot(x='datetime', y='N (RF2)', ax=ax[0], label='RF')
crns_daily_avg.plot(y='SWE [cm]', ax=ax[1], label='Obs')
moc21.plot(x='datetime', y='SWE (RF2)', ax=ax[1], label='RF')
re_swe.plot(x='dates', y='swe [cm]', ax=ax[1], label='Re-A')
ax[1].set_xlim([datetime.date(2020,11,22), datetime.date(2021,5,8)])
ax[0].set_ylabel('Neutron Counts [cph]')
ax[1].set_ylabel('SWE [cm]')
ax[0].set_xlabel('Time')
ax[0].set_title('A) Neutron Count Comparisons for CARC', loc='left')
ax[1].set_title('B) SWE Comparisons for CARC', loc='left')
ax[0].legend(loc='lower right', frameon=False)
ax[1].legend(frameon=False)
plt.tight_layout()
plt.savefig('./figures/carc_swe_results.png', bbox_inches='tight', facecolor='w')
#plt.show()
# --------------------------------------------------------------------------------

# Results -----------------------------------------------------------------------------------
re_swe = pd.read_csv('./data/analysis/swe/re_sw21.csv', parse_dates=['dates'])

fig, ax = plt.subplots(2,1, sharex=True)
mda21.plot(x='datetime', y='N (RF2)', ax=ax[0], label='RF')
sntl_swe.plot(x='Date', y='WTEQ [cm]', ax=ax[1], label='Obs')
mda21.plot(x='datetime', y='SWE (RF2)', ax=ax[1], label='RF')
re_swe.plot(x='dates', y='swe [cm]', ax=ax[1], label='Re-A')
ax[1].set_xlim([datetime.date(2020,11,22), datetime.date(2021,5,8)])
ax[0].set_ylabel('Neutron Counts [cph]')
ax[1].set_ylabel('SWE [cm]')
ax[0].set_xlabel('Time')
ax[0].set_title('A) Neutron Count Comparisons for Sleeping Woman', loc='left')
ax[1].set_title('B) SWE Comparisons for Sleeping Woman', loc='left')
ax[0].legend(loc='lower right', frameon=False)
ax[1].legend(frameon=False)
plt.tight_layout()
plt.savefig('./figures/sw_swe_results.png', bbox_inches='tight', facecolor='w')
#plt.show()
