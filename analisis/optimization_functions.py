from analisis.auxiliar_functions import calculate_area

import random
from tqdm import tqdm

import copy

def optimize_area(opt_func, polygon, rectangles, panel_size, restrictions, minimum_rectangles_to_delete = 1, iterations = 100):
    optimal_rectangles = copy.deepcopy(rectangles)
    len_opt_rectangles = [len(rect) for rect in optimal_rectangles]
    optimal_area = calculate_area(polygon, len_opt_rectangles, panel_size)

    for i in tqdm(range(iterations)):
        temporal_rectangles = copy.deepcopy(optimal_rectangles)
        for i in range(len(temporal_rectangles)):
            if len(temporal_rectangles[i]) == 0:
                continue
            number_of_rectangles = random.randint(minimum_rectangles_to_delete,len(temporal_rectangles[i]))
            rectangles_to_remove = random.sample(temporal_rectangles[i], number_of_rectangles)
            for rect in rectangles_to_remove:
                temporal_rectangles[i].remove(rect)
        temporal_rectangles = opt_func(polygon,panel_size,restrictions,temporal_rectangles, optimizing = True)
        len_temp_rectangles =  [len(rect) for rect in temporal_rectangles]
        temporal_area = calculate_area(polygon, len_temp_rectangles,panel_size)
        if temporal_area > optimal_area:
            print("Se encontro un mejor posicionamiento con un area total de :", temporal_area)
            optimal_rectangles = temporal_rectangles.copy()
            optimal_area = temporal_area
        if i%10 == 0:
            print(optimal_rectangles)
    return optimal_rectangles

            
        

