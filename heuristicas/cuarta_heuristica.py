import numpy as np
import matplotlib.path
from shapely.geometry import Point, Polygon

def check_availability(center, panel_size, polygon, restrictions, placed_rectangles):
    # Step 1: Check if the rectangle is fully inside the polygon
    dx, dy = panel_size
    x, y = center
    x_bl = x - dx / 2
    y_bl = y - dy / 2
    bbpath = matplotlib.path.Path(polygon)
    result = bbpath.contains_points([
        (x_bl, y_bl),               # Bottom-left corner
        (x_bl + dx, y_bl),          # Bottom-right corner
        (x_bl, y_bl + dy),          # Top-left corner
        (x_bl + dx, y_bl + dy)      # Top-right corner
    ])
    if not np.all(result):
        return False
    
    # Step 2: Check if the center is within any restriction areas
    for rest in restrictions:
        center_point = Point(center)
        fig_rest = Polygon(rest)
        if center_point.within(fig_rest):
            return False
    
    # Step 3: Check if the rectangle does not overlap with any other rectangles in the list
    width1, height1 = panel_size
    left1 = x - width1 / 2
    right1 = x + width1 / 2
    top1 = y - height1 / 2
    bottom1 = y + height1 / 2

    for center2, size2 in placed_rectangles:
        x2, y2 = center2
        width2, height2 = size2
        left2 = x2 - width2 / 2
        right2 = x2 + width2 / 2
        top2 = y2 - height2 / 2
        bottom2 = y2 + height2 / 2
        
        if not (left1 >= right2 or left2 >= right1 or top1 >= bottom2 or top2 >= bottom1):
            return False
    
    return True

def sweep_line_algorithm(map_polygon, restrictions, panel_sizes):
    # Initialize sweep line (horizontal)
    sweep_line_position = 0
    sweep_line_step = 10  # Adjust step size as needed
    placed_rectangles = []

    while sweep_line_position < max(x for x, y in map_polygon):  # Use map boundary conditions
        for rect in panel_sizes:
            rect_width, rect_height = rect
            x = sweep_line_position
            y = 0  # Start placing rectangles from the top of the map

            while y + rect_height <= max(y for x, y in map_polygon):
                # Check availability of the rectangle
                if check_availability((x, y), rect, map_polygon, restrictions, placed_rectangles):
                    # Place the rectangle
                    placed_rectangles.append(((x, y), rect))
                    # Move the rectangle along the sweep line
                    x += rect_width
                else:
                    # Move to the next vertical position
                    y += sweep_line_step
        
        # Move the sweep line to the next position
        sweep_line_position += sweep_line_step

    return placed_rectangles

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as mpl_Polygon, Rectangle as mpl_Rectangle

def plot_map_and_rectangles(map_polygon, restrictions, placed_rectangles):
    fig, ax = plt.subplots()

    # Plot the map polygon
    map_poly = mpl_Polygon(map_polygon, closed=True, edgecolor='black', facecolor='none')
    ax.add_patch(map_poly)

    # Plot the restriction areas
    for rest in restrictions:
        rest_poly = mpl_Polygon(rest, closed=True, edgecolor='red', facecolor='red', alpha=0.5)
        ax.add_patch(rest_poly)

    # Plot the placed rectangles with color fill and transparency
    for (x, y), (width, height) in placed_rectangles:
        rect = mpl_Rectangle((x - width / 2, y - height / 2), width, height, 
                             edgecolor='blue', facecolor='lightblue', alpha=0.5)
        ax.add_patch(rect)
    
    # Set the aspect of the plot to be equal
    ax.set_aspect('equal')
    
    # Set limits based on map boundaries
    x_min = min(x for x, y in map_polygon)
    x_max = max(x for x, y in map_polygon)
    y_min = min(y for x, y in map_polygon)
    y_max = max(y for x, y in map_polygon)
    
    ax.set_xlim(x_min - 5, x_max + 5)
    ax.set_ylim(y_min - 5, y_max + 5)

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Map, Restrictions, and Placed Rectangles')
    plt.grid(True)
    plt.show()

# Example usage
map_polygon = [(10.0, 0.0), (0.0, 16.0), (0.0, 29.0), (12.0, 33.0), (33.0, 33.0), (46.0, 16.0), (46.0, 6.0), (38.0, 0.0), (10.0, 0.0)]
restrictions = [[(9.0, 22.0), (9.0, 25.0), (12.0, 28.0), (16.0, 29.0), (17.0, 27.0), (12.0, 23.0), (9.0, 22.0)],
                [(25.0, 22.0), (27.0, 25.0), (29.0, 27.0), (30.0, 25.0), (27.0, 21.0), (25.0, 22.0)],
                [(25.0, 22.0), (27.0, 21.0), (29.0, 17.0), (27.5, 15.0), (25.0, 17.0), (25.0, 22.0)],
                [(16.0, 11.0), (17.0, 13.0), (24.0, 8.0), (27.0, 5.0), (26.0, 4.0), (19.0, 7.0), (16.0, 11.0)]]
panel_sizes = [(5.0, 10.0), (2.0, 4.0)]

placed_rectangles = sweep_line_algorithm(map_polygon, restrictions, panel_sizes)
plot_map_and_rectangles(map_polygon, restrictions, placed_rectangles)
