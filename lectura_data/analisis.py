import matplotlib.patches
import matplotlib.pyplot
import numpy as np
from shapely.geometry import Point, Polygon 
from triangulator.ear_clipping_method import triangulate


def contains_rectangle(x, y, panel_size, polygon):
    (dx, dy) = panel_size
    bbpath = matplotlib.path.Path(polygon) 
    result = bbpath.contains_points([(x, y), (x + dx, y), (x, y + dy), (x + dx, y + dy)])
    return np.all(result)

def check_center(center, restrictions):
    for rest in restrictions:
        center_point = Point(center)
        fig_rest = Polygon(rest)
        is_in_rest = center_point.within(fig_rest)
        if is_in_rest:
            return False
    return True

def check_availability(center, center_size, pads_data, polygon, restrictions, rectangles):
    dx, dy = center_size
    x, y = center
    x_bl = x - dx / 2
    y_bl = y - dy / 2
    bbpath = matplotlib.path.Path(polygon) 
    result = bbpath.contains_points([
        (x_bl, y_bl),              
        (x_bl + dx, y_bl),          
        (x_bl, y_bl + dy),          
        (x_bl + dx, y_bl + dy)     
    ])
    if not np.all(result):
        return False
    
    for rest in restrictions:
        center_point = Point(center)
        fig_rest = Polygon(rest)
        if center_point.within(fig_rest):
            return False
    
    width1, height1 = center_size
    left1 = x - width1 / 2
    right1 = x + width1 / 2
    top1 = y - height1 / 2
    bottom1 = y + height1 / 2
    for i in range(len(rectangles)): 
        for center2 in rectangles[i]:
            width1, height1 = pads_data[i]
            x2, y2 = center2
            left2 = x2 - width1 / 2
            right2 = x2 + width1 / 2
            top2 = y2 - height1 / 2
            bottom2 = y2 + height1 / 2
            
            if not (left1 >= right2 or left2 >= right1 or top1 >= bottom2 or top2 >= bottom1):
                return False
        
    return True


def check_rectangles(center, center_size, pads_data, rectangles):
    dx, dy = center_size
    x, y = center
    width1, height1 = center_size
    left1 = x - width1 / 2
    right1 = x + width1 / 2
    top1 = y - height1 / 2
    bottom1 = y + height1 / 2
    for i in range(len(rectangles)): 
        for center2 in rectangles[i]:
            width1, height1 = pads_data[i]
            x2, y2 = center2
            left2 = x2 - width1 / 2
            right2 = x2 + width1 / 2
            top2 = y2 - height1 / 2
            bottom2 = y2 + height1 / 2
            
            if not (left1 >= right2 or left2 >= right1 or top1 >= bottom2 or top2 >= bottom1):
                return False
    return True

def calculate_area(polygon, rectangles, panel_size):
    triangles = triangulate(polygon)
    areas = []
    for trian in triangles:
        t_area = 0.5 * abs(
            trian[0][0] * (trian[1][1] - trian[2][1]) +
            trian[1][0] * (trian[2][1] - trian[0][1]) +
            trian[2][0] * (trian[0][1] - trian[1][1])
        )
        areas.append(t_area)
    cover_area = 0
    quantity_rect = []
    total_area = sum(areas)
    for i in range(len(rectangles)):
        aux_rects = len(rectangles[i])
        quantity_rect.append(aux_rects)
        print(panel_size[i])
        cover_area += panel_size[i][0]*panel_size[i][1]*aux_rects
    print(f"Rectangles: {quantity_rect} Area covered: {cover_area/total_area}")     

    
        