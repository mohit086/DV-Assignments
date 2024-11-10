# convert this to code to all variables 
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from matplotlib.colors import PowerNorm
from datetime import datetime
from netCDF4 import Dataset, num2date
from datetime import datetime
import imageio


variable_names = ['precipitation_amount', 'relative_humidity', 'mean_vapor_pressure_deficit', 'surface_downwelling_shortwave_flux_in_air', ]
file_names = ['pr', 'rmax', 'vpd', 'srad']
long_names = ['precipitation', 'maximum relative humidity', 'vapour pressure deficit', 'downward_shortwave_radiation']

# variable_names = ['precipitation_amount', 'relative_humidity', 'mean_vapor_pressure_deficit', 'surface_downwelling_shortwave_flux_in_air', 'potential_evapotranspiration', 'relative_humidity']
# file_names = ['pr', 'rmax', 'vpd', 'srad', 'pet', 'rmin']
# long_names = ['precipitation', 'maximum relative humidity', 'vapour pressure deficit', 'downward_shortwave_radiation', 'potential evapotranspiration', 'minimum relative humidity']
def contour(target_date, variable_name, long_name, file_name):
        global lon1, lon2
        cmap = 'jet_r'
        if file_name == 'pr':
            cmap='YlGnBu'
        elif file_name == 'rmax':
             cmap='YlGnBu'
        elif file_name == 'vpd':
             cmap='jet'
        else:
             cmap='YlOrRd'
        date_index = next((i for i, date in enumerate(dates) if date == target_date), None)

        if date_index is not None:
            # get the variable for the specified date like a serires
            var = data.variables[variable_name][date_index, :, :]  

            vmin = np.min(var)
            vmax = np.max(var)

            # meshgrid for lat and long
            lon, lat = np.meshgrid(lon1, lat1)

            # cartoyp and PlateeCaree projection
            fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})

            ax.set_extent([-130, -60, 20, 55], crs=ccrs.PlateCarree())  #change latitude and longitude bounds because we know it is USA

            ax.set_aspect(1.3)  # set aspect ratio to make inner map taller

            # add ocean and land stuff like coastlines, don't add states as those will get confused with contour lines
            ax.add_feature(cfeature.OCEAN, zorder=0, color='lightblue')  # Ocean background
            ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black', color='whitesmoke')  # Land background
            ax.coastlines(resolution='50m', color='black', linewidth=1)  # Coastlines

            
            if variable_name == 'surface_downwelling_shortwave_flux_in_air':
                cmap = 'jet'
            
            contour_filled = ax.contourf(lon, lat, var, cmap=cmap, 
                                        norm=PowerNorm(gamma=1.0, vmin=vmin, vmax=vmax), # use powernorm for proper scaling and use of all colors
                                        transform=ccrs.PlateCarree())

            # Put contours on top of the filled contours to make it clearer
            contour_lines = ax.contour(lon, lat, var, colors='black', linewidths=0.5, transform=ccrs.PlateCarree())

            # Put colorbar and labels
            plt.colorbar(contour_filled, ax=ax, orientation='vertical', label=long_name + f"{data.variables[variable_name].units}")
            plt.title(f'{long_name} {target_date.strftime("%B %d, %Y")}')
            
            # Save the file
            # plt.show()
            plt.savefig(f'../images/contour_frames_{file_name}/{target_date.strftime("%B %d, %Y")}.png')



for file_name, variable_name, long_name in zip(file_names, variable_names, long_names):
    data = Dataset(f'../../data/{file_name}.nc', mode='r')
    lat1 = data.variables['lat'][:]
    lon1 = data.variables['lon'][:]
    time = data.variables['day'][:]  # Replace 'day' with the actual time variable in your file
    time_units = data.variables['day'].units  # Get time units
    dates = num2date(time, time_units)  # Convert numerical time to datetime objects
    
    step=10
    target_dates = []
    images = []
    for day_index in range(0, time.shape[0], step):
        # target_dates.append(dates[day_index]
        contour(target_date=dates[day_index], variable_name=variable_name, long_name=long_name, file_name=file_name)
        images.append(imageio.imread(f'../images/contour_frames_{file_name}/{dates[day_index].strftime("%B %d, %Y")}.png'))
    imageio.mimsave(f'../gifs/{file_name}_contours.gif', images, duration=1.5)  # Adjust duration for speed
    data.close()

