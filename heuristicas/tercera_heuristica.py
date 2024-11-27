import matplotlib.patches
import matplotlib.pyplot
import numpy as np  
import csv
import math
from shapely.geometry import Point, Polygon 
import sys
import os
sys.path.append(os.path.abspath("TD8_ProyectoFinal/"))
from lectura_data.generacion_mapa import fun_generacion_mapa
from lectura_data.xml_parsing import xml_data_extractor
import random

def subdivide(arrays, center):
    subdivision = {'First Quadrant':[], 'Second Quadrant':[], 'Third Quadrant':[], 'Fourth Quadrant':[]}

    for array in arrays["first half"]:
        if array.x > center.x and array.y > center.y:
            subdivision['First Quadrant'].append(array)
        elif array.x < center.x and array.y > center.y:
            subdivision['Second Quadrant'].append(array)

    for array in arrays["second half"]:
        if array.x < center.x and array.y < center.y:
            subdivision['Third Quadrant'].append(array)
        elif array.x > center.x and array.y < center.y:
            subdivision['Fourth Quadrant'].append(array)
    return subdivision

def check_availability(center, panel_size, polygon, restrictions, rectangles):
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

    for center2 in rectangles:
        x2, y2 = center2
        left2 = x2 - width1 / 2
        right2 = x2 + width1 / 2
        top2 = y2 - height1 / 2
        bottom2 = y2 + height1 / 2
        
        if not (left1 >= right2 or left2 >= right1 or top1 >= bottom2 or top2 >= bottom1):
            return False
    
    return True

def relocation(subdivision, panel_size, polygon, restrictions, epsilon:float = 0.1):
    ''' Precondición: los centros de los paneles ya estan subdivididos relativo al centro del poligono
    '''
    for i in range (3):
        for i in subdivision['First Quadrant']:
            while check_availability(i, panel_size, polygon, restrictions, subdivision['First Quadrant']):
                if random.random(0,1) > epsilon:
                    i.x *= 0.9
                    i.y *= 1.10
                else:
                    indicadora = random.randint(0,1)
                    i.x *= 1 - 0.10*indicadora
                    i.y *= 1 + 0.10*indicadora

        for j in subdivision["Second Quadrant"]:
            while check_availability(i, panel_size, polygon, restrictions, subdivision["Second Quadrant"]):
                if random.random(0,1) > epsilon:
                    i.x *= 1.1
                    i.y *= 1.1
                else:
                    indicadora = random.randint(0,1)
                    i.x *= 1 + 0.1*indicadora
                    i.y *= 1 + 0.1*indicadora 

        for k in subdivision["Third Quadrant"]:
            while check_availability(i, panel_size, polygon, restrictions, subdivision["Third Quadrant"]):
                if random.random(0,1) > epsilon:
                    i.x *= 1.1
                    i.y *= 0.9
                else:
                    indicadora = random.randint(0,1)
                    i.x *= 1 + 0.1*indicadora
                    i.y *= 1 - 0.1*indicadora

        for l in subdivision["Fourth Quadrant"]:
            while check_availability(i, panel_size, polygon, restrictions, subdivision["Fourth Quadrant"]):
                if random.random(0,1) > epsilon:
                    i.x *= 0.9
                    i.y *= 0.9
                else:
                    indicadora = random.randint(0,1)
                    i.x *= 1 - 0.1*indicadora
                    i.y *= 1 - 0.1*indicadora

    return subdivision



solucion = {'first half': [(13.58, 7.27, (2, 4)), (12.6, 13.7, (2, 4)), (6.07, 23.93, (2, 4)), (17.94, 22.93, (2, 4)), (3.88, 22.29, (2, 4)), (9.17, 18.03, (2, 4)), (10.85, 7.53, (2, 4)), (21.0, 21.23, (2, 4)), (11.54, 28.81, (2, 4)), (17.83, 3.0, (2, 4)), (8.5, 6.63, (2, 4)), (17.58, 15.9, (2, 4)), (21.95, 9.81, (2, 4)), (7.46, 12.33, (2, 4)), (5.72, 16.87, (2, 4)), (13.57, 21.6, (2, 4)), (17.68, 7.72, (2, 4)), (22.12, 2.13, (2, 4)), (18.37, 28.33, (2, 4)), (8.3, 22.85, (2, 4)), (20.16, 15.47, (2, 4)), (3.34, 26.54, (2, 4)), (1.83, 20.7, (2, 4)), (15.6, 7.01, (2, 4)), (8.86, 28.22, (2, 4)), (14.29, 30.18, (2, 4)), (15.49, 12.33, (2, 4)), (9.95, 13.9, (2, 4)), (3.4, 15.87, (2, 4)), (6.15, 28.23, (2, 4)), (13.17, 3.24, (2, 4)), (11.45, 20.31, (2, 4)), (15.42, 2.16, (2, 4)), (20.71, 27.29, (2, 4)), (19.88, 3.67, (2, 4)), (5.4, 11.81, (2, 4)), (15.61, 21.95, (2, 4)), (1.06, 25.17, (2, 4)), (16.31, 29.59, (2, 4)), (14.83, 16.68, (2, 4)), (10.64, 3.4, (2, 4))], 'second half': [(34.71, 26.27, (2, 4)), (44.3, 10.2, (2, 4)), (35.34, 9.64, (2, 4)), (22.6, 15.68, (2, 4)), (37.53, 11.53, (2, 4)), (31.7, 29.44, (2, 4)), (24.89, 28.01, (2, 4)), (26.77, 13.24, (2, 4)), (31.77, 8.56, (2, 4)), (29.28, 18.03, (2, 4)), (30.35, 24.13, (2, 4)), (40.82, 16.59, (2, 4)), (28.5, 28.53, (2, 4)), (35.77, 2.92, (2, 4)), (28.14, 9.1, (2, 4)), (30.14, 13.3, (2, 4)), (40.78, 12.15, (2, 4)), (23.27, 23.5, (2, 4)), (33.15, 14.22, (2, 4)), (39.99, 4.38, (2, 4)), (35.3, 17.2, (2, 4)), (29.05, 3.35, (2, 4)), (38.36, 20.84, (2, 4)), (35.31, 22.17, (2, 4)), (33.54, 2.21, (2, 4)), (43.15, 16.28, (2, 4)), (26.12, 9.21, (2, 4)), (25.37, 4.01, (2, 4)), (32.66, 24.95, (2, 4)), (37.98, 4.85, (2, 4)), (31.19, 4.46, (2, 4)), (33.07, 18.95, (2, 4)), (38.06, 16.64, (2, 4)), (24.75, 14.75, (2, 4)), (23.96, 8.54, (2, 4)), (25.66, 23.01, (2, 4)), (42.29, 6.67, (2, 4)), (28.11, 22.2, (2, 4)), (24.83, 18.87, (2, 4))]}
subdiv = subdivide(solucion)
reloc = relocation(subdiv)
