

/* Road Colours */

.road250  [zoom<=9]{ 
  .line[hway_num != ""] { line-color: @road_edge;   }
  .fill[hway_num != ""] { line-color: @state_highway ; } }

.road250  [zoom<=7]{ 
  .line[hway_num != ""] { line-color: @road_edge;   }
  .fill[hway_num != ""] { line-color: @state_highway ; } }

.road250 { [zoom=10],[zoom=11] { 
  .line[hway_num != ""] { line-color: @road_edge;   }
  .fill[hway_num != ""] { line-color: @state_highway ;   }
  .line[surface = "sealed"] { [hway_num = ""]  {line-color: @road_edge ;}}
  .fill[surface = "sealed"] { [hway_num = ""] {line-color: @road ;}}
}}


.road  
   [zoom>=13]{
  .line[surface = "metalled"] {line-color: @road_edge ;}
  .mid[surface = "metalled"] {line-color: @road2 ;}
  .fill[surface = "metalled"] {line-color: @road ; }
  .line[surface = "unmetalled"] {line-color: @road_edge ;}
  .fill[surface = "unmetalled"] {line-color: @road2 ;}}
[zoom>=12]{ 
  .line[hway_num != ""] { line-color: @road_edge;   }
  .fill[hway_num != ""] { line-color: @state_highway ;   }
  .line[surface = "sealed" ]{ [hway_num = ""]  {line-color: @road_edge ;}}
  .fill[surface = "sealed"] { [hway_num = ""] {line-color: @road ;}}
  }
  
/*Road Widths */

.road250[zoom<=9] {
  .line[hway_num != ""] {line-width: 2 + 1 ;}
  .fill[hway_num != ""] {line-width: 2; } }

.road250[zoom<=7] {
  .line[hway_num != ""] {line-width: 1 + 0.5 ;}
  .fill[hway_num != ""] {line-width: 1; } }

.road250 {[zoom=10],[zoom=11]  {
  .line[hway_num != ""] {line-width: 2 + 1 ;}
  .fill[hway_num != ""] {line-width: 2; }
  .line[surface = "sealed"] { [hway_num = ""] {line-width: 1 + 0.5 ;}}
  .fill[surface = "sealed"] { [hway_num = ""] {line-width: 1 ;}}
}}
.road250 {[zoom>11]  {
  .line[hway_num != ""] {line-width: 0 ;}
  .fill[hway_num != ""] {line-width: 0; }
  .line[surface = "sealed"] { [hway_num = ""] {line-width: 0 ;}}
  .fill[surface = "sealed"] { [hway_num = ""] {line-width: 0 ;}}
}}
.road[zoom>=12] {
  .line[hway_num != ""] {line-width: 2.5 + 1 ;}
  .fill[hway_num != ""] {line-width: 2.5; }
  .line[surface = "sealed"] { [hway_num = ""] {line-width: 1.5 + 1 ;}}
  .fill[surface = "sealed"] { [hway_num = ""] {line-width: 1.5 ;}}
  .line[surface = "metalled"] {line-width: 0 ;}
  .mid[surface = "metalled"] {line-width: 0 ;}
  .fill[surface = "metalled"] {line-width: 0 ; }
  .line[surface = "unmetalled"] {line-width: 0 ;}
  .fill[surface = "unmetalled"] {line-width: 0 ;}
}

.road[zoom>=14] {
  .line[surface = "unmetalled"] {line-width: 2 + 1 ;}
  .fill[surface = "unmetalled"] {line-width: 2 ;}
  .line[hway_num != ""] {line-width: 4 + 2 ;}
  .fill[hway_num != ""] {line-width: 4; }
  .line[surface = "sealed"] { [hway_num = ""] {line-width: 4 + 2 ;}}
  .fill[surface = "sealed"] { [hway_num = ""] {line-width: 4 ;}}
  .line[surface = "metalled"] {line-width: 3 + 2 ;}
  .mid[surface = "metalled"] {line-width: 3 ;}
  .fill[surface = "metalled"] {line-width: 3 ;  line-dasharray:24,10;}
}

#topo50_track_cl[zoom>=13] {
  [track_use = "vehicle"] {  line-dasharray:15,5;  line-color: @road_edge;
  line-width: 1;}
  [track_use = "foot"] {line-dasharray:6,3;  line-color: @road_edge;
  line-width: 1;}
  }




/*
#topo50_road_cl::outer {
  line-color: @road_edge;
  line-width: 5;
  line-cap: square;}



#topo50_road_cl::unsealed { line-width: 4; line-color: @road2; line-cap: square; 
}
#topo50_road_cl::metalled {
[surface = "metalled"]
{ line-width: 4; line-color: @road; line-cap: square; line-dasharray:24,10;} }


#topo50_road_cl::sealed {
  [surface = "sealed"] {
  line-width: 4;
  line-color: @road; 
  line-cap: square;
  }
  
  }

#topo50_road_cl::highway {
  [hway_num != ""] {
  line-width: 4;
  line-color: @state_highway ;
  line-cap: square;}
  }

*/
