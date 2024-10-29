# DataStructures/Utils.py

class FunctionNotImplemented(Exception):
    """Excepción personalizada para funciones no implementadas."""
    def __init__(self, message="Esta función aún no ha sido implementada."):
        self.message = message
        super().__init__(self.message)

def reraise(exp, context):
    """Relevanta excepciones con un contexto adicional"""
    raise Exception(f"{context}: {str(exp)}")
