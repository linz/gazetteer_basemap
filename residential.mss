/* Residential areas */

.residential
{
  .topo500[zoom<13],
  .topo50[zoom>=13]
  {
  line-width: 0.5;
  line-color: @dark_grey;
  polygon-fill: @residential;
  }
  .topo50.fill[zoom>=13]
  {
  polygon-fill: @dark_grey;
  }
}
