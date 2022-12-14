#!/bin/bash

# read and get Western US UCLA Snow Reanalysis
cd ./data/raw_data/snow/ucla_swe
echo "Saving files to ./data/raw_data/snow/ucla_swe"
# Reanalysis for Moccasin -----------------------------------------------------------------------------------------
# get WY 2019
wget --http-user=$1 --http-password=$2 --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --no-check-certificate --auth-no-challenge=on -r --reject "index.html*" -np -e robots=off -nd https://n5eil01u.ecs.nsidc.org/SNOWEX/WUS_UCLA_SR.001/2018.10.01/WUS_UCLA_SR_v01_N47_0W110_0_agg_16_WY2018_19_SWE_SCA_POST.nc
wget --http-user=$1 --http-password=$2 --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --no-check-certificate --auth-no-challenge=on -r --reject "index.html*" -np -e robots=off -nd https://n5eil01u.ecs.nsidc.org/SNOWEX/WUS_UCLA_SR.001/2018.10.01/WUS_UCLA_SR_v01_N47_0W110_0_agg_16_WY2018_19_SWE_SCA_POST.nc.xml
# get WY 2020
wget --http-user=$1 --http-password=$2 --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --no-check-certificate --auth-no-challenge=on -r --reject "index.html*" -np -e robots=off -nd https://n5eil01u.ecs.nsidc.org/SNOWEX/WUS_UCLA_SR.001/2019.10.01/WUS_UCLA_SR_v01_N47_0W110_0_agg_16_WY2019_20_SWE_SCA_POST.nc
wget --http-user=$1 --http-password=$2 --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --no-check-certificate --auth-no-challenge=on -r --reject "index.html*" -np -e robots=off -nd https://n5eil01u.ecs.nsidc.org/SNOWEX/WUS_UCLA_SR.001/2019.10.01/WUS_UCLA_SR_v01_N47_0W110_0_agg_16_WY2019_20_SWE_SCA_POST.nc.xml
# get WTY 2021
wget --http-user=$1 --http-password=$2 --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --no-check-certificate --auth-no-challenge=on -r --reject "index.html*" -np -e robots=off -nd https://n5eil01u.ecs.nsidc.org/SNOWEX/WUS_UCLA_SR.001/2020.10.01/WUS_UCLA_SR_v01_N47_0W110_0_agg_16_WY2020_21_SWE_SCA_POST.nc
wget --http-user=$1 --http-password=$2 --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --no-check-certificate --auth-no-challenge=on -r --reject "index.html*" -np -e robots=off -nd https://n5eil01u.ecs.nsidc.org/SNOWEX/WUS_UCLA_SR.001/2020.10.01/WUS_UCLA_SR_v01_N47_0W110_0_agg_16_WY2020_21_SWE_SCA_POST.nc.xml

# Reanalysis for Moise N/Sleeping Woman -----------------------------------------------------------------------------------------
# get WY 2021
wget --http-user=$1 --http-password=$2 --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --no-check-certificate --auth-no-challenge=on -r --reject "index.html*" -np -e robots=off -nd https://n5eil01u.ecs.nsidc.org/SNOWEX/WUS_UCLA_SR.001/2020.10.01/WUS_UCLA_SR_v01_N47_0W115_0_agg_16_WY2020_21_SWE_SCA_POST.nc
wget --http-user=$1 --http-password=$2 --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --no-check-certificate --auth-no-challenge=on -r --reject "index.html*" -np -e robots=off -nd https://n5eil01u.ecs.nsidc.org/SNOWEX/WUS_UCLA_SR.001/2020.10.01/WUS_UCLA_SR_v01_N47_0W115_0_agg_16_WY2020_21_SWE_SCA_POST.nc.xml

echo "Download Complete"
echo "Heading back to main project dir"
cd ../../../..
