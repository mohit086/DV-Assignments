# Instructions

There are two main folders - _sciviz_ and _infoviz_ each of them with their own data, images/gifs and code.

Ensure you have the required libraries -

```pip install numpy pandas matplotlib basemap imageio xarray scipy```

## Scientific Visualizations

#### Data Handling

In _sciviz/data_, do the following -

```chmod +x get_data.sh && ./get_data.sh```
```python3 clip.py```

This will download the datasets and clip them from June 1 to August 31.

#### Quiver Plots

Go to _sciviz/quiverplots/code_ and run the python files present there. The gifs will be stored in _sciviz/quiverplots/gifs_, and the images in _sciviz/quiverplots/images_. The code is appropriately commented and can be tweaked to change the visualizations.

#### Color Maps

#### Contour Plots
Go to _sciviz/contourplots/code_ and run the python files present there. The gifs will be stored in _sciviz/contourplots/gifs_, and the images in _sciviz/contourplots/images_. The code is appropriately commented and can be tweaked to change the visualizations.

NOTE:
1. Note that the images folder contains files either named in the format day{index} or with a specific date present in them
The specific dated files correspond to maps generated using cartopy while the others correspond to maps generated using basemap
2. Experimental images that show only contour lines or those that use only the contour fill alone aren't shown here. Refer to the report for the same.

## Information Visualizations

#### Data Handling

Run _preprocessing.py_ present in _infoviz/data_ (ensure chinese_buddhism.gexf is present there) . It will save a list of .csv files. The main graph is _nodes.csv_ and _edges.csv_, while the others are for the subgraphs.

#### Node-Link Diagrams

There is no code. Just open the chinese_buddhism.gephi file to see the graphs. The saved images are present in _nodelink/images_.

#### Parallel Coordinates Plots

First install live-server or http-server using the sudo command
npm i live-server
Now navigate to the root directory of the project and type live-server
Click on the link to see the directory structure
click on assignment-2 > infoviz > code > pcp_variant1.html to see the first three plots and similarly pcp_variant2.html to see the next three plots
The plots, their interactions and uses are explained in the report
The images of the plots are also present in the images directory

#### Treemaps
