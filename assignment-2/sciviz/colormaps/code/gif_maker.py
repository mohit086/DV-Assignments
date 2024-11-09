import imageio.v2 as imageio
import netCDF4 as nc
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import xarray as xr
import imageio
import os
from matplotlib.colors import Normalize
import datetime

def plot_tmmx(day,ax,colormap,norm=None):
  # Open the NetCDF file
    file_path = '../../data/tmmx.nc' 
    dataset = xr.open_dataset(file_path)

    
    latitudes = dataset['lat'].values
    longitudes = dataset['lon'].values
    # print(f"Min: {(dataset.air_temperature.min() - 273.15).values:.2f}°C, Max: {(dataset.air_temperature.max() - 273.15).values:.2f}°C")
    req_thing = 'air_temperature'
    t_max = dataset.variables[req_thing].values  # Adjust according to your file
    t_max_celsius=t_max-273.15
    t_max_slice= t_max_celsius[day, :, :]
    
    start_date = datetime.datetime(2021, 6, 1)
    current_date = start_date + datetime.timedelta(days=day)
    # Format the date to display as "June 1st," "June 2nd," etc.
    date_str = current_date.strftime("%B %d")

    # print('Latitudes shape:', latitudes.shape)
    # print('Longitudes shape:', longitudes.shape)
    
    # Create a Basemap instance
    # #plt.figure(figsize=(4, 4))
    m = Basemap(projection='lcc', resolution='i',
                lat_0=37.5, lon_0=-96,
                llcrnrlon=-119, urcrnrlon=-64,
                llcrnrlat=22, urcrnrlat=50)

    # Draw coastlines and countries
    m.drawcoastlines()
    m.drawcountries()

    # Convert lat/lon to map projection coordinates
    dx = np.diff(longitudes)[0]/2.0
    dy = np.diff(latitudes)[0]/2.0
    lon_edges = np.concatenate([[longitudes[0] - dx], longitudes + dx])
    lat_edges = np.concatenate([[latitudes[0] - dy], latitudes + dy])
    if norm is None:
        norm = Normalize(vmin=-10, vmax=55)
    # Convert lat/lon to map projection coordinates
    lon_grid, lat_grid = np.meshgrid(lon_edges, lat_edges)
    x, y = m(lon_grid, lat_grid)
    # Create color map using pcolormesh
    if(norm is None):
      mesh = m.pcolormesh(x, y, t_max_slice, cmap=colormap, shading='auto',norm=norm, ax=ax)
    else:
      mesh = m.pcolormesh(x, y, t_max_slice, cmap=colormap, shading='auto', norm=norm, ax=ax)

    # Add colorbar
    cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
    cbar.set_label('Temperature (°C)')

    # Add title
    ax.set_title(f"Maximum Near-Surface Air Temperature over the USA - {date_str} {colormap}")

    # Show the plot
    # plt.show()

    # Close the dataset
    dataset.close()

def save_tmmx_images(days, colourmap):
    output_dir='../images/final_images_for_gif_'+colourmap
    os.makedirs(output_dir, exist_ok=True)
    start_date = datetime.datetime(2024, 6, 1)  # Starting date (June 1, 2024)
    
    for day in days:
        fig, ax = plt.subplots(1, 1, figsize=(7, 8))
        plot_tmmx(day, ax, colourmap)
        
        # Calculate the current date based on the day index
        current_date = start_date + datetime.timedelta(days=day)
        date_str = current_date.strftime("%B %d")
        
        # Update the title
        ax.set_title(f"Maximum Near-Surface Air Temperature over the USA - {date_str}")
        
        # Save the plot as an image file
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'day_{day:03d}_{colourmap}.png'),
                       dpi=300, bbox_inches='tight')
        plt.close(fig)


days_to_save = [6,9,27,44,52,56,69,80,91]
save_tmmx_images(days_to_save,'seismic')
# Path to the folder containing the images
image_folder = '../images/final_images_for_gif_seismic'
output_path = '../gifs/seismic.gif'
images = []

# Load and sort the images by filename
for file_name in sorted(os.listdir(image_folder)):
    if file_name.endswith('.png') or file_name.endswith('.jpg'):
        file_path = os.path.join(image_folder, file_name)
        images.append(imageio.imread(file_path))

# Saving as a GIF
imageio.mimsave(output_path, images, fps=2)

print(f"GIF created and saved as {output_path}")
