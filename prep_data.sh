#!/bin/sh

# Clear out existing data
rm -rf data/*

# Copy data from source folders, converting coordsys to EPSG:900913

src=/usr/local/data

echo "Compiling basemap data set" > prep_data.log

for series in topo50 topo250 topo500; do
mkdir data/$series
for f in $src/$series/*.shp; do
   echo "Processing $f"
   echo "Processing $f" >> prep_data.log
   tf="data/$series/"`basename $f .shp`"_gm.shp"
   ogr2ogr -t_srs EPSG:900913 $tf $f >> prep_data.log 2>&1
   echo "Indexing $tf" >> prep_data.log
   shapeindex $tf >> prep_data.log 2>&1
done;
echo "Compiling $series/coastline polygons"
echo "Compiling $series/coastline polygons" >> prep_data.log
python makepoly.py data/$series/coastline_gm.shp data/$series/coastline_poly_gm.shp >> prep_data.log 2>&1
 
shapeindex data/$series/coastline_poly_gm.shp
done;


