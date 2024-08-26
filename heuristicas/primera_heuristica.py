import matplotlib.patches
import matplotlib.pyplot
import numpy as np  
import math
from shapely.geometry import Point, Polygon 
import sys
import os
sys.path.append(os.path.abspath("TD8_ProyectoFinal/"))
from lectura_data.generacion_mapa import fun_generacion_mapa
from lectura_data.xml_parsing import xml_data_extractor


def generate_panel_arrays(nx, ny, panel_size, indentation, offset_x, offset_y):
    (dx, dy) = panel_size
    Array = [(i * panel_size[0] + indentation * j % dx + offset_x, j * panel_size[1] + offset_y) 
             for i in range(nx)
             for j in range(ny)]
    return Array 

def plot_rectangle(x, y, dx, dy, color='r', facecolor='none'):
    Xs = [x, x, x + dx, x + dx, x]
    Ys = [y, y + dy, y + dy, y, y]
    if facecolor == 'none':
        matplotlib.pyplot.plot(Xs, Ys, color)
    else:
        matplotlib.pyplot.fill(Xs, Ys, facecolor=facecolor, edgecolor=color)

def plot_rectangles(Array, panel_size, color='r', facecolor='none'):
    (dx, dy) = panel_size
    for (x, y) in Array:
        plot_rectangle(x, y, dx, dy, color=color, facecolor=facecolor)

def plot_polygon(Points):
    Xs, Ys = zip(*Points)
    matplotlib.pyplot.plot(Xs, Ys, 'b')
    matplotlib.pyplot.plot([Xs[-1], Xs[0]], [Ys[-1], Ys[0]], 'b')

def contains_rectangle(x, y, panel_size, polygon):
    (dx, dy) = panel_size
    bbpath = matplotlib.path.Path(polygon) 
    result = bbpath.contains_points([(x, y), (x + dx, y), (x, y + dy), (x + dx, y + dy)])
    return np.all(result)

def contains_rectangles(Array, panel_size, polygon):
    okay_panels  = [(x, y) for (x, y) in Array if contains_rectangle(x, y, panel_size, polygon)]
    return okay_panels


def solve(polygon, panel_size):
    """Search for different offsets to find the solution that maximizes the number of panels."""
    max_panel = 0 
    best_panels, best_array, best_indentation, best_offset_x, best_offset_y = None, None, None, None, None

    # Use the original polygon without modification
    original_polygon = np.array(polygon)

    # Calculate the bounding box of the original polygon
    min_x = original_polygon[:, 0].min()
    min_y = original_polygon[:, 1].min()
    max_x = original_polygon[:, 0].max()      
    max_y = original_polygon[:, 1].max()

    # Determine grid size based on the bounding box
    n_x = int(max_x // panel_size[0] + panel_size[0])
    n_y = int(max_y // panel_size[1] + panel_size[1])

    # Iterate over possible offsets and indentations
    for indentation in range(0, int(panel_size[0])):
        for offset_x in range(-int(panel_size[0]), int(panel_size[0])):
            for offset_y in range(-int(panel_size[1]), int(panel_size[1])):
                # Generate the array of possible panels
                Array = generate_panel_arrays(n_x, n_y, panel_size, indentation, offset_x, offset_y)
                okay_panels = contains_rectangles(Array, panel_size, original_polygon)

                if len(okay_panels) > max_panel: 
                    max_panel = len(okay_panels)
                    best_indentation, best_offset_x, best_offset_y = indentation, offset_x, offset_y
                    best_panels = okay_panels
                    best_array = Array 
                    
                    print("Maximal number of panels is", max_panel)
                    print("Indentation is {}, offset is ({}, {})".
                           format(best_indentation, best_offset_x, best_offset_y))

    return best_panels, best_array

def check_center(center, restrictions):
    for rest in restrictions:
        center_point = Point(center)
        fig_rest = Polygon(rest)
        is_in_rest = not center_point.within(fig_rest)
        if is_in_rest:
            return True
    return False


def check_panels(panels,panel_size, restrictions):
    width, heigth = panel_size
    true_panels = []
    true_centers = []
    for i in range(len(panels)):
        center = (panels[i][0] + width/2, panels[i][1] + heigth/2)
        if check_center(center,restrictions):
            true_panels.append(panels[i])
            true_centers.append(center)
    return true_panels, true_centers



if __name__ == "__main__":

    
    file_path_bony = 'C:/Users/valen/OneDrive/Escritorio/Bony/Di tella/TD8FINAL/TD8_ProyectoFinal/mapas/Entrada_v2.xml'
    polygon, pads_data, restrictions , angulo= xml_data_extractor(file_path_bony)
    print(pads_data)
    # panel_size_s = (2, 4)
    # panel_size_m = (5, 10)
    # polygon = [(10.0, 0.0), (0.0, 16.0), (0.0, 29.0), (12.0, 33.0), (33.0, 33.0), (46.0, 16.0), (46.0, 6.0), (38.0, 0.0), (10.0, 0.0)]
    # restrictions = [[(9.0, 22.0), (9.0, 25.0), (12.0, 28.0), (16.0, 29.0), (17.0, 27.0), (12.0, 23.0), (9.0, 22.0)], [(25.0, 22.0), (27.0, 25.0), (29.0, 27.0), (30.0, 25.0), (27.0, 21.0), (25.0, 22.0)], [(25.0, 22.0), (27.0, 21.0), (29.0, 17.0), (27.5, 15.0), (25.0, 17.0), (25.0, 22.0)], [(16.0, 11.0), (17.0, 13.0), (24.0, 8.0), (27.0, 5.0), (26.0, 4.0), (19.0, 7.0), (16.0, 11.0)]]


    panels, arrays = solve(polygon, pads_data[0])

    true_panels, true_centers = check_panels(panels, pads_data[0], restrictions)

    fun_generacion_mapa(polygon,restrictions,true_centers,pads_data[0])

    



      
