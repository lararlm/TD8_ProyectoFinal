import numpy as np
import random  
import math
from shapely.geometry import Point, Polygon 
import sys
import os
sys.path.append(os.path.abspath("TD8_ProyectoFinal/"))
from lectura_data.generacion_mapa import fun_generacion_mapa
from lectura_data.xml_parsing import xml_data_extractor
from lectura_data.analisis import check_availability
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



if __name__ == "__main__":

    # file_path_bony = 'C:/Users/valen/OneDrive/Escritorio/Bony/Di tella/TD8FINAL/TD8_ProyectoFinal/mapas/pol.01.xml'
    file_path_bony = 'C:/Users/valen/OneDrive/Escritorio/Bony/Di tella/TD8FINAL/TD8_ProyectoFinal/mapas/Entrada_v2.xml'
    polygon, pads_data, restrictions , angulo = xml_data_extractor(file_path_bony)
    rectangles = initialize_heuristic(polygon, pads_data, restrictions, file_path_bony)
    fun_generacion_mapa(polygon,restrictions,rectangles,pads_data)