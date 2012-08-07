#!/bin/sh
#
# Script executes steps required to build the data supporting the WFS layer
# of geographic names for 

dbname=ccrook
host=/var/run/postgresql
tddxml=tdd-4.2.xml

# Load the geographic names layer into the database

echo "Loading point codes from $tddxml"

python get_codes.py $tddxml pointcodes.csv

# Load the definition which labels to generate at each zoom scale...

echo "Loading point codes into database"

psql --host=${host} --dbname=${dbname} <<END_PSQL
drop table if exists pointcodes;
create table pointcodes(code varchar(10) primary key, value text );
\copy pointcodes from pointcodes.csv csv header;
END_PSQL
