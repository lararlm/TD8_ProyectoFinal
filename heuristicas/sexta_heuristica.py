import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import random
from shapely.geometry import Polygon, Point

from shapely.geometry import Polygon, Point
import random
import numpy as np

################

# Function to create a rectangle polygon based on its center and dimensions
def create_rectangle_polygon(x, y, width, height):
    return Polygon([
        (x - width / 2, y - height / 2),
        (x + width / 2, y - height / 2),
        (x + width / 2, y + height / 2),
        (x - width / 2, y + height / 2)
    ])


# Check for overlaps between a new rectangle and all existing rectangles
def has_overlap(new_rect, existing_rects):
    for rect in existing_rects:
        if new_rect.intersects(rect):
            return True
    return False

# Fitness function - Calculate how well the rectangles are placed
def calculate_fitness(individual, outer_polygon, restriction_polygons):
    outer_poly = Polygon(outer_polygon)
    fitness = 0
    placed_rectangles = []

    for (x, y, rectangle) in individual:
        width, height = rectangle
        rect_poly = create_rectangle_polygon(x, y, width, height)

        # Ensure the rectangle is inside the outer polygon and does not overlap any restricted areas or other rectangles
        if outer_poly.contains(rect_poly) and \
           not any(Polygon(r).intersects(rect_poly) for r in restriction_polygons) and \
           not has_overlap(rect_poly, placed_rectangles):
            fitness += rect_poly.area  # Reward for valid rectangle placement
            placed_rectangles.append(rect_poly)  # Add this rectangle to the placed ones
        else:
            fitness -= 1000  # Penalize invalid placement (overlap, restriction area, etc.)
    
    return fitness

# Initialize population without overlap and restriction issues
def initialize_population(outer_polygon, rectangles, restriction_polygons, num_individuals, num_rects):
    population = []
    outer_poly = Polygon(outer_polygon)
    minx, miny, maxx, maxy = outer_poly.bounds

    for _ in range(num_individuals):
        individual = []
        placed_rectangles = []

        for _ in range(num_rects):
            width, height = rectangles[0]

            for _ in range(100):  # Try up to 100 times to find a valid placement
                x = random.uniform(minx + width / 2, maxx - width / 2)
                y = random.uniform(miny + height / 2, maxy - height / 2)
                rect_poly = create_rectangle_polygon(x, y, width, height)

                # Ensure the rectangle does not overlap or fall inside restricted polygons
                center = Point(x, y)
                if outer_poly.contains(rect_poly) and \
                   all(not Polygon(r).contains(center) for r in restriction_polygons) and \
                   not has_overlap(rect_poly, placed_rectangles):
                    individual.append((x, y, (width, height)))
                    placed_rectangles.append(rect_poly)
                    break  # Valid position found; move to the next rectangle
        population.append(individual)

    return population

# Mutation - Adjust the position of a rectangle and check for validity
def mutate(individual, outer_polygon, restriction_polygons):
    outer_poly = Polygon(outer_polygon)
    placed_rectangles = [create_rectangle_polygon(x, y, w, h) for (x, y, (w, h)) in individual]

    for i, (x, y, rect) in enumerate(individual):
        width, height = rect

        for _ in range(10):
            dx, dy = np.random.uniform(-2, 2), np.random.uniform(-2, 2)
            new_x, new_y = x + dx, y + dy
            new_rect_poly = create_rectangle_polygon(new_x, new_y, width, height)

            # Ensure the new position is valid
            if outer_poly.contains(new_rect_poly) and \
               not any(Polygon(r).contains(Point(new_x, new_y)) for r in restriction_polygons) and \
               not has_overlap(new_rect_poly, placed_rectangles):
                individual[i] = (new_x, new_y, (width, height))
                placed_rectangles[i] = new_rect_poly  # Update placed rectangles
                break  # Valid mutation found

# Crossover - Combine two individuals
def crossover(parent1, parent2):
    mid_point = len(parent1) // 2
    child = parent1[:mid_point] + parent2[mid_point:]
    return child

# Genetic algorithm combining interior initialization, mutation, and crossover
def genetic_algorithm(outer_polygon, restriction_polygons, rectangles, num_generations=10, num_individuals=10, num_rects=60):
    population = initialize_population(outer_polygon, rectangles, restriction_polygons, num_individuals, num_rects)

    for generation in range(num_generations):
        # Evaluate fitness
        population_fitness = [
            (individual, calculate_fitness(individual, outer_polygon, restriction_polygons))
            for individual in population
        ]
        population_fitness.sort(key=lambda x: x[1], reverse=True)  # Sort by fitness
        
        # Select the top individuals to be parents
        parents = [individual for individual, fitness in population_fitness[:num_individuals // 2]]
        
        # Create the next generation
        new_population = []
        while len(new_population) < num_individuals:
            parent1, parent2 = random.choice(parents), random.choice(parents)
            child = crossover(parent1, parent2)
            mutate(child, outer_polygon, restriction_polygons)
            new_population.append(child)
        
        population = new_population

    # Return the best solution found
    best_individual = max(population, key=lambda ind: calculate_fitness(ind, outer_polygon, restriction_polygons))
    return best_individual



# Plotting the solution
def plot_solution(outer_polygon, restriction_polygons, best_individual):
    fig, ax = plt.subplots()
    
    # Plot the outer polygon
    outer_poly = Polygon(outer_polygon)
    x, y = outer_poly.exterior.xy
    ax.plot(x, y, 'b-', label='Outer Polygon')
    
    # Plot the restriction polygons
    for restriction in restriction_polygons:
        restr_poly = Polygon(restriction)
        rx, ry = restr_poly.exterior.xy
        ax.fill(rx, ry, color='red', alpha=0.5)
    
    # Plot the rectangles
    for (x, y, rect) in best_individual:
        width, height = rect
        rect_patch = Rectangle(
            (x - width / 2, y - height / 2),
            width,
            height,
            linewidth=1,
            edgecolor='green',
            facecolor='none'
        )
        ax.add_patch(rect_patch)

    ax.set_aspect('equal', 'box')
    plt.title('Rectangles Placed Inside the Outer Polygon')
    plt.legend(loc='upper right')
    plt.show()

# Example usage
outer_polygon = [
    (10.0, 0.0), (0.0, 16.0), (0.0, 29.0), (12.0, 33.0),
    (33.0, 33.0), (46.0, 16.0), (46.0, 6.0), (38.0, 0.0), (10.0, 0.0)
]
restriction_polygons = [
    [(9.0, 22.0), (9.0, 25.0), (12.0, 28.0), (16.0, 29.0), (17.0, 27.0), (12.0, 23.0), (9.0, 22.0)],
    [(25.0, 22.0), (27.0, 25.0), (29.0, 27.0), (30.0, 25.0), (27.0, 21.0), (25.0, 22.0)],
    [(25.0, 22.0), (27.0, 21.0), (29.0, 17.0), (27.5, 15.0), (25.0, 17.0), (25.0, 22.0)],
    [(16.0, 11.0), (17.0, 13.0), (24.0, 8.0), (27.0, 5.0), (26.0, 4.0), (19.0, 7.0), (16.0, 11.0)]
]
rectangles = [(2, 4)]  # Single rectangle size
num_rects = 100  # Number of rectangles to place

best_individual = genetic_algorithm(
    outer_polygon,
    restriction_polygons,
    rectangles,
    num_generations=50,
    num_individuals=8,
    num_rects=num_rects
)
print(f"Number of rectangles placed: {len(best_individual)}")
plot_solution(outer_polygon, restriction_polygons, best_individual)

