#!/bin/bash

tif=$1
outf=$2

#rm="echo rm"
rm=rm

$rm -f temp1.tif
gdalwarp -s_srs EPSG:2193 -t_srs EPSG:3785 $tif temp1.tif

# Extract the geotif info
listgeo -tfw temp1.tif
listgeo temp1.tif > temp1.mtd

# Create a mask image for the boundary resulting from warping
# First make a white version of the original image

convert -quiet -white-threshold 0% $tif temp1_mask0.tif
if [ -e ${tif%tif}tfw ]; then
   cp ${tif%tif}tfw temp1_mask0.tfw
else
   listgeo -tfw $tif
   mv ${tif%tif}tfw temp1_mask0.tfw
fi
gdalwarp -s_srs EPSG:2193 -t_srs EPSG:3785 temp1_mask0.tif temp1_mask1.tif
convert -quiet -black-threshold 1% temp1_mask1.tif temp1_mask2.tif

# Now make the image transparent in sea areas...

convert -quiet -black-threshold 100% temp1.tif temp1_black.tif
cp temp1_black.tif temp1_mask3.tif
cp temp1.tfw temp1_mask3.tfw
# Paint the islands and coastline onto the image
echo "Painting out coast"
while [ $# -gt 2 ]; do 
    shift
    shpfile=$2
    if [ ! -e $shpfile ]; then
        echo "Shapefile $2 does not exist :-("
    else
    
        echo "Processing $shpfile"
	layer=`basename $shpfile .shp`
        echo gdal_rasterize -burn 255 -l $layer $shpfile temp1_mask3.tif
        gdal_rasterize -burn 255 -l $layer $shpfile temp1_mask3.tif
    fi
done

# Invert the original image, as want it to be transparent where it is currently light
convert -quiet -negate temp1.tif temp1_mask4.tif

# Combine the masks using the minimum value
convert -quiet -evaluate-sequence min temp1_mask2.tif temp1_mask3.tif temp1_mask5.tif
convert -quiet -evaluate-sequence min temp1_mask4.tif temp1_mask5.tif temp1_mask6.tif


# Build a black image with the minimum value as opacity
rm $outf
rm temp1.tif
convert -quiet temp1_black.tif temp1_mask5.tif -compose copy_opacity -composite temp1.tif
geotifcp -g temp1.mtd temp1.tif $outf

$rm temp1_mask0.tif temp1_mask0.tfw temp1_mask1.tif
$rm temp1_mask2.tif temp1_mask3.tif temp1_mask3.tfw temp1_mask4.tif temp1_mask5.tif
$rm temp1_black.tif
$rm temp1.tfw
$rm temp1.mtd
$rm temp1.tif


