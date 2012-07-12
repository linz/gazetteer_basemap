
.lake
{
   .topo500[zoom<=8],
   .topo250[zoom>8][zoom<=13],
   .top50[zoom>13]
   {
       polygon-fill: @light_water; 
       line-color: @dark_water;
   }
   .topo500[zoom<=8]
   {
       line-width: 0.5;
   }
}


.river
{
   .topo500[zoom>9][zoom<=12],
   .topo50[zoom>12]
   {
       line-width: 1; 
       line-color: @dark_water; 
   }
}

#topo500_river_cl {[zoom<10] {line-width: 0; line-color: @dark_water;} 
 }
#topo500_river_cl {[zoom=10],[zoom=11],[zoom=12] {line-width: 1; line-color: @dark_water;} 
 }
#topo500_river_cl {[zoom>=13] {line-width: 0; line-color: @dark_water;} 
 }

#topo50_river_cl { [zoom<=12] {line-width: 0; line-color: red;}
  [zoom>12] {line-width: 1; line-color: @dark_water;} 
 }



#topo50_river_poly {[zoom<=12] {line-width:0 ; line-color:yellow; polygon-opacity: 0;}
  [zoom>12] { polygon-fill: @light_water; line-color: @dark_water;  }
  
}
#topo50_lagoon_poly {[zoom<=11] {line-width:0 ; line-color:yellow; polygon-opacity: 0;}
  [zoom>11] { polygon-fill: @light_water; line-color: @dark_water;  }
  
}


#topo50_drain { [zoom>=13] { line-width: 1;  line-color: @dark_water;}
}

#topo50_canal { [zoom>=13] { line-width: 1;  line-color: @dark_water;}
}
  
  
#topo50_coastline [zoom>=13]{
  line-color: @dark_water;
  line-width: 0.5;
  }
#topo500_coastline [zoom<13]{
  line-color: @dark_water;
  line-width: 0.5;
  }

#topo50_island [zoom>11] {
  line-color: @dark_water;
  line-width: 0.5;
  }
