#!/bin/sh

tif=$1
outf=$2

gdalwarp -s_srs EPSG:2193 -t_srs EPSG:3785 $tif temp1.tif

# Extract the geotif info
listgeo -tfw temp1.tif

# Create a mask image for the boundary resulting from warping
# First make a white version of the original image
convert -quiet -white-threshold 0% $tif temp1_mask.tif
if [ -e ${tif%tif}tfw ]; then
   cp ${tif%tif}tfw temp1_mask.tfw
else
   listgeo -tfw $tif
   mv ${tif%tif}tfw temp1_mask.tfw
fi
gdalwarp -s_srs EPSG:2193 -t_srs EPSG:3785 temp1_mask.tif temp1_mask1.tif
convert -quiet -black-threshold 1% temp1_mask1.tif temp1_mask2.tif
rm temp1_mask.tif temp1_mask.tfw temp1_mask1.tif

# Now make the image transparent in sea areas...

convert -quiet -black-threshold 100% temp1.tif temp1_mask3.tif
cp temp1.tfw temp1_mask3.tfw
# Paint the islands and coastline onto the image
echo "Painting out coast"
while [ $# -ge 2 ]; do 
    shift
    if [ ! -e $2 ]; then
        echo "Shapefile $2 does not exist :-("
    else
    
        echo "Processing $2"
	layer=`basename $2 .shp`
        gdal_rasterize -burn 255 -l $layer $2 temp1_mask3.tif
    fi
done
convert -quiet -evaluate-sequence min temp2_mask2.tif temp1_mask3.tif temp1_mask4.tif
rm temp1_mask1.tif temp1_mask2.tif

convert -quiet temp2.tif temp1_mask4.tif -compose copy_opacity -composite $outf
mv temp1.tfw ${outf%tif}tfw
rm temp1_mask4.tif


