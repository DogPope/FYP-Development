import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("carrauntoohil_data_set.csv")
x = df['longitude']
y = df['latitude']
z = df['elevation']
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c='blue', marker='o')
ax.set_xlabel('Longitude')
ax.set_facecolor(color="lightgrey")
ax.set_ylabel('Latitude')
ax.set_zlabel('Elevation')
ax.set_title('3D Visualization of Geographic Data')
plt.show()