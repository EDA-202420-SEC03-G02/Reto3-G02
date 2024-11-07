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
    filename="C:\\Users\\dfeli\\Downloads\\Universidad Segundo Semestre\\Estructura De Datos Y Algoritmos\\Retos\\Reto 3\\Reto3-G02\\Data\\accidents-large.csv"
    input_file = csv.DictReader(open(filename, encoding="utf-8"))
    astart_time = get_time()
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
        lista_al=catalog["accidents_list"]
        lista_al["elements"].append(accident_data)


    total_accidents = rbt.size(accidents_tree)

    first_five = accidents_list[:5]
    last_five = accidents_list[-5:]
    aend_time = get_time()
    delta = delta_time(astart_time, aend_time)
    return total_accidents, first_five, last_five,delta
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
def sort_criteria_by_visibility_and_distance(accidente1, accidente2):
    # Verificar si ambas visibilidades están presentes
    visibility1 = accidente1.get("Visibility(mi)")
    visibility2 = accidente2.get("Visibility(mi)")

    # Si la visibilidad es None, considerar como menor para el orden
    if visibility1 is None and visibility2 is None:
        return False  # Son iguales en cuanto a orden
    elif visibility1 is None:
        return True  # accidente1 es "menor" porque su visibilidad es None
    elif visibility2 is None:
        return False  # accidente2 es "menor" porque su visibilidad es None

    # Comparar las visibilidades
    if visibility1 != visibility2:
        return visibility1 < visibility2  # Ordenar de menor a mayor visibilidad

    # Si las visibilidades son iguales, ordenar por distancia
    distance1 = accidente1.get("Distance(mi)", 0)  # Considerar 0 si no hay distancia
    distance2 = accidente2.get("Distance(mi)", 0)

    return distance1 > distance2  # Ordenar de mayor a menor distancia


def ordenar_estados_por_accidentes(analisis_estados):
    # Ordenar estados en base a la cantidad de accidentes (mayor a menor)
    for i in range(al.size(analisis_estados) - 1):
        for j in range(i + 1, al.size(analisis_estados)):
            if analisis_estados[i]["Total Accidentes"] < analisis_estados[j]["Total Accidentes"]:
                temp = analisis_estados[i]
                analisis_estados[i] = analisis_estados[j]
                analisis_estados[j] = temp
    return analisis_estados


def sort_criteria_by_date_and_severity(accident1, accident2):
    # Ordenar por fecha (más reciente a más antiguo)
    if accident1["start_time"] != accident2["start_time"]:
        return accident1["start_time"] < accident2["start_time"]  # Invertir el orden
    # Si las fechas son iguales, ordenar por severidad (mayor a menor)
    return accident1["severity"] > accident2["severity"]  

def sort_criteria_by_severity(accident1, accident2):
    # Comparison logic here, e.g.:
    return accident1['severity'] < accident2['severity']


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
    astart_time = get_time()
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
    aend_time = get_time()
    delta = delta_time(astart_time, aend_time)
    return total_accidents, respuesta, height, node_count, element_count,delta



def req_2(catalog, visibilidad_rango, lista_estados):
    
    min_visibilidad, max_visibilidad = visibilidad_rango
    astart_time = get_time()
    accidentes_filtrados = al.new_list()

    # Filtrar los accidentes en el árbol dentro del rango de visibilidad y gravedad 4
    search_tree(catalog['accidents_tree'], catalog['accidents_tree']["root"], datetime.min, datetime.max, accidentes_filtrados)

    # Seleccionar solo los accidentes con gravedad 4, visibilidad en el rango, y en los estados especificados
    accidentes_validos = al.new_list()
    for i in range(al.size(accidentes_filtrados)):
        accidente = al.get_element(accidentes_filtrados, i)
        visibilidad = accidente.get("visibility(mi)")  # Usa get para evitar KeyError
        if (accidente["severity"] == 4 and 
            visibilidad is not None and  # Asegúrate de que visibilidad no sea None
            min_visibilidad <= visibilidad <= max_visibilidad and 
            accidente["state"] in lista_estados):
            al.add_last(accidentes_validos, accidente)

    # Análisis por estado
    analisis_estados = []
    for estado in lista_estados:
        accidentes_estado = al.new_list()
        
        # Filtrar accidentes por estado
        for j in range(al.size(accidentes_validos)):
            accidente = al.get_element(accidentes_validos, j)
            if accidente['state'] == estado:
                al.add_last(accidentes_estado, accidente)

        if al.size(accidentes_estado) > 0:
            # Cálculo de estadísticas
            num_accidentes = al.size(accidentes_estado)
            visibilidad_total = 0
            distancia_total = 0
            accidente_mayor_distancia = al.get_element(accidentes_estado, 0)

            for k in range(num_accidentes):
                accidente_actual = al.get_element(accidentes_estado, k)
                visibilidad_total += accidente_actual.get("visibility(mi)", 0)  # Sumar visibilidad (0 si es None)
                distancia_total += accidente_actual.get("distance(mi)", 0)  # Sumar distancia (0 si es None)

                # Verificar si este accidente tiene una mayor distancia afectada
                if accidente_actual.get("distance(mi)", 0) > accidente_mayor_distancia.get("distance(mi)", 0):
                    accidente_mayor_distancia = accidente_actual

            # Calcular promedios
            visibilidad_promedio = visibilidad_total / num_accidentes
            distancia_promedio = distancia_total / num_accidentes

            # Agregar los resultados del estado al análisis
            analisis_estados.append({
                "Estado": estado,
                "Total Accidentes": num_accidentes,
                "Visibilidad Promedio": visibilidad_promedio,
                "Distancia Promedio": distancia_promedio,
                "Accidente Mayor Distancia": {
                    "ID": accidente_mayor_distancia["id"],
                    "Fecha de Inicio": accidente_mayor_distancia["start_time"],
                    "Visibilidad": accidente_mayor_distancia.get("visibility(mi)", 0),  # Mostrar 0 si es None
                    "Distancia": accidente_mayor_distancia.get("distance(mi)", 0)  # Mostrar 0 si es None
                }
            })

    # Ordenar los estados por cantidad de accidentes de mayor a menor
    analisis_estados_ordenado = sorted(analisis_estados, key=lambda x: x["Total Accidentes"], reverse=True)
    aend_time = get_time()
    delta = delta_time(astart_time, aend_time)
    return analisis_estados_ordenado,delta

pass


def req_3(catalog, n):
    """
    Función para obtener los N accidentes más recientes y severos con visibilidad < 2 millas y precipitaciones.
    """
    # Suponiendo que `accidents_tree` es un árbol que ya contiene accidentes.
    my_rbt = catalog['accidents_tree']

    # Filtrar accidentes en el árbol con visibilidad < 2 millas y precipitaciones
    astart_time = get_time()
    accidentes_filtrados = al.new_list()
    
    search_tree(my_rbt, my_rbt["root"], datetime.min, datetime.max, accidentes_filtrados)

    # Seleccionar solo los accidentes que cumplen con los requisitos
    accidentes_validos = al.new_list()
    for i in range(al.size(accidentes_filtrados)):
        accidente = al.get_element(accidentes_filtrados, i)
        
        # Imprimir el contenido del accidente para depuración
        

        visibilidad = accidente.get("visibility(mi)")
        precipitacion = accidente.get("precipitation")
        
        # Verificar si cumple con los criterios
        if accidente['visibility(mi)'] is not None and accidente['visibility(mi)'] < 2 and accidente['precipitation(in)'] not in (None, 0.0):


        
            al.add_last(accidentes_validos, accidente)

    # Ordenar por severidad
    al.merge_sort(accidentes_validos, sort_criteria_by_severity)

    # Limitar la cantidad a N
    respuesta = accidentes_validos['elements'][:n] if n < al.size(accidentes_validos) else accidentes_validos['elements']

    # Obtener estadísticas del árbol
    height = rbt.height_tree(my_rbt["root"])
    node_count = rbt.size_tree(my_rbt["root"])
    element_count = rbt.size_tree(my_rbt["root"])
    aend_time = get_time()
    delta = delta_time(astart_time, aend_time)
    return al.size(accidentes_validos), respuesta, height, node_count, element_count,delta

    pass

def req_4(catalog,start_date_str, end_date_str):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    astart_time = get_time()
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
    aend_time = get_time()
    delta = delta_time(astart_time, aend_time)
    return total_accidents, respuesta, height, node_count, element_count,delta
            
            
    
pass


def clasificar_hora(hora):
    """Clasifica la hora en franjas horarias."""
    if hora >= 6 and hora < 12:
        return "Mañana"
    elif hora >= 12 and hora < 18:
        return "Tarde"
    elif hora >= 18 and hora < 24:
        return "Noche"
    else:
        return "Madrugada"
def count_accidents(my_rbt):
    count = 0
    
    def traverse_tree(node):
        nonlocal count
        if node is not None:
            traverse_tree(node['left'])
            count += 1  # Contar este nodo
            traverse_tree(node['right'])




def req_5(catalog, start_date_str, end_date_str, weather_conditions):
    # Obtiene el árbol de accidentes desde el control
    astart_time = get_time()
    my_rbt = catalog['accidents_tree']
    
    # Convierte las cadenas de fecha a objetos datetime
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    # Cuenta el total de accidentes en el árbol
    total_accidents_count = count_accidents(my_rbt)
   
    
    # Define las franjas horarias a analizar
    time_slots = [
        ("00:00 - 01:00"), ("01:00 - 02:00"), ("02:00 - 03:00"), 
        ("03:00 - 04:00"), ("04:00 - 05:00"), ("05:00 - 06:00"), 
        ("06:00 - 07:00"), ("07:00 - 08:00"), ("08:00 - 09:00"),
        ("09:00 - 10:00"), ("10:00 - 11:00"), ("11:00 - 12:00"),
        ("12:00 - 13:00"), ("13:00 - 14:00"), ("14:00 - 15:00"),
        ("15:00 - 16:00"), ("16:00 - 17:00"), ("17:00 - 18:00"),
        ("18:00 - 19:00"), ("19:00 - 20:00"), ("20:00 - 21:00"),
        ("21:00 - 22:00"), ("22:00 - 23:00"), ("23:00 - 00:00")
    ]
    
    # Inicializa una lista para almacenar los resultados
    results = []
    
    # Obtiene todos los accidentes del árbol
    accidents_list = get_all_accidents(my_rbt)  # Asegúrate de que esta función esté implementada correctamente
    
    # Inicializa el conteo para cada franja horaria
    for time_slot in time_slots:
        total_accidents = 0  # Contador para accidentes en la franja actual
        total_severity = 0    # Contador para la severidad total en la franja actual
        weather_count = {}    # Diccionario para contar las condiciones climáticas
        
        # Filtrar accidentes según las condiciones y las fechas
        for accident_id in accidents_list:
            accident_data = get_data(catalog, accident_id)  # Obtiene los datos del accidente
          
            
            # Verifica que los datos del accidente sean válidos
            if accident_data is not None and isinstance(accident_data, dict):
                # Obtén la fecha directamente del objeto datetime
                accident_date = accident_data['start_time']  # Debe ser un objeto datetime

                # Verifica si la fecha del accidente está dentro del rango especificado
                if start_date <= accident_date <= end_date:
                    # Filtrar por condiciones climáticas
                    accident_weather = accident_data.get('weather_condition', '')
                    if accident_weather in weather_conditions:
                        # Obtener la hora del accidente
                        accident_time_hour = accident_date.hour  # Usa directamente el objeto datetime
                        accident_time_slot = f"{accident_time_hour:02}:00 - {accident_time_hour + 1:02}:00"
                        
                        # Verificar si el accidente está en la franja horaria actual
                        if accident_time_slot == time_slot:
                            total_accidents += 1  # Incrementa el contador de accidentes
                            total_severity += accident_data.get('severity', 0)  # Suma la severidad del accidente
                            # Incrementa el conteo de la condición climática
                            weather_count[accident_weather] = weather_count.get(accident_weather, 0) + 1

        # Calcular severidad promedio
        average_severity = total_severity / total_accidents if total_accidents > 0 else 0
        # Determinar la condición climática predominante
        predominant_weather = max(weather_count, key=weather_count.get) if weather_count else "N/A"

        # Almacena los resultados de la franja horaria actual
        results.append({
            "time_slot": time_slot,
            "total_accidents": total_accidents,
            "average_severity": average_severity,
            "predominant_weather": predominant_weather
        })
    
    # Obtener características del árbol
    height = rbt.height_tree(my_rbt["root"])  # Altura del árbol
    node_count = rbt.size_tree(my_rbt["root"])  # Conteo de nodos en el árbol
    element_count = rbt.size_tree(my_rbt["root"])  # Conteo de elementos en el árbol
    aend_time = get_time()
    delta = delta_time(astart_time, aend_time)
    # Retorna los resultados, altura, conteo de nodos y conteo de elementos
    return results, height, node_count, element_count,delta

def get_all_accidents(my_rbt):
    """
    Función auxiliar para obtener todos los accidentes del árbol.
    
    Args:
        my_rbt: El árbol rojo-negro de accidentes.

    Returns:
        List: Lista de todos los accidentes.
    """
    # Aquí debes implementar la lógica para recorrer el árbol y obtener todos los accidentes
    # Por ejemplo, un recorrido en orden (in-order) podría funcionar
    accidents = []
    
    def traverse_tree(node):
        if node is not None:
            traverse_tree(node['left'])  # Llamada recursiva a la izquierda
            accidents.append(node['key'])  # Asumiendo que los datos del accidente están aquí
            traverse_tree(node['right'])  # Llamada recursiva a la derecha

    traverse_tree(my_rbt['root'])  # Comenzar desde la raíz
    return accidents

def req_6(catalog,start_date_str, end_date_str, humedad, lst_condados):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    astart_time = get_time()
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
    aend_time = get_time()
    delta = delta_time(astart_time, aend_time)
    return total_accidents, respuesta, height, node_count, element_count,delta
        
        
         
                    
                    
    pass
def traverse_tree(node, min_lat, max_lat, min_long, max_long, accidents_in_range):
    """
    Realiza un recorrido en orden del árbol rojo-negro y agrega los accidentes dentro del rango geográfico
    especificado a la lista `accidents_in_range`.
    
    Parámetros:
    - node: el nodo actual del árbol (inicia con el nodo raíz).
    - min_lat, max_lat: rango de latitud.
    - min_long, max_long: rango de longitud.
    - accidents_in_range: lista para almacenar los accidentes en el rango.
    """
    if node is None:
        return  # Caso base: si el nodo es None, termina la recursión

    # Recorrido en orden (izquierda - nodo - derecha)

    # 1. Visitar el subárbol izquierdo
    traverse_tree(node['left'], min_lat, max_lat, min_long, max_long, accidents_in_range)
    
    # 2. Procesar el nodo actual (si tiene datos de accidente)
    accident_data = node['value']
    if accident_data is not None:
        start_lat = accident_data.get('start_lat', 0)
        start_lng = accident_data.get('start_lng', 0)  # Asegurado de coincidir con la carga de datos

        # Comprobar si el accidente está dentro del rango de latitud y longitud
        if min_lat <= start_lat <= max_lat and min_long <= start_lng <= max_long:
            # Recopilar información del accidente
            accident_info = {
                "accident_id": accident_data.get('id', ''),
                "start_time": accident_data.get('start_time', datetime.now()),
                "city": accident_data.get('city', 'N/A'),
                "state": accident_data.get('state', 'N/A'),
                "description": accident_data.get('description', '')[:40],  # Limitar a 40 caracteres
                "duration_hours": accident_data.get('duration_hours', 0),
                "start_lat": start_lat,
                "start_lng": start_lng
            }
            # Agregar el accidente a la lista
            accidents_in_range['elements'].append(accident_info)
            # Incrementar el tamaño de la lista
            accidents_in_range['size'] += 1

    # 3. Visitar el subárbol derecho
    traverse_tree(node['right'], min_lat, max_lat, min_long, max_long, accidents_in_range)



def count_nodes_in_tree(node):
    """
    Cuenta los nodos en un árbol rojo-negro, comenzando desde el nodo dado.
    
    Parámetro:
    - node: el nodo actual del árbol
    
    Retorna:
    - La cantidad total de nodos en el árbol.
    """
    if node is None:
        return 0
    # Contar el nodo actual y luego contar en sus hijos izquierdo y derecho
    return 1 + count_nodes_in_tree(node['left']) + count_nodes_in_tree(node['right'])

def req_7(catalog, min_lat, max_lat, min_long, max_long):
    """
    Obtiene los accidentes en un rango geográfico y retorna una selección de ellos.
    
    Parámetros:
    - catalog: diccionario que contiene el árbol de accidentes ('accidents_tree')
    - min_lat, max_lat: rango de latitud
    - min_long, max_long: rango de longitud
    
    Retorna:
    - Diccionario con el total de accidentes en el rango y la lista de accidentes seleccionados.
    """
    # Lista para almacenar los accidentes encontrados en el rango
    astart_time = get_time()
    accidents_in_range = al.new_list()
    
    # Obtener el árbol de accidentes desde el catálogo
    accidents_tree = catalog.get('accidents_tree')
    
    # Realizar el recorrido del árbol en busca de accidentes en el rango
    traverse_tree(accidents_tree['root'], min_lat, max_lat, min_long, max_long, accidents_in_range)
    
    # Calcular el total de accidentes en el rango
    total_accidents_in_range = accidents_in_range["size"]
    
    # Seleccionar una muestra (por ejemplo, los primeros 5 accidentes) para mostrar
    selected_accidents = accidents_in_range["elements"][:5] if accidents_in_range else []
    
    # Retornar el total y la muestra de accidentes
    aend_time = get_time()
    delta = delta_time(astart_time, aend_time)
    return {
        "total_accidents_in_range": total_accidents_in_range,
        "accidents": selected_accidents
    },delta






pass

 
def req_8(catalog):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    astart_time = get_time()
    
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
