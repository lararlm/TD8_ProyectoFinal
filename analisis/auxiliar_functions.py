import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.patches
import math
from shapely.geometry import Point, Polygon 

def rotation(polygon, restrictions, angle = 0, rectangles = None, translation_vector = None):
    '''
        polygon: el poligono del mapa
        restrictions: Son las restricciones como coordenadas.
        angle: angulo de rotacion
        rectangles: rectangulos presentes en la solucion
        translation_vector: vector de translacion
    
    Esta funcion normaliza el poligono, las restricciones y los rectangulos y luego los rota a cierto angulo


    '''
    angle_rad = math.radians(angle)
    rotation_matrix = np.array([[math.cos(angle_rad), -math.sin(angle_rad)], 
                                [math.sin(angle_rad), math.cos(angle_rad)]])
    
    points = np.array(polygon)
    rotated_points = points @ rotation_matrix.T

    if translation_vector is None:
        min_x, min_y = rotated_points.min(axis=0)
        translation_vector = np.array([-min_x, -min_y])

    translated_points = rotated_points + translation_vector
    rotated_polygon = [tuple(point) for point in translated_points]

    rotated_restrictions = [restr @ rotation_matrix.T for restr in restrictions]
    translated_restrictions = [restr + translation_vector for restr in rotated_restrictions]
    rotated_restrictions_total = [[tuple(point) for point in restr] for restr in translated_restrictions]

    if rectangles:
        rectangles_rot =  [tuple(((rect @ rotation_matrix.T) + translation_vector).tolist()) for rect in rectangles]
        return rotated_polygon, rotated_restrictions_total, rectangles_rot, translation_vector
    
    return rotated_polygon, rotated_restrictions_total, translation_vector




def calculate_area(polygon, rectangles, rect_size):
    '''
        polygon: el poligono del mapa
        rectangles: son los rectangulos de la solucion.
        rect_size: los tamaños de los paneles
        Esta funcion calcula el porcentaje del area cubierta por los rectangulos en el mapa.

    '''
    count_rectangles = [len(rect) for rect in rectangles]
    area_polygon = Polygon(polygon)
    total_area = area_polygon.area
    cover_area = 0
    for i in range(len(count_rectangles)):
        count_rects = count_rectangles[i]
        cover_area += rect_size[i][0] * rect_size[i][1] * count_rects
    return cover_area / total_area



def change_dimensions(polygon,rect_size,restrictions,size_to_change, rectangles= None):
    new_rectangles = None
    if rectangles:
        new_rectangles = [[(x * size_to_change, y * size_to_change) for (x, y) in rectangle] for rectangle in rectangles]
    new_restrictions = [[(x * size_to_change, y * size_to_change) for (x, y) in restriction] for restriction in restrictions]
    new_polygon = [(x * size_to_change, y * size_to_change) for (x, y) in polygon]
    new_panel = [(x * size_to_change, y * size_to_change) for (x, y) in rect_size]
    return new_polygon,new_panel,new_restrictions,new_rectangles

