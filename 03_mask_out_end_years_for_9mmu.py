# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 11:59:28 2017

@author: braatenj
"""

import gdal
import numpy as np
import math


def get_dims(fileName):
  src = gdal.Open(fileName)
  ulx, xres, xskew, uly, yskew, yres  = src.GetGeoTransform()
  sizeX = src.RasterXSize
  sizeY = src.RasterYSize
  lrx = ulx + (sizeX * xres)
  lry = uly + (sizeY * yres)
  return [ulx,uly,lrx,lry,xres,-yres,sizeX,sizeY]

def make_geo_trans(fileName, trgtDim):
  src   = gdal.Open(fileName)
  ulx, xres, xskew, uly, yskew, yres  = src.GetGeoTransform()
  return((trgtDim[0], xres, xskew, trgtDim[1], yskew, yres))

def get_intersec(files):
  ulxAll=[]
  ulyAll=[]
  lrxAll=[]
  lryAll=[]
  for fn in files:
    dim = get_dims(fn)
    ulxAll.append(dim[0])
    ulyAll.append(dim[1])
    lrxAll.append(dim[2])
    lryAll.append(dim[3])
  return([max(ulxAll),min(ulyAll),min(lrxAll),max(lryAll)])

def get_offsets(fileName, trgtDim):
  dim = get_dims(fileName)
  xoff = math.floor(abs(dim[0]-trgtDim[0])/dim[4])
  yoff = math.ceil(abs(dim[1]-trgtDim[1])/dim[4])
  xsize = abs(trgtDim[0]-trgtDim[2])/dim[4]
  ysize = abs(trgtDim[1]-trgtDim[3])/dim[4]
  return([int(i) for i in [xoff, yoff, xsize, ysize]])

def get_band(fileName, trgtDim, band):
  offsets = get_offsets(fileName, trgtDim)
  src = gdal.Open(fileName)
  band = src.GetRasterBand(band)
  array = band.ReadAsArray(
            offsets[0],
            offsets[1],
            offsets[2],
            offsets[3])
  return(array)

def write_img(refFileName, trgtDim, outFile):
  outRef = gdal.Open(refFileName)
  nBands = outRef.RasterCount
  dataType = outRef.GetRasterBand(1).DataType
  geoTrans = make_geo_trans(refFileName, trgtDim)
  proj = outRef.GetProjection()
  dims = get_offsets(refFileName, trgtDim)
  driver = gdal.GetDriverByName('ENVI')
  driver.Register()
  outImg = driver.Create(outFile, dims[2], dims[3], nBands, dataType) # file, col, row, nBands, dataTypeCode
  outImg.SetGeoTransform(geoTrans)
  outImg.SetProjection(proj)
  return(outImg)


#############################################################################################################
#############################################################################################################
#############################################################################################################

# inputs
labFile = '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/olym/label_v01_mmu9/nccn_gee_vs_idl_olym_greatest_fast_disturbance_mmu9_tight.bsq'
patchFile = '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/olym/label_v01_mmu9/nccn_gee_vs_idl_olym_greatest_fast_disturbance_mmu9_tight_patchid.bsq'
lastYear = 2011
# mora = 2010
# noca = 2010
# olym = 2011



# get the intersection    
trgtDim = get_intersec([labFile, patchFile])

# load the forest mask image and index the nonForest pixels
labImg = get_band(labFile, trgtDim, 1)

# find background pixels
bckgrnd = np.where(labImg > lastYear)


print(len(bckgrnd[0]))

#labal file
outFile = labFile.replace('.bsq', '_end'+str(lastYear)+'.bsq')
outImg = write_img(labFile, trgtDim, outFile)

for band in range(1,gdal.Open(labFile).RasterCount+1):
  print('  band: '+str(band))
  img = get_band(labFile, trgtDim, band)
  img[bckgrnd] = 0  
  outBand = outImg.GetRasterBand(band) 
  outBand.WriteArray(img)

outImg = None


#patch file
outFile = patchFile.replace('.bsq', '_end'+str(lastYear)+'.bsq')
outImg = write_img(patchFile, trgtDim, outFile)

for band in range(1,gdal.Open(patchFile).RasterCount+1):
  print('  band: '+str(band))
  img = get_band(patchFile, trgtDim, band)
  img[bckgrnd] = 0  
  outBand = outImg.GetRasterBand(band) 
  outBand.WriteArray(img)

outImg = None







