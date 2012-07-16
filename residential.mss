/* Residential areas */

.residential
{
  .topo500[zoom<13],
  .topo50[zoom>=13]
  {
  line-width: 0.5;
  line-color: @residential2;
  polygon-fill: @residential;
  }
  .topo50.fill[zoom>=13]
  {
  polygon-fill: @residential2;
  }
}
