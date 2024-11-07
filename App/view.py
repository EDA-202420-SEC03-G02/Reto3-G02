import sys
import sys
import App.logic as lg
from tabulate import tabulate
from datetime import datetime

def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función de la lógica donde se crean las estructuras de datos
    return lg.new_logic()
pass

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8 (Bono)")
    print("0- Salir")

def load_data(control):
    """
    Carga los datos de los accidentes y muestra el total de accidentes cargados,
    así como los cinco primeros y cinco últimos accidentes.
    """    
    print("Cargando información de los accidentes...")
    total_accidents, first_five, last_five = lg.load_data(control, "accidents-large.csv")

    print(f"\nTotal de accidentes cargados: {total_accidents}")
    
    print("\nPrimeros cinco accidentes cargados:")
    display_accidents(first_five)
    
    print("\nÚltimos cinco accidentes cargados:")
    display_accidents(last_five)

def display_accidents(accidents):
    """
    Muestra la información requerida de un conjunto de accidentes en formato tabular.
    """
    table = []
    for accident in accidents:
        table.append([
            accident["id"],
            accident["start_time"],
            accident["city"],
            accident["state"],
            accident["description"],
            f"{accident['duration_hours']:.3f}"
        ])
    
    # Usamos tabulate para imprimir los resultados en formato tabular
    print(tabulate(table, headers=[
        "ID", "Fecha y Hora de Inicio", "Ciudad", "Estado", "Descripción", "Duración (horas)"
    ], tablefmt="fancy_grid"))

def print_req_1(control):
    """
    Función que imprime la solución del Requerimiento 1 en consola
    """
    # Solicitar las fechas de inicio y fin al usuario
    start_date = str(input("Ingrese la fecha inicial del período a consultar (formato %Y-%m-%d %H:%M:%S): "))
    end_date = str(input("Ingrese la fecha final del período a consultar (formato %Y-%m-%d %H:%M:%S): "))
    
    # Llamar a la función que obtiene la información de los accidentes
    total_accidents, accidents_info, height, node_count, element_count = lg.req_1(control, start_date, end_date)
    
    # Imprimir el total de accidentes
    print(f"Total de accidentes en el intervalo de fechas: {total_accidents}")
    
    
    if total_accidents > 10:
        # Primeros 5 accidentes
        first_five = accidents_info[:5]
        last_five = accidents_info[-5:]

        # Tabla para los primeros 5 accidentes
        print("\nPrimeros 5 accidentes:")
        table_first_five = []
        for accident in first_five:
            table_first_five.append([
                accident['id'],
                accident['start_time'],
                f"{accident['city']} - {accident['state']}",
                accident['description'][:40],  # limitar la descripción a 40 caracteres
                f"{accident['duration_hours']:.3f} horas"  # Usar get para evitar KeyError
            ])
        
        headers = ["ID", "Fecha y hora de inicio", "Ciudad y estado", "Descripción", "Duración"]
        print(tabulate(table_first_five, headers=headers, tablefmt="grid"))

        # Tabla para los últimos 5 accidentes
        print("\nÚltimos 5 accidentes:")
        table_last_five = []
        for accident in last_five:
            table_last_five.append([
                accident['id'],
                accident['start_time'],
                f"{accident['city']} - {accident['state']}",
                accident['description'][:40],  # limitar la descripción a 40 caracteres
                f"{accident['duration_hours']:.3f} horas"  
            ])
        
        print(tabulate(table_last_five, headers=headers, tablefmt="grid"))
    else:
        # Si hay 10 o menos accidentes, imprimir todos en una sola tabla
        print("Lista de accidentes:")
        table = []
        for accident in accidents_info:
            table.append([
                accident['id'],
                accident['start_time'],
                f"{accident['city']} - {accident['state']}",
                accident['description'][:40],  # limitar la descripción a 40 caracteres
                f"{accident['duration_hours']:.3f} horas"  
            ])

        headers = ["ID", "Fecha y hora de inicio", "Ciudad y estado", "Descripción", "Duración"]
        print(tabulate(table, headers=headers, tablefmt="grid"))
    
    # Imprimir características del árbol
    print("Características del árbol:")
    print(f"Altura: {height}")
    print(f"Número de nodos: {node_count}")
    print(f"Número de elementos: {element_count}")
pass


def print_req_2(control):
    """
    Función que imprime la solución del Requerimiento 2 en consola.
    """
    # Solicitar el rango de visibilidad al usuario
    visibilidad_min = float(input("Ingrese el límite inferior del rango de visibilidad en millas: "))
    visibilidad_max = float(input("Ingrese el límite superior del rango de visibilidad en millas: "))
    visibilidad_rango = (visibilidad_min, visibilidad_max)

    # Solicitar la lista de estados al usuario
    lista_estados_input = input("Ingrese la lista de estados separados por comas (por ejemplo, CA,NY,TX): ")
    lista_estados = [estado.strip() for estado in lista_estados_input.split(",") if estado.strip()]

    if not lista_estados:
        print("Error: Debe ingresar al menos un estado.")
        return

    # Llamar a la función que obtiene la información de los accidentes
    resultados = lg.req_2(control, visibilidad_rango, lista_estados)

    # Imprimir el total de accidentes
    total_accidentes = sum(estado["Total Accidentes"] for estado in resultados)
    print(f"Total de accidentes graves en el rango de visibilidad {visibilidad_rango}: {total_accidentes}")
    print("=" * 80)

    # Imprimir el análisis por estado en tablas
    for estado in resultados:
        print(f"Estado: {estado['Estado']}")
        
        # Información general de accidentes en el estado
        table_estado = [
            [
                estado["Total Accidentes"],
                f"{estado['Visibilidad Promedio']:.2f} millas",
                f"{estado['Distancia Promedio']:.2f} millas"
            ]
        ]
        headers_estado = ["Total Accidentes", "Visibilidad Promedio", "Distancia Promedio"]
        print(tabulate(table_estado, headers=headers_estado, tablefmt="grid"))

        # Información del accidente con mayor distancia afectada
        accidente_mayor_distancia = estado["Accidente Mayor Distancia"]
        table_accidente = [
            [
                accidente_mayor_distancia['ID'],
                accidente_mayor_distancia['Fecha de Inicio'],
                accidente_mayor_distancia['Visibilidad'],
                accidente_mayor_distancia['Distancia']
            ]
        ]
        headers_accidente = ["ID", "Fecha de Inicio", "Visibilidad", "Distancia Afectada"]
        print("\nAccidente con mayor distancia afectada:")
        print(tabulate(table_accidente, headers=headers_accidente, tablefmt="grid"))
        print("-" * 80)

    

    

    pass


def print_req_3(control):
    """
    Función que imprime la solución del Requerimiento 3 en consola.
    """
    n = int(input("Ingrese el número N de accidentes a mostrar: "))
    total_accidentes, respuesta, height, node_count, element_count = lg.req_3(control, n) 

    # Imprimir total de accidentes encontrados
    print(f"Total de accidentes encontrados: {total_accidentes}")
    print("\nAccidentes más recientes y severos con visibilidad menor a 2 millas y precipitaciones:")

    # Crear la tabla para los accidentes
    accidentes_tabla = [
        [
            accidente.get('id', 'N/A'),
            accidente.get('start_time', 'N/A'),
            accidente.get('city', 'N/A'),
            accidente.get('state', 'N/A'),
            accidente.get('description', 'N/A')[:40],
            accidente.get('duration_hours', 'N/A')
        ]
        for accidente in respuesta if isinstance(accidente, dict)
    ]
    
    # Encabezados para la tabla de accidentes
    headers_accidentes = ["ID", "Fecha de Inicio", "Ciudad", "Estado", "Descripción", "Duración (horas)"]
    print(tabulate(accidentes_tabla, headers=headers_accidentes, tablefmt="grid"))

    # Crear tabla para las características del árbol
    tree_stats = [
        ["Altura del árbol", height],
        ["Número de nodos en el árbol", node_count],
        ["Cantidad de elementos en el árbol", element_count]
    ]
    print("\nCaracterísticas del árbol rojo-negro:")
    print(tabulate(tree_stats, tablefmt="grid"))

    

    pass


def print_req_4(control):
    """
    Función que imprime la solución del Requerimiento 4 en consola
    """
    # Solicitar las fechas de inicio y fin al usuario
    start_date = str(input("Ingrese la fecha inicial del período a consultar (formato %Y-%m-%d %H:%M:%S): "))
    end_date = str(input("Ingrese la fecha final del período a consultar (formato %Y-%m-%d %H:%M:%S): "))
    
    # Llamar a la función que obtiene la información de las vías y accidentes
    total_accidents, roads_info, height, node_count, element_count = lg.req_4(control, start_date, end_date)
    
    # Verificar si se obtuvo información
    if not roads_info:
        print("No se encontraron datos para el intervalo de fechas proporcionado.")
        return
    
    # Crear una tabla para mostrar la información de las vías
    table = []
    for road in roads_info["elements"]:
        table.append([
            road['street'],  # Nombre de la vía
            road['city'],    # Ciudad
            road['county'],  # Condado
            road['state'],   # Estado
            (road['number_severity_3'] + road['number_severity_4']) / (road['number_severity_3'] + road['number_severity_4']) if (road['number_severity_3'] + road['number_severity_4']) > 0 else 0,  # Peligrosidad promedio
            road['number_severity_3'],  # Total de accidentes severidad 3
            road['number_severity_4'],  # Total de accidentes severidad 4
            road['Average_visibility']  # Visibilidad promedio
        ])
    
    # Definir los encabezados de la tabla
    headers = [
        "Nombre de la vía", 
        "Ciudad", 
        "Condado", 
        "Estado", 
        "Peligrosidad Promedio", 
        "Total Accidentes Severidad 3", 
        "Total Accidentes Severidad 4", 
        "Visibilidad Promedio"
    ]
    
    # Imprimir la tabla
    print(tabulate(table, headers=headers, tablefmt="grid"))

    # Imprimir características del árbol
    print("Características del árbol:")
    print(f"Altura: {height}")
    print(f"Número de nodos: {node_count}")
    print(f"Número de elementos: {element_count}")




def print_req_5(control):
    """
    Función que imprime la solución del Requerimiento 5 en consola.
    """
    # Solicitar las fechas de inicio y fin al usuario
    start_date = str(input("Ingrese la fecha inicial del período a consultar (formato %Y-%m-%d): "))
    end_date = str(input("Ingrese la fecha final del período a consultar (formato %Y-%m-%d): "))
    
    # Solicitar las condiciones climáticas
    weather_conditions_input = input("Ingrese las condiciones climáticas separadas por comas (ejemplo: niebla, lluvia): ")
    # Convertir la entrada de condiciones climáticas en una lista
    weather_conditions = [condition.strip() for condition in weather_conditions_input.split(",")]
    
    # Llamar a la función que obtiene la información de los accidentes
    results, height, node_count, element_count = lg.req_5(control, start_date, end_date, weather_conditions)
    
    # Imprimir resultados en tabla
    print("\nResultados del Requerimiento 5:")
    results_table = [
        [
            result["time_slot"],
            result["total_accidents"],
            f"{result['average_severity']:.2f}",
            result["predominant_weather"]
        ]
        for result in results if isinstance(result, dict)
    ]
    
    # Encabezados para la tabla de resultados
    headers_results = ["Franja Horaria", "Total Accidentes Graves", "Promedio Severidad", "Condición Climática Predominante"]
    print(tabulate(results_table, headers=headers_results, tablefmt="grid"))

    # Tabla para las características del árbol
    tree_stats = [
        ["Altura del árbol", height],
        ["Número de nodos en el árbol", node_count],
        ["Cantidad de elementos en el árbol", element_count]
    ]
    print("\nCaracterísticas del árbol de accidentes:")
    print(tabulate(tree_stats, tablefmt="grid"))

    




def print_req_6(control):
    """
    Función que imprime la solución del Requerimiento 6 en consola
    """
    # Solicitar las fechas de inicio y fin al usuario
    start_date = str(input("Ingrese la fecha inicial del período a consultar (formato %Y-%m-%d %H:%M:%S): "))
    end_date = str(input("Ingrese la fecha final del período a consultar (formato %Y-%m-%d %H:%M:%S): "))
    humedad = float(input("Ingrese el nivel mínimo de humedad (en %): "))
    lst_condados = input("Ingrese la lista de condados separados por comas: ").split(",")
    
    # Llamar a la función que obtiene la información de los accidentes
    total_accidents, counties_info, height, node_count, element_count = lg.req_6(control, start_date, end_date, humedad, lst_condados)
    
    # Verificar si se obtuvo información
    if not counties_info:
        print("No se encontraron datos para el intervalo de fechas y condiciones proporcionadas.")
        return
    
    # Crear una tabla para mostrar la información de los condados
    table = []
    for county_data in counties_info["elements"]:
        table.append([
            county_data['county'],  # Condado
            county_data['Accidents_county'],  # Número de accidentes en el condado
            county_data['Average_temperature'],  # Temperatura promedio
            county_data['Average_humidity'],  # Humedad promedio
            county_data['Average_wind_speed'],  # Velocidad del viento promedio
            county_data['Average_distance'],  # Distancia promedio
            county_data['id'],  # ID del accidente más severo
            county_data['temperature(f)'],  # Temperatura del accidente más severo
            county_data['humidity(%)'],  # Humedad del accidente más severo
            county_data['distance(mi)'],  # Distancia del accidente más severo
            county_data['description']  # Descripción del accidente más severo
        ])
    
    # Definir los encabezados de la tabla
    headers = [
        "Condado", 
        "Número de Accidentes", 
        "Temperatura Promedio (°F)", 
        "Humedad Promedio (%)", 
        "Velocidad del Viento Promedio (mph)", 
        "Distancia Promedio (mi)", 
        "ID del Accidente Más Severo", 
        "Temperatura del Accidente Más Severo (°F)", 
        "Humedad del Accidente Más Severo (%)", 
        "Distancia del Accidente Más Severo (mi)", 
        "Descripción del Accidente Más Severo"
    ]
    
    # Imprimir la tabla
    print(tabulate(table, headers=headers, tablefmt="grid"))

    # Imprimir características del árbol
    print("Características del árbol:")
    print(f"Altura: {height}")
    print(f"Número de nodos: {node_count}")
    print(f"Número de elementos: {element_count}")




def print_req_7(control):
    """
    Función que imprime la solución del Requerimiento 7 en consola.
    """
    # Solicitar los límites geográficos
    min_lat = float(input("Ingrese la latitud mínima: "))
    max_lat = float(input("Ingrese la latitud máxima: "))
    min_long = float(input("Ingrese la longitud mínima: "))
    max_long = float(input("Ingrese la longitud máxima: "))
    
    # Llamar a la función req_7 con los límites geográficos
    result = lg.req_7(control, min_lat, max_lat, min_long, max_long)
    
    # Imprimir el conteo total de accidentes en el rango
    print("Total de accidentes en el rango geográfico:", result["total_accidents_in_range"])
    
    # Preparar los detalles de cada accidente en formato de tabla
    accidents_table = [
        [
            accident["accident_id"],
            accident["start_time"],
            accident["city"],
            accident["state"],
            accident["description"],
            accident["duration_hours"]
        ]
        for accident in result["accidents"]
    ]
    
    # Encabezados para la tabla de accidentes
    headers = ["ID del Accidente", "Fecha y Hora de Inicio", "Ciudad", "Estado", "Descripción", "Duración (horas)"]
    
    # Imprimir la tabla de accidentes
    print("\nLista de accidentes en el rango geográfico:")
    print(tabulate(accidents_table, headers=headers, tablefmt="grid"))

    



def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
