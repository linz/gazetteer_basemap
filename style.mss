/* Map background */

Map {
  background-color: @map_base;
}
 
/* Background for islands on basemap */

.land_base 
{
  .topo500[zoom<12],
  .topo50[zoom>=12]
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

.snow
{
   polygon-fill: @snow;
   polygon-opacity: 0.5;
}

.contour  
{
  .topo500[zoom>=10][zoom<13],
  .topo50[zoom>=13]
  {
      line-color: @contour;
      line-width: 0.5;
      line-opacity: 0.5;
  }
}

