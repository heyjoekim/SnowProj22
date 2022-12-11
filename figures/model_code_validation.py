import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
from sklearn import linear_model
from sklearn.model_selection import train_test_split, cross_val_score, RepeatedKFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.inspection import PartialDependenceDisplay, partial_dependence
from pathlib import Path

# functions -----------------------------------------------------------------
def calcSWE(N, b=0.24):
    # calc SWE using values from Data Process
    N_cal = 5067.011725916952
    N_0 = 7952.389911835688
    N_wat = 0.24*N_0
    lamb = -4.8
    
    swe = lamb*np.log((N-N_wat)/(N_cal-N_wat))
    return(swe)


def calcH(temp, rh):
    # calculate absolute pressure in g/m^-3
    ew = 6.112 * np.exp((17.62*temp)/(243.12+temp))
    K = 216.68
    H = (rh/100) * (ew*K)/(temp+273.16)
    return(H)


def PDPwrapper(regmod, xtrain, i):
    # wrapper for Partial depdendence
    pdp_df = pd.DataFrame()
    dep = partial_dependence(regmod, xtrain, i)
    pdp_df[xtrain.columns[i]] = np.array(dep.get('values')).flatten()
    pdp_df[''.join(['y', str(i)])] = np.array(dep.get('average')).flatten()
    return (pdp_df)


def lmPDP(pdp_df, press_test=False):
    # get x and y values from PDP results
    xmod = pdp_df.iloc[:,0]
    ymod = pdp_df.iloc[:,1]

    # fit constant
    xmod = sm.add_constant(xmod)
    # do OLS regression fit
    if press_test == True:
        model = sm.OLS(np.log(ymod), xmod)
    else:
        model = sm.OLS(ymod, xmod)
    results = model.fit()
    return(results)

# ----------------------------------------------------------------------------------------
    
# RANDOM FOREST REGRESSIONS -----------------------------------------------------------------
# import regression dataframe
crns = pd.read_csv('./data/processed/regression/crns_lm.csv')
crns_swe = pd.read_csv('./data/processed/swe/crns_swe.csv', parse_dates=['UTC'])

# get y-response variable, X-features (T, RH, and P)
features1 = crns[['N_cor [cph]', 'T [degC]', 'RH [%]', 'P [mb]']].copy()
y1 = features1['N_cor [cph]']
X1 = features1.drop('N_cor [cph]', axis=1)

# do a test/train split of 3:7
X_train1, X_test1, y_train1, y_test1 = train_test_split(X1, y1, test_size=0.3, random_state=42)

# fit randomforest
RF1 = RandomForestRegressor(random_state=1)
# fit with training data
RF1.fit(X_train1, y_train1)
# predict with testing data
y_pred1 = RF1.predict(X_test1)
# calc swe
swe1 = calcSWE(y_pred1)

# create second features with P and H (abs. pressure)
features2 = crns[['N_cor [cph]', 'P [mb]', 'H [gm3]']]
y2 = features2['N_cor [cph]']
X2 = features2.drop('N_cor [cph]', axis=1)

# create train/test split
X_train2, X_test2, y_train2, y_test2 = train_test_split(X2,
                                                        y2,
                                                        test_size=0.3,
                                                        random_state=42)

# fit random forest
RF2 = RandomForestRegressor(random_state=1, n_estimators=1000, oob_score=True)
RF2.fit(X_train2, y_train2)
y_pred2 = RF2.predict(X_test2)
swe2 = calcSWE(y_pred2)
# ---------------------------------------------------------------------------------------

# PARTIAL DEPENDENCE ----------------------------------------------------------------
pdp_RF1_T = PDPwrapper(RF1, X_train1, 0)
pdp_RF1_RH = PDPwrapper(RF1, X_train1, 1)
pdp_RF1_P = PDPwrapper(RF1, X_train1, 2)
pdp_RF2_P = PDPwrapper(RF2, X_train2, 0)
pdp_RF2_H = PDPwrapper(RF2, X_train2, 1)

# fit models
mod_RF1_T = lmPDP(pdp_RF1_T)
mod_RF1_RH = lmPDP(pdp_RF1_RH)
mod_RF1_P = lmPDP(pdp_RF1_P, press_test=True)
mod_RF2_P = lmPDP(pdp_RF2_P, press_test=True)
mod_RF2_H = lmPDP(pdp_RF2_H)

# print(mod_RF2_P.summary())
# --------------------------------------------------------------------------------------

# SWE Comparisons ----------------------------------------------------------------------
# read weather data
mda21 = pd.read_csv('./data/processed/meso/mda21.csv', parse_dates=['datetime'])
moc21 = pd.read_csv('./data/processed/meso/moc21.csv', parse_dates=['datetime'])
# read snotel data
sntl_swe = pd.read_csv('./data/processed/swe/sntl_sw21.csv', parse_dates=['Date'])

moc21_features = moc21.drop('datetime', axis=1)
moc21_features['H [gm3]'] = calcH(moc21_features['Air Temp [degC]'], moc21_features['RH [%]'])
moc21_features2 = moc21_features.drop(['Air Temp [degC]', 'RH [%]'], axis=1)
moc21_features = moc21_features.drop('H [gm3]', axis=1)

moc21_features.columns = X_test1.columns
moc21_features2.columns = X_test2.columns
N1 = RF1.predict(moc21_features)
N2 = RF2.predict(moc21_features2)

moc21['N (RF1)'] = N1
moc21['N (RF2)'] = N2
moc21['SWE (RF1)'] = calcSWE(N1)
moc21['SWE (RF2)'] = calcSWE(N2)

mda21_features = mda21.drop('datetime', axis=1)
mda21_features['H [gm3]'] = calcH(mda21_features['Air Temp [degC]'], mda21_features['RH [%]'])
mda21_features2 = mda21_features.drop(['Air Temp [degC]', 'RH [%]'], axis=1)
mda21_features = mda21_features.drop('H [gm3]', axis=1)

mda21_features.columns = X_test1.columns
mda21_features2.columns = X_test2.columns
N1 = RF1.predict(mda21_features)
N2 = RF2.predict(mda21_features2)

mda21['N (RF1)'] = N1
mda21['N (RF2)'] = N2
mda21['SWE (RF1)'] = calcSWE(N1)
mda21['SWE (RF2)'] = calcSWE(N2)