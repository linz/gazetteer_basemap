#!/bin/sh
#
# Script executes steps required to build the data supporting the WFS layer
# of geographic names for 

dbname=ccrook
host=/var/run/postgresql
geonameshp=geographic_name.shp

# Load the geographic names layer into the database

echo "Loading geographic_name layer from $geonameshp"

psql --host=${host} --dbname=${dbname} --command="drop table if exists geographic_name"
ogr2ogr -f PostgreSQL PG:"dbname=${dbname} host=${host}" ${geonameshp}

# Load the definition which labels to generate at each zoom scale...

echo "Loading mapping of names to zoom levels and styles"

psql --host=${host} --dbname=${dbname} <<END_PSQL
drop table if exists label_zoom_map;
create table label_zoom_map( code varchar(4), min_zoom int, max_zoom int, style varchar(4));
\copy label_zoom_map from label_zoom_map.csv csv header;
END_PSQL

# Run the script to generate the map labels

echo "Generating the map labels"

psql --host=${host} --dbname=${dbname} --file=create_map_labels.sql

# Dump and zip the map labels

echo "Dumping the map labels"

rm -f map_labels.zip map_labels.dump

pg_dump --host=${host} --encoding=utf8 --format=custom --no-acl --file=map_labels.dump --table=map_labels ${dbname}

zip -m map_labels.zip map_labels.dump

