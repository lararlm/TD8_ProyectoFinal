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
def initialize_population(pop_size, rectangles, outer_polygon):
    population = []
    outer_poly = Polygon(outer_polygon)

    for _ in range(pop_size):
        width, height = random.choice(rectangles)  # Randomly select a rectangle size
        attempts = 0
        
        while attempts < 100:  # Limit attempts to find a valid position
            # Generate random position for the center of the rectangle
            x, y = random_position_within_polygon(outer_polygon, (width, height))
            rectangle_polygon = create_rectangle_polygon(x, y, (width, height))

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

                
print(estimate_population_size([(0, 0), (10, 0), (10, 10), (0, 10)], [(2, 4)]))
population = initialize_population(12, [(2, 4)],[(0, 0), (10, 0), (10, 10), (0, 10)])
print(population)
print(calculate_fitness(population, [(0, 0), (10, 0), (10, 10), (0, 10)], [[(1, 1), (1, 2), (2,1)]]))


import matplotlib.pyplot as plt
from shapely.geometry import Polygon, box

def plot_polygon_and_rectangles(outer_polygon, rectangles):
    # Create a matplotlib figure
    fig, ax = plt.subplots()

    # Plot the outer polygon
    outer_poly = Polygon(outer_polygon)
    x, y = outer_poly.exterior.xy
    ax.fill(x, y, alpha=0.5, fc='lightblue', ec='black', label='Outer Polygon')

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
outer_polygon = [(0, 0), (10, 0), (10, 10), (0, 10)]  # Define your outer polygon
rectangles = [(5.41, 4.57, (2, 4)), (3.01, 3.33, (2, 4)), (7.62, 5.01, (2, 4)), (2.35, 7.96, (2, 4))]
# Now plot
plot_polygon_and_rectangles(outer_polygon, rectangles)
