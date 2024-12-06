# Instructions

Repo link - https://github.com/mohit086/DV-Assignments/tree/main/assignment-3

There are three folders - one for each workflow - each with their own code and images.

Ensure you have the required libraries -

```
pip install numpy pandas plotly squarify matplotlib imageio scikit-learn
```

or 

```
conda install numpy pandas plotly squarify matplotlib imageio scikit-learn
```

### Data and preprocessing
Original dataset (Used in Assignment-1) is saved as ```original.csv``` in the _data_ folder. The supplementary dataset is saved as ```supplementary.csv``` in the same location. Run the
```preproc.py``` file present in ```data``` to create the merged dataset ```base.csv```.

### Workflow 1

### Workflow 2

### Workflow 3

Run the ```workflow_3.py``` file in the ```workflow_3``` folder. The images get saved to ```workflow_3/images/```. Note that it can take some time (5-10 seconds) to complete running.

```
python3 workflow_3.py
```

If you get the error

```qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem. Available platform plugins are: eglfs, minimal, minimalegl, offscreen, vnc, webgl, xcb.```

please write ```export QT_QPA_PLATFORM=offscreen``` in the console before running, it should work.
