import time 
import csv
from DataStructures import array_list as array
from DataStructures import map_linear_probing as lp
from datetime import datetime
from DataStructures import red_black_tree as rbt
def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    catalog = {
        'accidents_tree': rbt.new_map(),  # Inicializar el árbol rojo-negro
        'accidents_list': []  # Inicializar la lista de accidentes
    }
    return catalog
pass


# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    filename="C:\\Users\\dfeli\\Downloads\\Universidad Segundo Semestre\\Estructura De Datos Y Algoritmos\\Retos\\Reto 3\\Reto3-G02\\Data\\accidents-large.csv"
    input_file = csv.DictReader(open(filename, encoding="utf-8"))
    accidents_tree = catalog['accidents_tree']  # Obtener el árbol del catálogo
    accidents_list = catalog['accidents_list']  # Obtener la lista del catálogo

    for accident in input_file:
        accident_id = accident["ID"] if accident["ID"] else "Unknown"
        source = accident["Source"] if accident["Source"] else "Unknown"
        severity = int(accident["Severity"]) if accident["Severity"].isdigit() else None
        start_time = datetime.strptime(accident["Start_Time"], "%Y-%m-%d %H:%M:%S") if accident["Start_Time"] else None
        end_time = datetime.strptime(accident["End_Time"], "%Y-%m-%d %H:%M:%S") if accident["End_Time"] else None
        start_lat = float(accident["Start_Lat"]) if accident["Start_Lat"] else None
        start_lng = float(accident["Start_Lng"]) if accident["Start_Lng"] else None
        end_lat = float(accident["End_Lat"]) if accident["End_Lat"] else start_lat
        end_lng = float(accident["End_Lng"]) if accident["End_Lng"] else start_lng
        distance = float(accident["Distance(mi)"]) if accident["Distance(mi)"] else None
        description = accident["Description"] if accident["Description"] else "Unknown"
        street = accident["Street"] if accident["Street"] else "Unknown"
        city = accident["City"] if accident["City"] else "Unknown"
        county = accident["County"] if accident["County"] else "Unknown"
        state = accident["State"] if accident["State"] else "Unknown"
        temperature = float(accident["Temperature(F)"]) if accident["Temperature(F)"] else None
        wind_chill = float(accident["Wind_Chill(F)"]) if accident["Wind_Chill(F)"] else None
        humidity = float(accident["Humidity(%)"]) if accident["Humidity(%)"] else None
        pressure = float(accident["Pressure(in)"]) if accident["Pressure(in)"] else None
        visibility = float(accident["Visibility(mi)"]) if accident["Visibility(mi)"] else None
        wind_direction = accident["Wind_Direction"] if accident["Wind_Direction"] else "Unknown"
        wind_speed = float(accident["Wind_Speed(mph)"]) if accident["Wind_Speed(mph)"] else None
        precipitation = float(accident["Precipitation(in)"]) if accident["Precipitation(in)"] else None
        weather_condition = accident["Weather_Condition"] if accident["Weather_Condition"] else "Unknown"

        duration_hours = (end_time - start_time).total_seconds() / 3600 if start_time and end_time else None

        accident_data = {
            "id": accident_id,
            "source": source,
            "severity": severity,
            "start_time": start_time,
            "end_time": end_time,
            "start_lat": start_lat,
            "start_lng": start_lng,
            "end_lat": end_lat,
            "end_lng": end_lng,
            "distance(mi)": distance,
            "description": description,
            "street": street,
            "city": city,
            "county": county,
            "state": state,
            "temperature(f)": temperature,
            "wind_chill(f)": wind_chill,
            "humidity(%)": humidity,
            "pressure(in)": pressure,
            "visibility(mi)": visibility,
            "wind_direction": wind_direction,
            "wind_speed(mph)": wind_speed,
            "precipitation(in)": precipitation,
            "weather_condition": weather_condition,
            "duration_hours": duration_hours
        }

        rbt.put(accidents_tree, accident_id, accident_data)
        accidents_list.append(accident_data)

    total_accidents = rbt.size(accidents_tree)

    first_five = accidents_list[:5]
    last_five = accidents_list[-5:]

    return total_accidents, first_five, last_five
pass

# Funciones de consulta sobre el catálogo

def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Consulta en las Llamar la función del modelo para obtener un dato
    accident_data = rbt.get(catalog['accidents_tree'], id)
    
    if accident_data is not None:
        return accident_data
    else:
        return "Accidente no encontrado."
pass

def sort_criteria_by_date_and_severity(accident1, accident2):
    # Ordenar por fecha (más reciente a más antiguo)
    if accident1["start_time"] != accident2["start_time"]:
        return accident1["start_time"] < accident2["start_time"]  # Invertir el orden
    # Si las fechas son iguales, ordenar por severidad (mayor a menor)
    return accident1["severity"] > accident2["severity"]  

def search_tree(catalog, node, start_date, end_date, accidents_list):
    """
    Busca accidentes en el árbol que están dentro del rango de fechas especificado.
    """
    if node is not None:
        # Recorrer el subárbol izquierdo
        search_tree(catalog, node["left"], start_date, end_date, accidents_list)

        # Obtener el accidente correspondiente a la llave del nodo
        accident_data = rbt.get(catalog, node["key"])  
        if accident_data:
            # Verificar si la fecha de inicio del accidente está dentro del rango
            if start_date <= accident_data["start_time"] <= end_date:
                array.add_last(accidents_list, accident_data)  # Agregar el accidente a la lista

        # Recorrer el subárbol derecho
        search_tree(catalog, node["right"], start_date, end_date, accidents_list)

def req_1(catalog, start_date_str, end_date_str):
    """
    Lista los accidentes ocurridos entre dos fechas.
    """
    my_rbt = catalog['accidents_tree']
    # Convertir las fechas de entrada a objetos datetime
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")
    
    accidents_list = array.new_list()  # Usar la nueva lista

    # Iniciar la búsqueda en el árbol
    search_tree(my_rbt, my_rbt["root"], start_date, end_date, accidents_list)

    # Ordenar los accidentes usando merge_sort
    array.merge_sort(accidents_list, sort_criteria_by_date_and_severity)  # Ordenar por fecha y severidad

    # Limitar la salida si hay más de 10 accidentes
    total_accidents = array.size(accidents_list)
    if total_accidents > 10:
        first_five = array.sub_list(accidents_list, 0, 5)  # Primeros 5
        last_five = array.sub_list(accidents_list, total_accidents - 5, 5)  # Últimos 5
        accidents_list = array.new_list()  # Reiniciar la lista
        array.add_all(accidents_list, first_five['elements'])  # Agregar primeros 5
        array.add_all(accidents_list, last_five['elements'])  # Agregar últimos 5

    # Preparar la salida
    respuesta = []
    for i in range(array.size(accidents_list)):
        accident = array.get_element(accidents_list, i)
        respuesta.append({
            "id": accident["id"],
            "start_time": accident["start_time"],
            "city": accident["city"],
            "state": accident["state"],
            "description": accident["description"][:40],  # limitar a 40 caracteres
            "duration_hours": accident.get("duration_hours", "N/A")  # Usar get para evitar KeyError
        })

    # Obtener características del árbol
    height = rbt.height_tree(my_rbt["root"])
    node_count = rbt.size_tree(my_rbt["root"])
    element_count = rbt.size_tree(my_rbt["root"])

    return total_accidents, respuesta, height, node_count, element_count


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(catalog):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(catalog):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
