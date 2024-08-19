import matplotlib.patches
import matplotlib.pyplot
import numpy 
import math

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
    return numpy.all(result)

def contains_rectangles(Array, panel_size, polygon):
    okay_panels  = [(x, y) for (x, y) in Array if contains_rectangle(x, y, panel_size, polygon)]
    return okay_panels

def solve(polygon, panel_size):
    """Search for different offsets to find the solution that maximizes the number of panels."""
    max_panel = 0 
    best_panels, best_array, best_indentation, best_offset_x, best_offset_y = None, None, None, None, None

    # No rotation, angle is 0 degrees
    rotated_polygon = numpy.array(polygon)
    min_x = rotated_polygon[:, 0].min()
    min_y = rotated_polygon[:, 1].min()
    rotated_polygon[:, 0] -= (min_x - 1)
    rotated_polygon[:, 1] -= (min_y - 1)
    max_x = rotated_polygon[:, 0].max()      
    max_y = rotated_polygon[:, 1].max()

    n_x = int(max_x // panel_size[0] + panel_size[0])
    n_y = int(max_y // panel_size[1] + panel_size[1])

    for indentation in range(0, panel_size[0]):
        for offset_x in range(-panel_size[0], panel_size[0]):
            for offset_y in range(-panel_size[1], panel_size[1]):
                # Generate the array 
                Array = generate_panel_arrays(n_x, n_y, panel_size, indentation, offset_x, offset_y)
                okay_panels = contains_rectangles(Array, panel_size, rotated_polygon)

                if len(okay_panels) > max_panel: 
                    max_panel = len(okay_panels)
                    best_indentation, best_offset_x, best_offset_y = indentation, offset_x, offset_y
                    best_panels = okay_panels
                    best_array = Array 

                    print("Maximal number of panels is", max_panel)
                    print("Indentation is {}, offset is ({}, {})".
                           format(best_indentation, best_offset_x, best_offset_y))

    # Visualize best result 
    plot_polygon(rotated_polygon)
    plot_rectangles(best_array, panel_size)
    plot_rectangles(best_panels, panel_size, color='k', facecolor='lime')

    matplotlib.pyplot.axis('equal')
    matplotlib.pyplot.show()

    return max_panel, best_indentation, best_offset_x, best_offset_y

if __name__ == "__main__":
    panel_size = (2, 4)
    polygon = [(10.0, 0.0), (0.0, 16.0), (0.0, 29.0), (12.0, 33.0), (33.0, 33.0), (46.0, 16.0), (46.0, 6.0), (38.0, 0.0), (10.0, 0.0)]

    solve(polygon, panel_size)  
