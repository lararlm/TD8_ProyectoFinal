import xml.etree.ElementTree as ET

def xml_data_extractor(file_path: str):

    
    # Parsing del archivo XML
    tree = ET.parse(file_path)
    root = tree.getroot()

    yacimiento_coordinates = []
    semilla_data = []
    restricciones_data = []
    angulo = root.find(".//Esfuerzo_horizontal_mínimo").get("Ángulo")
    angulo = float(angulo.replace(",",".")) if angulo else None
    # Extraemos la información del polígono del yacimiento
    for area in root.findall(".//Área[@Capa='Yacimiento']"):
        # Extraemos cada vértice del polígono
        for vertice in area.findall(".//Vértice"):
            x = float(vertice.get('X').replace(",", "."))
            y = float(vertice.get('Y').replace(",", "."))
            # Guardamos las coordenadas en la lista
            yacimiento_coordinates.append((x, y))
    
    # Extraemos la información de los pads (semillas)
    for semilla in root.findall(".//Semilla"):
        # Extraemos el largo y ancho de cada pad
        for pad in semilla.findall(".//PAD"):
            largo = float(pad.get('Largo').replace(",", "."))
            ancho = float(pad.get('Ancho').replace(",", "."))
            # Guardamos la información en la lista
            semilla_data.append((ancho, largo))
        
    # Extraemos la información de los polígonos obstáculo
    for restriccion in root.findall(".//Restricción"):
        restriccion_vertices = []
        # Extraemos cada vértice del polígono
        for vertice in restriccion.findall(".//Vértice"):
            x = float(vertice.get('X').replace(",", "."))
            y = float(vertice.get('Y').replace(",", "."))
            # Guardamos las coordenadas en la lista
            restriccion_vertices.append((x, y))
        # Añadimos a la lista de polígonos obstáculo
        restricciones_data.append(restriccion_vertices)
    
    return yacimiento_coordinates, semilla_data, restricciones_data, angulo





# # # file_path_bony = 'C:/Users/valen/OneDrive/Escritorio/Bony/Di tella/TD8FINAL/TD8_ProyectoFinal/mapas/pol.01.xml'
# yacimiento_coords, panel_size, restricciones_data , angulo= xml_data_extractor(file_path_lari)
# print(yacimiento_coords ,panel_size, restricciones_data)

# # print("Yacimiento Coordinates:", yacimiento_coords)
# # print("Pads Data (Largo, Ancho, Angulo):", panel_size , angulo)
# # print("Restricciones Data:", restricciones_data)


# # rectangles = [[panel_size[0][0], panel_size[0][1], 10 , 15]]
# rectangles = []

# # print(rectangles)