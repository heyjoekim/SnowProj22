import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import netCDF4 as nc
import datetime
from pathlib import Path

# important Constants
# location of CARC and rough location of Mocassin Mesonet
CARC_lat = 47.059422
CARC_lon = -109.955567

# location of Moiese N Mesonet
moiese_lat = 47.42
moiese_lon = -114.26

# location of Sleeping Woman
sw_sntl_lat = 47.183333
sw_sntl_lon = -114.333333

# Functions
def read_SNOTEL(f):
    # Read in Sleeping Woman Snotel Data
    sntl = pd.read_csv(f, skiprows=3, parse_dates=['Date'], na_values=-99.9)
    # drop unused column
    sntl.drop(['Unnamed: 10'], axis=1, inplace=True)
    # drop values after Jun 1
    sntl = sntl[~(sntl['Date']>'2021-06-01')]
    # convert swe from in to cm
    sntl['WTEQ (cm)'] = sntl['WTEQ.I-1 (in) ']*2.54
    # return only useful data
    sntl_df = sntl[['Date', 'WTEQ (cm)', 'TOBS.I-1 (degC) ']].copy()
    sntl_df.columns = ['Date', 'WTEQ [cm]', 'TOBS [degC]']
    return(sntl_df)


def read_MESONET(f):
    meso = pd.read_csv('./data/mesonet/MT_Mesonet_WY19_moccasin_daily_data.csv',
                      parse_dates=['datetime'])
    # Change columns names for easier typing
    meso.columns = ['station_key',
                    'datetime',
                    'Air Temp [degC]',
                    'Atmospheric Pressure [kPa]',
                    'RH [%]']
    meso['Pressure [hPa]'] = meso['Atmospheric Pressure [kPa]']*10
    return(meso[['datetime', 'Air Temp [degC]', 'RH [%]', 'Pressure [hPa]']])

def read_Reanalysis(f, dates, target_lat, target_lon):
    # read in reanalysis dataset and get swe in cm
    # read in file
    re = nc.Dataset(f)
    # get lat, lon, swe
    lat = re.variables['Latitude'][:]
    lon = re.variables['Longitude'][:]
    swe_array = re.variables['SWE_Post'][:,:,:,:]
    
    # get index of location from target_lat and target_lon
    m = int(np.floor((lat[0]-target_lat)/0.0044441223))
    n = int(np.floor((lon[0]-target_lon)/-0.004447937))
    
    # extract swe and swe_sd
    # order is ensemble (0)swe, (1)sd, (2)median, (3)25% and (4)75%
    swe = swe_array[:,0,n,m]
    swe_sd = swe_array[:,1,n,m]
    
    # save DataFrame
    df = pd.DataFrame({'dates':dates,
                        'swe [cm]':swe*100,
                        'swe_sd [cm]':swe_sd*100})
    df.set_index('dates', inplace=True)
    return(df)

# Data Processing 
# 1: CRNS Processing ------------------------------------------------------------
print('Starting Processing on CRNS data')
# Read in CRNS data
crns_dat = pd.read_csv('./data/crns/CRNS_CARC_MT_20210601.txt',
       header=1,
       parse_dates=[0,14])

crns_dat[' N1 [cph]'] = crns_dat[' N1 [cph]'].where(crns_dat[' N1 [cph]']>2000, np.NaN)
crns_dat[' T7 [C]'] = crns_dat[' T7 [C]'].where(crns_dat[' T7 [C]']>-60, np.NaN)
crns_dat[' H7 [%]'] = crns_dat[' H7 [%]'].where(crns_dat[' H7 [%]']<=100, np.NaN)

# Calculate Correction Factors
# counting rates (Raw, uncorrected)
N_raw = crns_dat[' N1 [cph]']
# F BAR
# constants
beta = 0.0077
# get pressures
p = crns_dat[' P4 [mb]']
p0 = np.nanmean(p)

f_bar = np.exp(beta*(p-p0))

# F SOL
f_sol = crns_dat[' fsol']

# F HUM
temp = crns_dat[' T7 [C]']
rh = crns_dat [' H7 [%]']

ew = 6.112 * np.exp((17.62*temp)/(243.12+temp))
K = 216.68
H = (rh/100) * (ew*K)/(temp+273.16)
f_hum = 1 + (0.0054*H)

# total correction factor
F_t = f_bar*f_sol*f_hum

# calculate N
crns_dat['N_cor [cph]'] = crns_dat[' N1 [cph]']*F_t
#calibration
cal_start = pd.Timestamp('2021-05-06T09', tz='MST').astimezone('UTC').to_datetime64()
cal_end = pd.Timestamp('2021-05-06T17', tz='MST').astimezone('UTC').to_datetime64()

N_cal = crns_dat[(crns_dat['UTC']>cal_start) & (crns_dat['UTC']<cal_end)]['N_cor [cph]'].mean()

# theoretical counting
theta_g = 0.167
rho = 1.136
a0 = 0.0808
a1 = 0.3720
a2 = 0.1150

N_0 = N_cal / ((a0/(theta_g*rho+a2))+a1)

N_wat = 0.24*N_0
lamb = -4.8

crns_dat['SWE [cm]'] = lamb*np.log((crns_dat['N_cor [cph]']-N_wat)/(N_cal-N_wat))
# create DataFrame for Regression
print('Saving data file for regression model to ./data/processed/')
crns_lm_dat = crns_dat[['N_cor [cph]', ' T7 [C]', ' H7 [%]', ' P4 [mb]']]
crns_lm_dat.columns = ['N_cor [cph]', 'T [degC]', 'RH [%]', 'P [mb]']
crns_lm_dat = crns_lm_dat.dropna(how='any').reset_index(drop=True)
print('Saved')
# save df
fpath = Path('./data/processed/regression/crns_lm.csv')
fpath.parent.mkdir(parents=True, exist_ok=True)
crns_lm_dat.to_csv(fpath, index=False)
# CRNS SWE and N counts
print('Saving data file for CRNS swe to ./data/processed/')
crns_swe_df = crns_dat[['UTC', 'N_cor [cph]', 'SWE [cm]']]
# save df
fpath = Path('./data/processed/swe/crns_swe.csv')
fpath.parent.mkdir(parents=True, exist_ok=True)
crns_swe_df.to_csv(fpath, index=False)
print('Saved')
# # Create Daily dataset
# crns.set_index('UTC', inplace=True)
# crns_daily = crns.resample('D').mean()
print('Finished CRNS Processing')
# ------------------------------------------------------------------------------

# MESONET Processing -----------------------------------------------------------
print('Starting Processing on Mesonet Data')
# Read in Mesonet for Mocassin for WY 2019, 2020, and 2021
moc19 = read_MESONET('./data/mesonet/MT_Mesonet_WY19_moccasin_daily_data.csv')
moc20 = read_MESONET('./data/mesonet/MT_Mesonet_WY20_moccasin_daily_data.csv')
moc21 = read_MESONET('./data/mesonet/MT_Mesonet_WY21_moccasin_daily_data.csv')

# save df
fpath = Path('./data/processed/meso/moc19.csv')
fpath.parent.mkdir(parents=True, exist_ok=True)
moc19.to_csv(fpath, index=False)
# save df
fpath = Path('./data/processed/meso/moc20.csv')
fpath.parent.mkdir(parents=True, exist_ok=True)
moc20.to_csv(fpath, index=False)
# save df
fpath = Path('./data/processed/meso/moc21.csv')
fpath.parent.mkdir(parents=True, exist_ok=True)
moc21.to_csv(fpath, index=False)


# Read in Mesonet for Mocassin for WY 2021
mda21 = read_MESONET('./data/mesonet/MT_Mesonet_WY21_mdamoies_daily_data.csv')
# save df
fpath = Path('./data/processed/meso/mda21.csv')
fpath.parent.mkdir(parents=True, exist_ok=True)
mda21.to_csv(fpath, index=False)
print('Finished Mesonet Processing')
# ------------------------------------------------------------------------------

# SNOTEL Processing -------------------------------------------------------------
print('Starting Processing on SNOTEL Data')
f='./data/snow/snotel/783_STAND_WATERYEAR=2021.csv'
sw21 = read_SNOTEL(f)
# f='./data/snow/snotel/783_STAND_WATERYEAR=2022.csv'
# sw22 = read_SNOTEL(f)
# save df
fpath = Path('./data/processed/swe/sntl_sw21.csv')
fpath.parent.mkdir(parents=True, exist_ok=True)
sw21.to_csv(fpath, index=False)
print('Finished SNOTEL Processing')
# -------------------------------------------------------------------------------

# WUS_UCLA_SR Processing --------------------------------------------------------------
print('Starting Processing on Snow Reanalysis Data')
dates_wy19 = pd.date_range(start='2018-10-01', end='2019-09-30')
dates_wy20 = pd.date_range(start='2019-10-01', end='2020-09-30')
dates_wy21 = pd.date_range(start='2020-10-01', end='2021-09-30')

f = './data/snow/ucla_swe/WUS_UCLA_SR_v01_N47_0W110_0_agg_16_WY2018_19_SWE_SCA_POST.nc'
CARC_re_19 = read_Reanalysis(f, dates_wy19, CARC_lat, CARC_lon)
f = './data/snow/ucla_swe/WUS_UCLA_SR_v01_N47_0W110_0_agg_16_WY2019_20_SWE_SCA_POST.nc'
CARC_re_20 = read_Reanalysis(f, dates_wy20, CARC_lat, CARC_lon)
f = './data/snow/ucla_swe/WUS_UCLA_SR_v01_N47_0W110_0_agg_16_WY2020_21_SWE_SCA_POST.nc'
CARC_re_21 = read_Reanalysis(f, dates_wy21, CARC_lat, CARC_lon)
f = './data/snow/ucla_swe/WUS_UCLA_SR_v01_N47_0W115_0_agg_16_WY2020_21_SWE_SCA_POST.nc'
SW_re_21 = read_Reanalysis(f, dates_wy21, sw_sntl_lat, sw_sntl_lon)

# correct date ranges
# WY2021 CARC lines up with CRNS dates
CARC_re_21 = CARC_re_21.iloc[52:244]
# save df
fpath = Path('./data/processed/swe/re_carc21.csv')
fpath.parent.mkdir(parents=True, exist_ok=True)
CARC_re_21.to_csv(fpath, index=False)

# all others go from Oct 1 to Jun 1
CARC_re_19 = CARC_re_19.iloc[0:244]
# save df
fpath = Path('./data/processed/swe/re_carc19.csv')
fpath.parent.mkdir(parents=True, exist_ok=True)
CARC_re_19.to_csv(fpath, index=False)

CARC_re_20 = CARC_re_20.iloc[0:244]
# save df
fpath = Path('./data/processed/swe/re_carc20.csv')
fpath.parent.mkdir(parents=True, exist_ok=True)
CARC_re_20.to_csv(fpath, index=False)

SW_re_21 = SW_re_21.iloc[0:244]
# save df
fpath = Path('./data/processed/swe/re_sw21.csv')
fpath.parent.mkdir(parents=True, exist_ok=True)
SW_re_21.to_csv(fpath, index=False)
print('Finished Snow Reanalysis Processing')
# ----------------------------------------------------------------------------------------