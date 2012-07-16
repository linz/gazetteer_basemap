

.railway { 
  [zoom>=13] { line-color: @railway ; line-width: 1.5;}
  [zoom>=11][zoom<13] { line-color: @railway; line-width: 1;}
  [zoom=10] { line-color: @railway;  line-width: 0.5; }
  /*[zoom<=10] { line-color: @railway; line-width: 0.5;} */
  }

/* Build up the roads using several different symbolisers.  These will be drawn in the order 
   they occur, so put unsealed roads under sealed roads under highways
*/

.road[hway_num = ""][surface != "sealed"]::road
{
   /* Topo250 used until zoomed well in */

   .topo50[zoom>=12]
   {
       line-color: @road;
       line-width: 1.5;
       [zoom=12] { line-width: 0.5; }
       [zoom=13] { line-width: 1.0; }
   
   }
}

.road[hway_num = ""][surface = "sealed"]::sealed_road
{
   /* Topo250 used until zoomed well in */

   .topo250[zoom>=9][zoom<12]
   {
      line-color: @road;
 
       [zoom=9] { line-width: 0.5; }
       [zoom=10] { line-width: 1.0; }
       [zoom=11] { line-width: 1.5; }
   }
   .topo50[zoom>=12]
   {
       line-color: @road;
       line-width: 3;
       [zoom=12] { line-width: 1.5; }
       [zoom=13] { line-width: 2; }
   }
}

.road[hway_num != ""]::highway
{
   /* Topo250 used until zoomed well in */

   .topo250[zoom>=6][zoom<12]
   {
       line-color: @state_highway;
       [zoom=6] { line-width: 0.5; }
       [zoom=7] { line-width: 1; }
       [zoom=8] { line-width: 1.5; }
       [zoom=9] { line-width: 1.5; }
       [zoom=10] { line-width: 2; }
       [zoom=11] { line-width: 2; }
   }
   .topo50[zoom>=12]
   {
      line-color: @state_highway;
      line-width: 3;
   }
}

.track
{
  .topo50[zoom>=12] 
  {
      line-color: @track;
      line-width: 1;
      [track_use = "vehicle"] {  line-dasharray:10,2; }
      [track_use = "foot"] { line-dasharray:4,2; }
  }
}

