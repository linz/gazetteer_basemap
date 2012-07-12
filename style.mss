/* Map background */

Map {
  background-color: @map_base;
}
 
/* Background for islands on basemap */

.land_base 
{
  .topo500[zoom<13],
  .topo50[zoom>=13]
   {
   polygon-fill: @land_base;
   line-color: @land_base;
   line-width: 0.5;
   }
}

.coastline
{
  .topo500[zoom<13],
  .topo50[zoom>=13]
   {
   line-color: @dark_water;
   line-width: 0.5;
   }
}

/* Currently only using topo250 hill shading ... */

.hillshade
{
   .topo250 {raster-opacity:0.1;}
}

/* Vegetation layers */

.vege {
  .exotic.topo50[zoom>=13],
  .exotic.topo250[zoom<13] 
  {
  polygon-fill: @exotic;
  }
  .native.topo50[zoom>=13],
  .native.topo250[zoom<13] 
  {
  polygon-fill: @native;
  }
}

/*
#topo500_snow {polygon-fill: #ffffff;
polygon-opacity: 0.75;}

 #topo50_hillshade_raster {raster-opacity:0.1;}


#topo50_building_poly[zoom>=13] {
  building-fill: @dark_grey;}

#topo50_residential[zoom>=13] {
  polygon-fill: @residential;}
#topo500_residential[zoom<13] {
  line-color: @dark_grey;
  line-width: 1;
  polygon-fill: @residential;
polygon-opacity: 0.75;}


.elevation  {line-color: @contours;}
.topo50_contour
{ [zoom<13] {  line-width: 0; }
  [zoom>=13] {  line-width: 0.5; } }

#topo500_contours 
{ [zoom>13] {  line-width: 0; }  
[zoom<13] {  line-width: 0.5; }
[zoom<10] {  line-width: 0; }}




#topo50_primary_parcels { [zoom>=12]{
  polygon-fill: rgba(128,128,128,0);
  line-width:0.5;
line-color:rgba(128,128,128,0.5)}}

#topo50_railway_cl { 
  [zoom>=13] { line-color: #000000; line-width: 2;}
  [zoom>10] { line-color: #000000; line-width: 1;}
  [zoom<=10] { line-color: #000000; line-width: 0.5;}
  }
 



#topo50_shelterbelt {[zoom>=13]{
  line-color: @native;
  line-width: 1;}
  }


#topo50_fence_cl { [zoom>=13]{
  line-color: #000000;
  line-width: 0.5;
  }}


#topo50_racetrack[zoom>=13] {polygon-fill: @light_grey;}

#topo50_airport[zoom>=13] {polygon-fill: @light_grey;}

#topo50_runway[zoom>=13] {polygon-fill: @dark_grey;}

*/


