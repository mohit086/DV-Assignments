import os
import numpy as np
import xarray as xr
import imageio.v2 as imageio
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap, Normalize

# custom color map
colors = ["#cce7ff","#99ccff","#66b3ff","#3399ff","#007fff","#0066cc","#004c99","#003366","#00264d","#001a33"]
custom_cmap = LinearSegmentedColormap.from_list("custom_blue", colors, N=10)

# load datasets and extract values for lon and lat
dir_data = xr.open_dataset('../../data/th.nc')
speed_data = xr.open_dataset('../../data/vs.nc')
lon = dir_data['lon'].values
lat = dir_data['lat'].values

start_date = datetime(2021, 6, 1) # starting date
num_arrows = 1000 # number of arrows
day_list = [8,9,10,11,88,89,90,91] # list of days to visualize
num_frames = len(day_list) # for the gif
images = [] # for the gif
norm = Normalize(vmin=0, vmax=10) # for normalizing the colormap
os.makedirs('../images/color_quiver', exist_ok=True)

# downsample for even grid and faster results
step_lon = len(lon) // int(np.sqrt(num_arrows))
step_lat = len(lat) // int(np.sqrt(num_arrows))

# index arrays
lon_indices = np.arange(0, len(lon), step_lon)[:int(np.sqrt(num_arrows))]
lat_indices = np.arange(0, len(lat), step_lat)[:int(np.sqrt(num_arrows))]

sample_lon, sample_lat = np.meshgrid(lon[lon_indices], lat[lat_indices]) # sampling grid
print("Running...")

for day in day_list:
    wind_speed = speed_data['wind_speed'].isel(day=day).values
    wind_dir = dir_data['wind_from_direction'].isel(day=day).values
    wind_rad = np.deg2rad(wind_dir) # degrees to radians
    V = np.cos(wind_rad) # horizontal component
    U = np.sin(wind_rad) # vertical component

    # sample at specified indices
    U_sample = U[lat_indices[:, None], lon_indices]
    V_sample = V[lat_indices[:, None], lon_indices]
    speed_sample = wind_speed[lat_indices[:, None], lon_indices]

    # Basemap projection for the US, with continents, coasts, longitudes and latitudes
    fig, ax = plt.subplots(figsize=(9, 6))
    m = Basemap(llcrnrlon=-123, llcrnrlat=20, urcrnrlon=-62, urcrnrlat=50,
                projection='lcc', lat_1=33, lat_2=45, lat_0=39.5, lon_0=-98, ax=ax)
    m.drawmapboundary(fill_color='#A6CAE0')
    m.fillcontinents(color='#E1DCBD', lake_color='#A6CAE0', alpha=0.7)
    m.drawcoastlines(color='#404040', linewidth=0.8)
    m.drawcountries(color='#404040', linewidth=0.6)
    m.drawparallels(np.arange(20, 51, 10), labels=[1, 0, 0, 0], fontsize=8, color='#808080', linewidth=0.5)
    m.drawmeridians(np.arange(-120, -60, 10), labels=[0, 0, 0, 1], fontsize=8, color='#808080', linewidth=0.5)

    x, y = m(sample_lon, sample_lat) # sample points -> projection coordinates

    # the quiver plot. Values can be changed for experimentation
    q = m.quiver(x, y, U_sample, V_sample, speed_sample, cmap=custom_cmap, norm=norm, scale=40)
    plt.colorbar(q, label='Wind Speed (m/s)', orientation='vertical', fraction=0.06, aspect=10)

    # Save the figures and make the gif
    current_date = start_date + timedelta(days=day)
    date_str = current_date.strftime("%-d %b")
    plt.title(f"Wind Direction Analysis - {date_str}", fontsize=14, pad=20)
    plt.tight_layout()
    fig.savefig(f'../images/color_quiver/{date_str.replace(" ", "_")}.png', format='png')
    plt.close(fig)
    images.append(imageio.imread(f'../images/color_quiver/{date_str.replace(" ", "_")}.png'))
    imageio.mimsave(f'../gifs/color_quiver.gif', images, fps=2)

print("Completed")