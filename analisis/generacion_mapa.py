import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Polygon, box, Point
from shapely.plotting import plot_polygon

def fun_generacion_mapa(yacimiento_coords, restricciones_data, rectangles, rect_size):
    # Plotting the extracted data
    plt.figure(figsize=(10, 8))

    # Plot Yacimiento (polygon)
    if yacimiento_coords:
        yac_x, yac_y = zip(*yacimiento_coords)
        plt.plot(yac_x, yac_y, 'bo-', label='Yacimiento')

    # Plot Restricciones (obstacle polygons)
    for restriccion in restricciones_data:
        if restriccion:
            restriccion_x, restriccion_y = zip(*restriccion)
            plt.plot(restriccion_x, restriccion_y, 'ro-')

    # Plot Pads as rectangles
    for n in range(len(rectangles)):
        for i, rect in enumerate(rectangles[n]):
            if rect:  # Ensure the rectangle data is not empty
                width, height = rect_size[n]
                # Expecting rect to be a tuple or list: (center_x, center_y, width, height)
                # Calculate the bottom left corner of the rectangle
                center_x, center_y = rect
                bottom_left_x = center_x - width/2
                bottom_left_y = center_y - height/2
                # Create the rectangle patch
                rectangle = patches.Rectangle((bottom_left_x, bottom_left_y), width, height,
                                            linewidth=1, edgecolor='g', facecolor='y')
                plt.gca().add_patch(rectangle)
                plt.plot(center_x, center_y, 'rx', label='Center' if i == 0 else "")

    # Optionally, you can plot Semilla (Pads) information as rectangles or points
    # Here, we'll plot them as points
    # Plot Pads as rectangles
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Yacimiento, Semilla, and Restricciones Visualization')
    plt.legend()

    # Display the plot
    plt.grid(True)
    plt.show()

def plot_solution(main_polygon_coords, restriction_polygons_coords, new_rects, panel_size):
    placed_rectangles = []
    if new_rects:
        placed_rectangles = inverse_answer_conversion(new_rects, panel_size)
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect("equal", adjustable="box")

    # Plot the main polygon
    main_polygon = Polygon(main_polygon_coords)
    plot_polygon(main_polygon, ax=ax, add_points=False, color='lightblue', alpha=0.5, label='Yacimiento')

    # Plot restriction polygons
    for i, restriction_coords in enumerate(restriction_polygons_coords):
        restriction_polygon = Polygon(restriction_coords)
        plot_polygon(restriction_polygon, ax=ax, color='red', alpha=0.5, label=f'Restricciones' if i == 0 else "")

    # Plot placed rectangles and their centers
    centers = []
    for i, rect in enumerate(placed_rectangles):
        x, y = rect.exterior.xy
        ax.plot(x, y, color='darkblue', alpha=0.7, linewidth=2, solid_capstyle='round', label=f'Máquinas de extracción' if i == 0 else "")
        ax.fill(x, y, color='darkblue', alpha=0.3)

        # Calculate the center point of the rectangle
        center_x = rect.centroid.x
        center_y = rect.centroid.y
        centers.append((center_x, center_y))
        ax.plot(center_x, center_y, marker = "o", color = 'darkblue', markersize=5)  

    # Set plot labels and legend
    ax.set_title('Solución')
    ax.legend()
    ax.grid()
    plt.show()


def inverse_answer_conversion(new_rects, panel_size):
    rectangles_placed = []
    width_1, height_1 = panel_size[0]
    if len(panel_size) == 2:
        width_2 , height2 = panel_size[1]
        for centroid_coords in new_rects[0]:
            x, y = centroid_coords
            # Create a rectangle (polygon) centered at (x, y)
            rectangle = Polygon([
                (x - width_1 / 2, y - height_1 / 2),
                (x + width_1 / 2, y - height_1 / 2),
                (x + width_1 / 2, y + height_1 / 2),
                (x - width_1 / 2, y + height_1 / 2)
            ])
            rectangles_placed.append(rectangle)
        for centroid_coords in new_rects[1]:
            x, y = centroid_coords
            # Create a rectangle (polygon) centered at (x, y)
            rectangle = Polygon([
                (x - width_2 / 2, y - height2 / 2),
                (x + width_2 / 2, y - height2 / 2),
                (x + width_2 / 2, y + height2 / 2),
                (x - width_2 / 2, y + height2 / 2)
            ])
            rectangles_placed.append(rectangle)
    elif len(panel_size) == 1:
        for centroid_coords in new_rects[0]:
            x, y = centroid_coords
            # Create a rectangle (polygon) centered at (x, y)
            rectangle = Polygon([
                (x - width_1 / 2, y - height_1 / 2),
                (x + width_1 / 2, y - height_1 / 2),
                (x + width_1 / 2, y + height_1 / 2),
                (x - width_1 / 2, y + height_1 / 2)
            ])
            rectangles_placed.append(rectangle)

    return rectangles_placed
