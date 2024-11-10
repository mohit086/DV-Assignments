# Instructions

Repo link - https://github.com/mohit086/DV-Assignments/tree/main/assignment-2

There are two main folders - _sciviz_ and _infoviz_ each of them with their own data, images/gifs and code.

Ensure you have the required libraries -

```pip install numpy pandas matplotlib basemap imageio xarray scipy cartopy netCDF4```

or 

```conda install numpy pandas matplotlib basemap imageio xarray scipy cartopy netCDF4```

## Scientific Visualizations

#### Data Handling

In _sciviz/data_, do the following -

```chmod +x get_data.sh && ./get_data.sh```

```python3 clip.py```

This will download the datasets and clip them from June 1 to August 31. Clipped datasets are also available in the releases section of the repository.

#### Quiver Plots

Go to _sciviz/quiverplots/code_ and run the python files present there. The gifs will be stored in _sciviz/quiverplots/gifs_, and the images in _sciviz/quiverplots/images_. The code is appropriately commented and can be tweaked to change the visualizations.

If you get the error

```qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem. Available platform plugins are: eglfs, minimal, minimalegl, offscreen, vnc, webgl, xcb.```

please write ```export QT_QPA_PLATFORM=offscreen``` in the console before running, it should work. This error doesn't come up in jupyter notebooks, so we have kept the .ipynb files as well.

#### Color Maps

Go to _sciviz/colormaps/code_ . 

For viewing different experiments on the maximum temperature colormap, run different_experiments.py. The images will be stored in _sciviz/colormaps/images_ in the different_experiments folder. The 'days' list in different_experiments.py takes the index of days for which the colormaps have to be made. I have used days = [27] for color palette and discretization experiments and days = [1,45,91] for scaling approaches in the report but you can tweak the days list to modify the days on which the visualizations are generated. Index 0 corresponds to June 1 and so on until index 91 which corresponds to August 31. 

For viewing the plots of significant weather events during this period run inferences.py. The images will be stored in _sciviz/colormaps/images_ in the inferences folder.

For viewing the GIF of maximum temperature run gif_maker.py. The GIF will be stored in _sciviz/colormaps/gifs_ as seismic.gif and the images used to make it will be stored in  _sciviz/colormaps/images_ in the final_images_for_gif_seismic folder. The code is appropriately commented and can be modified to change the visualizations.

Note that each colormap takes about 8 seconds to generate, so the time raken to generate visualizations for a large number of days will be long.

#### Contour Plots
Go to _sciviz/contourplots/code_ and run the python files present there. The gifs will be stored in _sciviz/contourplots/gifs_, and the images in _sciviz/contourplots/images_. The code is appropriately commented and can be tweaked to change the visualizations.

NOTE:
1. Note that the images folder contains files either named in the format day{index} or with a specific date present in them. The specific dated files correspond to maps generated using cartopy while the others correspond to maps generated using basemap. \
2. Experimental images that show only contour lines or those that use only the contour fill alone aren't shown here. Refer to the report for the same.

## Information Visualizations

#### Data Handling

Run _preprocessing.py_ present in _infoviz/data_ (ensure chinese_buddhism.gexf is present there) . It will save a list of .csv files. The main graph is _nodes.csv_ and _edges.csv_, while the others are for the subgraphs.

#### Node-Link Diagrams

There is no code. Just open the chinese_buddhism.gephi file to see the graphs. The images are present in _infoviz/nodelink/images_.

#### Parallel Coordinates Plots

Install _http-server_ or _live-server_ using the command ```npm i live-server``` or ensure you have the VSCode Live Server Extension. \
Navigate to _infoviz/pcp_ and run ```live-server```. \
Click on the link to see the directory structure, and navigate appropriately to pcp_variant1.html, pcp_variant2.html, pcp_variant3.html. \
The interactions and uses of all the plots are explained in the report. Treemap images are saved in _infoviz/pcp/images_.

#### Treemaps

Install _http-server_ or _live-server_ using the command ```npm i live-server``` or ensure you have the VSCode Live Server Extension. \
Navigate to _infoviz/treemap_ and run ```live-server```. \
Click on the link to see the directory structure, and navigate appropriately to treemap1.html, treemap2.html, treemap3.html. \
The interactions and uses of all the treemaps are explained in the report. Treemap images are saved in _infoviz/treemap/images_.
