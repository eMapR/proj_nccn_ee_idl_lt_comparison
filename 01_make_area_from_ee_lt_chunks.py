
import os
import fnmatch
import json
import sys
import subprocess
import multiprocessing



def run_cmd(cmd):
  print(cmd)  
  return subprocess.call(cmd, shell=True)

def get_bounds(coords):
  x = []
  y = []  
  for coord in coords:
    x.append(coord[0])
    y.append(coord[1])
  return [min(x), max(y), max(x), min(y)]



"""
# get the arguments
arg = sys.argv
chunkDir = arg[1]
outDir = arg[2]  
clipFile = arg[3]
clipFeature = arg[4]
name = arg[5]  
indexID = arg[6]
nVert = int(arg[7])
startYear = int(arg[8])
endYear = int(arg[9])
proj = arg[10]
delete = arg[11]
"""

chunkDir = '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/noca'
outDir = '/vol/v1/proj/nccn/gee_idl_lt_compare/raster/noca' 
clipFile = '/vol/v1/proj/nccn/gee_idl_lt_compare/vector/LPa01_LEWI_MORA_NOCA_OLYM.geojson'
clipAttribute = 'PARK_CODE'
clipFeature = 'NOCA'
name = 'nccn_gee_vs_idl_noca' 
indexID = 'nbr'
nVert = 7
startYear = 1984
endYear = 2012
proj = 'EPSG:5070'
delete = 'keep'


# make sure path parts are right
if chunkDir[-1] != '/':
  chunkDir += '/'
if outDir[-1] != '/':
  outDir += '/'


# find the tif chunks
tifs = []
for root, dirnames, filenames in os.walk(chunkDir):
  for filename in fnmatch.filter(filenames, '*.tif'):
    tifs.append(os.path.join(root, filename))
    
    
# make a list of tile tifs
vrtFile = chunkDir+name+'.vrt'
tileListFile = vrtFile.replace('.vrt', '_filelist.txt')
tileList = open(tileListFile, 'w')
for tif in tifs:
  tileList.write(tif+'\n')
tileList.close()


# create vrt
cmd = 'gdalbuildvrt -input_file_list '+tileListFile+' '+vrtFile
subprocess.call(cmd, shell=True)


# define the list of replacement types in the new out images    
outTypes = ['vert_yrs.bsq',
            'vert_src.bsq',
            'vert_fit.bsq',
            'ftv_'+indexID+'.bsq',            
            'ftv_tcb.bsq',
            'ftv_tcg.bsq',
            'ftv_tcw.bsq']

# make a list of band ranges for each out type
vertStops = []
for vertType in range(4):  
  vertStops.append(vertType*nVert+1)

nYears = (endYear - startYear) + 1
ftvStops = []  
for ftvType in range(1,5):  
  ftvStops.append(ftvType*nYears+vertStops[-1])
  
bandStops = vertStops+ftvStops
bandRanges = [range(bandStops[i],bandStops[i+1]) for i in range(len(bandStops)-1)]


# load the tile features
with open(clipFile) as f:
  features = json.load(f)

coords = []
for i in range(len(features['features'])):
  if features['features'][i]['properties'][clipAttribute] == clipFeature:
    coords = coords+features['features'][i]['geometry']['coordinates'][0]



#features['features'][1]['properties']['PARK_CODE'] == 'LEWI'
bounds = get_bounds(coords)
projwin = ' '.join([str(coord) for coord in bounds])
 
# make a list of all the gdal_translate commands needed for the ee conus chunk
cmdList = []
if not os.path.isdir(outDir):
  os.mkdir(outDir)

for i in range(len(outTypes)):
  outFile = outDir+name+'_'+outTypes[i]
  bands = ' -b '+' -b '.join([str(band) for band in bandRanges[i]])
  cmd = 'gdal_translate -q --config GDAL_DATA "/usr/lib/anaconda/share/gdal" -of ENVI -a_srs ' + proj + bands + ' -projwin '+projwin+' '+ vrtFile + ' ' + outFile    
  cmdList.append(cmd)  

# run the commands in parallel 
pool = multiprocessing.Pool(processes=len(cmdList))
pool.map(run_cmd, cmdList)  
pool.close()



