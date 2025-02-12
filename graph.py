import pandas as pd
import numpy as np

class three_dimensional_weighted_graph():
    def __init__(latitude, longitude, elevation):
        # The 'pass' keyword is a placeholder. It tells the interpreter to move past without throwing a syntax error.
        pass

    def djikstras():
        # Placeholder code to stop syntax errors.
        return True
        
    def a_star():
        # Placeholder code to stop syntax errors.
        return True
    
    def theta_star():
        # Placeholder code to prevent Syntax errors.
        return True
    
    # Process data from CSV File.
    def import_data():
        file_read = pd.read_csv('carrauntoohil_data_set.csv')
        x = file_read['longitude']
        y = file_read['latitude']
        z = file_read['elevation']
        np.zeros(x,y,z)