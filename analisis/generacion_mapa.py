import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Polygon, box, Point
from shapely.plotting import plot_polygon

def plot_solution(polygon, restrictions, rectangles, rect_size, rect_color = "darkblue"):
    '''
    polygon: el poligono del mapa
    restrictions: restricciones del mapa
    rectangles: son los rectangulos de la solucion.
    rect_size: los tamaños de los rectangulos
    rect_color: color de los rectangulos 

    Esta funcion grafica el mapa con los rectangulos y las restricciones.
    '''
    placed_rectangles = []
    if rectangles:
        placed_rectangles = inverse_answer_conversion(rectangles, rect_size)
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect("equal", adjustable="box")

    # Plot the main polygon
    main_polygon = Polygon(polygon)
    plot_polygon(main_polygon, ax=ax, add_points=False, color='lightblue', alpha=0.5, label='Yacimiento')

    # Plot restriction polygons
    for i, restriction_coords in enumerate(restrictions):
        restriction_polygon = Polygon(restriction_coords)
        plot_polygon(restriction_polygon, ax=ax, color='red', alpha=0.5, label=f'Restricciones' if i == 0 else "")

    # Plot placed rectangles and their centers
    centers = []
    for i, rect in enumerate(placed_rectangles):
        x, y = rect.exterior.xy
        ax.plot(x, y, color=rect_color, alpha=0.7, linewidth=2, solid_capstyle='round', label=f'Máquinas de extracción' if i == 0 else "")
        ax.fill(x, y, color=rect_color, alpha=0.3)

        # Calculate the center point of the rectangle
        center_x = rect.centroid.x
        center_y = rect.centroid.y
        centers.append((center_x, center_y))
        ax.plot(center_x, center_y, marker = "o", color = rect_color, markersize=5)  

    # Set plot labels and legend
    ax.set_title('Solución')
    ax.legend()
    ax.grid()
    plt.show()


def inverse_answer_conversion(rectangles, rect_size):
    rectangles_placed = []
    width_1, height_1 = rect_size[0]
    if len(rect_size) == 2:
        width_2 , height2 = rect_size[1]
        for centroid_coords in rectangles[0]:
            x, y = centroid_coords
            # Create a rectangle (polygon) centered at (x, y)
            rectangle = Polygon([
                (x - width_1 / 2, y - height_1 / 2),
                (x + width_1 / 2, y - height_1 / 2),
                (x + width_1 / 2, y + height_1 / 2),
                (x - width_1 / 2, y + height_1 / 2)
            ])
            rectangles_placed.append(rectangle)
        for centroid_coords in rectangles[1]:
            x, y = centroid_coords
            # Create a rectangle (polygon) centered at (x, y)
            rectangle = Polygon([
                (x - width_2 / 2, y - height2 / 2),
                (x + width_2 / 2, y - height2 / 2),
                (x + width_2 / 2, y + height2 / 2),
                (x - width_2 / 2, y + height2 / 2)
            ])
            rectangles_placed.append(rectangle)
    elif len(rect_size) == 1:
        for centroid_coords in rectangles[0]:
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
