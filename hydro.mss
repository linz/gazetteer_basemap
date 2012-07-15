
.lake
{
   .topo500[zoom<=10],
   .topo250[zoom>10][zoom<=12],
   .topo50[zoom>12]
   {
       polygon-fill: @light_water; 
       line-color: @dark_water;
       line-width: 0.5;
   }
}


.river
{
   .topo500[zoom>8][zoom<=10],
   .topo250[zoom>10][zoom<=12],
   .topo50[zoom>12]
   {
       line-width: 0.5; 
       line-color: @dark_water; 
   }
}

.river_poly
{
   .topo500[zoom>8][zoom<=10],
   .topo250[zoom>10][zoom<=12],
   .topo50[zoom>12]
   { 
       polygon-fill: @light_water; 
       line-color: @dark_water;  
       line-width: 0.5; 
   }
}
