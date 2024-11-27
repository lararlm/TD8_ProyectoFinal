import sys
import os
from shapely.geometry import Polygon, Point, box
import matplotlib.pyplot as plt
import matplotlib.patches
import numpy as np  
import math

def rotation(polygon, restrictions, angle, rectangles = None, translation_vector = None):
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

# def translation(polygon, restrictions, translate, rectangles = None):
#     poly = np.array(polygon)
#     restr = np.array(restrictions)
#     min_x, min_y = poly.min(axis = 0)
#     minimos = np.array([min_x, min_y])
#     if translate == 1:
#         poly = poly - minimos
#         restr = [r - minimos for r in restr]
#         if rectangles != None:
#             pads = [rect - minimos for rect in rectangles]
#             restric = [tuple(j) for j in restr]
#             return list(poly), restric, pads

#     elif translate == -1:
#         min_x, min_y = poly.min(axis = 0)
#         poly = poly + minimos
#         restr = [r + minimos for r in restr]
#         if rectangles != None:
#             pads = [rect + minimos for rect in rectangles]
#             restric = [tuple(j) for j in restr]
#             return list(poly), restric, pads
#     else:
#         print("last parameter should be either 1 or -1")

#     restric = [tuple(j) for j in restr]
#     return list(poly), restric, minimos
    