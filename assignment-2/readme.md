## Instructions to Run

Ensure you have the required libraries -

`pip install xarray matplotlib numpy pandas imageio basemap`

### Sciviz

#### Data Handling

In _sciviz/data_, do the following -

`chmod +x get_data.sh`
`./get_data.sh`
`python3 clip.py`

This will download the datasets and clip them from June 1 to August 31.

#### Quiver Plots

Go to _sciviz/quiverplots/code_ and run the python files present there. The gifs will be stored in _sciviz/quiverplots/gifs_, and the images in _sciviz/quiverplots/images_. You can tweak the code to change the gif speed or the number of frames.

#### Color Maps

#### Contour Plots

### Infoviz

#### Data Handling

Run the _preprocessing.py_ python file present in the infoviz directory. It will save a list of .csv files in _infoviz/data_. The main graph is _nodes.csv_ and _edges.csv_, while the others are for the subgraphs.

#### Node-Link Diagrams

#### Parallel Coordinates Plots

First install live-server or http-server using the sudo command
npm i live-server
Now navigate to the root directory of the project and type live-server
Click on the link to see the directory structure
click on assignment-2 > infoviz > code > pcp_variant1.html to see the first three plots and similarly pcp_variant2.html to see the next three plots
The plots are explained in the report
The images of the plots are also present in the images directory

#### Treemaps
