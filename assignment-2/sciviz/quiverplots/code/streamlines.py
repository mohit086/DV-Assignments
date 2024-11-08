import os
import numpy as np
import xarray as xr
import imageio.v2 as imageio
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from datetime import datetime, timedelta
from scipy.interpolate import RegularGridInterpolator
from matplotlib.colors import LinearSegmentedColormap, Normalize

# custom color map
colors = ["#cce7ff","#99ccff","#66b3ff","#3399ff","#007fff","#0066cc","#004c99","#003366","#00264d","#001a33"]
custom_cmap = LinearSegmentedColormap.from_list("custom_blue", colors, N=10)

# load datasets and extract values for lon and lat
dir_data = xr.open_dataset('../../data/th.nc')
speed_data = xr.open_dataset('../../data/vs.nc')

downsample_factor = 10 # for faster results
start_date = datetime(2021, 6, 1) # starting date
num_arrows = 1000 # number of arrows
day_list = [8,9,10,11,88,89,90,91] # list of days to visualize
num_frames = len(day_list) # for the gif
images = [] # for the gif
norm = Normalize(vmin=0, vmax=10) # for normalizing the colormap
os.makedirs('../images/streamlines', exist_ok=True)

print("Running...")

for day in day_list:
    # Basemap projection for the US, with continents, coasts, longitudes and latitudes
    fig, ax = plt.subplots(figsize=(9, 6))
    m = Basemap(llcrnrlon=-123, llcrnrlat=20, urcrnrlon=-62, urcrnrlat=50,
                projection='lcc', lat_1=33, lat_2=45, lat_0=39.5, lon_0=-98, ax=ax)
    m.drawmapboundary(fill_color='#A6CAE0')
    m.fillcontinents(color='#E1DCBD', lake_color='#A6CAE0', alpha=0.7)
    m.drawcoastlines(color='#404040', linewidth=0.8)
    m.drawcountries(color='#404040', linewidth=0.6)
    m.drawparallels(np.arange(20,51,10), labels=[1,0,0,0], fontsize=8, color='#808080', linewidth=0.5)
    m.drawmeridians(np.arange(-120,-60,10), labels=[0,0,0,1], fontsize=8, color='#808080', linewidth=0.5)

    # define the grid resolution (50km spacing)
    nx = int((m.xmax - m.xmin) / 50000)
    ny = int((m.ymax - m.ymin) / 50000)

    # create a mesh grid
    x = np.linspace(m.xmin, m.xmax, nx)
    y = np.linspace(m.ymin, m.ymax, ny)
    x_grid, y_grid = np.meshgrid(x, y)

    # convert grid to lat-lon
    lon_grid, lat_grid = m(x_grid, y_grid, inverse=True)

    # extract the speed and direction
    wind_dir = dir_data['wind_from_direction'].isel(day=day)
    wind_speed = speed_data['wind_speed'].isel(day=day)
    wind_rad = np.deg2rad(90 - wind_dir) # meteorological to math convention
    U = wind_speed * np.cos(wind_rad) # horizontal component
    V = wind_speed * np.sin(wind_rad) # vertical component

    # Set up interpolators to resample wind data on the map grid
    lats = dir_data.lat.values
    lons = dir_data.lon.values
    U_interp = RegularGridInterpolator((lats, lons), U.values,bounds_error=False, fill_value=0)
    V_interp = RegularGridInterpolator((lats, lons), V.values,bounds_error=False, fill_value=0)
    speed_interp = RegularGridInterpolator((lats, lons), wind_speed.values,bounds_error=False, fill_value=0)

    # Interpolate U, V, and speed on the projection grid
    points = np.column_stack((lat_grid.flatten(), lon_grid.flatten()))
    U_grid = U_interp(points).reshape(x_grid.shape)
    V_grid = V_interp(points).reshape(x_grid.shape)
    speed_grid = speed_interp(points).reshape(x_grid.shape)
    U_grid, V_grid = m.rotate_vector(U_grid, V_grid, lon_grid, lat_grid) # to align with map orientation

    # Streamlines. Change values for experimentation
    stream = ax.streamplot(x, y, U_grid, V_grid,color=speed_grid,cmap=custom_cmap,norm=norm,linewidth=1,density=2)
    plt.colorbar(stream.lines, label='Wind Speed (m/s)', orientation='vertical', fraction=0.06, aspect=10)

    # Save the figures and make the gif
    current_date = start_date + timedelta(days=day)
    date_str = current_date.strftime("%-d %b")
    plt.title(f"Wind Streamlines - {date_str}", fontsize=14, pad=20)
    plt.tight_layout()
    fig.savefig(f'../images/streamlines/{date_str.replace(" ", "_")}.png', format='png')
    plt.close(fig)
    images.append(imageio.imread(f'../images/streamlines/{date_str.replace(" ", "_")}.png'))
    imageio.mimsave(f'../gifs/streamlines.gif', images, fps=2)

print("Completed")