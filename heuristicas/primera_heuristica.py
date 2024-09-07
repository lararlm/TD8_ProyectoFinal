import matplotlib.patches
import matplotlib.pyplot
import numpy as np  
import csv
import math
from shapely.geometry import Point, Polygon 
import sys
import os
sys.path.append(os.path.abspath("TD8_ProyectoFinal/"))
from lectura_data.analisis import check_rectangles, calculate_area
from lectura_data.generacion_mapa import fun_generacion_mapa
from lectura_data.xml_parsing import xml_data_extractor


def solve(polygon, actual_panel, xml_file_path, restrictions, rectangles, panel_size):
    """Search for different offsets to find the solution that maximizes the number of panels."""
    solution_num = 0
    max_panel = 0 
    best_panels, best_array, best_indentation, best_offset_x, best_offset_y, best_centers = None, None, None, None, None, None

    # Use the original polygon without modification
    original_polygon = np.array(polygon)

    # Calculate the bounding box of the original polygon
    min_x = original_polygon[:, 0].min()
    min_y = original_polygon[:, 1].min()
    max_x = original_polygon[:, 0].max()      
    max_y = original_polygon[:, 1].max()

    # Determine grid size based on the bounding box
    n_x = int(max_x // actual_panel[0] + actual_panel[0])
    n_y = int(max_y // actual_panel[1] + actual_panel[1])

    # Iterate over possible offsets and indentations
    for indentation in range(0, int(actual_panel[0])):
        for offset_x in range(-int(actual_panel[0]), int(actual_panel[0])):
            for offset_y in range(-int(actual_panel[1]), int(actual_panel[1])):
                # Generate the array of possible panels
                Array = generate_panel_arrays(n_x, n_y, actual_panel, indentation, offset_x, offset_y)
                okay_panels = contains_rectangles(Array, actual_panel, original_polygon)
                okay_panels, okay_centers = check_panels(okay_panels, actual_panel, panel_size, restrictions,rectangles)

                if len(okay_panels) > max_panel: 
                    max_panel = len(okay_panels)
                    best_indentation, best_offset_x, best_offset_y = indentation, offset_x, offset_y
                    best_centers = okay_centers
                    best_panels = okay_panels
                    best_array = Array 

                    filename = "Solution_" + str(solution_num) + "1st"+ ".csv" 
                    folder_path = os.path.dirname(xml_file_path)
                    folder_name = os.path.splitext(os.path.basename(xml_file_path))[0]
                    csv_folder_path = os.path.join(folder_path, folder_name)
                    os.makedirs(csv_folder_path, exist_ok=True)
                    csv_filename = os.path.join(csv_folder_path, filename)

                    with open(csv_filename, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        
                        # Optionally write a header
                        writer.writerow(["Center_X", "Center_Y"])
                        
                        # Write each coordinate to the file
                        writer.writerows(best_centers)

                    solution_num+=1
                    
                    print("Maximal number of panels is", max_panel)

                    print("Indentation is {}, offset is ({}, {})".
                           format(best_indentation, best_offset_x, best_offset_y))

    return  best_centers

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

def check_center(center, restrictions):
    for rest in restrictions:
        center_point = Point(center)
        fig_rest = Polygon(rest)
        is_in_rest = center_point.within(fig_rest)
        if is_in_rest:
            return False
    return True


def check_panels(panels, actual_panel, panel_size, restrictions, rectangles):
    width, heigth = actual_panel
    true_panels = []
    true_centers = []
    for i in range(len(panels)):
        center = (panels[i][0] + width/2, panels[i][1] + heigth/2)
        if check_center(center,restrictions) and check_rectangles(center,actual_panel,panel_size,rectangles):
            true_panels.append(panels[i])
            true_centers.append(center)
    return true_panels, true_centers


def grid_heuristic(polygon, panel_size, xml_file_path, restrictions, rectangles = None):
    if not rectangles:
        rectangles = [[] for _ in range(len(panel_size))]
    for i in range(len(panel_size)):
        actual_panel = panel_size[i]
        sub_rectangles = solve(polygon,actual_panel,xml_file_path,restrictions,rectangles,panel_size)
        rectangles[i].extend(sub_rectangles)
    return rectangles
    
        


if __name__ == "__main__":

    file_path_bony = 'C:/Users/valen/OneDrive/Escritorio/Bony/Di tella/TD8FINAL/TD8_ProyectoFinal/mapas/pol.01.xml'
    file_path_bony = 'C:/Users/valen/OneDrive/Escritorio/Bony/Di tella/TD8FINAL/TD8_ProyectoFinal/mapas/pol.1s.07.xml'
    # file_path_bony = 'C:/Users/valen/OneDrive/Escritorio/Bony/Di tella/TD8FINAL/TD8_ProyectoFinal/mapas/Entrada_v2.xml'
    polygon, pads_data, restrictions , angulo = xml_data_extractor(file_path_bony)
    rectangles = grid_heuristic(polygon, pads_data, file_path_bony, restrictions)
    rectangles = grid_heuristic(polygon, pads_data, file_path_bony, restrictions, rectangles)
    fun_generacion_mapa(polygon,restrictions,rectangles,pads_data)
    calculate_area(polygon,rectangles,pads_data)