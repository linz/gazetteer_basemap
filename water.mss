
#topo500_lake_poly {[zoom<=8] {polygon-fill: @light_water; line-color: @dark_water;
    line-width: 0.5;
  }}

/*
#topo500_lake_poly {[zoom=9],[zoom=10],[zoom=11],[zoom=12],[zoom=13] {
  polygon-fill: @light_water; line-color:@dark_water;
  }} */

#topo250_lake_poly {[zoom=9],[zoom=10],[zoom=11],[zoom=12],[zoom=13] {
  polygon-fill: @light_water; line-color:@dark_water;
  }} 

 
#topo50_lake_poly {[zoom>13] {
  polygon-fill: @light_water;
  line-color:@dark_water;
  }}



.hydro {[zoom>13]{
  polygon-fill: @light_water;
  line-color: @dark_water;
  }}


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
  
  
#topo50_sea {
  polygon-fill: @light_water;
  line-width: 0;}

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
