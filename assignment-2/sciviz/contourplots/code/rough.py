import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime


file_name = 'srad'
file_path = f'../../data/{file_name}.nc'  # Update with your NetCDF file path
dataset = nc.Dataset(file_path)
print(dataset.variables['surface_downwelling_shortwave_flux_in_air'].units)





#just to see the variable names to use in other files