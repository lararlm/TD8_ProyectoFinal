from lectura_and_analisis.analisis import calculate_area
import random
from tqdm import tqdm

import copy

def optimize_area(opt_func,polygon,rectangles,pads_data,restrictions, minimum_rectangles_to_delete = 1, iterations = 100):
    optimal_rectangles = copy.deepcopy(rectangles)
    len_opt_rectangles = [len(rect) for rect in optimal_rectangles]
    optimal_area = calculate_area(polygon, len_opt_rectangles, pads_data)
    for _ in tqdm(range(iterations)):
        temporal_rectangles = copy.deepcopy(optimal_rectangles)
        for i in range(len(temporal_rectangles)):
            number_of_rectangles = random.randint(minimum_rectangles_to_delete,len(temporal_rectangles[i]))
            rectangles_to_remove = random.sample(temporal_rectangles[i], number_of_rectangles)
            for rect in rectangles_to_remove:
                temporal_rectangles[i].remove(rect)
        temporal_rectangles = opt_func(polygon,pads_data,restrictions,temporal_rectangles)
        len_temp_rectangles =  [len(rect) for rect in temporal_rectangles]
        temporal_area = calculate_area(polygon,len_temp_rectangles,pads_data)
        if temporal_area > optimal_area:
            print("Se encontro un mejor posicionamiento con un area total de :", temporal_area)
            optimal_rectangles = temporal_rectangles.copy()
            optimal_area = temporal_area
    return optimal_rectangles

            
        




