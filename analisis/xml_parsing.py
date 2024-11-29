import xml.etree.ElementTree as ET

def xml_data_extractor(file_path: str):
    '''
    file_path: path del mapa para extraer info.

    Esta funcion toma los archivos XML que tenemos y saca la informacion del yacimiento, los tamaños de los paneles, las restricciones y el angulo de los paneles.
    '''

    tree = ET.parse(file_path)
    root = tree.getroot()
    polygon = []
    rect_size = []
    restrictions = []
    angulo = root.find(".//Esfuerzo_horizontal_mínimo").get("Ángulo")
    angulo = float(angulo.replace(",",".")) if angulo else None
    for area in root.findall(".//Área[@Capa='Yacimiento']"):
        for vertice in area.findall(".//Vértice"):
            x = float(vertice.get('X').replace(",", "."))
            y = float(vertice.get('Y').replace(",", "."))
            polygon.append((x, y))
    
    for semilla in root.findall(".//Semilla"):
        for pad in semilla.findall(".//PAD"):
            largo = float(pad.get('Largo').replace(",", "."))
            ancho = float(pad.get('Ancho').replace(",", "."))
            rect_size.append((ancho, largo))
        
    for restriccion in root.findall(".//Restricción"):
        restriccion_vertices = []
        for vertice in restriccion.findall(".//Vértice"):
            x = float(vertice.get('X').replace(",", "."))
            y = float(vertice.get('Y').replace(",", "."))
            restriccion_vertices.append((x, y))
        restrictions.append(restriccion_vertices)
    
    return polygon, rect_size, restrictions, angulo
