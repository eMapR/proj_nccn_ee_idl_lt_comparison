# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 13:38:56 2017

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

def write_img(outFile, refImg, trgtDim, nBands, dataType):
  convertDT = {
    'uint8': 1,
    'int8': 1,
    'uint16': 2,
    'int16': 3,
    'uint32': 4,
    'int32': 5,
    'float32': 6,
    'float64': 7,
    'complex64': 10,
    'complex128': 11
  }
  dataType = convertDT[dataType]
  geoTrans = make_geo_trans(refImg, trgtDim)
  proj = gdal.Open(refImg).GetProjection()
  dims = get_offsets(refImg, trgtDim)
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
park = 'mora'
eeVert =   '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/'+park+'/label_v01/nccn_gee_vs_idl_'+park+'_greatest_fast_disturbance_mmu11_tight.bsq'
maskFile = '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/'+park+'/label_v01/nccn_gee_vs_idl_'+park+'_greatest_fast_disturbance_mmu11_tight_nodata.bsq'
idlVert =  '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/idl_2012_vrt/idl_2012_greatest_fast_dist_mmu11_'+park+'.bsq'

# '/vol/v1/general_files/datasets/spatial_data/forestmask/final/forestNonForestmask_WAORCA.bsq'

# get the intersection    
trgtDim = get_intersec([eeVert, idlVert])

# load the YOD
eeYOD = get_band(eeVert, trgtDim, 1)
idlYOD = get_band(idlVert, trgtDim, 1)
mask = get_band(maskFile, trgtDim, 1)

# load the aoi image and index the outOfBounds pixels
dif = eeYOD - idlYOD
difClass = np.copy(dif)
same = np.where((dif == 0) & (mask != -9999))
eeGreater = np.where((dif > 0) & (dif < 100) & (mask != -9999))
eeLess = np.where((dif < 0) & (dif > -100) & (mask != -9999))
eeNew = np.where((dif > 1900) & (mask != -9999))
eeMissing = np.where((dif < -1900) & (mask != -9999))

difClass[same] = 0
difClass[eeGreater] = 1
difClass[eeLess] = -1
difClass[eeNew] = 2
difClass[eeMissing] = -2

areaLU = {
  'mora': 3849615839.81,
  'lewi': 125183017.544 + 583819097.942,
  'olym': 11476232307.7,
  'noca': 10438479217.3
}

nLocAgree = sum([len(same[0]),len(eeGreater[0]),len(eeLess[0])])
YODagree = round((len(same[0])/float(nLocAgree))*100, 2)
YODlater = round((len(eeGreater[0])/float(nLocAgree))*100, 2)
YODearlier = round((len(eeLess[0])/float(nLocAgree))*100, 2)


print('% of park pixels where EE LT DIST same location: '+str(round(((nLocAgree*900.0)/areaLU[park])*100, 2)))
print('% of same DIST location where YOD same: '+str(YODagree))
print('% of same DIST location where EE YOD later: '+str(YODlater))
print('% of same DIST location where EE YOD earlier: '+str(YODearlier))
print('% of same DIST location where EE YOD later | mean dif: '+str(round(np.mean(dif[eeGreater]), 2)))
print('% of same DIST location where EE YOD earlier | mean dif: '+str(round(np.mean(dif[eeLess]), 2)))
print('% of park pixels where EE DIST added: '+str(round(((len(eeNew[0])*900.0)/areaLU[park])*100, 2)))
print('% of park pixels where EE DIST missing: '+str(round(((len(eeMissing[0])*900.0)/areaLU[park])*100, 2)))




eeMAG = get_band(eeVert, trgtDim, 2)
idlMAG = get_band(idlVert, trgtDim, 2)

goods = np.where((dif == 0) & (eeYOD > 1900) & (mask != -9999))

#plt.hexbin(eeMAG[goods], idlMAG[goods])
print('Magnitude correlation: '+ str(round(np.corrcoef(eeMAG[goods], idlMAG[goods])[0,1], 2)))

eeDUR = get_band(eeVert, trgtDim, 3)
idlDUR = get_band(idlVert, trgtDim, 3)

#plt.hexbin(eeDUR[goods], idlDUR[goods])
print('Duration correlation: '+ str(round(np.corrcoef(eeDUR[goods], idlDUR[goods])[0,1], 2)))

outFile = eeVert.replace('.bsq','_yod_dif.bsq')
outImg = write_img(outFile, eeVert, trgtDim, 1, 'int16')
outBand = outImg.GetRasterBand(1) 
outBand.WriteArray(difClass)
outImg = None





