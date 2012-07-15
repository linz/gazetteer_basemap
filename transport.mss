

.railway { 
  [zoom>=13] { line-color: @railway ; line-width: 2;}
  [zoom>=11][zoom<13] { line-color: @railway; line-width: 1;}
  [zoom=10] { line-color: @railway;  line-width: 0.5; }
  /*[zoom<=10] { line-color: @railway; line-width: 0.5;} */
  }

/* Build up the roads using several different symbolisers.  These will be drawn in the order 
   they occur, so put casing under road, and non-highways under highways

   Note: casing layers could be combined, as all drawn underneath other symbolisers with the same colour
*/

.road[hway_num = ""]::casing
{
   /* Topo250 used until zoomed well in */

   .topo250[zoom<12]
   {
       [zoom>10][zoom<12]
       {
           line-color: @road_edge;
           line-width: 3;
       }
       [zoom>=10][zoom<12][surface = "sealed"]
       {
           line-color: @road_edge;
           line-width: 3;
       }
   }
   .topo50[zoom>=12]
   {
       line-color: @road_edge;
       line-width: 3;
       
       [surface = "sealed"]
       {
           line-color: @road_edge;
           line-width: 4;
       }
   }
}

.road[hway_num != ""]::hway_casing

{
   /* Topo250 used until zoomed well in */

   .topo250[zoom<12]
   {
       [zoom>=10][zoom<12]
       {
           line-color: @road_edge;
           line-width: 4;
       }
   }
   .topo50[zoom>=12]
   {
       line-color: @road_edge;
       line-width: 5;
   }
}

.road[hway_num = ""]::road
{
   /* Topo250 used until zoomed well in */

   .topo250[zoom<12]
   {
 
       [zoom=10][surface = "sealed"]
       {
           line-color: @road;
           line-width: 1.5;
       }
 
       [zoom=11][surface = "sealed"]
       {
           line-color: @road;
           line-width: 2;
       }
   }
   .topo50[zoom>=12]
   {
       line-color: @road2;
       line-width: 2;

       [surface = "sealed"]
       {
           line-color: @road;
           line-width: 3;
       }
   }
}

.road[hway_num != ""]::hway
{
   /* Topo250 used until zoomed well in */

   .topo250[zoom>=6][zoom<12]
   {
       line-color: @state_highway;
       line-width: 0.5;
       [zoom>6]
       { 
           line-width: 1;
       }
       [zoom>7][zoom<10]
       { 
           line-color: @state_highway;
           line-width: 2;
       }
       [zoom>=10][zoom<12]
       {
           line-color: @state_highway;
           line-width: 3;
       }
   }
   .topo50[zoom>=12]
   {
      line-color: @state_highway;
      line-width: 4;
   }
}

.track
{
  .topo50[zoom>=12] 
  {
  [track_use = "vehicle"] 
  {  
      line-dasharray:10,2;  
      line-color: @road_edge;
      line-width: 1;
  }
  [track_use = "foot"] 
  {
      line-dasharray:4,2;  
      line-color: @road_edge;
      line-width: 1;
   }
  }
}

