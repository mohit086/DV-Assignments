import os
import numpy as np
import xarray as xr
import imageio.v2 as imageio
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from datetime import datetime, timedelta

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

# downsample for even grid and faster results
step_lon = len(lon) // int(np.sqrt(num_arrows))
step_lat = len(lat) // int(np.sqrt(num_arrows))

# index arrays
lon_indices = np.arange(0, len(lon), step_lon)[:int(np.sqrt(num_arrows))]
lat_indices = np.arange(0, len(lat), step_lat)[:int(np.sqrt(num_arrows))]

sample_lon, sample_lat = np.meshgrid(lon[lon_indices], lat[lat_indices]) # sampling grid
os.makedirs('../images/length_quiver', exist_ok=True)
print("Running...")

for day in day_list:

    wind_speed = speed_data['wind_speed'].isel(day=day).values
    wind_dir = dir_data['wind_from_direction'].isel(day=day).values
    wind_rad = np.deg2rad(wind_dir) # degrees to radians
    V = np.cos(wind_rad) # horizontal component
    U = np.sin(wind_rad) # vertical component

    # sample at specified indices, and scale by the wind speed
    U_sample = U[lat_indices[:, None], lon_indices] * wind_speed[lat_indices[:, None], lon_indices]
    V_sample = V[lat_indices[:, None], lon_indices] * wind_speed[lat_indices[:, None], lon_indices]

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

    # quiver plot. Values can be changed for experimentation
    q = m.quiver(x, y, U_sample, V_sample, color='blue', scale=200, width=0.0015)
    plt.quiverkey(q, 0.9, 1.05, 4, '4 m/s', labelpos='E', coordinates='axes', fontproperties={'size': 10}) # key
    
    # Save the figures and make the gif
    current_date = start_date + timedelta(days=day)
    date_str = current_date.strftime("%-d %b")
    plt.title(f"Wind Direction Analysis - {date_str}", fontsize=14, pad=20)
    plt.tight_layout()
    fig.savefig(f'../images/length_quiver/{date_str.replace(" ", "_")}.png', format='png')
    plt.close(fig)
    images.append(imageio.imread(f'../images/length_quiver/{date_str.replace(" ", "_")}.png'))
    imageio.mimsave(f'../gifs/length_quiver.gif', images, fps=2)

print("Completed")