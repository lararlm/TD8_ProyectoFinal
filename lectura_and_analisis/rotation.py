import sys
import os
from shapely.geometry import Polygon, Point, box
import matplotlib.pyplot as plt
import matplotlib.patches
import numpy as np  
import math

def rotation(outer_polygon, angle):
    rotated_outer_polygon = []
    angle_rad = math.radians(angle)
    rotation_matrix = np.array([[math.cos(angle_rad), -math.sin(angle_rad)], 
                                [math.sin(angle_rad), math.cos(angle_rad)]])
    
    for point in outer_polygon:
        point_array = np.array(point)  
        rot_point = rotation_matrix @ point_array  
        rotated_outer_polygon.append(tuple(rot_point))
    
    return rotated_outer_polygon

# 9. Plot the outer polygon, rectangles, and restriction polygons
def plot_polygon(outer_polygon, restrictions):
    fig, ax = plt.subplots()

    # Plot the outer polygon
    outer_poly = Polygon(outer_polygon)
    x, y = outer_poly.exterior.xy
    ax.fill(x, y, alpha=0.5, fc='lightblue', ec='black', label='Outer Polygon')

    for pol in restrictions:
        pol = Polygon(pol)
        x, y = pol.exterior.xy
        ax.fill(x, y, alpha=0.5, fc='blue', ec='black', label='Restriction')
    ax.set_aspect('equal')
    plt.show()

polygon = [(10.0, 0.0), (0.0, 16.0), (0.0, 29.0), (12.0, 33.0), (33.0, 33.0), (46.0, 16.0), (46.0, 6.0), (38.0, 0.0), (10.0, 0.0)]
restrictions = [[(9.0, 22.0), (9.0, 25.0), (12.0, 28.0), (16.0, 29.0), (17.0, 27.0), (12.0, 23.0), (9.0, 22.0)], [(25.0, 22.0), (27.0, 25.0), (29.0, 27.0), (30.0, 25.0), (27.0, 21.0), (25.0, 22.0)], [(25.0, 22.0), (27.0, 21.0), (29.0, 17.0), (27.5, 15.0), (25.0, 17.0), (25.0, 22.0)], [(16.0, 11.0), (17.0, 13.0), (24.0, 8.0), (27.0, 5.0), (26.0, 4.0), (19.0, 7.0), (16.0, 11.0)]]
rotated_pol = rotation(polygon, 45)
rotated_rest = [rotation(rest, 45) for rest in restrictions]
plot_polygon(polygon, restrictions)
plot_polygon(rotated_pol, rotated_rest)