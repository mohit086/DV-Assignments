## Instructions to Run

Ensure you have the required libraries - 

```pip install xarray matplotlib numpy pandas imageio basemap```

### Sciviz

#### Data Handling

In _sciviz/data_, do the following - 

```chmod +x get_data.sh```
```./get_data.sh```
```python3 clip.py```

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

#### Treemaps

