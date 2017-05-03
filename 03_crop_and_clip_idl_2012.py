# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 14:55:01 2017

@author: braatenj
"""

import gdal
import subprocess
from glob import glob
import os


def get_dims(fileName):
  src = gdal.Open(fileName)
  ulx, xres, xskew, uly, yskew, yres  = src.GetGeoTransform()
  sizeX = src.RasterXSize
  sizeY = src.RasterYSize
  lrx = ulx + (sizeX * xres)
  lry = uly + (sizeY * yres)
  return [ulx,uly,lrx,lry,xres,-yres,sizeX,sizeY]


vrtFile = '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/idl_2012_vrt/idl_2012_greatest_fast_dist_mmu11.vrt'
boundsFile = '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/mora/nccn_gee_vs_idl_mora_ftv_nbr.bsq'
clipFile = '/vol/v1/proj/nccn/gee_idl_lt_compare/vector/LPa01_LEWI_MORA_NOCA_OLYM.geojson'
outFile = '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/idl_2012_vrt/idl_2012_greatest_fast_dist_mmu11_mora.bsq'

dims = get_dims(boundsFile)
projwin = "{0} {1} {2} {3}".format(dims[0],dims[1],dims[2],dims[3]);
ext = "{0} {3} {2} {1}".format(dims[0],dims[1],dims[2],dims[3]);

tempFile = outFile.replace('.bsq', '_temp.bsq')
cmdTrans = 'gdal_translate -q --config GDAL_DATA "/usr/lib/anaconda/share/gdal" -of ENVI -projwin '+projwin+' '+ vrtFile + ' ' + tempFile    
cmdWarp = 'gdalwarp -of ENVI -dstnodata None -q -tr 30 30 -cutline '+clipFile+' -te '+ ext+' '+tempFile+' '+outFile

subprocess.call(cmdTrans, shell=True)
subprocess.call(cmdWarp, shell=True)

delete = glob(os.path.dirname(outFile)+'/*temp*')
if len(delete) != 0:
  for this in delete:  
    os.remove(this)
  

