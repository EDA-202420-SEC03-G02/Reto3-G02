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
    filename=r"C:\\Users\\danie\\Downloads\\reto 3\\Reto3-G02-1\\Data\\accidents-small.csv"
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
    for i in range(array.size(analisis_estados) - 1):
        for j in range(i + 1, array.size(analisis_estados)):
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



def req_2(catalog, visibilidad_rango, lista_estados):
    
    min_visibilidad, max_visibilidad = visibilidad_rango
    accidentes_filtrados = array.new_list()

    # Filtrar los accidentes en el árbol dentro del rango de visibilidad y gravedad 4
    search_tree(catalog['accidents_tree'], catalog['accidents_tree']["root"], datetime.min, datetime.max, accidentes_filtrados)

    # Seleccionar solo los accidentes con gravedad 4, visibilidad en el rango, y en los estados especificados
    accidentes_validos = array.new_list()
    for i in range(array.size(accidentes_filtrados)):
        accidente = array.get_element(accidentes_filtrados, i)
        visibilidad = accidente.get("visibility(mi)")  # Usa get para evitar KeyError
        if (accidente["severity"] == 4 and 
            visibilidad is not None and  # Asegúrate de que visibilidad no sea None
            min_visibilidad <= visibilidad <= max_visibilidad and 
            accidente["state"] in lista_estados):
            array.add_last(accidentes_validos, accidente)

    # Análisis por estado
    analisis_estados = []
    for estado in lista_estados:
        accidentes_estado = array.new_list()
        
        # Filtrar accidentes por estado
        for j in range(array.size(accidentes_validos)):
            accidente = array.get_element(accidentes_validos, j)
            if accidente['state'] == estado:
                array.add_last(accidentes_estado, accidente)

        if array.size(accidentes_estado) > 0:
            # Cálculo de estadísticas
            num_accidentes = array.size(accidentes_estado)
            visibilidad_total = 0
            distancia_total = 0
            accidente_mayor_distancia = array.get_element(accidentes_estado, 0)

            for k in range(num_accidentes):
                accidente_actual = array.get_element(accidentes_estado, k)
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

    return analisis_estados_ordenado

    pass


def req_3(catalog, n):
    """
    Función para obtener los N accidentes más recientes y severos con visibilidad < 2 millas y precipitaciones.
    """
    # Suponiendo que `accidents_tree` es un árbol que ya contiene accidentes.
    my_rbt = catalog['accidents_tree']

    # Filtrar accidentes en el árbol con visibilidad < 2 millas y precipitaciones
    accidentes_filtrados = array.new_list()
    search_tree(my_rbt, my_rbt["root"], datetime.min, datetime.max, accidentes_filtrados)

    # Seleccionar solo los accidentes que cumplen con los requisitos
    accidentes_validos = array.new_list()
    for i in range(array.size(accidentes_filtrados)):
        accidente = array.get_element(accidentes_filtrados, i)
        
        # Imprimir el contenido del accidente para depuración
        

        visibilidad = accidente.get("visibility(mi)")
        precipitacion = accidente.get("precipitation")
        
        # Verificar si cumple con los criterios
        if accidente['visibility(mi)'] is not None and accidente['visibility(mi)'] < 2 and accidente['precipitation(in)'] not in (None, 0.0):


        
            array.add_last(accidentes_validos, accidente)

    # Ordenar por severidad
    array.merge_sort(accidentes_validos, sort_criteria_by_severity)

    # Limitar la cantidad a N
    respuesta = accidentes_validos['elements'][:n] if n < array.size(accidentes_validos) else accidentes_validos['elements']

    # Obtener estadísticas del árbol
    height = rbt.height_tree(my_rbt["root"])
    node_count = rbt.size_tree(my_rbt["root"])
    element_count = rbt.size_tree(my_rbt["root"])

    return array.size(accidentes_validos), respuesta, height, node_count, element_count

    pass

def req_4(catalog,start_date_str, end_date_str):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
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

    traverse_tree(my_rbt['root'])
    return count



def req_5(control, start_date_str, end_date_str, weather_conditions):
    # Obtiene el árbol de accidentes desde el control
    my_rbt = control['accidents_tree']
    
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
            accident_data = get_data(control, accident_id)  # Obtiene los datos del accidente
          
            
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

    # Retorna los resultados, altura, conteo de nodos y conteo de elementos
    return results, height, node_count, element_count

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



def req_6(catalog,start_date_str, end_date_str,Humidity,condado):
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
