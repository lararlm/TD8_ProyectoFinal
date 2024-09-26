import random
from shapely.geometry import Polygon, Point, box

# Estimate how many rectangles can fit inside the polygon
def estimate_population_size(outer_polygon, rectangle_sizes):
    poly = Polygon(outer_polygon)
    poly_area = poly.area
    
    total_area = sum(width * height for width, height in rectangle_sizes)
    avg_area_per_rectangle = total_area / len(rectangle_sizes) if rectangle_sizes else 0  # Avoid division by zero
    
    # Estimate the population size as the total polygon area divided by the average area per rectangle
    pop_size = int(poly_area / avg_area_per_rectangle) if avg_area_per_rectangle > 0 else 0
    
    return pop_size

# Initialize population with random rectangle placements
def initialize_population(pop_size, rectangles, outer_polygon, restriction_polygons):
    population = []
    outer_poly = Polygon(outer_polygon)

    for _ in range(pop_size):
        width, height = random.choice(rectangles)  # Randomly select a rectangle size
        attempts = 0
        
        while attempts < 100:  # Limit attempts to find a valid position
            # Generate random position for the center of the rectangle
            x, y = random_position_within_polygon(outer_polygon, (width, height))
            rectangle_polygon = create_rectangle_polygon(x, y, (width, height))

            # Ensure the center is not within any restriction polygon
            if is_center_in_restriction(rectangle_polygon, restriction_polygons):
                attempts += 1
                continue

            # Check if the rectangle is fully contained in the outer polygon
            if outer_poly.contains(rectangle_polygon):
                # Check for overlaps with existing rectangles
                if not any(overlaps(x, y, width, height, existing_rect) for existing_rect in population):
                    population.append((round(x, 2), round(y, 2), (width, height)))  # Store the center and dimensions
                    break  # Exit while loop when a valid position is found

            attempts += 1

    return population


def random_position_within_polygon(outer_polygon, rect):
    outer_poly = Polygon(outer_polygon)
    min_x, min_y, max_x, max_y = outer_poly.bounds
    width, height = rect

    # Randomly generate the center of the rectangle
    x = random.uniform(min_x + width / 2, max_x - width / 2)
    y = random.uniform(min_y + height / 2, max_y - height / 2)

    return round(x, 2), round(y, 2)

def create_rectangle_polygon(x, y, rect):
    width, height = rect
    return box(x - width / 2, y - height / 2, x + width / 2, y + height / 2)

def overlaps(x, y, width, height, existing_rect):
    # Calculate the corners of the new rectangle
    new_rect = box(x - width / 2, y - height / 2, x + width / 2, y + height / 2)
    
    # Existing rectangle corners
    ex, ey, (ew, eh) = existing_rect
    existing_rect_polygon = box(ex - ew / 2, ey - eh / 2, ex + ew / 2, ey + eh / 2)

    # Check for intersection between the new rectangle and the existing rectangle
    return new_rect.intersects(existing_rect_polygon)


def overlaps_restrictions(rectangle_polygon, restriction_polygons):
    # Check if the rectangle overlaps any of the restriction polygons
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
    
    for (x, y, rect) in individual:
        rectangle_polygon = create_rectangle_polygon(x, y, rect)
        
        # Check if the rectangle is within the outer polygon
        if outer_poly.contains(rectangle_polygon):
            # Penalty for rectangles with centers inside restriction polygons
            if is_center_in_restriction(rectangle_polygon, restriction_polygons):
                fitness -= 1000  # Deep penalty for center inside restriction
            
            # Penalty for overlapping rectangles
            overlap_penalty = 0
            for (x2, y2, rect2) in individual:
                if (x, y) != (x2, y2):  # Avoid self-comparison
                    rectangle_polygon2 = create_rectangle_polygon(x2, y2, rect2)
                    if rectangle_polygon.intersects(rectangle_polygon2):
                        overlap_penalty += 1000  # Deep penalty for overlap
            
            fitness += rect[0] * rect[1] - overlap_penalty  # Area of the rectangle minus overlap penalty
        else:
            fitness -= 1000  # Penalize if the rectangle is outside the outer polygon

    return fitness

                
#print(estimate_population_size([(0, 0), (10, 0), (10, 10), (0, 10)], [(2, 4)]))
#population = initialize_population(12, [(2, 4)],[(0, 0), (10, 0), (10, 10), (0, 10)])
#print(population)
#print(calculate_fitness(population, [(0, 0), (10, 0), (10, 10), (0, 10)], [[(1, 1), (1, 2), (2,1)]]))


import matplotlib.pyplot as plt
from shapely.geometry import Polygon, box

def plot_polygon_and_rectangles(outer_polygon, rectangles, restrictions):
    # Create a matplotlib figure
    fig, ax = plt.subplots()

    # Plot the outer polygon
    outer_poly = Polygon(outer_polygon)
    x, y = outer_poly.exterior.xy
    ax.fill(x, y, alpha=0.5, fc='lightblue', ec='black', label='Outer Polygon')

    for pol in restrictions:
        pol = Polygon(pol)
        x, y = pol.exterior.xy
        ax.fill(x, y, alpha=0.5, fc='blue', ec='black', label='Outer Polygon')

    # Plot each rectangle
    for rect in rectangles:
        x_center, y_center, (width, height) = rect
        rectangle_polygon = create_rectangle_polygon(x_center, y_center, (width, height))
        x_rect, y_rect = rectangle_polygon.exterior.xy
        ax.fill(x_rect, y_rect, alpha=0.5, fc='orange', ec='black', label='Rectangle')

    # Set equal aspect ratio
    ax.set_aspect('equal')
    
    # Show the plot
    plt.show()

# Example usage
#outer_polygon = [(0, 0), (10, 0), (10, 10), (0, 10)]  # Define your outer polygon
#population = initialize_population(12, [(2, 4)],outer_polygon)
# Now plot
#print(calculate_fitness(population, [(0, 0), (10, 0), (10, 10), (0, 10)], [[(1, 1), (1, 2), (2,1)]]))
#plot_polygon_and_rectangles(outer_polygon, population)


# Selection process: choosing the fittest individuals
def selection(population, fitness_scores, num_select):
    sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]
    return sorted_population[:num_select]

def crossover(parent1, parent2):
    split = len(parent1) // 2
    child1 = parent1[:split] + parent2[split:]
    child2 = parent2[:split] + parent1[split:]
    return child1, child2

from tqdm import tqdm

def gen_algo(pop_size, generations, outer_polygon, restrictions, rectangles):
    estimated_size = estimate_population_size(outer_polygon, rectangles)
    generation = []
    for _ in range(pop_size):
        generation.append(initialize_population(estimated_size, rectangles, outer_polygon, restrictions))

    # Use tqdm to track progress over generations
    for _ in tqdm(range(generations), desc="Generations Progress"):
        fitnesses = [calculate_fitness(pop, outer_polygon, restrictions) for pop in generation]
        best = selection(generation, fitnesses, pop_size // 2)

        new_population = []
        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(best, 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([child1, child2])
        
        generation = new_population

    # Get the best solution from the final population
    final_fitness_scores = [calculate_fitness(ind, outer_polygon, restrictions) for ind in generation]
    best_solution = generation[final_fitness_scores.index(max(final_fitness_scores))]

    return best_solution, max(final_fitness_scores)



#sol, fit = gen_algo(10, 100, [(0, 0), (10, 0), (10, 10), (0, 10)], [[(1, 1), (1, 2), (2,1)]], [(2, 4)])
#plot_polygon_and_rectangles(outer_polygon, sol)
#print(fit)

sol, fit = gen_algo(100, 100, [(10.0, 0.0), (0.0, 16.0), (0.0, 29.0), (12.0, 33.0), (33.0, 33.0), (46.0, 16.0), (46.0, 6.0), (38.0, 0.0), (10.0, 0.0)],[[(9.0, 22.0), (9.0, 25.0), (12.0, 28.0), (16.0, 29.0), (17.0, 27.0), (12.0, 23.0), (9.0, 22.0)], [(25.0, 22.0), (27.0, 25.0), (29.0, 27.0), (30.0, 25.0), (27.0, 21.0), (25.0, 22.0)], [(25.0, 22.0), (27.0, 21.0), (29.0, 17.0), (27.5, 15.0), (25.0, 17.0), (25.0, 22.0)], [(16.0, 11.0), (17.0, 13.0), (24.0, 8.0), (27.0, 5.0), (26.0, 4.0), (19.0, 7.0), (16.0, 11.0)]], [(2, 4)])
plot_polygon_and_rectangles([(10.0, 0.0), (0.0, 16.0), (0.0, 29.0), (12.0, 33.0), (33.0, 33.0), (46.0, 16.0), (46.0, 6.0), (38.0, 0.0), (10.0, 0.0)], sol, [[(9.0, 22.0), (9.0, 25.0), (12.0, 28.0), (16.0, 29.0), (17.0, 27.0), (12.0, 23.0), (9.0, 22.0)], [(25.0, 22.0), (27.0, 25.0), (29.0, 27.0), (30.0, 25.0), (27.0, 21.0), (25.0, 22.0)], [(25.0, 22.0), (27.0, 21.0), (29.0, 17.0), (27.5, 15.0), (25.0, 17.0), (25.0, 22.0)], [(16.0, 11.0), (17.0, 13.0), (24.0, 8.0), (27.0, 5.0), (26.0, 4.0), (19.0, 7.0), (16.0, 11.0)]])
print(fit)