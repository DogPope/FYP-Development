# FYP-Development
Github Repository for Final Year Project Design code and implementation.
This application will allow a user to decide on a route between two points on a terrain system, using mapping and traversal techniques to find the optimal path between them.

## Recommended Approach
The recommended approach to this is just to view the Notebook files, as they demonstrate the project in it's entirety.
The main algorithm that this project uses to find a path is located in the `graph_traversal.ipynb` file.

## Project Running
To start, import the necessary environment into the program. The requirements.txt file contains the necessary libraries, and the Python version used for running is 3.12.2
Run the following command to import the environment:
```powershell
pip install -r requirements.txt
```

## Generate Custom Data Set
To generate a custom data set, the `generate_data_set.py` script can be run. This script asks for a valid Latitude and Longitude and generates a 4km squared plot from it in CSV format. It requires an API key, so running it requires access to the relevant Google Services.

# To-Do
- [x] Implement GZip for Pandas data sets. Allows me to zip the files before sending them.