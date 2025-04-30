import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.sample import sample_gen
from shapely.geometry import Point

# Load your existing point data
# Assuming you have a CSV with lat, long, elevation columns
points_df = pd.read_csv('carrauntoohil_data_set.csv')

# Convert to GeoPandas DataFrame
geometry = [Point(xy) for xy in zip(points_df['longitude'], points_df['latitude'])]
geo_df = gpd.GeoDataFrame(points_df, geometry=geometry, crs="EPSG:4326")

# Path to land cover raster (e.g., CORINE Land Cover)
landcover_path = 'ireland_landcover.tif'

# Open the land cover raster
with rasterio.open(landcover_path) as src:
    # Make sure coordinate systems match
    if geo_df.crs != src.crs:
        geo_df = geo_df.to_crs(src.crs)
    
    # Sample the raster at each point location
    landcover_values = []
    for point in geo_df.geometry:
        # Get coordinates in the raster's coordinate system
        x, y = point.x, point.y
        
        # Sample the raster at this point
        for val in sample_gen(src, [(x, y)]):
            landcover_values.append(val[0])  # Extract the first band value
    
    # Add land cover values to your dataframe
    geo_df['landcover_code'] = landcover_values

# Optional: Add descriptive land cover names
# This depends on your specific land cover dataset and its classification scheme
landcover_classes = {
    1: 'Urban fabric',
    2: 'Industrial/commercial',
    3: 'Mine/dump sites',
    # Add more based on your specific land cover classification
    23: 'Broad-leaved forest',
    24: 'Coniferous forest',
    25: 'Mixed forest',
    # etc.
}

# Map codes to descriptive names
geo_df['landcover_type'] = geo_df['landcover_code'].map(landcover_classes)

# Save the enriched dataset
geo_df.to_csv('points_with_landcover.csv', index=False)
print("Data enrichment complete!")