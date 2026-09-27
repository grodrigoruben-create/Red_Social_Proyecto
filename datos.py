from pila import Pila

PUBLICACIONES_PRECARGADAS = [
    {"id": 1, "usuario": "ana_gomez", "titulo": "Atardecer en la playa", "categoria": "Naturaleza", "imagen": "uploads/playa.jpg"},
    {"id": 2, "usuario": "lara.belen.v", "titulo": "Montañas nevadas", "categoria": "Paisaje", "imagen": "uploads/montaña.jpg"},
    {"id": 3, "usuario": "Lucas_Silva", "titulo": "Bosque místico", "categoria": "Naturaleza", "imagen": "uploads/bosque.jpg"},
    {"id": 4, "usuario": "Emmanuel_GLZ", "titulo": "Café matutino", "categoria": "Estilo de vida", "imagen": "uploads/cafe.jpg"},
    {"id": 5, "usuario": "is_luisangel", "titulo": "Arquitectura moderna", "categoria": "Diseño", "imagen": "uploads/arquitectura.jpg"},
    {"id": 6, "usuario": "Sofía_M", "titulo": "Paseo por la ciudad", "categoria": "Urbano", "imagen": "uploads/ciudad.jpg"},
    {"id": 7, "usuario": "its.Trebor", "titulo": "Camino rural", "categoria": "Paisaje", "imagen": "uploads/camino.jpg"},
    {"id": 8, "usuario": "Elena_Rossi", "titulo": "Aventura en el desierto", "categoria": "Viajes", "imagen": "uploads/desierto.jpg"},
    {"id": 9, "usuario": "alejandra_Ruiz", "titulo": "Cielo estrellado", "categoria": "Noche", "imagen": "uploads/cielo.jpg"},
    {"id": 10, "usuario": "[liam.v]", "titulo": "Fauna silvestre", "categoria": "Animales", "imagen": "uploads/fauna.jpg"}
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
    pub.setdefault("comentarios", []).append(comentario)
    registrar_accion("COMENTARIO", f"En '{pub['titulo']}': \"{comentario}\"")