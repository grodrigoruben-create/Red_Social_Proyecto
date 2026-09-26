class Pila:
    def __init__(self):
        self.items = []

    def push(self, elemento):
        """Agrega un elemento al tope de la pila."""
        self.items.append(elemento)

    def pop(self):
        """Remueve y retorna el elemento del tope de la pila."""
        if not self.es_vacia():
            return self.items.pop()
        return None

    def peek(self):
        """Retorna el elemento del tope sin removerlo."""
        if not self.es_vacia():
            return self.items[-1]
        return None

    def es_vacia(self):
        """Verifica si la pila está vacía."""
        return len(self.items) == 0

    def obtener_elementos(self):
        """Retorna una copia de la lista de elementos."""
        return list(self.items)