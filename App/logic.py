import time 
import csv
from DataStructures import array_list as al
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
        'accidents_list': al.new_list() # Inicializar la lista de accidentes
    }
    return catalog
pass

# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    filename="C:\\EDA20242\\Reto3-G02\\Data\\Data\\Data\\accidents-large.csv"
    input_file = csv.DictReader(open(filename, encoding="utf-8"))
    accidents_tree = catalog['accidents_tree']  # Obtener el árbol del catálogo
    accidents_list = catalog['accidents_list']["elements"]  # Obtener la lista del catálogo

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
        lista_array=catalog["accidents_list"]
        lista_array["elements"].append(accident_data)


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
                al.add_last(accidents_list, accident_data)  # Agregar el accidente a la lista

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
    
    accidents_list = al.new_list()  # Usar la nueva lista

    # Iniciar la búsqueda en el árbol
    search_tree(my_rbt, my_rbt["root"], start_date, end_date, accidents_list)

    # Ordenar los accidentes usando merge_sort
    al.merge_sort(accidents_list, sort_criteria_by_date_and_severity)  # Ordenar por fecha y severidad

    # Limitar la salida si hay más de 10 accidentes
    total_accidents = al.size(accidents_list)
    if total_accidents > 10:
        first_five = al.sub_list(accidents_list, 0, 5)  # Primeros 5
        last_five = al.sub_list(accidents_list, total_accidents - 5, 5)  # Últimos 5
        accidents_list = al.new_list()  # Reiniciar la lista
        al.add_all(accidents_list, first_five['elements'])  # Agregar primeros 5
        al.add_all(accidents_list, last_five['elements'])  # Agregar últimos 5

    # Preparar la salida
    respuesta = []
    for i in range(al.size(accidents_list)):
        accident = al.get_element(accidents_list, i)
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


def req_2(catalog, start_date_str, end_date_str):
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


def req_4(catalog, start_date_str, end_date_str):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    my_rbt = catalog['accidents_tree']
    # Convertir las fechas de entrada a objetos datetime
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")
    
    accidents_list = al.new_list()  # Usar la nueva lista
    
     # Iniciar la búsqueda en el árbol
    search_tree(my_rbt, my_rbt["root"], start_date, end_date, accidents_list)
    
    # Ordenar los accidentes usando merge_sort
    al.merge_sort(accidents_list, sort_criteria_by_date_and_severity)  # Ordenar por fecha y severidad
    
    # Preparar la salida
    respuesta = al.new_list()
    diccionario_requerido_vias={}
    lista_de_calles=al.new_list()
    total_accidents=0
    
    
    
    
    for accidente in accidents_list["elements"]:
         # Filtrar por severidad y visibilidad
        if (accidente["visibility(mi)"] is None or accidente["visibility(mi)"] < 1) and accidente["severity"] >= 3:
            calle = accidente["street"]
            total_accidents+=1
            # Si la vía no está en el diccionario, inicializarla
            if calle not in diccionario_requerido_vias:
                al.add_last(lista_de_calles, calle)
                diccionario_requerido_vias[calle] = {
                    "city": accidente["city"],
                    "county": accidente["county"],
                    "state": accidente["state"],
                    "number_severity_3": 0,
                    "number_severity_4": 0,
                    "total_visibility": 0,
                    "accident_count": 0
                }
            
            # Contar accidentes por severidad
            if accidente["severity"] == 3:
                diccionario_requerido_vias[calle]["number_severity_3"] += 1
            elif accidente["severity"] == 4:
                diccionario_requerido_vias[calle]["number_severity_4"] += 1
            
            # Sumar visibilidad y contar accidentes
            if accidente["visibility(mi)"] is not None:
                diccionario_requerido_vias[calle]["total_visibility"] += accidente["visibility(mi)"]
            diccionario_requerido_vias[calle]["accident_count"] += 1
    
            
    
    
    
    for calle in lista_de_calles["elements"]:
        dic_calle=diccionario_requerido_vias[calle]
        average_visibility = dic_calle["total_visibility"] / dic_calle["accident_count"] 
        accident_data = {
            "street": calle,
            "city": dic_calle["city"],
            "county": dic_calle["county"],
            "state": dic_calle["state"],
            "number_severity_3": dic_calle["number_severity_3"],
            "number_severity_4": dic_calle["number_severity_4"],
            "Average_visibility": average_visibility
        }
        al.add_last(respuesta, accident_data)
     # Obtener características del árbol
    height = rbt.height_tree(my_rbt["root"])
    node_count = rbt.size_tree(my_rbt["root"])
    element_count = rbt.size_tree(my_rbt["root"])
   
    return total_accidents, respuesta, height, node_count, element_count
            
            
    
pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog, start_date_str, end_date_str, humedad, lst_condados ):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    my_rbt = catalog['accidents_tree']
    # Convertir las fechas de entrada a objetos datetime
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")
    
    accidents_list = al.new_list()  # Usar la nueva lista
    
     # Iniciar la búsqueda en el árbol
    search_tree(my_rbt, my_rbt["root"], start_date, end_date, accidents_list)
    
    # Ordenar los accidentes usando merge_sort
    al.merge_sort(accidents_list, sort_criteria_by_date_and_severity)  # Ordenar por fecha y severidad
    
    dpor_condados={}
    total_accidents=0
    respuesta = al.new_list()
    
    for accidente in accidents_list["elements"]:
        if (accidente["humidity(%)"] is not None and accidente["humidity(%)"] >= humedad) and accidente["severity"]>=3:
            total_accidents+=1
            if accidente["county"] in lst_condados:
                condado=accidente["county"]
                if condado not in dpor_condados:
                    dpor_condados[condado]={"Number_accidents":0,
                                            "Accidents_county": 0,
                                            "total_temperature": 0,
                                            "total_humidity": 0,
                                            "total_wind_speed": 0,
                                            "total_distance": 0,
                                            "id":None,
                                            "temperature(f)":None,
                                            "humidity(%)":None,
                                            "distance(mi)":None,
                                            "description":None,
                                            "severity":None,
                                            
                                            }
                dpor_condados[condado]["Accidents_county"] += 1
                dpor_condados[condado]["total_humidity"] += accidente["humidity(%)"]
                dpor_condados[condado]["total_distance"] += accidente["distance(mi)"]
                dpor_condados[condado]["total_temperature"] += accidente["temperature(f)"]

                # Verificar si el valor de velocidad del viento no es None antes de sumar
                if accidente["wind_speed(mph)"] is not None:
                    dpor_condados[condado]["total_wind_speed"] += accidente["wind_speed(mph)"]

                
                
                if (dpor_condados[condado]["severity"] is None) or accidente["severity"]>=dpor_condados[condado]["severity"]:
                    dpor_condados[condado]["severity"] = accidente["severity"]
                    dpor_condados[condado]["start_time"] = accidente["start_time"]
                    dpor_condados[condado]["end_time"] = accidente["end_time"]
                    dpor_condados[condado]["id"] = accidente["id"]
                    dpor_condados[condado]["temperature(f)"] = accidente["temperature(f)"]
                    dpor_condados[condado]["humidity(%)"] = accidente["humidity(%)"]
                    dpor_condados[condado]["distance(mi)"] = accidente["distance(mi)"]
                    dpor_condados[condado]["description"] = accidente["description"]
    
    
    for condado in lst_condados:
        if condado in dpor_condados:
            dic_condado =dpor_condados[condado]
            average_temperature = dic_condado["total_temperature"] / dic_condado["Accidents_county"] 
            average_humidity = dic_condado["total_humidity"] / dic_condado["Accidents_county"]
            average_wind_speed = dic_condado["total_wind_speed"] / dic_condado["Accidents_county"]
            average_distance = dic_condado["total_distance"] / dic_condado["Accidents_county"]
            accident_data = {
            
            
            
            "county":condado,
            "Accidents_county": dic_condado["Accidents_county"],
            "Average_temperature":  average_temperature,
            "Average_humidity": average_humidity,
            "Average_wind_speed": average_wind_speed,
            "Average_distance": average_distance,
            "id":dic_condado["id"],
            "temperature(f)":dic_condado["temperature(f)"],
            "humidity(%)":dic_condado["humidity(%)"],
            "distance(mi)":dic_condado["distance(mi)"],
            "description":dic_condado["description"]
          }
        al.add_last(respuesta, accident_data)
     # Obtener características del árbol
    height = rbt.height_tree(my_rbt["root"])
    node_count = rbt.size_tree(my_rbt["root"])
    element_count = rbt.size_tree(my_rbt["root"])
   
    return total_accidents, respuesta, height, node_count, element_count
        
        
         
                    
                    
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
