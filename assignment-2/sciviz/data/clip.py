import xarray as xr
import glob
import os

file_paths = glob.glob('*_2021.nc')
print("Clipping in progress...")

for file_path in file_paths:
    dataset = xr.open_dataset(file_path)
    filtered_data = dataset.sel(day=slice('2021-06-01', '2021-08-31'))
    new_file_path = file_path.replace('_2021','')
    filtered_data.to_netcdf(new_file_path)
    dataset.close()
    os.remove(file_path)

print("Clipping completed")