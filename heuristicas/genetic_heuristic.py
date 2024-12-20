import random
import sys
import os
sys.path.append(os.path.abspath("C:/Users/juani/OneDrive/Escritorio/Facultad/TD8FINAL/TD8"))
from lectura_and_analisis.analisis import calculate_area
from shapely.geometry import Polygon, Point, box, LineString
import matplotlib.pyplot as plt
from tqdm import tqdm
import matplotlib.patches
import numpy as np  
import csv
import math
from shapely.geometry import Point, Polygon 
from lectura_and_analisis.generacion_mapa import fun_generacion_mapa
from lectura_and_analisis.xml_parsing import xml_data_extractor
from lectura_and_analisis.analisis_copy import check_availability
from heuristicas.grid_heuristic import *


def subdivide(arrays, center):
    subdivision = {
        'First Quadrant': [],
        'Second Quadrant': [],
        'Third Quadrant': [],
        'Fourth Quadrant': []
    }
    for array in arrays:
        if array[0] > center[0] and array[1] > center[1]:
            subdivision['First Quadrant'].append(array)
        elif array[0] < center[0] and array[1] > center[1]:
            subdivision['Second Quadrant'].append(array)
        elif array[0] < center[0] and array[1] < center[1]:
            subdivision['Third Quadrant'].append(array)
        elif array[0] > center[0] and array[1] < center[1]:
            subdivision['Fourth Quadrant'].append(array)
    
    return subdivision  

def relocation(subdivision, panel_size, polygon, restrictions, center, panel_dimensions, epsilon:float = 0.1):
    ''' Precondición: los centros de los paneles ya estan subdivididos relativo al centro del poligono
    '''
    for _ in range (3):
        for i in subdivision['First Quadrant']:
            while not any(overlap(i, existing_rect) for existing_rect in subdivision['First Quadrant']):
                if random.random() > epsilon:
                    i[0] *= 0.9
                    i[1] *= 1.10
                    print("relocation happening!")
                else:
                    indicadora = random.randint(0,1)
                    i[0] *= 1 - 0.10*indicadora
                    i[1] *= 1 + 0.10*indicadora
                    print("relocation happening!")

        for j in subdivision["Second Quadrant"]:
            while not any(overlap( j, existing_rect) for existing_rect in subdivision["Second Quadrant"]):
                if random.random() > epsilon:
                    j[0] *= 1.1
                    j[1] *= 1.1
                    print("relocation happening!")
                else:
                    indicadora = random.randint(0,1)
                    j[0] *= 1 + 0.1*indicadora
                    j[1] *= 1 + 0.1*indicadora 
                    print("relocation happening!")

        for k in subdivision["Third Quadrant"]:
            while not any(overlap(k, existing_rect) for existing_rect in subdivision["Third Quadrant"]):
                if random.random() > epsilon:
                    k[0] *= 1.1
                    k[1] *= 0.9
                else:
                    indicadora = random.randint(0,1)
                    k[0] *= 1 + 0.1*indicadora
                    k[1] *= 1 - 0.1*indicadora

        for l in subdivision["Fourth Quadrant"]:
            while not any(overlap(l, existing_rect) for existing_rect in subdivision["Fourth Quadrant"]):
                if random.random() > epsilon:
                    l[0] *= 0.9
                    l[1] *= 0.9
                    print("relocation happening!")
                else:
                    indicadora = random.randint(0,1)
                    l[0] *= 1 - 0.1*indicadora
                    l[1] *= 1 - 0.1*indicadora

    
    return subdivision

def dissolve(subdivision):
    original = []
    for key in subdivision:
        original.extend(subdivision[key]) 
    return original

def overlap(rect1, rect2):
    x1, y1, (w1, h1) = rect1
    x2, y2, (w2, h2) = rect2

    return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)

def initialize_population(pop_size, rectangles, outer_polygon, restriction_polygons):
    population = []
    outer_poly = Polygon(outer_polygon)
    occupied_positions = set()  

    for _ in range(pop_size):
        width, height = random.choice(rectangles)  
        attempts = 0 

        while attempts < 1000: 
            x, y = random_position_within_polygon(outer_polygon, (width, height))
            rectangle_polygon = create_rectangle_polygon(x, y, (width, height))
            rectangle = (x, y, (width, height))  

           
            if outer_poly.contains(rectangle_polygon):
                if (not is_center_in_restriction(rectangle_polygon, restriction_polygons) and 
                    not any(overlap(rectangle, existing_rect) for existing_rect in population)):
                    population.append((round(x, 2), round(y, 2), (width, height)))
                    occupied_positions.add(rectangle)  

            attempts += 1
    return population


def estimate_population_size(outer_polygon, rectangle_sizes):
    poly = Polygon(outer_polygon)
    poly_area = poly.area
    
    area_per_rectangle = sum(width * height for width, height in rectangle_sizes)
    avg_area_per_rectangle = area_per_rectangle / len(rectangle_sizes) if rectangle_sizes else 0  

    if avg_area_per_rectangle > 0:
        estimated_pop_size = int(poly_area / avg_area_per_rectangle)
    else:
        return 0  
    return estimated_pop_size



def random_position_within_polygon(outer_polygon, rect):
    outer_poly = Polygon(outer_polygon)
    min_x, min_y, max_x, max_y = outer_poly.bounds
    width, height = rect

    x = random.uniform(min_x + width / 2, max_x - width / 2)
    y = random.uniform(min_y + height / 2, max_y - height / 2)
    
    return round(x, 2), round(y, 2)


def create_rectangle_polygon(x, y, rect):
    width, height = rect
    return box(x - width / 2, y - height / 2, x + width / 2, y + height / 2)


def overlaps(x, y, width, height, existing_rect):
    new_rect = box(x - width / 2, y - height / 2, x + width / 2, y + height / 2)
    
    ex, ey, (ew, eh) = existing_rect 
    existing_rect_polygon = box(ex - ew / 2, ey - eh / 2, ex + ew / 2, ey + eh / 2) 
     
    return new_rect.intersects(existing_rect_polygon)


def overlaps_restrictions(rectangle_polygon, restriction_polygons):
    for restriction in restriction_polygons:
        if rectangle_polygon.intersects(Polygon(restriction)):
            return True
    return False


def is_center_in_restriction(rectangle_polygon, restriction_polygons):
    center = rectangle_polygon.centroid
    for restriction in restriction_polygons:
        if Point(center).within(Polygon(restriction)):
            return True
    return False




def calculate_fitness(individual, outer_polygon, restriction_polygons):
    fitness = 0
    outer_poly = Polygon(outer_polygon)
    edge = LineString(outer_polygon)
    print("this individual has the form: ", individual)
    for (x, y, rect) in individual:
        rectangle_polygon = create_rectangle_polygon(x, y, rect)

        if outer_poly.contains(rectangle_polygon):
            distance_to_edge = edge.distance(Point(x, y))
            edge_reward = max(0, 1 / distance_to_edge) 

            overlap_penalty = 0
            proximity_reward = 0

            
            for (x2, y2, rect2) in individual:
                if (x, y) != (x2, y2): 
                    rectangle_polygon2 = create_rectangle_polygon(x2, y2, rect2)
                    if rectangle_polygon.intersects(rectangle_polygon2):
                        overlap_penalty += 1000000  
                    else:
                        dist = np.linalg.norm([x - x2, y - y2])
                        if dist > 0 and dist <= 0.3*rectangle_polygon.area:
                            proximity_reward += max(0, 1 / dist)  

            fitness += rect[0] * rect[1] + edge_reward + proximity_reward - overlap_penalty
        else:
            fitness -= 10000 

    return fitness



def plot_polygon_and_rectangles(outer_polygon, rectangles, restrictions):
    fig, ax = plt.subplots()

    outer_poly = Polygon(outer_polygon)
    x, y = outer_poly.exterior.xy
    ax.fill(x, y, alpha=0.5, fc='lightblue', ec='black', label='Outer Polygon')

    for pol in restrictions:
        pol = Polygon(pol)
        x, y = pol.exterior.xy
        ax.fill(x, y, alpha=0.5, fc='blue', ec='black', label='Restriction')

    for rect in rectangles:
        x_center, y_center, (width, height) = rect
        rectangle_polygon = create_rectangle_polygon(x_center, y_center, (width, height))
        x_rect, y_rect = rectangle_polygon.exterior.xy
        ax.fill(x_rect, y_rect, alpha=0.5, fc='orange', ec='black', label='Rectangle')

    ax.set_aspect('equal')
    plt.show()


def selection(population, fitness_scores, num_select):
    sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]
    return sorted_population[:num_select]


def crossover(parent1, parent2):

    child1 = {
        "First Quadrant": parent1["First Quadrant"], 
        "Second Quadrant": parent2["Second Quadrant"],
        "Third Quadrant": parent1["Third Quadrant"],
        "Fourth Quadrant": parent2["Fourth Quadrant"]
    }
    
    child2 = {
        "First Quadrant": parent2["First Quadrant"], 
        "Second Quadrant": parent1["Second Quadrant"],
        "Third Quadrant": parent2["Third Quadrant"],
        "Fourth Quadrant": parent1["Fourth Quadrant"]
    }

    dissolved_child1 = dissolve(child1)
    dissolved_child2 = dissolve(child2)
    
    dissolved_child1 = resolve_conflicts(dissolved_child1)
    dissolved_child2 = resolve_conflicts(dissolved_child2)
    print("Child1 has ", child1["First Quadrant"][0], " as first coordinate.")

    return dissolved_child1, dissolved_child2

def mutate(individual, outer_polygon, restriction_polygons, tipo):
    outer_poly = Polygon(outer_polygon)
    placed_rectangles = [create_rectangle_polygon(x, y, (w, h)) for (x, y, (w, h)) in individual]
    print(type(placed_rectangles[0]))
    mutations = 0
    for i, (x, y, rect) in enumerate(individual):
        width, height = rect
        if tipo == 1:
            for j in range(1000):
                dx, dy = np.random.uniform(-2, 2), np.random.uniform(-2, 2)
                new_x, new_y = x + dx, y + dy
                new_rect = create_rectangle_polygon(new_x, new_y, (width, height))
                new_rect_poly = Polygon(new_rect)

                if outer_poly.contains(Polygon(new_rect_poly)) and not any(Polygon(r).intersects(new_rect_poly) is not None for r in restriction_polygons) and not any(new_rect_poly.intersects(Polygon(exist)) is not None for exist in placed_rectangles):
                    individual[i] = (new_x, new_y, (width, height))
                    placed_rectangles[i] = new_rect_poly  
                    mutations += 1
                if mutations == 5:
                    break

        if tipo == 2:
            for k in range(1000):
                new_x, new_y = random_position_within_polygon(outer_polygon, rect)
                new_rect = create_rectangle_polygon(new_x, new_y, (width, height))
                new_rect_poly = Polygon(new_rect)
                if outer_poly.contains(new_rect_poly) and not any(Polygon(r).intersects(new_rect_poly) for r in restriction_polygons) and not any(new_rect_poly.intersects(exist) for exist in placed_rectangles):
                    individual[i] = (new_x, new_y, (width, height))
                    placed_rectangles[i] = new_rect_poly 
                    mutations += 1
                if mutations == 5:
                    break
    print("there were " + str(mutations) + " mutations")
    print("the structure of the individuals is effectively preserved in mutation: ", individual[0])
    return individual
            
def dissolve(subdivision):  

    original = []
    for quadrant in subdivision.values():
        original.extend(quadrant)  
    print("the structure of the individuals is effectively preserved in dissolution: ", original[0])
    return original

def resolve_conflicts(rect_list): 

    valid_rectangles = []
    
    for rect in rect_list:
        x, y, (width, height) = rect
        rectangle_polygon = create_rectangle_polygon(x, y, (width, height))
        
        if not any(overlap(rect, valid_rect) for valid_rect in valid_rectangles):
            valid_rectangles.append(rect)
    print("the structure of the individuals is effectively preserved after resolving conflicts ", valid_rectangles[0])       
    return valid_rectangles


def center(arrays):
    np_points = np.array([array[:2] for array in arrays])
    
    center_x, center_y = np.mean(np_points, axis=0)
    
    return round(center_x, 2), round(center_y, 2)

 
def gen_algo(pop_size, generations, outer_polygon, restrictions, panel_dimensions):
    centro = center(outer_polygon)
    estimated_size = estimate_population_size(outer_polygon, panel_dimensions)
    generation = []
    for _ in range(pop_size):
        generation.append(initialize_population(estimated_size, panel_dimensions, outer_polygon, restrictions))
        print("generation incoming...", generation)
    for _ in tqdm(range(generations), desc="Generations Progress"):
        fitnesses = [calculate_fitness(pop, outer_polygon, restrictions) for pop in generation]
        best = selection(generation, fitnesses, pop_size // 2)

        new_population = []
        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(best, 2)
            parent1 = relocation(subdivide(parent1, centro), parent1[0][2], outer_polygon, restrictions, center(parent1), panel_dimensions)
            parent2 = relocation(subdivide(parent2, centro), parent2[0][2], outer_polygon, restrictions, center(parent2), panel_dimensions)
            child1, child2 = crossover(parent1, parent2)
            child1_mutated = mutate(child1, outer_polygon, restrictions, 1)
            child2_mutated = mutate(child2, outer_polygon, restrictions, 2)

            new_population.extend([child1_mutated, child2_mutated])
        generation = new_population

    final_fitness_scores = [calculate_fitness(ind, outer_polygon, restrictions) for ind in generation]
    print("final fitness scores?: ", final_fitness_scores)
    best_solution = generation[final_fitness_scores.index(max(final_fitness_scores))]

    return best_solution, max(final_fitness_scores)

def grid_heuristic(polygon, panel_size, restrictions, rectangles, rand = True):
    for i in range(len(panel_size)):
        improvment = True
        while improvment:
            improvment = False
            actual_panel = panel_size[i]
            sub_rectangles = solve(polygon,actual_panel,restrictions,rectangles,panel_size,rand)
            if sub_rectangles:
                improvment = True
                rectangles[i].extend(sub_rectangles)
    return rectangles

polygon = xml_data_extractor("TD8\mapas\pol.1s.00.xml")
restrictions = [[(9.0, 22.0), (9.0, 25.0), (12.0, 28.0), (16.0, 29.0), (17.0, 27.0), (12.0, 23.0), (9.0, 22.0)], [(25.0, 22.0), (27.0, 25.0), (29.0, 27.0), (30.0, 25.0), (27.0, 21.0), (25.0, 22.0)], [(25.0, 22.0), (27.0, 21.0), (29.0, 17.0), (27.5, 15.0), (25.0, 17.0), (25.0, 22.0)], [(16.0, 11.0), (17.0, 13.0), (24.0, 8.0), (27.0, 5.0), (26.0, 4.0), (19.0, 7.0), (16.0, 11.0)]]
sol, fit = gen_algo(10, 10, polygon,restrictions, [(2, 4)])
print(calculate_area(polygon, [len(sol)], [(2, 4)]))
solution = grid_heuristic(polygon, [(2, 4)], restrictions, sol)
print(solution)

#IMPRIMIMOS LA SOLUCIÓN
plot_polygon_and_rectangles(polygon, solution, restrictions)