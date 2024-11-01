import netCDF4 as nc
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import imageio
import os
import datetime


file_name = 'srad'
file_path = f'../../data/{file_name}.nc'  # Update with your NetCDF file path
dataset = nc.Dataset(file_path)
print(dataset.variables)
