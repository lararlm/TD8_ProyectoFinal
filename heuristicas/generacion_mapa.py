import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
    for i, rect in enumerate(rectangles):
        if rect:  # Ensure the rectangle data is not empty
            width, height = rect_size
            # Expecting rect to be a tuple or list: (center_x, center_y, width, height)
            # Calculate the bottom left corner of the rectangle
            center_x, center_y = rect
            bottom_left_x = center_x - width/2
            bottom_left_y = center_y - height/2
            # Create the rectangle patch
            rectangle = patches.Rectangle((bottom_left_x, bottom_left_y), width, height,
                                          linewidth=1, edgecolor='g', facecolor='g')
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
