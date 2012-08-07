
-- Create a table of town names, joining together those towns with multiple 
-- entries in the geographic_name table.  These are taken to be any points
-- with the same size, code, and name within 20km of each other.
-- This radius is set in the st_buffer line (actually half this distance is
-- set.

drop table if exists town_names;

with t1(name, code, size, geom) as
(select 
   initcap(name),
   desc_code,
   size,
   st_buffer( st_transform(wkb_geometry,2193),10000, 2 )
 from
   geographic_name
 where desc_code in ('SBRB','POPL','TOWN','USAT','METR')
),
t2(name,code,size,geom) as
(select
   name,
   code,
   size,
   st_union(geom)
 from t1
 group by name, code, size
),
t3(name,code,size,geom) as
(select 
   name,
   code,
   size,
   ST_GeometryN(geom,generate_series(1,St_NumGeometries(geom)))
  from t2
  where geometrytype(geom) = 'MULTIPOLYGON'
 ),
t4( name, code, size, geom ) as
(
select 
  name,
  code,
  size,
  st_centroid(geom)
from
  t2
where 
  geometrytype(geom)='POLYGON'
union
select
  name,
  code,
  size,
  st_centroid(geom)
from
  t3
  )
select * into town_names from t4;    

-- Now build the table of map labels

drop table if exists map_labels;

create table map_labels 
(
	label_id serial primary key,
	label varchar(125),
	zoom_level int,
	style varchar(4),
	geom geometry
);
create index idx_map_labels_geom on map_labels using Gist(geom);

insert into map_labels( label, zoom_level, style, geom )
select
  tn.name,
  zl as zoom_level,
  zs.style,
  st_transform(tn.geom,3857)
from 
  generate_series(5,14) as zl,
  town_names tn,
  label_zoom_map zs
where
  tn.code = zs.code and 
  zl >= zs.min_zoom and
  (zs.max_zoom is null or zl <= zs.max_zoom);

