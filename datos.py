from pila import Pila

PUBLICACIONES_PRECARGADAS = [
    {"id": 1, "titulo": "Atardecer en la playa", "categoria": "Naturaleza"},
    {"id": 2, "titulo": "Montañas nevadas", "categoria": "Paisaje"},
    {"id": 3, "titulo": "Bosque místico", "categoria": "Naturaleza"},
    {"id": 4, "titulo": "Café matutino", "categoria": "Estilo de vida"},
    {"id": 5, "titulo": "Arquitectura moderna", "categoria": "Diseño"},
    {"id": 6, "titulo": "Paseo por la ciudad", "categoria": "Urbano"},
    {"id": 7, "titulo": "Camino rural", "categoria": "Paisaje"},
    {"id": 8, "titulo": "Aventura en el desierto", "categoria": "Viajes"},
    {"id": 9, "titulo": "Cielo estrellado", "categoria": "Noche"},
    {"id": 10, "titulo": "Fauna silvestre", "categoria": "Animales"}
]

COMENTARIOS_PREDETERMINADOS = [
    "¡Increíble publicación!",
    "¡Me encanta!",
    "Excelente contenido.",
    "¡Espectacular!"
]

pila_historial = Pila()
pila_likes = Pila()

def registrar_accion(accion, detalle):
    """Registra un evento en la Pila de Historial (push)."""
    pila_historial.push({"accion": accion, "detalle": detalle})

def dar_like(pub):
    """Agrega a la Pila de Likes si no tiene Like previamente."""
    likes = pila_likes.obtener_elementos()
    if not any(item['id'] == pub['id'] for item in likes):
        pila_likes.push(pub)
        registrar_accion("DAR_LIKE", f"Diste Like a: '{pub['titulo']}'")
        return True
    return False

def retirar_like(pub):
    """Retira un Like buscando en la Pila de Likes con una Pila Auxiliar."""
    pila_auxiliar = Pila()
    encontrado = False

    while not pila_likes.es_vacia():
        elem = pila_likes.pop()
        if elem['id'] == pub['id'] and not encontrado:
            encontrado = True
            registrar_accion("QUITAR_LIKE", f"Quitaste Like de: '{pub['titulo']}'")
            break
        else:
            pila_auxiliar.push(elem)

    # Restaurar los demás elementos
    while not pila_auxiliar.es_vacia():
        pila_likes.push(pila_auxiliar.pop())

    return encontrado

def agregar_comentario(pub, comentario):
    """Registra el comentario en el historial."""
    registrar_accion("COMENTARIO", f"En '{pub['titulo']}': \"{comentario}\"")