import matplotlib.pyplot as plt
from shapely.geometry import Polygon, box, Point
from shapely.plotting import plot_polygon
import numpy as np
import sys
import os
sys.path.append(os.path.abspath("TD8_ProyectoFinal/"))
from lectura_and_analisis.xml_parsing import xml_data_extractor
from lectura_and_analisis.optimization_functions import optimize_area
from lectura_and_analisis.generacion_mapa import fun_generacion_mapa


from shapely.affinity import rotate

def place_rectangles(main_polygon_coords, restriction_polygons_coords, rectangle_size, angle=0):
    main_polygon = Polygon(main_polygon_coords)
    restriction_polygons = [Polygon(coords) for coords in restriction_polygons_coords]
    placed_rectangles = []

    # Find the minimum y-coordinate to start placing rectangles
    min_y = min(y for x, y in main_polygon_coords)
    height, width = rectangle_size

    # Start placing rectangles from the left-bottom corner
    current_y = min_y

    while True:
        # Calculate the leftmost x-coordinate in the current row area
        leftmost_x_candidates = [x for x, y in main_polygon.exterior.coords]
        if not leftmost_x_candidates:
            break  # Stop if no valid x-coordinates are found
        
        leftmost_x = min(leftmost_x_candidates)
        current_x = leftmost_x  # Reset current_x for each new row

        # Place rectangles in the current row
        while True:
            # Create a new rectangle at the current position
            new_rect = box(current_x, current_y, current_x + width, current_y + height)

            # Rotate the rectangle around its center by the specified angle
            new_rect = rotate(new_rect, angle, origin='center')

            # Calculate the center point of the rotated rectangle
            center_point = new_rect.centroid

            # Check if the rotated rectangle is fully inside the main polygon
            # and its center is not inside any restriction polygons
            if main_polygon.contains(new_rect) and not any(restriction.contains(center_point) for restriction in restriction_polygons):
                placed_rectangles.append(new_rect)  # Add the rectangle to the list of placed rectangles
                current_x += width  # Move the x-coordinate to the right for the next rectangle
            else:
                # If the rectangle cannot be placed, move it to the right incrementally
                found_spot = False
                for offset in np.arange(1, 1000):  # Adjust offset until a valid position is found or limit is reached
                    adjusted_x = current_x + offset

                    # Create a new rectangle at the adjusted position
                    new_rect = box(adjusted_x, current_y, adjusted_x + width, current_y + height)
                    # Rotate the rectangle
                    new_rect = rotate(new_rect, angle, origin='center')
                    center_point = new_rect.centroid

                    # Check again for placement
                    if main_polygon.contains(new_rect) and not any(restriction.contains(center_point) for restriction in restriction_polygons):
                        placed_rectangles.append(new_rect)  # Place the rectangle
                        current_x = adjusted_x + width  # Update current_x to the new position
                        found_spot = True
                        break

                # If no valid position was found after the maximum offset, break to the next row
                if not found_spot:
                    break

        # Move to the next row
        current_y += height  # Move up for the next row

        # If the new row exceeds the height of the main polygon, stop the process
        if current_y + height > max(y for _, y in main_polygon_coords):
            break

    # Return the list of placed rectangles
    return placed_rectangles


def plot_solution(main_polygon_coords, restriction_polygons_coords, placed_rectangles):
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))

    # Plot the main polygon
    main_polygon = Polygon(main_polygon_coords)
    plot_polygon(main_polygon, ax=ax, add_points=False, color='lightblue', alpha=0.5, label='Main Polygon')

    # Plot restriction polygons
    for i, restriction_coords in enumerate(restriction_polygons_coords):
        restriction_polygon = Polygon(restriction_coords)
        plot_polygon(restriction_polygon, ax=ax, color='red', alpha=0.5, label=f'Restriction {i+1}' if i == 0 else "")

    # Plot placed rectangles and their centers
    centers = []
    for i, rect in enumerate(placed_rectangles):
        x, y = rect.exterior.xy
        ax.plot(x, y, color='green', alpha=0.7, linewidth=2, solid_capstyle='round', label=f'Placed Rectangles' if i == 0 else "")
        ax.fill(x, y, color='green', alpha=0.3)

        # Calculate the center point of the rectangle
        center_x = rect.centroid.x
        center_y = rect.centroid.y
        centers.append((center_x, center_y))
        ax.plot(center_x, center_y, 'go', markersize=5)  # Plot the center as a red dot

    # Set plot labels and legend
    ax.set_title('Polygon with Restrictions and Placed Rectangles')
    ax.legend()
    plt.show()


from shapely.ops import unary_union

def compute_total_covered_area(placed_rectangles):
    # Merge all rectangles into a single geometry to handle overlaps
    merged_rectangles = unary_union(placed_rectangles)
    # Compute the area of the merged geometry
    total_area = merged_rectangles.area
    return total_area


def compute_coverage_ratio(placed_rectangles, main_polygon_coords):
    # Calculate the total area covered by the rectangles
    total_covered_area = compute_total_covered_area(placed_rectangles)
    
    # Create a Polygon object from the main polygon coordinates
    main_polygon = Polygon(main_polygon_coords)
    main_polygon_area = main_polygon.area
    
    # Compute the coverage ratio
    coverage_ratio = total_covered_area / main_polygon_area
    return coverage_ratio

def answer_conversion(rectangles_placed):
    new_rects = [[], []]
    for polygon in rectangles_placed:
        centroid = polygon.centroid
        new_rects[1].append((centroid.x, centroid.y))
    return new_rects



# Example usage
'''
outer_polygon =  [(10.0, 0.0), (0.0, 16.0), (0.0, 29.0), (12.0, 33.0), (33.0, 33.0), (46.0, 16.0), (46.0, 6.0), (38.0, 0.0), (10.0, 0.0)]

restriction_polygons = [[(9.0, 22.0), (9.0, 25.0), (12.0, 28.0), (16.0, 29.0), (17.0, 27.0), (12.0, 23.0), (9.0, 22.0)], [(25.0, 22.0), (27.0, 25.0), (29.0, 27.0), (30.0, 25.0), (27.0, 21.0), (25.0, 22.0)], [(25.0, 22.0), (27.0, 21.0), (29.0, 17.0), (27.5, 15.0), (25.0, 17.0), (25.0, 22.0)], [(16.0, 11.0), (17.0, 13.0), (24.0, 8.0), (27.0, 5.0), (26.0, 4.0), (19.0, 7.0), (16.0, 11.0)], [(20.0, 11.0), (21.0, 13.0), (17.0, 14.0), (18.0, 13.0), (20.0, 11.0)], [(32.0, 11.0), (37.0, 13.0), (36.0, 14.0), (31.0, 13.0), (32.0, 11.0)], [(34.0, 11.0), (41.0, 12.0), (42.0, 8.0), (33.0, 7.0), (34.0, 11.0)]]

rectangle_size = (4.0, 2.0)
'''

file_path_lari = 'C:/Users/44482978/Desktop/TD8/TD8FINAL/TD8_ProyectoFinal/mapas/pol.01.xml'
yacimiento_coords, pads_data, restricciones_data , angulo= xml_data_extractor(file_path_lari)
print(pads_data)
rectangle_size = (pads_data[len(pads_data) - 1][1], pads_data[len(pads_data) - 1][0])
print(rectangle_size)

# Place the rectangles along the bottom line
placed_rectangles = place_rectangles(yacimiento_coords, restricciones_data, rectangle_size, 0)
plot_solution(yacimiento_coords, restricciones_data, placed_rectangles)
coverage_ratio = compute_coverage_ratio(placed_rectangles, yacimiento_coords)
print(f"The ratio of the covered area to the polygon area is {coverage_ratio:.2%}.")


placed_rectangles = answer_conversion(placed_rectangles)
# Plot the solutio

# Example usage
new_result = optimize_area(place_rectangles, yacimiento_coords, placed_rectangles, pads_data, restricciones_data, 1, 10)

fun_generacion_mapa(yacimiento_coords, restricciones_data, placed_rectangles, rectangle_size)

