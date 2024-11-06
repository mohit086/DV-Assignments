import netCDF4 as nc
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import imageio
import os
import datetime

#use basemap


variable_names = ['precipitation_amount', 'relative_humidity', 'mean_vapor_pressure_deficit', 'surface_downwelling_shortwave_flux_in_air']
file_names = ['pr', 'rmax', 'vpd', 'srad']
long_names = ['precipitation', 'relative humidity', 'vapour pressure deficit', 'downward_shortwave_radiation']

# file_vars

# experiments:
'''
tweak number of levels
see countours with and without labels
try different contour fills like viridis, blues
try plain contours
change the number of levels to get a balance between amount of information and clutter
'''

for file_name, variable_name, long_name in zip(file_names, variable_names, long_names):
    print(f'doing for {file_name}')
# file_var = 'rmax'
# req_thing = 'relative_humidity'

# format the NetCDF file name
    file_path = f'../../data/{file_name}.nc'  
    dataset = nc.Dataset(file_path)

    # Assume 'lat', 'lon', and something like 'precipitation_amount' are the variable names in your NetCDF file
    latitudes = dataset.variables['lat'][:]
    longitudes = dataset.variables['lon'][:]


    # Fetch the precipitation or something else's data
    req_amount = dataset.variables[variable_name][:]  # Adjust according to your file
    num_days = req_amount.shape[0]  # Get the number of days

    # print('num_days is' , num_days)
    # Create a directory for images
    os.makedirs(f'../images/contour_frames_{file_name}', exist_ok=True)

    # Create contour plots for each day and save as images
    step = num_days//11
    # print(f'step is {step}')
    for day_index in range(0, num_days, step):
        # if (day_index % 5) != 0:
        #     continue
        # Select a specific time step for the current day
        req_slice = req_amount[day_index, :, :]  # Select the day
        
        # Create a Basemap instance
        plt.figure(figsize=(14, 10))
        m = Basemap(projection='lcc', resolution='i', 
                    lat_0=37.5, lon_0=-96,
                    llcrnrlon=-119, urcrnrlon=-64, 
                    llcrnrlat=22, urcrnrlat=50)

        # Draw coastlines, states, and country boundaries for context
        m.drawcoastlines()
        # m.drawstates()
        m.drawcountries()

        # Convert lat/lon to map projection coordinates
        lon_grid, lat_grid = np.meshgrid(longitudes, latitudes)
        x, y = m(lon_grid, lat_grid)

        # Define a colormap and contour levels for precipitation
        # cmap = plt.get_cmap('Blues') # blues is more intuitive

        cmap = plt.get_cmap('jet_r')
        levels = np.linspace(np.min(req_slice), np.max(req_slice), 12)
        if file_name == 'srad':
            cmap = plt.get_cmap('jet')


        # Create filled contour map
        contourf = m.contourf(x, y, req_slice, levels=levels, cmap=cmap, extend='both') # do both contour and contour fill to get clear contours
        contour = m.contour(x, y, req_slice, levels=levels, colors='black', linewidths=0.5)

        # Add color bar with better labeling
        cbar = plt.colorbar(contourf, orientation='vertical', pad=0.02, shrink=0.8, label=long_name)
        cbar.ax.tick_params(labelsize=10)

        # Add title for the current day
        plt.title(f'{long_name} Distribution over the USA - Day {day_index + 1}', fontsize=15)

        # Save the current figure
        print(f'done for {day_index+1} th day')
        plt.savefig(f'../images/contour_frames_{file_name}/day{day_index + 1}.png')
        plt.close()  # Close the figure to free memory

    # Create a GIF from the saved images

    print('going to make a gif now')
    images = []
    for day_index in range(0, num_days, step):
        # if day_index % 5 != 0:
        #     continue
        images.append(imageio.imread(f'../images/contour_frames_{file_name}/day{day_index + 1}.png'))

    # Save as GIF
    imageio.mimsave(f'../gifs/{file_name}_contours.gif', images, duration=1.5)  # Adjust duration for speed

    # Cleanup: Remove the temporary image files

    # Close the dataset
    dataset.close()
