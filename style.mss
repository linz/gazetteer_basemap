/* ---- PALETTE ---- */

@light_grey: #D1D1D1;
@dark_grey: #B3B0A9;

@residential: @light_grey; 
/* @exotic: #E5F2C7;
 @native: #D2DEB5; */
@native: rgba(190,210,113,1);
@exotic: rgba(206,216,168,1);
@light_water: #D0E6F4;
@dark_water: #0D85D8;
@contours: #e8933f;
@road: #e8933f;
@state_highway: #EB704F;

Map {
  background-color: #E1DFC5;
}
 
#topo500_snow {polygon-fill: #ffffff;
polygon-opacity: 0.75;}

#topo50_hillshade_raster {raster-opacity:0.1;}
#topo250_hillshade {raster-opacity:0.1;}


#topo50_building_poly[zoom>=13] {
  building-fill: @dark_grey;}

#topo50_residential[zoom>=13] {
  polygon-fill: @residential;}
#topo500_residential[zoom<13] {
  line-color: @dark_grey;
  line-width: 1;
  polygon-fill: @residential;
polygon-opacity: 0.75;}

#topo50_exotic {
  polygon-fill: @exotic;
  polygon-opacity: 0.75;}

#topo50_native {
  polygon-fill: @native;
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




