from analisis.auxiliar_functions import calculate_area

import random
from tqdm import tqdm

import copy

def optimize_area(opt_func, polygon, rectangles, rect_size, restrictions, minimum_rectangles_to_delete = 1, iterations = 100):
    '''
    opt_func: funcion que se va a utilizar para la optimizacion
    polygon: el poligono del mapa
    rectangles: son los rectangulos de la solucion.
    rect_size: los tamaños de los paneles
    restrictions: restricciones del mapa
    minimum_rectangles_to_delete: cantidad minima de rectangulos a eliminar
    iterations: cantidad de veces que se hace la busqueda local de eliminar

    Esta funcion es nuestra funcion de optimizacion que elimina rectangulos y llama a la opt_func.
    '''
    optimal_rectangles = copy.deepcopy(rectangles)
    optimal_area = calculate_area(polygon, optimal_rectangles, rect_size)

    for i in tqdm(range(iterations)):
        temporal_rectangles = copy.deepcopy(optimal_rectangles)
        for i in range(len(temporal_rectangles)):
            if len(temporal_rectangles[i]) == 0:
                continue
            number_of_rectangles = random.randint(minimum_rectangles_to_delete,len(temporal_rectangles[i]))
            rectangles_to_remove = random.sample(temporal_rectangles[i], number_of_rectangles)
            for rect in rectangles_to_remove:
                temporal_rectangles[i].remove(rect)
        temporal_rectangles = opt_func(polygon,restrictions, rect_size, temporal_rectangles, optimizing = True)
        temporal_area = calculate_area(polygon, temporal_rectangles,rect_size)
        if temporal_area > optimal_area:
            print("Se encontro un mejor posicionamiento con un area total de :", temporal_area)
            optimal_rectangles = temporal_rectangles.copy()
            optimal_area = temporal_area
    return optimal_rectangles

            
        

