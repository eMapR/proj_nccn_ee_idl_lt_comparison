# -*- coding: utf-8 -*-
"""
Created on Tue May  2 20:09:05 2017

@author: braatenj
"""

import gdal
import numpy as np

imgFile = ['/vol/v1/proj/nccn/gee_idl_lt_compare/raster/gee_lt_9mmu_end_match_nccn_idl/ee_nccn_gee_vs_idl_lewi_greatest_fast_disturbance_mmu9_tight_patchid_end2012.bsq',
           '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/gee_lt_9mmu_end_match_nccn_idl/ee_nccn_gee_vs_idl_olym_greatest_fast_disturbance_mmu9_tight_patchid_end2011.bsq',
           '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/gee_lt_9mmu_end_match_nccn_idl/ee_nccn_gee_vs_idl_noca_greatest_fast_disturbance_mmu9_tight_patchid_end2010.bsq',
           '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/gee_lt_9mmu_end_match_nccn_idl/ee_nccn_gee_vs_idl_mora_greatest_fast_disturbance_mmu9_tight_patchid_end2010.bsq']

parks = ['lewi',
         'olym',
         'noca',
         'mora']


# these are patch numbers provided by Natasha based on the IDL version 2010-2012         
idlPatches = [3253,
              24739,
              13687,
              7498]
         
for i in range(len(parks)):         
  src = gdal.Open(imgFile[i])
  band = src.GetRasterBand(1)
  array = band.ReadAsArray()
  uni = np.unique(array)
  print(parks[i]+' n patches ee: '+str(len(uni)-1))
  print(parks[i]+' n patches idl: '+str(idlPatches[i]))
  print(parks[i]+' ratio ee to idl: '+str((len(uni)-1)/(idlPatches[i]+0.0)))
  print('')
  print('')
