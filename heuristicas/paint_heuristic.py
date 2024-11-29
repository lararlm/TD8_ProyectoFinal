import matplotlib.pyplot as plt
from shapely.geometry import Polygon, box, Point
from shapely.plotting import plot_polygon
import numpy as np
import sys
import os
sys.path.append(os.path.abspath("TD8FINAL/TD8_ProyectoFinal/"))
from heuristicas.grid_heuristic import grid_heuristic
from analisis.xml_parsing import xml_data_extractor
from analisis.optimization_functions import optimize_area
from shapely.affinity import rotate

def paint_heuristic(polygon, restrictions, rect_size, angle=0, optimizing = False):
    '''
    polygon: el poligono del mapa
    restrictions: restricciones del mapa
    rect_size: los tamaños de los paneles

    Esta es la funcion que implementa nuestra heuristica de pintado

    '''
    if len(rect_size)==2:
        rectangle_size = rect_size[1]
    else:
        rectangle_size = rect_size[0]

    rectangle_size = rectangle_size[::-1]

    main_polygon = Polygon(polygon)
    restriction_polygons = [Polygon(coords) for coords in restrictions]
    placed_rectangles = []
    min_y = min(y for x, y in polygon)
    height, width = rectangle_size

    current_y = min_y

    while True:
        leftmost_x_candidates = [x for x, y in main_polygon.exterior.coords]
        if not leftmost_x_candidates:
            break  
        
        leftmost_x = min(leftmost_x_candidates)
        current_x = leftmost_x  

        while True:

            new_rect = box(current_x, current_y, current_x + width, current_y + height)

            new_rect = rotate(new_rect, angle, origin='center')

            center_point = new_rect.centroid

            if main_polygon.contains(new_rect) and not any(restriction.contains(center_point) for restriction in restriction_polygons):
                placed_rectangles.append(new_rect)  
                current_x += width  
            else:
               
                found_spot = False
                for offset in np.arange(1, 1000):  
                    adjusted_x = current_x + offset

                    new_rect = box(adjusted_x, current_y, adjusted_x + width, current_y + height)
                    new_rect = rotate(new_rect, angle, origin='center')
                    center_point = new_rect.centroid

                    if main_polygon.contains(new_rect) and not any(restriction.contains(center_point) for restriction in restriction_polygons):
                        placed_rectangles.append(new_rect)  
                        current_x = adjusted_x + width  
                        found_spot = True
                        break

                
                if not found_spot:
                    break

        
        current_y += height 

       
        if current_y + height > max(y for _, y in polygon):
            break

    placed_rectangles = answer_conversion(placed_rectangles,len(rect_size))

    return placed_rectangles


def answer_conversion(rectangles_placed, quant_rect_types):
    '''
    rectangles_placed: rectangulos en la solucion en un formato de shapely
    quant_rect_types: cantidad de los tipos de rectangulos para el mapa

    Esta funcion transforma el formato de shapely al formato de coordenadas del centro del rectangulo que estuvimos usando en todo los codigos

    '''
    if quant_rect_types == 2:
        new_rects = [[], []]
        for polygon in rectangles_placed:
            centroid = polygon.centroid
            new_rects[1].append((centroid.x, centroid.y))
    if quant_rect_types == 1:
        new_rects = [[]]
        for polygon in rectangles_placed:
            centroid = polygon.centroid
            new_rects[0].append((centroid.x, centroid.y))

    return new_rects



