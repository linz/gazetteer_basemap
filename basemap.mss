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
   line-width: 0.0;
   }
}

.land_160
{
    polygon-fill: @land_160;
    line-color: @land_160;
    line-width: 0.0;
}

.land_300
{
    polygon-fill: @land_300;
    line-color: @land_300;
    line-width: 0.0;
}

.land_600
{
    polygon-fill: @land_600;
    line-color: @land_600;
    line-width: 0;
}

.land_900
{
    polygon-fill: @land_900;
    line-color: @land_900;
    line-width: 0.0;
}

.land_1200
{
    polygon-fill: @land_1200;
    line-color: @land_1200;
    line-width: 0.0;
}

.land_1800
{
    polygon-fill: @land_1800;
    line-color: @land_1800;
    line-width: 0.0;
}

.land_2100
{
    polygon-fill: @land_2100;
    line-color: @land_2100;
    line-width: 0.0;
}

.land_2400
{
    polygon-fill: @land_2400;
    line-color: @land_2400;
    line-width: 0.0;
}

.coastline
{
  .topo500[zoom<12],
  .topo50[zoom>=12]
   {
   line-color: @dark_water;
   line-width: 0.5;
   }
  .topo500[zoom<7]
   {
   line-width: 0.25;
   }
}

.wateredge.sand
{
   .topo50[zoom>=12]
   {
   polygon-fill: @sand;
   }
}

.wateredge.mud
{
   .topo50[zoom>=12]
   {
   polygon-fill: @mud;
   }
}

.wateredge.shingle
{
   .topo50[zoom>=12]
   {
   polygon-fill: @shingle;
   }
}

.rock
{
   .topo50[zoom>=12]
   {
   polygon-fill: @rock;
   }
}

/* Hillshading currently not working  */

.hillshade
{
   .topo250[zoom>4] 
    {
        raster-opacity: 1.0;
    }
}

/* Vegetation layers */

.vege {
  .exotic.topo50[zoom>=12],
  .exotic.topo250[zoom<12] 
  {
  polygon-fill: @exotic;
  polygon-opacity: 0.3;
  }
  .native.topo50[zoom>=12],
  .native.topo250[zoom<12] 
  {
  polygon-fill: @native;
  polygon-opacity: 0.3;
  }
}

.snow
{
   polygon-fill: @snow;
   polygon-opacity: 0.8
  ;
}

.contour  
{
  .topo500[zoom>=9][zoom<11],
  .topo250[zoom>=11][zoom<13],
  .topo50[zoom>=13]
  {
      line-color: @contour;
      line-width: 0.5;
      line-opacity: 0.5;
  }
}

