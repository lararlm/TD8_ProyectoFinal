import matplotlib.patches
import matplotlib.pyplot
import numpy as np  
import csv
import math
from shapely.geometry import Point, Polygon 
import sys
import os
sys.path.append(os.path.abspath("TD8_ProyectoFinal/"))
from lectura_data.generacion_mapa import fun_generacion_mapa
from lectura_data.xml_parsing import xml_data_extractor
import random


def rectangularize(polygon):
    min_X = min(polygon, key = lambda x: x[0])[0]
    min_Y = min(polygon, key = lambda y: y[1])[1]
    max_X = max(polygon, key = lambda x: x[0])[0]
    max_Y = max(polygon, key = lambda y: y[1])[1]

    rect_pol = [(min_X, min_Y), (min_X, max_Y), (max_X, min_Y), (max_X, max_Y)]
    return rect_pol

def tiling(polygon, pad_size):
    
    pass



