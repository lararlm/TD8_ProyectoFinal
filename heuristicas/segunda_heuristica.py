import matplotlib.patches
import matplotlib.pyplot
import numpy as np
import random  
import csv
import math
from shapely.geometry import Point, Polygon 
import sys
import os
sys.path.append(os.path.abspath("TD8_ProyectoFinal/"))
from lectura_data.generacion_mapa import fun_generacion_mapa
from lectura_data.xml_parsing import xml_data_extractor
from triangulator.ear_clipping_method import triangulate

def initialize_heuristic(polygon, panel_size, restriccions, xml_file_path):
    triangles = triangulate(polygon)
    areas = []
    for trian in triangles:
        t_area = 0.5 * abs(
            trian[0][0] * (trian[1][1] - trian[2][1]) +
            trian[1][0] * (trian[2][1] - trian[0][1]) +
            trian[2][0] * (trian[0][1] - trian[1][1])
        )
        areas.append(t_area)
        
    total_area = sum(areas)
    rate_triangle = [t/total_area for t in areas]
    iterations = 1000
    rectangles = [[] for _ in range(len(panel_size))]
    for i in range(len(panel_size)):
        sub_rectangles = []
        sampled_elements = random.choices(triangles,rate_triangle, k = 1000)
        for element in sampled_elements:
            sample_point = point_on_triangle(element[0],element[1],element[2])
            if check_availability(sample_point,panel_size[i],panel_size,polygon,restriccions,rectangles):
                rectangles[i].append(sample_point)  
    cover_area = 0
    quantity_rect = []
    for i in range(len(rectangles)):
        aux_rects = len(rectangles[i])
        
        quantity_rect.append(aux_rects)
        print(panel_size[i])
        cover_area += panel_size[i][0]*panel_size[i][1]*aux_rects
    print(f"Rectangles: {quantity_rect} Area covered: {cover_area/total_area}")
    return rectangles

    
def point_on_triangle(pt1, pt2, pt3):
    """
    Random point on the triangle with vertices pt1, pt2 and pt3.
    """
    x, y = sorted([random.random(), random.random()])
    s, t, u = x, y - x, 1 - y
    return (s * pt1[0] + t * pt2[0] + u * pt3[0],
            s * pt1[1] + t * pt2[1] + u * pt3[1])


def check_availability(center, center_size, pads_data, polygon, restrictions, rectangles):
    # Step 1: Check if the rectangle is fully inside the polygon
    dx, dy = center_size
    x, y = center
    x_bl = x - dx / 2
    y_bl = y - dy / 2
    bbpath = matplotlib.path.Path(polygon) 
    result = bbpath.contains_points([
        (x_bl, y_bl),              
        (x_bl + dx, y_bl),          
        (x_bl, y_bl + dy),          
        (x_bl + dx, y_bl + dy)     
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
    width1, height1 = center_size
    left1 = x - width1 / 2
    right1 = x + width1 / 2
    top1 = y - height1 / 2
    bottom1 = y + height1 / 2
    for i in range(len(rectangles)): 
        for center2 in rectangles[i]:
            width1, height1 = pads_data[i]
            x2, y2 = center2
            left2 = x2 - width1 / 2
            right2 = x2 + width1 / 2
            top2 = y2 - height1 / 2
            bottom2 = y2 + height1 / 2
            
            if not (left1 >= right2 or left2 >= right1 or top1 >= bottom2 or top2 >= bottom1):
                return False
        
    return True


if __name__ == "__main__":

    # file_path_bony = 'C:/Users/valen/OneDrive/Escritorio/Bony/Di tella/TD8FINAL/TD8_ProyectoFinal/mapas/pol.01.xml'
    file_path_bony = 'C:/Users/valen/OneDrive/Escritorio/Bony/Di tella/TD8FINAL/TD8_ProyectoFinal/mapas/Entrada_v2.xml'
    polygon, pads_data, restrictions , angulo = xml_data_extractor(file_path_bony)
    rectangles = initialize_heuristic(polygon, pads_data, restrictions, file_path_bony)
    fun_generacion_mapa(polygon,restrictions,rectangles,pads_data)