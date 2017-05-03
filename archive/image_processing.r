library(raster)
library(rgdal)

tsa_buffer_file = "/vol/v1/general_files/datasets/spatial_data/landsat_polygons/wrs_buffer.shp"
tsa_no_buf_file = "/vol/v1/general_files/datasets/spatial_data/landsat_polygons/wrs_alb_vor_poly.shp"
outdir = "/vol/v1/general_files/user_files/justin/idl_gee_lt_dif/"
  
readSHP = function(infile){
  return(readOGR(dsn = dirname(tsa_buffer_file), layer=sub(".shp","",basename(tsa_buffer_file))))
}

getTSA = function(shp, type, scene){
  if(type == "buffer"){this = which(shp$WRS_ALB__1 == scene)}
  else if(type == "no_buffer"){this = which(shp$WRS_ALB__1 == scene)}
  return(shp[this,])
}

writeKML = function(shp, outdir, outname){
  shp = spTransform(shp, CRS("+proj=longlat +datum=WGS84"))
  outfile = paste0(outdir,outname,".kml")
  writeOGR(shp, outfile, layer=outname, drive="KML")
}


#047027
shp = readSHP(tsa_buffer_file)
tsa = getTSA(shp, "buffer", "47027")
writeKML(tsa, outdir, "tsa_047027_buffer")


