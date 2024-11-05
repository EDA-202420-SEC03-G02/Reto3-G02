RED = 0
BLACK = 1
def rotate_left(node):
    """
    Realiza una rotación a la izquierda en el nodo.
    
    Args:
        node: El nodo en el que se realizará la rotación

    Returns:
        El nuevo nodo raíz después de la rotación
    """
    right_child = node["right"]
    node["right"] = right_child["left"]
    right_child["left"] = node
    right_child["color"] = node["color"]
    change_color(node, RED)
    
    # Actualizar el tamaño de los subárboles
    right_child["size"] = node["size"]
    node["size"] = 1 + (node["left"]["size"] if node["left"] else 0) + (node["right"]["size"] if node["right"] else 0)
    
    return right_child
def rotate_right(node):
    """
    Realiza una rotación a la derecha en el nodo.
    
    Args:
        node: El nodo en el que se realizará la rotación

    Returns:
        El nuevo nodo raíz después de la rotación
    """
    left_child = node["left"]
    node["left"] = left_child["right"]
    left_child["right"] = node
    left_child["color"] = node["color"]
    change_color(node, RED)
    
    # Actualizar el tamaño de los subárboles
    left_child["size"] = node["size"]
    node["size"] = 1 + (node["left"]["size"] if node["left"] else 0) + (node["right"]["size"] if node["right"] else 0)
    
    return left_child
def flip_colors(node):
    """
    Cambia el color del nodo y de sus hijos.
    
    Args:
        node: El nodo cuyo color y el de sus hijos serán cambiados

    Returns:
        None
    """
    change_color(node, RED if node["color"] == BLACK else BLACK)
    if node["left"]:
        change_color(node["left"], BLACK if node["left"]["color"] == RED else RED)
    if node["right"]:
        change_color(node["right"], BLACK if node["right"]["color"] == RED else RED)

def insert_node(node, key, value):
    # Caso base: crear un nuevo nodo rojo si el nodo es None (hoja vacía)
    if node is None:
        return new_node(key, value, RED)

    # Insertar el nodo en la posición correcta (comportamiento de un BST)
    if key < get_key(node):
        node["left"] = insert_node(node["left"], key, value)
    elif key > get_key(node):
        node["right"] = insert_node(node["right"], key, value)
    else:
        # Si la clave ya existe, actualizar el valor
        node["value"] = value
        return node

    # Mantener las propiedades del árbol rojo-negro
    if is_red(node["right"]) and not is_red(node["left"]):
        node = rotate_left(node)
    if is_red(node["left"]) and is_red(node["left"]["left"]):
        node = rotate_right(node)
    if is_red(node["left"]) and is_red(node["right"]):
        flip_colors(node)

    # Actualizar el tamaño del subárbol
    node["size"] = 1 + (node["left"]["size"] if node["left"] else 0) + (node["right"]["size"] if node["right"] else 0)
    return node

def new_node(key, value, color=RED):
    """
    Crea un nuevo nodo para un árbol rojo-negro  y lo retorna.
    color:0 - rojo  color:1 - negro
    Args:
        value: El valor asociado a la llave
        key: la llave asociada a la pareja
        size: El tamaño del subarbol que cuelga de este nodo
        color: El color inicial del nodo

    Returns:
        Un nodo con la pareja <llave, valor>
    Raises:
        Exception
    """
    node = {
        "key": key,
        "value": value,
        "size": 1,
        "left": None,
        "right": None,
        "color": color,
        "type": "RBT",
    }

    return node


def is_red(my_node):
    """
    Informa si un nodo es rojo
    Args:
        my_node: El nodo a revisar

    Returns:
        True si el nodo es rojo, False de lo contrario
    Raises:
        Exception
    """
    return my_node is not None and my_node["color"] == RED


def get_value(my_node):
    """Retorna el valor asociado a una pareja llave valor
    Args:
        my_node: El nodo con la pareja llave-valor
    Returns:
        El valor almacenado en el nodo
    Raises:
        Exception
    """
    value = None
    if my_node is not None:
        value = my_node["value"]
    return value


def get_key(my_node):
    """Retorna la llave asociado a una pareja llave valor
    Args:
        my_node: El nodo con la pareja llave-valor
    Returns:
        La llave almacenada en el nodo
    Raises:
        Exception
    """
    key = None
    if my_node is not None:
        key = my_node["key"]
    return key


def change_color(my_node, color):
    """Cambia el color de un nodo
    Args:
        my_node: El nodo a cambiar
        color: El nuevo color del nodo
    Returns:
        None
    Raises:
        Exception
    """
    my_node["color"] = color


def new_map():
    my_rbt={
        "root":None,
        "type":"RBT"
    }
    return my_rbt

def put(my_rbt, key, value):
    my_rbt["root"] = insert_node(my_rbt["root"], key, value)
    # Asegurarse de que la raíz sea negra después de la inserción
    change_color(my_rbt["root"], BLACK)
    return my_rbt

def get_node(node, key):
    """
    Busca un nodo con una llave específica en el árbol rojo-negro.
    Args:
        node: El nodo actual en el árbol durante la búsqueda
        key: La llave a buscar

    Returns:
        El nodo que contiene la llave `key`, o None si no se encuentra.
    """
    while node is not None:
        if key < node["key"]:
            node = node["left"]
        elif key > node["key"]:
            node = node["right"]
        else:
            return node
    return None
    
def get(my_rbt, key):
    node = get_node(my_rbt["root"], key)
    return node["value"] if node is not None else None


def contains(my_rbt, key):
    return get(my_rbt, key) is not None



def size_tree(node):
    """
    Retorna el número de nodos en el árbol rojo-negro.

    Args:
        node: El nodo raíz del árbol (o subárbol).

    Returns:
        El número de nodos en el árbol.
    """
    if node is None:
        return 0  # Si el nodo es None, no hay nodos en este subárbol

    # Contar el nodo actual y recursivamente contar los nodos en los hijos izquierdo y derecho
    left_size = size_tree(node.get("left"))  # Usa get para evitar KeyError
    right_size = size_tree(node.get("right"))  # Usa get para evitar KeyError

    return 1 + left_size + right_size


def size(my_rbt):
    """Retorna el número de entradas en la tabla de símbolos."""
    if my_rbt["root"] is None:
        return 0  # El árbol está vacío, retorna 0
    return size_tree(my_rbt["root"])  # Retorna el tamaño del subárbol comenzando desde la raíz

def is_empty(my_rbt):
    return my_rbt["root"] is None  # Retorna True si la raíz es None


def key_set_tree(node):
    """
    Recolecta las llaves del árbol en una lista.
    
    :param node: El nodo actual del árbol
    :type node: dict
    :return: Lista de llaves en el subárbol
    :rtype: list
    """
    keys = []
    if node is not None:
        keys.extend(key_set_tree(node["left"]))   # Recursión al hijo izquierdo
        keys.append(node["key"])                   # Agregar la llave del nodo actual
        keys.extend(key_set_tree(node["right"]))  # Recursión al hijo derecho
    return keys

def key_set(my_rbt):
  
   if my_rbt is None or "root" not in my_rbt:
        raise ValueError("El árbol no está inicializado correctamente.")
    
   keys = key_set_tree(my_rbt["root"]) if my_rbt["root"] is not None else []

   return {
        "size": len(keys),
        "elements": keys  # Cambiar "keys" a "elements"
     }


def value_set_tree(node):
    """
    Recolecta todos los valores del árbol y los retorna en una lista.
    
    :param node: Nodo actual del árbol
    :type node: dict
    :return: Lista de valores
    :rtype: list
    """
    if node is None:
        return []
    
    # Recolectar valores recursivamente
    return value_set_tree(node["left"]) + [node["value"]] + value_set_tree(node["right"])

def value_set(my_rbt):
    values = value_set_tree(my_rbt["root"]) if my_rbt["root"] is not None else []
    return {
        "size": len(values),
        "elements": values  
     }

def min_key(my_rbt):
    """
    Retorna la clave mínima en el árbol rojo-negro.
    
    :param my_rbt: El árbol de búsqueda
    :type my_rbt: dict
    :return: La clave mínima, o None si el árbol está vacío
    :rtype: any
    """
    if my_rbt["root"] is None:
        return None  # Si el árbol está vacío

    return min_key_tree(my_rbt["root"])


def max_key(my_rbt):
    """
    Retorna la clave máxima en el árbol rojo-negro.
    
    :param my_rbt: El árbol de búsqueda
    :type my_rbt: dict
    :return: La clave máxima, o None si el árbol está vacío
    :rtype: any
    """
    if my_rbt["root"] is None:
        return None  # Si el árbol está vacío

    return max_key_tree(my_rbt["root"])


def min_key_tree(node):
    """
    Encuentra la clave mínima en el subárbol.
    
    :param node: Nodo actual del árbol
    :type node: dict
    :return: La clave mínima en el subárbol
    :rtype: any
    """
    current = node
    while current["left"] is not None:
        current = current["left"]
    return current["key"]


def max_key_tree(node):
    """
    Encuentra la clave máxima en el subárbol.
    
    :param node: Nodo actual del árbol
    :type node: dict
    :return: La clave máxima en el subárbol
    :rtype: any
    """
    current = node
    while current["right"] is not None:
        current = current["right"]
    return current["key"]

def floor(my_rbt, key):
    """
    Retorna la llave que precede a la llave key en el árbol rojo-negro.
    
    :param my_rbt: El árbol de búsqueda
    :type my_rbt: dict
    :param key: La llave de búsqueda
    :type key: any
    :return: La llave predecesora a key
    :rtype: any
    """
    return floor_key(my_rbt["root"], key)


def floor_key(node, key):
    """
    Encuentra la llave predecesora a key en el subárbol.
    
    :param node: Nodo actual del árbol
    :type node: dict
    :param key: La llave de búsqueda
    :type key: any
    :return: La llave predecesora a key
    :rtype: any
    """
    if node is None:
        return None  # Si el nodo es None, no hay llaves en este subárbol

    # Si la llave del nodo es igual a key, retornamos esa llave
    if node["key"] == key:
        return node["key"]

    # Si la llave del nodo es mayor que key, buscamos en el subárbol izquierdo
    if node["key"] > key:
        return floor_key(node["left"], key)

    # Si la llave del nodo es menor que key, verificamos si hay una llave predecesora en el subárbol derecho
    right_floor = floor_key(node["right"], key)
    return right_floor if right_floor is not None else node["key"]

def ceiling(my_rbt, key):
    """
    Retorna la llave que sucede a la llave key en el árbol rojo-negro.
    
    :param my_rbt: El árbol de búsqueda
    :type my_rbt: dict
    :param key: La llave de búsqueda
    :type key: any
    :return: La llave sucesora a key
    :rtype: any
    """
    return ceiling_key(my_rbt["root"], key)


def ceiling_key(node, key):
    """
    Encuentra la llave sucesora a key en el subárbol.
    
    :param node: Nodo actual del árbol
    :type node: dict
    :param key: La llave de búsqueda
    :type key: any
    :return: La llave sucesora a key
    :rtype: any
    """
    if node is None:
        return None  # Si el nodo es None, no hay llaves en este subárbol

    # Si la llave del nodo es igual a key, retornamos esa llave
    if node["key"] == key:
        return node["key"]

    # Si la llave del nodo es menor que key, buscamos en el subárbol derecho
    if node["key"] < key:
        return ceiling_key(node["right"], key)

    # Si la llave del nodo es mayor que key, verificamos si hay una llave sucesora en el subárbol izquierdo
    left_ceiling = ceiling_key(node["left"], key)
    return left_ceiling if left_ceiling is not None else node["key"]

def select(my_rbt, pos):
    """
    Retorna la k-ésima llave en el árbol rojo-negro, de izquierda a derecha.
    
    :param my_rbt: El árbol de búsqueda
    :type my_rbt: dict
    :param pos: La posición de la llave (0-indexed)
    :type pos: int
    :return: La llave en la posición pos
    :rtype: any
    """
    return select_key(my_rbt["root"], pos)


def select_key(node, pos):
    """
    Encuentra la k-ésima llave en el subárbol.
    
    :param node: Nodo actual del árbol
    :type node: dict
    :param pos: La posición de la llave (0-indexed)
    :type pos: int
    :return: La llave en la posición pos
    :rtype: any
    """
    if node is None:
        return None  # Si el nodo es None, no hay llaves en este subárbol

    left_size = node["left"]["size"] if node["left"] is not None else 0

    if pos < left_size:
        return select_key(node["left"], pos)  # Busca en el subárbol izquierdo
    elif pos > left_size:
        return select_key(node["right"], pos - left_size - 1)  # Busca en el subárbol derecho, ajustando la posición
    else:
        return node["key"]  # El nodo actual es la k-ésima llave


def rank(my_rbt, key):
    """
    Retorna el número de llaves en el árbol que son estrictamente predecesoras a la llave key.
    
    :param my_rbt: El árbol de búsqueda
    :type my_rbt: dict
    :param key: La llave a buscar
    :type key: any
    :return: El número de llaves estrictamente menores que key
    :rtype: int
    """
    return rank_keys(my_rbt["root"], key)


def rank_keys(node, key):
    """
    Encuentra el número de llaves que son estrictamente predecesoras a key en el subárbol.
    
    :param node: Nodo actual del árbol
    :type node: dict
    :param key: La llave a buscar
    :type key: any
    :return: El número de llaves estrictamente menores que key
    :rtype: int
    """
    if node is None:
        return 0  # Si el nodo es None, no hay llaves en este subárbol

    if key < node["key"]:
        return rank_keys(node["left"], key)  # Solo buscamos en el subárbol izquierdo
    elif key > node["key"]:
        left_size = node["left"]["size"] if node["left"] is not None else 0
        return left_size + 1 + rank_keys(node["right"], key)  # Contamos el nodo actual y buscamos en el derecho
    else:
        # Si la llave es igual, no contamos el nodo actual
        return node["left"]["size"] if node["left"] is not None else 0
    

def height_tree(node):
    """
    Calcula la altura de un subárbol.

    :param node: Nodo actual del árbol
    :type node: dict
    :return: La altura del árbol
    :rtype: int
    """
    if node is None:
        return -1  # La altura de un árbol vacío se define como -1

    left_height = height_tree(node["left"])
    right_height = height_tree(node["right"])

    return 1 + max(left_height, right_height)  # La altura es 1 más que la mayor altura de los hijos

def height(my_rbt):
    """
    Retorna la altura del árbol de búsqueda.

    :param my_rbt: El árbol de búsqueda
    :type my_rbt: dict
    :return: La altura del árbol
    :rtype: int
    """
    return height_tree(my_rbt["root"])  # Calculamos la altura a partir de la raíz

def keys(my_rbt, key_initial, key_final):
    """
    Retorna todas las llaves del árbol que se encuentren entre [key_initial, key_final].
    
    Args:
        my_rbt (red_black_tree): La tabla de símbolos.
        key_initial (any): Límite inferior.
        key_final (any): Límite superior.
    
    Returns:
        dict: Un diccionario que contiene el tamaño y la lista de llaves en el rango especificado.
    """
    result = []
    # Usar la función keys_range() para obtener las llaves en el rango
    keys_range_tree(my_rbt["root"], key_initial, key_final, result)

    return {
        "size": len(result),
        "elements": result
    }

def keys_range_tree(node, key_initial, key_final, result):
    """Función auxiliar para recorrer el árbol y encontrar las llaves en el rango especificado."""
    if node is None:
        return

    # Comparar las llaves para determinar el recorrido
    if key_initial < node["key"]:
        keys_range_tree(node["left"], key_initial, key_final, result)

    if key_initial <= node["key"] <= key_final:
        result.append(node["key"])

    if key_final > node["key"]:
        keys_range_tree(node["right"], key_initial, key_final, result)

def values(my_rbt, key_initial, key_final):
    """
    Retorna todos los valores del árbol que se encuentren entre [key_initial, key_final].

    Args:
        my_rbt (red_black_tree): La tabla de símbolos.
        key_initial (any): Límite inferior.
        key_final (any): Límite superior.

    Returns:
        dict: Un diccionario que contiene el tamaño y la lista de valores en el rango especificado.
    """
    result = []
    # Usar la función values_range() para obtener los valores en el rango
    values_range_tree(my_rbt["root"], key_initial, key_final, result)

    return {
        "size": len(result),
        "elements": result
    }

def values_range_tree(node, key_initial, key_final, result):
    """Función auxiliar para recorrer el árbol y encontrar los valores en el rango especificado."""
    if node is None:
        return

    # Comparar las llaves para determinar el recorrido
    if key_initial < node["key"]:
        values_range_tree(node["left"], key_initial, key_final, result)

    if key_initial <= node["key"] <= key_final:
        result.append(node["value"])

    if key_final > node["key"]:
        values_range_tree(node["right"], key_initial, key_final, result)

def diametro(my_rbt, node):
    """
    Calcula el diámetro del árbol rojo-negro y el camino correspondiente.
     dict: Un diccionario con el diámetro y el camino correspondiente
    """
    if my_rbt["root"] is None:
        return {"diameter": 0, "path": []}
    diam={"diameter": 0, "path": []}
    
    node= my_rbt["root"]
    izq=  height_tree(node["left"])
    der=  height_tree(node["right"])
    
    if izq>der:
        izq
    

