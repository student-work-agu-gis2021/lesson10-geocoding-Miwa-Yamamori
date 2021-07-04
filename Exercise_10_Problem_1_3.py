#!/usr/bin/env python
# coding: utf-8

# ## Problem 1: Geocode shopping centers
# 
# In problem 1 the task is to find out the addresses for a list of shopping centers and to geocode these addresses in order to represent them as points. The output should be stored in a Shapefile called `shopping_centers.shp` 
# 

# Import modules
import geopandas as gpd
import pandas as pd
# Read the data (replace "None" with your own code)
fp = r'shopping_centers.txt'

# I specify the columns name, when I read the file. 
data = pd.read_csv(fp, sep = ';', names = ['id','name','addr'])

# YOUR CODE HERE 1 to read the data

#print(data.head())
#print("type: ", type(data))

#TEST COEE
# Check your input data
print(data)

# - Geocode the addresses using the Nominatim geocoding service. Store the output in a variable called `geo`:

# Geocode the addresses using Nominatim
geo = None
from geopandas.tools import geocode

# Geocode addresses using Nominatim. Remember to provide a custom "application name" in the user_agent parameter!
#YOUR CODE HERE 2 for geocoding

# After running 'pip install geopy' in the shell
# Create geo by using geocode.
geo = geocode(data['addr'], provider = 'nominatim', user_agent = 'autogis')
# I found the postal code is a bit diffrent from the adress in the text file.
# Also the coordinates in geo is a bit misaligned. Also, I counld not find the way to solve this problem.


#TEST CODE
# Check the geocoded output
print(geo)

#TEST CODE
# Check the data type (should be a GeoDataFrame!)
print(type(geo))


# Check that the coordinate reference system of the geocoded result is correctly defined, and **reproject the layer into JGD2011** (EPSG:6668):

# YOUR CODE HERE 3 to set crs.
from pyproj import CRS

# Check the geo's crs is '6668'
geo.crs = CRS.from_epsg(6668).to_wkt()

#TEST CODE
# Check layer crs
print(geo.crs)


# YOUR CODE HERE 4 to join the tables
# Create geodata by .join() 
geodata = geo.join(data)
#print("geodata.crs: ", geodata.crs)

#TEST CODE
# Check the join output
print(geodata.head())


# - Save the output as a Shapefile called `shopping_centers.shp` 

# Define output filepath
out_fp = r'shopping_centers.shp'

# YOUR CODE HERE 5 to save the output
geodata.to_file(out_fp)

# TEST CODE
# Print info about output file
print("Geocoded output is stored in this file:", out_fp)


# ## Problem 2: Create buffers around shopping centers
# 
# Let's continue with our case study and calculate a 1.5 km buffer around the geocoded points. 
 

# YOUR CODE HERE 6 to create a new column
# Create a new column 'buffer' in geodata
geodata['buffer'] = None

# YOUR CODE HERE 7 to set buffer column
# Check the crs is '32634', so the unit will be "meter"
geodata.crs = CRS.from_epsg(32634).to_wkt()
# Create a variable which stores buffer of 1.5km = 1500m
buffer = geodata.buffer(1500)

#print("buffer.crs: ", buffer.crs)
# Assign buffer to 'buffer' of geodata's column
geodata['buffer'] = buffer

#TEST CODE
print(geodata.head())

#TEST CODE
# Check the data type of the first value in the buffer-column
print(type(geodata.at[0,'buffer']))


#TEST CODE
# Check the areas of your buffers in km^2
print(round(gpd.GeoSeries(geodata["buffer"]).area / 1000000))
# 1.5 * 1.5 * 3.14 = 7.065

# - Replace the values in `geometry` column with the values of `buffer` column:

# YOUR CODE HERE 8 to replace the values in geometry
geodata['geometry'] = geodata['buffer']

#TEST CODE
print(geodata.head())


# ## Problem 3: How many people live near shopping centers? 
# 
# Last step in our analysis is to make a spatial join between our buffer layer and population data in order to find out **how many people live near each shopping center**. 
# 

# YOUR CODE HERE 9
# Read population grid data for 2018 into a variable `pop`. 
# Specify the file path of population data
fp_pop = r'data/500m_mesh_suikei_2018_shape_13/500m_mesh_2018_13.shp'
# Read the file as pop
pop = gpd.read_file(fp_pop)
#print("pop.cols: ", pop.columns)

# Appdate the columns
pop = pop[['PTN_2020', 'geometry']]
#print("pop.col: ", pop.columns)

#TEST CODE
# Check your input data
print("Number of rows:", len(pop))
print(pop.head(3))


# In[ ]:


# Create a spatial join between grid layer and buffer layer. 
# YOUR CDOE HERE 10 for spatial join
# In order to make join, set the crs to be same as geodata's
pop.crs = CRS.from_epsg(32634).to_wkt()

# After 'pip install Rtree'
# Make sjoin with some options
join = gpd.sjoin(geodata, pop, how = 'inner', op = 'intersects')

# YOUR CODE HERE 11 to report how many people live within 1.5 km distance from each shopping center
grouped = join.groupby(['name'])

for key, group in grouped:
  print(round(group['PTN_2020'].sum()), "people live within 1.5 km from", key)


# **Reflections:**
#     
# - How challenging did you find problems 1-3 (on scale to 1-5), and why?
# - What was easy?
# - What was difficult?

# YOUR ANSWER HERE
# 5
# I am not sure about sjoin's output, especially what data is stored in the each columns.
# The area of buffer is (1.5km ^ 2) * 3.14 = 7, so it seems correct.
# But in the result of the last print, each store has same population, and it should be wrong.
# I could not find where I made a mistake.

# Well done!
