# Area-shielding

Topographic shielding of cosmic radiation flux is a key parameter in using cosmogenic nuclides to determine surface exposure ages or erosion rates.
This ArcGIS toolbox is to derive the topographic shielding for an area using DEMs. The procedure is based on Codilean (2006) that iterates a set of 
hillshade functions for a range of illumination azimuth and elevation angle pairs to identify the DEM cells that are in shadow and calculate 
the shielding factor for the whole area. 

This tool was writen by python and can be imported as an Toolbox in ArcGIS to implement this analysis.

This tool can also be used to derived the topographic shielding for individual sample points. This requires the additonal steps to extract values
from the topographic shielding raster to the sample points. The related ArcGIS tools are also included in the toolbox. However, to derive the 
shielding factor for sample points is not efficent using this method. A new tools was redeveloped in 2018 (Li 2018): https://github.com/yingkui2003/topo-shielding.

Cite this work:

Li, Y. Determining topographic shielding from digital elevation models for cosmogenic nuclide analysis: 
a GIS approach and field validation. J. Mt. Sci. 10, 355–362 (2013). https://doi.org/10.1007/s11629-013-2564-1
