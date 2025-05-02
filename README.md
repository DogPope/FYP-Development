# FYP-Development
Github Repository for Final Year Project Design code and implementation.
This application will allow a user to decide on a route between two points on a terrain system, using mapping and traversal techniques to find the optimal path between them.

## Project Running
To start, import the necessary environment into the program. The requirements.txt file contains the necessary libraries, and the Python version used for running is 3.12.2
Run the following command to import the environment:
```powershell
pip install -r requirements.txt
```

# To-Do
- [ ] Implement GZip for Pandas data sets. Allows me to zip the files before sending them.
- [ ] Reverse the order of Pandas Datasets when imported into MatPlotLib. It displays the Path on the wrong side.

Yes, you can absolutely implement your own pathfinding algorithm for a graph that takes elevation into account! This is a great use case for a custom implementation since terrain elevation can significantly impact the optimal path.

You can still use a NetworkX graph for storing your data structure but implement your own A* algorithm that properly weighs elevation changes. Here's how you could approach this:

This custom A* pathfinding implementation takes elevation into account while still using NetworkX graphs as your data structure. Here's a breakdown of how it works:

### Key Components

1. **Distance Calculation**: Uses the Haversine formula to calculate distances between coordinates, accounting for Earth's curvature.

2. **Elevation Penalty Function**: The core of this implementation - calculates how much harder it is to traverse a path based on slope:
   - Uphill penalties increase exponentially with steepness
   - Slight downhill grades are actually beneficial (easier than flat terrain)
   - Very steep downhill grades become costly again (dangerous/difficult)

3. **Customizable Weighting**: The `elevation_weight` parameter lets you tune how much elevation changes matter compared to distance.

### How to Use It

You'll need to structure your NetworkX graph with these required node attributes:
- `lat`: Latitude in decimal degrees
- `lon`: Longitude in decimal degrees  
- `elevation`: Elevation in meters

Then simply call:
```python
path, cost = find_path(G, source_node, target_node, elevation_weight=1.0)
```

### Additional Customization

You can further tune the algorithm for your specific terrain by:

1. Adjusting the elevation penalty calculation in `calculate_elevation_penalty()`
2. Changing the `elevation_weight` parameter (higher values make elevation more important)
3. Adding additional terrain factors (like vegetation or surface type) if you have that data

Would you like me to explain any specific part of the implementation in more detail?

```py
import networkx as nx
import heapq
import numpy as np
from math import sqrt

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points in kilometers."""
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

def calculate_elevation_penalty(elev1, elev2, distance):
    """
    Calculate penalty for elevation changes.
    
    Args:
        elev1: Elevation of starting point in meters
        elev2: Elevation of ending point in meters
        distance: Horizontal distance in kilometers
    
    Returns:
        A penalty factor to multiply with the distance
    """
    # Calculate elevation difference and slope
    elev_diff = elev2 - elev1
    
    # Avoid division by zero
    if distance < 0.001:  # Less than 1 meter horizontally
        distance = 0.001
    
    # Calculate slope as a percentage
    slope_percent = (elev_diff / (distance * 1000)) * 100
    
    # Penalties can be adjusted based on your terrain requirements
    
    # Uphill penalty (positive slope)
    if slope_percent > 0:
        # Steeper uphill is more costly
        # Example: 10% slope adds 50% more cost, 20% adds 150% more
        return 1 + (slope_percent / 20) ** 1.5
    
    # Downhill penalty (negative slope)
    else:
        # Very steep downhill can also be difficult/dangerous
        # Moderate downhill is easier than flat, but very steep is harder
        steep_factor = min(abs(slope_percent) / 15, 1.0)  # How steep relative to threshold
        
        # Slight downhill is beneficial (0.8x cost when slope is around -5%)
        # Very steep downhill becomes costly again
        if abs(slope_percent) < 10:
            return 0.8 + steep_factor * 0.2
        else:
            return 0.9 + steep_factor * 0.6

def heuristic(node1, node2, G):
    """
    Estimate the cost from node1 to node2 using haversine distance.
    This is the heuristic function for A*.
    """
    lat1, lon1 = G.nodes[node1]['lat'], G.nodes[node1]['lon']
    lat2, lon2 = G.nodes[node2]['lat'], G.nodes[node2]['lon']
    return haversine_distance(lat1, lon1, lat2, lon2)

def find_path(G, source, destination, elevation_weight=1.0):
    """
    Custom A* pathfinding algorithm that takes elevation into account.
    
    Args:
        G: NetworkX graph where nodes have 'lat', 'lon', and 'elevation' attributes
        source: Starting node ID
        destination: Goal node ID
        elevation_weight: Weight factor for elevation penalties (higher means elevation matters more)
        
    Returns:
        Tuple of (path, total_cost) where path is a list of nodes
    """
    if source not in G or destination not in G:
        raise ValueError("Source or destination node not in graph")
    
    # Priority queue for open nodes: (f_score, node_id)
    open_set = [(0, source)]
    # For each node, which node it can most efficiently be reached from
    came_from = {}
    
    # For each node, the cost of getting from start to that node
    g_score = {node: float('inf') for node in G.nodes()}
    g_score[source] = 0
    
    # For each node, the total cost of getting from start to goal passing through that node
    f_score = {node: float('inf') for node in G.nodes()}
    f_score[source] = heuristic(source, destination, G)
    
    # Keep track of nodes in the open set for fast membership checking
    open_set_hash = {source}
    
    while open_set:
        # Get the node with lowest f_score
        current_f, current = heapq.heappop(open_set)
        open_set_hash.remove(current)
        
        # If we reached the destination
        if current == destination:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(source)
            path.reverse()
            return path, g_score[destination]
        
        # Check all neighbors
        for neighbor in G.neighbors(current):
            # Get node attributes
            current_lat = G.nodes[current]['lat']
            current_lon = G.nodes[current]['lon']
            current_elev = G.nodes[current]['elevation']
            
            neighbor_lat = G.nodes[neighbor]['lat']
            neighbor_lon = G.nodes[neighbor]['lon']
            neighbor_elev = G.nodes[neighbor]['elevation']
            
            # Calculate base distance
            distance = haversine_distance(current_lat, current_lon, neighbor_lat, neighbor_lon)
            
            # Apply elevation penalty
            elev_penalty = calculate_elevation_penalty(current_elev, neighbor_elev, distance)
            
            # Final weighted cost for this edge
            cost = distance * (1 + (elev_penalty - 1) * elevation_weight)
            
            # Tentative g_score
            tentative_g_score = g_score[current] + cost
            
            # If this path is better than any previous one
            if tentative_g_score < g_score[neighbor]:
                # This path is the best until now, record it
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, destination, G)
                
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)
    
    # If we get here, no path was found
    return None, float('inf')


# Example usage:
def create_example_graph():
    """Create a simple example graph with elevation data"""
    G = nx.Graph()
    
    # Add some nodes with lat, lon, elevation
    nodes = {
        1: {'lat': 47.0, 'lon': -122.0, 'elevation': 100},
        2: {'lat': 47.02, 'lon': -122.01, 'elevation': 150},
        3: {'lat': 47.03, 'lon': -122.03, 'elevation': 300},
        4: {'lat': 47.01, 'lon': -122.05, 'elevation': 120},
        5: {'lat': 47.04, 'lon': -122.06, 'elevation': 90}
    }
    
    # Add nodes to graph
    for node_id, attrs in nodes.items():
        G.add_node(node_id, **attrs)
    
    # Add edges - in a real scenario, you'd connect based on your terrain
    G.add_edge(1, 2)
    G.add_edge(1, 4)
    G.add_edge(2, 3)
    G.add_edge(3, 5)
    G.add_edge(4, 5)
    
    return G

# Run example
if __name__ == "__main__":
    G = create_example_graph()
    
    # Find paths with different elevation weights
    path1, cost1 = find_path(G, 1, 5, elevation_weight=0.0)  # Ignore elevation
    path2, cost2 = find_path(G, 1, 5, elevation_weight=1.0)  # Normal elevation weight
    path3, cost3 = find_path(G, 1, 5, elevation_weight=3.0)  # High elevation weight
    
    print(f"Path ignoring elevation: {path1}, cost: {cost1:.2f}")
    print(f"Path with normal elevation weight: {path2}, cost: {cost2:.2f}")
    print(f"Path with high elevation weight: {path3}, cost: {cost3:.2f}")
```