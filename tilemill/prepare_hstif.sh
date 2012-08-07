#!/bin/bash
# Copyright 2012 Crown copyright (c)
#  Land Information New Zealand and the New Zealand Government.
#  All rights reserved
# 
#  This program is released under the terms of the new BSD license. See 
#  the LICENSE file for more information.
#
#===================================================================
#  Script to build a hillshading image file from the source.  The intention of this is
#  to build an image which is black, with the hillshading encoded in the alpha channel, which
#  can then be laid over the basemap.  It isn't working yet!
# 
#  This also converts from the source projection (2193) to 3785

rm="rm -f"
if [ $1 == '-d' ]; then
   rm="echo rm"
   shift
fi

tif=$1
outf=$2


$rm -f hstmp.tif
gdalwarp -s_srs EPSG:2193 -t_srs EPSG:3785 $tif hstmp.tif

# Extract the geotif info
listgeo hstmp.tif > hstmp.mtd

# Create a mask image for the boundary resulting from warping
# First make a white version of the original image

convert -quiet -white-threshold 0% $tif hstmp_mask0.tif
if [ -e ${tif%tif}tfw ]; then
   cp ${tif%tif}tfw hstmp_mask0.tfw
   chmod 644 hstmp_mask0.tfw
else
   cp $tif hstmp_copy.tif
   listgeo -tfw hstmp_copy.tif
   mv hstmp_copy.tfw hstmp_mask0.tfw
   rm -f hstmp_copy.tif
fi
gdalwarp -s_srs EPSG:2193 -t_srs EPSG:3785 hstmp_mask0.tif hstmp_mask1.tif
convert -quiet -black-threshold 1% hstmp_mask1.tif hstmp_mask2.tif

# Now make a mask for the sea areas (black=transparent in the sea areas

convert -quiet -black-threshold 100% hstmp.tif hstmp_mask3.tif
listgeo -tfw hstmp.tif
mv hstmp.tfw hstmp_mask3.tfw
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
        echo gdal_rasterize -burn 255 -l $layer $shpfile hstmp_mask3.tif
        gdal_rasterize -burn 255 -l $layer $shpfile hstmp_mask3.tif
    fi
done

# Invert the original image, as want it to be transparent where it is currently light
convert -quiet -negate hstmp.tif hstmp_mask4.tif

# Combine the masks using the minimum value
convert -quiet -evaluate-sequence min hstmp_mask2.tif hstmp_mask3.tif hstmp_mask5.tif
convert -quiet -evaluate-sequence min hstmp_mask4.tif hstmp_mask5.tif hstmp_mask6.tif


# Build a black image with the minimum value as opacity
# Idiosyncrasy in ImageMagick?  Seems to work if I build a png then convert to TIF,
# but not if I build a TIF directly

convert -quiet -colorspace Gray hstmp_mask6.tif hstmp_mask6.png
convert -quiet -black-threshold 100% hstmp.tif hstmp_black.png
convert hstmp_black.png hstmp_mask6.png -compose copy_opacity -composite hstmp_final.png
convert hstmp_final.png hstmp_final.tif

rm $outf
geotifcp -g hstmp.mtd hstmp_final.tif $outf

$rm hstmp_mask*.tif
$rm hstmp_black.png
$rm hstmp_mask6.png
$rm hstmp_final.png
$rm hstmp_final.tif
$rm hstmp.tif
$rm hstmp_mask0.tfw
$rm hstmp_mask3.tfw
$rm hstmp.mtd
