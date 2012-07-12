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

#topo500_snow {polygon-fill: #ffffff;
polygon-opacity: 0.75;}


.elevation  {line-color: @contours;}
.topo50_contour
{ [zoom<13] {  line-width: 0; }
  [zoom>=13] {  line-width: 0.5; } }

#topo500_contours 
{ [zoom>13] {  line-width: 0; }  
[zoom<13] {  line-width: 0.5; }
[zoom<10] {  line-width: 0; }}



#topo50_shelterbelt {[zoom>=13]{
  line-color: @native;
  line-width: 1;}
  }


#topo50_fence_cl { [zoom>=13]{
  line-color: #000000;
  line-width: 0.5;
  }}

