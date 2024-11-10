import netCDF4 as nc
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import xarray as xr
import imageio
import os
from matplotlib.colors import Normalize, LogNorm
import datetime

def plot_tmmx(day,ax,colourmap,norm=None):
  # Open the NetCDF file
    file_path = '../../data/tmmx.nc'  
    dataset = xr.open_dataset(file_path)
    latitudes = dataset['lat'].values
    longitudes = dataset['lon'].values
    # print(f"Min: {(dataset.air_temperature.min() - 273.15).values:.2f}°C, Max: {(dataset.air_temperature.max() - 273.15).values:.2f}°C")
    req_thing = 'air_temperature'
    t_max = dataset.variables[req_thing].values
    t_max_celsius=t_max-273.15
    
    t_max_slice= t_max_celsius[day, :, :]
    start_date = datetime.datetime(2021, 6, 1)
    current_date = start_date + datetime.timedelta(days=day)
    # Format the date to display 
    date_str = current_date.strftime("%B %d")
    
    # print('Latitudes shape:', latitudes.shape)
    # print('Longitudes shape:', longitudes.shape)
    # print('Temperature slice shape:', t_max_slice.shape)
    
    # Create a Basemap instance
    
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
        norm = Normalize(vmin=-10, vmax=55) # got these values from global parameters
        # Convert lat/lon to map projection coordinates
    lon_grid, lat_grid = np.meshgrid(lon_edges, lat_edges)
    x, y = m(lon_grid, lat_grid)
    # Create color map using pcolormesh
    mesh = m.pcolormesh(x, y, t_max_slice, cmap=colourmap, shading='auto', norm=norm, ax=ax)

    # Add colorbar
    cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
    cbar.set_label('Temperature (°C)')

    # Add title
    ax.set_title(f"Maximum Near-Surface Air Temperature over the USA - {date_str} {colourmap}")

    # Show the plot
    # plt.show()

    # Close the dataset
    dataset.close()

def plot_tmmn(day,ax,colourmap):
  # Open the NetCDF file
    file_path = '../../data/tmmn.nc'  
    dataset = xr.open_dataset(file_path)
    latitudes = dataset['lat'].values
    longitudes = dataset['lon'].values
    # print(f"Min: {(dataset.air_temperature.min() - 273.15).values:.2f}°C, Max: {(dataset.air_temperature.max() - 273.15).values:.2f}°C")
    req_thing = 'air_temperature'
    t_min = dataset.variables[req_thing].values
    t_min_celsius=t_min-273.15
    
    t_min_slice= t_min_celsius[day, :, :]
    start_date = datetime.datetime(2021, 6, 1)
    current_date = start_date + datetime.timedelta(days=day)
    # Format the date to display 
    date_str = current_date.strftime("%B %d")
    
    # print('Latitudes shape:', latitudes.shape)
    # print('Longitudes shape:', longitudes.shape)
    
    # Create a Basemap instance
    
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
    lon_grid, lat_grid = np.meshgrid(lon_edges, lat_edges)
    x, y = m(lon_grid, lat_grid)
    # Create color map using pcolormesh
    mesh = m.pcolormesh(x, y, t_min_slice, cmap=colourmap, shading='auto', ax=ax)

    # Add colorbar
    cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
    cbar.set_label('Temperature (°C)')

    # Add title
    ax.set_title(f"Minimum Near-Surface Air Temperature over the USA - {date_str} {colourmap}")

    # Show the plot
    # plt.show()

    # Close the dataset
    dataset.close()

def plot_srad(day,ax,colourmap):
  # Open the NetCDF file
    file_path = '../../data/srad.nc'  
    dataset = xr.open_dataset(file_path)

    latitudes = dataset['lat'].values
    longitudes = dataset['lon'].values
    
    req_thing = 'surface_downwelling_shortwave_flux_in_air'
    srad = dataset.variables[req_thing].values  
    
    srad_slice= srad[day, :, :]
    start_date = datetime.datetime(2021, 6, 1)
    current_date = start_date + datetime.timedelta(days=day)
    # Format the date to display 
    date_str = current_date.strftime("%B %d")
    
    # print('Latitudes shape:', latitudes.shape)
    # print('Longitudes shape:', longitudes.shape)
    
    # Create a Basemap instance

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
    lon_grid, lat_grid = np.meshgrid(lon_edges, lat_edges)
    x, y = m(lon_grid, lat_grid)
    # Create color map using pcolormesh
    mesh = m.pcolormesh(x, y, srad_slice, cmap=colourmap, shading='auto',ax=ax)

    # Add colorbar
    cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
    cbar.set_label('Solar Radiation')

    # Add title
    ax.set_title(f"Solar Radiation over the USA - {date_str} {colourmap}")

    # Show the plot
    # plt.show()

    # Close the dataset
    dataset.close()

def plot_bi(day,ax,colourmap):
  # Open the NetCDF file
    file_path = '../../data/bi.nc'  
    dataset = xr.open_dataset(file_path)

    
    latitudes = dataset['lat'].values
    longitudes = dataset['lon'].values

    req_thing = 'burning_index_g'
    bi = dataset.variables[req_thing].values 
    
    bi_slice= bi[day, :, :] 
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

    dx = np.diff(longitudes)[0]/2.0
    dy = np.diff(latitudes)[0]/2.0
    lon_edges = np.concatenate([[longitudes[0] - dx], longitudes + dx])
    lat_edges = np.concatenate([[latitudes[0] - dy], latitudes + dy])
    lon_grid, lat_grid = np.meshgrid(lon_edges, lat_edges)
    x, y = m(lon_grid, lat_grid)
    # Create color map using pcolormesh
    mesh = m.pcolormesh(x, y, bi_slice, cmap=colourmap, shading='auto', ax=ax)

    # Add colorbar
    cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
    cbar.set_label('Burning Index')

    # Add title
    ax.set_title(f"Burning Index over the USA - {date_str} {colourmap}")

    # Show the plot
    # plt.show()

    # Close the dataset
    dataset.close()

def plot_erc(day,ax,colourmap):
  # Open the NetCDF file
    file_path = '../../data/erc.nc'  
    dataset = xr.open_dataset(file_path)

    
    latitudes = dataset['lat'].values
    longitudes = dataset['lon'].values
    
    req_thing = 'energy_release_component-g'
    erc = dataset.variables[req_thing].values  
    
    erc_slice= erc[day, :, :]  
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
    lon_grid, lat_grid = np.meshgrid(lon_edges, lat_edges)
    x, y = m(lon_grid, lat_grid)
    # Create color map using pcolormesh
    mesh = m.pcolormesh(x, y, erc_slice, cmap=colourmap, shading='auto', ax=ax)

    # Add colorbar
    cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
    cbar.set_label('Energy Release Component')

    # Add title
    ax.set_title(f"Energy Release Component over the USA - {date_str} {colourmap}")

    # Show the plot
    # plt.show()

    # Close the dataset
    dataset.close()
  
def plot_fm100(day,ax,colourmap):
  # Open the NetCDF file
    file_path = '../../data/fm100.nc'  
    dataset = xr.open_dataset(file_path)

    
    latitudes = dataset['lat'].values
    longitudes = dataset['lon'].values

    dataset = xr.open_dataset(file_path)
    
    req_thing = 'dead_fuel_moisture_100hr'
    fm100 = dataset.variables[req_thing].values  
    
    fm100_slice= fm100[day, :, :] 
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
    lon_grid, lat_grid = np.meshgrid(lon_edges, lat_edges)
    x, y = m(lon_grid, lat_grid)
    # Create color map using pcolormesh
    mesh = m.pcolormesh(x, y, fm100_slice, cmap=colourmap, shading='auto', ax=ax)

    # Add colorbar
    cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
    cbar.set_label('Fuel Moisture (100 hr)')

    # Add title
    ax.set_title(f" Fuel Moisture (100 hr)  over the USA - {date_str} {colourmap}")

    # Show the plot
    # plt.show()

    # Close the dataset
    dataset.close()

def plot_fm1000(day,ax,colourmap):
  # Open the NetCDF file
    file_path = '../../data/fm1000.nc'  
    dataset = xr.open_dataset(file_path)

    
    latitudes = dataset['lat'].values
    longitudes = dataset['lon'].values

    dataset = xr.open_dataset(file_path)
    
    req_thing = 'dead_fuel_moisture_1000hr'
    fm1000 = dataset.variables[req_thing].values  
    
    fm1000_slice= fm1000[day, :, :] 
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
    lon_grid, lat_grid = np.meshgrid(lon_edges, lat_edges)
    x, y = m(lon_grid, lat_grid)
    # Create color map using pcolormesh
    mesh = m.pcolormesh(x, y, fm1000_slice, cmap=colourmap, shading='auto', ax=ax)

    # Add colorbar
    cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
    cbar.set_label('Fuel Moisture (1000 hr)')

    # Add title
    ax.set_title(f" Fuel Moisture (1000 hr)  over the USA - {date_str} {colourmap}")

    # Show the plot
    # plt.show()

    # Close the dataset
    dataset.close()

def save_images(days, dataset_type, colourmap, event_name):
   #Base directory for inferences
   base_dir = '../images/inferences'
   output_dir = os.path.join(base_dir, event_name)
   os.makedirs(output_dir, exist_ok=True)
   
   start_date = datetime.datetime(2021, 6, 1)

   # Dictionary mapping dataset types to their plotting functions and titles
   dataset_info = {
       'tmmx': {
           'plot_fn': plot_tmmx,
           'title': "Maximum Near-Surface Air Temperature over the USA"
       },
       'tmmn': {
           'plot_fn': plot_tmmn,
           'title': "Minimum Near-Surface Air Temperature over the USA"
       },
       'srad': {
           'plot_fn': plot_srad,
           'title': "Surface Downwelling Solar Radiation over the USA"
       },
       'erc': {
           'plot_fn': plot_erc,
           'title': "Energy Release Component over the USA"
       },
       'bi': {
           'plot_fn': plot_bi,
           'title': "Burning Index over the USA"
       },
       'fm100': {
           'plot_fn': plot_fm100,
           'title': "100-hour Dead Fuel Moisture over the USA"
       },
       'fm1000': {
           'plot_fn': plot_fm1000,
           'title': "1000-hour Dead Fuel Moisture over the USA"
       },
   }

   for day in days:
       fig, ax = plt.subplots(1, 1, figsize=(7, 8))
       
       # Get the appropriate plotting function and title
       plot_fn = dataset_info[dataset_type]['plot_fn']
       title_prefix = dataset_info[dataset_type]['title']
       
       # Plot the data
       plot_fn(day, ax, colourmap)
       
       # Calculate the current date
       current_date = start_date + datetime.timedelta(days=day)
       date_str = current_date.strftime("%d%B").lower()
       
       # Update the title
       ax.set_title(f"{title_prefix} - {current_date.strftime('%B %d')}")
       
       # Save the plot with new naming convention
       filename = f'{date_str}_{dataset_type}.png'
       plt.tight_layout()
       plt.savefig(os.path.join(output_dir, filename),
                   dpi=300, bbox_inches='tight')
       plt.close(fig)

# List of important weather events during the period
events = {
    'pacific_northwest_heatwave': {
        'days': [27],  # June 28
        'datasets': {
            'tmmx': 'seismic',
            'srad': 'YlOrRd'
        }
    },
    'death_valley_heat': {
        'days': [39],  # July 10
        'datasets': {
            'tmmx': 'seismic',
            'srad': 'YlOrRd'
        }
    },
    'dixie_fire': {
        'days': [44],  # July 15
        'datasets': {
            'erc': 'YlOrRd',
            'bi': 'YlOrRd',
            'fm1000': 'BrBG'
        }
    },
    'monument_fire': {
        'days': [62],  # August 2
        'datasets': {
            'erc': 'YlOrRd',
            'bi': 'YlOrRd',
            'fm1000': 'BrBG'
        }
    }
}

# Generate visualizations
for event_name, event_info in events.items():
    for dataset_type, colormap in event_info['datasets'].items():
        save_images(event_info['days'], dataset_type, colormap, event_name)
