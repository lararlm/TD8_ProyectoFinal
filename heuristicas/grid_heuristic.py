import matplotlib.patches
import matplotlib.pyplot
import numpy as np  
import csv
import random
from tqdm import tqdm
from shapely.geometry import Point, Polygon 
import sys
import os
sys.path.append(os.path.abspath("TD8_ProyectoFinal/"))
import json

def solve(polygon, actual_rect, restrictions, rectangles, rect_size, rand, optimizing):
    """
    polygon: Representacion del mapa como un poligono.
    actual_rect: Tamaño actual del rectangulo que se esta utilizando para la grilla
    restrictions: Son las restricciones como coordenadas.
    rectangles: Son todos los rectangulos que ya estan puestos actualmente en la solución
    rect_size: Lista de los tamaños disponibles para los rectangulos.
    rand: True or false para aplicar la aleatoriedad de los movimientos
    optimizing: True or false para saber si el codigo esta siendo utilizado para optimizacion.

    """
    solution_num = 0
    change = False
    max_panel = 0 
    best_panels, best_array, best_indentation, best_offset_x, best_offset_y, best_centers = None, None, None, None, None, None

    original_polygon = np.array(polygon)
    min_x = original_polygon[:, 0].min()
    min_y = original_polygon[:, 1].min()
    max_x = original_polygon[:, 0].max()      
    max_y = original_polygon[:, 1].max()

    n_x = int(max_x // actual_rect[0] + actual_rect[0])
    n_y = int(max_y // actual_rect[1] + actual_rect[1])

    counter = 0
    failed_attempts = 0
    output_best =  []
    repetitions = 0

    for indentation in range(0, int(actual_rect[0])):
        for offset_x in range(-int(actual_rect[0]), int(actual_rect[0])):
            for offset_y in range(-int(actual_rect[1]), int(actual_rect[1])):
                counter += 1
                random_movements = [0,0,0]
                if failed_attempts == 30 and optimizing:
                    return best_centers
                if rand:
                    random_movements = np.random.normal(0,0.2,3)
                real_offset_x = offset_x + random_movements[0]
                real_offset_y = offset_y + random_movements[1]
                real_id = indentation + random_movements[2]
                change = False
                Array = generate_panel_arrays(n_x, n_y, actual_rect, real_id, real_offset_x, real_offset_y)
                okay_panels = contains_rectangles(Array, actual_rect, original_polygon)
                okay_panels, okay_centers = check_panels(okay_panels, actual_rect, rect_size, restrictions,rectangles)
                if len(okay_panels) == max_panel:
                    change = random.choices([True,False],[6,94])
                if len(okay_panels)> max_panel or change: 
                    max_panel = len(okay_panels)
                    best_indentation, best_offset_x, best_offset_y = indentation, offset_x, offset_y
                    best_centers = okay_centers
                    best_panels = okay_panels
                    best_array = Array
                    failed_attempts = 0
                else:
                    failed_attempts += 1

                if counter % 100 == 0:
                    if best_centers not in output_best:
                        output_best.append(best_centers)
                    else:
                        repetitions += 1 
                        if repetitions == 3:
                            return best_centers
                        else:
                            break

                if failed_attempts == 30:
                    break

    return  best_centers

def grid_heuristic(polygon, restrictions, rect_size,  rand = True, rectangles = None, optimizing = False):
    """
    polygon: Representacion del mapa como un poligono.
    restrictions: Son las restricciones como coordenadas.
    rect_size: Lista de los tamaños disponibles para los rectangulos.
    rand: True or false para aplicar la aleatoriedad de los movimientos
    rectangles: Son todos los rectangulos que ya estan puestos actualmente en la solución
    optimizing: True or false para saber si el codigo esta siendo utilizado para optimizacion.
    """
    counter = 0
    if not rectangles:
        rectangles = [[] for _ in range(len(rect_size))]
    for i in range(len(rect_size)):
        improvment = True
        while improvment:
            improvment = False
            actual_rect = rect_size[i]
            sub_rectangles = solve(polygon,actual_rect,restrictions,rectangles,rect_size,rand, optimizing)
            if sub_rectangles:
                counter += 1
                improvment = True
                rectangles[i].extend(sub_rectangles)
    return rectangles

## Funciones auxiliares

def contains_rectangle(x, y, rect_size, polygon):
    '''
    x: El valor de x del centro del rectangulo
    y: El valor de y del centro del rectangulo
    rect_size: Tamaño del rectangulo
    polygon: Representacion del mapa como un poligono
    restrictions: Son las restricciones como coordenadas.
    Esta funcion chequea que los rectangulos esten dentro del poligono.

    '''
    (dx, dy) = rect_size
    bbpath = matplotlib.path.Path(polygon) 
    result = bbpath.contains_points([(x, y), (x + dx, y), (x, y + dy), (x + dx, y + dy)])
    return np.all(result)

def check_center(center, restrictions):
    '''
    center: centro del rectangulo
    restrictions: Son las restricciones como coordenadas.

    Esta funcion revisa que el centro del rectangulo no este dentro de las restricciones
    '''
    for rest in restrictions:
        center_point = Point(center)
        fig_rest = Polygon(rest)
        is_in_rest = center_point.within(fig_rest)
        if is_in_rest:
            return False
    return True

def check_rectangles(center, actual_size, rect_size, rectangles):
    '''
    center: centro del rectangulo
    actual_size: tamaño del rectangulo actual
    rect_size: tamaño de todos los rectangulos.
    rectangles: rectangulos de la solucion

    Esta funcion revisa que el nuevo rectangulo no se choque con los rectangulos ya existentes.
    '''
    dx, dy = actual_size
    x, y = center
    width1, height1 = actual_size
    left1 = x - width1 / 2
    right1 = x + width1 / 2
    top1 = y - height1 / 2
    bottom1 = y + height1 / 2
    for i in range(len(rectangles)): 
        for center2 in rectangles[i]:  
            width1, height1 = rect_size[i]
            x2, y2 = center2
            left2 = x2 - width1 / 2
            right2 = x2 + width1 / 2
            top2 = y2 - height1 / 2
            bottom2 = y2 + height1 / 2
            
            if not (left1 >= right2 or left2 >= right1 or top1 >= bottom2 or top2 >= bottom1):
                return False
    return True

def contains_rectangles(Array, rect_size, polygon):
    '''
    Array: vector que se utiliza para representar la grilla
    rect_size; tamaños de todos los rectangulos
    rectangles: rectangulos de la solucion

    Esta funcion llama a contains rectangles para ver si los rectangulos generados entran dentro del poligono
    '''
    okay_panels  = [(x, y) for (x, y) in Array if contains_rectangle(x, y, rect_size, polygon)]
    return okay_panels


def generate_panel_arrays(nx, ny, rect_size, indentation, offset_x, offset_y):
    '''
    n_x: numero de rectangulos que entran en la grilla en el eje X
    n_y: numero de rectangulos que entran en la grilla en el eje y
    rect_size: tamaños de todos los rectangulos
    identation: valor que determina el patron de la grilla
    offset_x: valor que determina el movimiento de la grilla en el eje x
    offset_y: valor que determina el movimiento de la grilla en el eje y
    '''
    (dx, dy) = rect_size
    Array = [(i * rect_size[0] + indentation * j % dx + offset_x, j * rect_size[1] + offset_y) 
             for i in range(nx)
             for j in range(ny)]
    return Array 

def contains_rectangle(x, y, rect_size, polygon):
    '''
    x: valor de x del centro del rectangulo
    y: valor de y del centro del rectangulo
    rect_size; tamaños de todos los rectangulos
    poligon: representacion del mapa como un poligono

    Esta funcion chequea que un rectangulo generado ente dentro del poligono
    '''
    (dx, dy) = rect_size
    bbpath = matplotlib.path.Path(polygon) 
    result = bbpath.contains_points([(x, y), (x + dx, y), (x, y + dy), (x + dx, y + dy)])
    return np.all(result)



def check_panels(panels, actual_rect, rect_size, restrictions, rectangles):
    '''
    panels: son los rectangulos de la grilla que entran dentro del poligono
    actual_rect: tamaño actual del rectangulo
    rect_size: tamaños de todos los rectangulos
    restrictions: son las restricciones como coordenadas.

    Esta funcion revisa que los rectangulos que entren dentro del poligono no tengan el centro del rectangulo dentro de las restricciones 
    y que no se choquen con los rectangulos que ya estan en la solucion

    '''
    width, heigth = actual_rect
    true_panels = []
    true_centers = []
    for i in range(len(panels)):
        center = (panels[i][0] + width/2, panels[i][1] + heigth/2)
        if check_center(center,restrictions) and check_rectangles(center,actual_rect,rect_size,rectangles):
            true_panels.append(panels[i])
            true_centers.append(center)
    return true_panels, true_centers

    
        