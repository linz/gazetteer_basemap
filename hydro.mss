
.lake
{
   .topo500[zoom<=8],
   .topo250[zoom>8][zoom<=12],
   .top50[zoom>=12]
   {
       polygon-fill: @light_water; 
       line-color: @dark_water;
       line-width: 0.5;
   }
}


.river
{
   .topo500[zoom>=10][zoom<13],
   .topo50[zoom>=13]
   {
       line-width: 1; 
       line-color: @dark_water; 
   }
}

.river_poly
{
   .topo500[zoom>=10][zoom<13],
   .topo50[zoom>=13]
   { 
       polygon-fill: @light_water; 
       line-color: @dark_water;  
   }
}
