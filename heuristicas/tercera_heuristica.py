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
    subdivision = {}
    for array in arrays:
        if array.x > center.x and array.y > center.y:
            subdivision['First Quadrant'].append(array)
        elif array.x < center.x and array.y > center.y:
            subdivision['Second Quadrant'].append(array)
        elif array.x < center.x and array.y < center.y:
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
    for i in subdivision['First Quadrant']:
        #while !check_availability(i, panel_size, polygon, restrictions, subdivision['First Quadrant']):
            if random.random(0,1) > epsilon:
                i.x *= 0.9
                i.y *= 1.10
            else:
                indicadora = random.randint(0,1)
                i.x *= 1 - 0.10*indicadora
                i.y *= 1 + 0.10*indicadora
            
    for j in subdivision["Second Quadrant"]:
        #while !check_availability(i, panel_size, polygon, restrictions, subdivision["Second Quadrant"]):
            if random.random(0,1) > epsilon:
                i.x *= 1.1
                i.y *= 1.1
            else:
                indicadora = random.randint(0,1)
                i.x *= 1 + 0.1*indicadora
                i.y *= 1 + 0.1*indicadora 
    
    for k in subdivision["Third Quadrant"]:
        #while !check_availability(i, panel_size, polygon, restrictions, subdivision["Third Quadrant"]):
            if random.random(0,1) > epsilon:
                i.x *= 1.1
                i.y *= 0.9
            else:
                indicadora = random.randint(0,1)
                i.x *= 1 + 0.1*indicadora
                i.y *= 1 - 0.1*indicadora

    for l in subdivision["Fourth Quadrant"]:
        #while !check_availability(i, panel_size, polygon, restrictions, subdivision["Fourth Quadrant"]):
            if random.random(0,1) > epsilon:
                i.x *= 0.9
                i.y *= 0.9
            else:
                indicadora = random.randint(0,1)
                i.x *= 1 - 0.1*indicadora
                i.y *= 1 - 0.1*indicadora

    pass    


    