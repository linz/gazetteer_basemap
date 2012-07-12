/* Residential areas */

.residential
{
  .topo500[zoom<13]
  {
  line-width: 1;
  line-color: @dark_grey;
  polygon-fill: @residential;
  }
  .topo50[zoom>=13]
  {
  polygon-fill: @residential;
  }
  .topo50.fill[zoom>=13]
  {
  polygon-fill: @dark_grey;
  }
}
