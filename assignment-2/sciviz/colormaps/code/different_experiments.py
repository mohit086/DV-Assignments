import netCDF4 as nc
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import xarray as xr
import imageio
import os
from matplotlib.colors import Normalize, LogNorm, BoundaryNorm
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
    # Format the date to display 
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

    # plt.show()

    # Close the dataset
    dataset.close()

def plot_tmmx_with_scale(day, ax, colormap, scaling_type):
    file_path = '../../data/tmmx.nc'
    dataset = xr.open_dataset(file_path)
    latitudes = dataset['lat'].values
    longitudes = dataset['lon'].values
    t_max = dataset['air_temperature'].values - 273.15  # Convert to Celsius
    t_max_slice = t_max[day, :, :]
    norm = None
    start_date = datetime.datetime(2021, 6, 1)
    current_date = start_date + datetime.timedelta(days=day)
    # Format the date to display
    date_str = current_date.strftime("%B %d")
    # Determine scaling limits
    if scaling_type == 'local':
        vmin, vmax = dataset.air_temperature[day].min() - 273.15, dataset.air_temperature[day].max() - 273.15
    elif scaling_type=='logarithmic':
            temp_min = np.nanmin(dataset.air_temperature[day])
            shift = abs(temp_min) + 1 if temp_min <= 0 else 0
            plot_data = t_max_slice + shift
            
            # Use LogNorm 
            norm = LogNorm(vmin=np.nanmin(plot_data), 
                         vmax=np.nanmax(plot_data))
    else:
        vmin, vmax = dataset.air_temperature.min() - 273.15, dataset.air_temperature.max() - 273.15  # Global scaling
    # print(f"Min: {(dataset.air_temperature[27].min() - 273.15).values:.2f}°C, Max: {(dataset.air_temperature[27].max() - 273.15).values:.2f}°C")
    # Continue with plotting using Basemap as before
    m = Basemap(projection='lcc', resolution='i', lat_0=37.5, lon_0=-96,
                llcrnrlon=-119, urcrnrlon=-64, llcrnrlat=22, urcrnrlat=50)
    m.drawcoastlines()
    m.drawcountries()
    dx = np.diff(longitudes)[0] / 2.0
    dy = np.diff(latitudes)[0] / 2.0
    lon_edges = np.concatenate([[longitudes[0] - dx], longitudes + dx])
    lat_edges = np.concatenate([[latitudes[0] - dy], latitudes + dy])
    lon_grid, lat_grid = np.meshgrid(lon_edges, lat_edges)
    x, y = m(lon_grid, lat_grid)
    if(scaling_type != "logarithmic"):
        norm = Normalize(vmin=vmin, vmax=vmax)
    mesh = m.pcolormesh(x, y, t_max_slice, cmap=colormap, shading='auto', norm=norm, ax=ax)
    # Add colorbar and title
    cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
    cbar.set_label('Temperature (°C)')
    ax.set_title(f'Max Temperature over USA - {date_str} - {scaling_type.capitalize()} Scaling')

    dataset.close()
    
def plot_tmmx_discrete(day, ax, colormap, levels=None):
    # Same as plot_tmmx but with discrete levels support

    file_path = '../../data/tmmx.nc'
    dataset = xr.open_dataset(file_path)
    latitudes = dataset['lat'].values
    longitudes = dataset['lon'].values
    
    # print(f"Min: {(dataset.air_temperature.min() - 273.15).values:.2f}°C, Max: {(dataset.air_temperature.max() - 273.15).values:.2f}°C")
    t_max = dataset.variables['air_temperature'].values
    t_max_celsius = t_max - 273.15
    t_max_slice = t_max_celsius[day, :, :]
    
    start_date = datetime.datetime(2021, 6, 1)
    current_date = start_date + datetime.timedelta(days=day)
    # Format the date to display
    date_str = current_date.strftime("%B %d")
    
    m = Basemap(projection='lcc', resolution='i',
                lat_0=37.5, lon_0=-96,
                llcrnrlon=-119, urcrnrlon=-64,
                llcrnrlat=22, urcrnrlat=50)
    m.drawcoastlines()
    m.drawcountries()
    
    dx = np.diff(longitudes)[0]/2.0
    dy = np.diff(latitudes)[0]/2.0
    lon_edges = np.concatenate([[longitudes[0] - dx], longitudes + dx])
    lat_edges = np.concatenate([[latitudes[0] - dy], latitudes + dy])
    lon_grid, lat_grid = np.meshgrid(lon_edges, lat_edges)
    x, y = m(lon_grid, lat_grid)
    
    if levels is not None:
        # Create discrete colormap
        n_levels = len(levels) - 1
        cmap = plt.cm.get_cmap(colormap, n_levels) 
        norm = BoundaryNorm(levels, n_levels)
        mesh = m.pcolormesh(x, y, t_max_slice, cmap=cmap, 
                           norm=norm, shading='auto', ax=ax)
    else:
        # Regular continuous colormap
        mesh = m.pcolormesh(x, y, t_max_slice, cmap=colormap, 
                           vmin=-10, vmax=55, shading='auto', ax=ax)
    
    cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', 
                       fraction=0.046, pad=0.04, 
                       boundaries=levels if levels is not None else None,
                       ticks=levels if levels is not None else None)
    cbar.set_label('Temperature (°C)')
    
    if levels is not None:
        ax.set_title(f'Maximum Temperature (°C) - {date_str} - Discrete {len(levels)-1} levels')
    else:
        ax.set_title(f'Maximum Temperature (°C) - {date_str} - Continuous')
    
    dataset.close()



def save_tmmx_plots(days,base_output_dir='../images/different_experiments'):
    # Save temperature plots with different colormapping experiments
    # 1. Basic Color Schemes
    sequential_cmaps = ["viridis", "YlOrRd", "Reds"]  # Sequential
    diverging_cmaps = ["RdBu_r", "RdYlBu_r", "seismic"]  # Diverging
    perceptual_cmaps = ["magma", "inferno", "cividis"]  # Perceptually uniform
    
    # Create main output directory
    os.makedirs(base_output_dir, exist_ok=True)
    
    # 1. Color Palette Selection
    output_dir = os.path.join(base_output_dir, '1_color_schemes')
    os.makedirs(output_dir, exist_ok=True)
    
    for cmap in sequential_cmaps + diverging_cmaps + perceptual_cmaps:
        category = 'sequential' if cmap in sequential_cmaps else 'diverging' if cmap in diverging_cmaps else 'perceptual'
        for day in days:
            print(f'Processing basic scheme - {category} - {cmap} - day {day}')
            fig, ax = plt.subplots(figsize=(10, 8))
            plot_tmmx(day, ax, cmap)
            plt.savefig(os.path.join(output_dir, f'day_{day:03d}_{category}_{cmap}.png'),
                       dpi=300, bbox_inches='tight')
            plt.close(fig)
    
    #2. Scaling Approaches

    # Output directory
    output_dir = os.path.join(base_output_dir, '2_scaling_approaches')
    os.makedirs(output_dir, exist_ok=True)
    # Scaling approaches
    scaling_types = ['global','local','logarithmic']

    # Process each day and scaling type
    for day in days:
        print(f'Processing scaling approaches - day {day}')
        
        for scale_type in scaling_types:
            fig, ax = plt.subplots(figsize=(10, 8))
            plot_tmmx_with_scale(day, ax, colormap='seismic', scaling_type=scale_type)
            
            # Save plot
            output_path = os.path.join(output_dir, f'day_{day:03d}_scale_{scale_type}.png')
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
    
    # 3. Discretization Methods
    output_dir = os.path.join(base_output_dir, '3_discretization')
    os.makedirs(output_dir, exist_ok=True)
    
    discretizations = {
        'continuous': None,
        'discrete_5deg': np.arange(-10, 56, 5),  # [-10, -5, 0, 5, ..., 50, 55]
        'discrete_10deg': np.arange(-10, 66, 10), # [-10, 0, 10, ..., 60]
    }
   
    for day in days:
        print(f'Processing discretization methods - day {day}')
        for discr_name, levels in discretizations.items():
            fig, ax = plt.subplots(figsize=(10, 8))
            plot_tmmx_discrete(day, ax, 'seismic', levels)
            plt.savefig(os.path.join(output_dir, f'day_{day:03d}_discrete_{discr_name}.png'),
                       dpi=300, bbox_inches='tight')
            plt.close(fig)
            
# days=[27] # For choosing different color palettes and discretization
days=[1,45,91] # For different scaling algorithms
save_tmmx_plots(days) 