# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 12:54:59 2017

@author: braatenj

This script searches through the list of images that
intersect the NCCN parks and pulls out the day of year (DOY)
and makes a list of them. From the list the min and max are
printed and so is a histogram of the DOY distribution.

The min and max are used to define the date range in the
GEE LandTrendr run. We want to have similar starting data for
the comparison of GEE and IDL versions of LandTrendr results

"""

from matplotlib import pyplot as plt

files = [
  '/vol/v1/scenes/045026/targz_files.txt',
  '/vol/v1/scenes/046027/landsat_scenes.txt',
  '/vol/v1/scenes/045027/targz_files.txt',
  '/vol/v1/scenes/045028/targz_files.txt',
  '/vol/v1/scenes/046026/targz_files.txt',
  '/vol/v1/scenes/046027/landsat_scenes.txt',
  '/vol/v1/scenes/046028/landsat_scenes.txt',
  '/vol/v1/scenes/047026/targz_files.txt',
  '/vol/v1/scenes/047027/targz_files.txt',
  '/vol/v1/scenes/047028/targz_files.txt',
  '/vol/v1/scenes/048026/targz_files.txt',
  '/vol/v1/scenes/048027/targz_files.txt'
]

doys = []
years = []
for thisFile in files:

  with open(files[0]) as f:
      lines = f.readlines()

  for line in lines:
    doys.append(int(line[13:16]))
    years.append(int(line[9:13]))

print('min doy : '+ str(min(doys)))
print('max doy : '+ str(max(doys)))
plt.hist(doys)

print('min year : '+ str(min(years)))
print('max year : '+ str(max(years)))
plt.hist(years)

















