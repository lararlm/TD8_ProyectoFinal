import matplotlib.pyplot as plt
from shapely.geometry import Polygon, box, Point
from shapely.plotting import plot_polygon
import numpy as np
import sys
import os
sys.path.append(os.path.abspath("TD8FINAL/TD8_ProyectoFinal/"))
from heuristicas.grid_heuristic import grid_heuristic
from analisis.xml_parsing import xml_data_extractor
from analisis.optimization_functions import optimize_area
from shapely.affinity import rotate

def paint_heuristic(main_polygon_coords, restriction_polygons_coords, panel_size, angle=0, optimizing = False):
    if len(panel_size)==2:
        rectangle_size = panel_size[1]
    else:
        rectangle_size = panel_size[0]

    rectangle_size = rectangle_size[::-1]

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

    placed_rectangles = answer_conversion(placed_rectangles,len(panel_size))

    return placed_rectangles


def answer_conversion(rectangles_placed, panels):
    if panels == 2:
        new_rects = [[], []]
        for polygon in rectangles_placed:
            centroid = polygon.centroid
            new_rects[1].append((centroid.x, centroid.y))
    if panels == 1:
        new_rects = [[]]
        for polygon in rectangles_placed:
            centroid = polygon.centroid
            new_rects[0].append((centroid.x, centroid.y))

    return new_rects

from shapely.geometry import Point, Polygon

