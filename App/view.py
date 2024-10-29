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
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass


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
