import requests
import urllib.parse

API_KEY = "17739df0-e5fa-423f-9a03-8974d5381e1b"

MEDIOS_TRANSPORTE = {
    "1": ("car", "🚗 Automóvil / Auto"),
    "2": ("truck", "🚛 Camión de Carga"),
    "3": ("bike", "🚴 Bicicleta")
}


def obtener_coordenadas(ciudad):
    """Obtiene latitud y longitud de una ciudad usando la API de Geocoding."""
    url = f"https://graphhopper.com/api/1/geocode?q={urllib.parse.quote(ciudad)}&locale=es&key={API_KEY}"
    try:
        response = requests.get(url).json()
        if response.get("hits"):
            point = response["hits"][0]["point"]
            return point["lat"], point["lng"]
    except Exception as e:
        print(f"❌ Error al conectar con el servicio de geocodificación: {e}")
    return None, None


def elegir_medio_transporte():
    """Solicita al usuario que elija el medio de transporte para el viaje."""
    print("\n🚗 Seleccione el medio de transporte:")
    for clave, (codigo, nombre) in MEDIOS_TRANSPORTE.items():
        print(f"  {clave}. {nombre}")

    while True:
        opcion = input("Ingrese el número de opción: ").strip()
        if opcion in MEDIOS_TRANSPORTE:
            return MEDIOS_TRANSPORTE[opcion][0]
        print("❌ Opción inválida, intente nuevamente.")


def calcular_viaje(origen, destino, vehiculo):
    """Calcula la ruta, distancia (km y millas), tiempo y narrativa del viaje."""
    lat1, lon1 = obtener_coordenadas(origen)
    lat2, lon2 = obtener_coordenadas(destino)

    if lat1 is None or lat2 is None:
        print(f"❌ Error: No se pudieron encontrar las coordenadas para {origen} o {destino}.")
        return

    print("\n🛣️  Consultando ruta terrestre optimizada en GraphHopper...")
    
    url = f"https://graphhopper.com/api/1/route?point={lat1},{lon1}&point={lat2},{lon2}&profile={vehiculo}&locale=es&key={API_KEY}&instructions=true"
    res = requests.get(url).json()

    if "paths" in res:
        path = res["paths"][0]
    
        distancia_km = path["distance"] / 1000
        distancia_millas = distancia_km * 0.621371
        tiempo_ms = path["time"]

    
        segundos_totales = int(tiempo_ms / 1000)
        horas = segundos_totales // 3600
        minutos = (segundos_totales % 3600) // 60
        segundos = segundos_totales % 60

        
        print("\n" + "="*60)
        print(f"🌎 PLANIFICACIÓN DE RUTA: {origen.upper()} ➜ {destino.upper()}")
        print("="*60)
        print(f"📍 Distancia total: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
        print(f"⏱️  Duración estimada: {horas} horas, {minutos} minutos y {segundos} segundos")
        print(f"🚛 Perfil de Transporte: {vehiculo.upper()}")
        print("-"*60)

        print("🗺️  NARRATIVA DEL VIAJE (INSTRUCCIONES PASO A PASO):")
        for idx, inst in enumerate(path.get("instructions", []), 1):
            dist_inst = inst['distance'] / 1000
            print(f"  {idx}. {inst['text']} ({dist_inst:.2f} km)")
        print("="*60 + "\n")
    else:
        print("❌ No se pudo calcular una ruta terrestre válida entre las ciudades proporcionadas.")



while True:
    print("\n--- 🌎 Planificador de Viajes Chile - Argentina (API GraphHopper) ---")
    origen = input("Ciudad de Origen (Chile) (o presione 's' para salir): ").strip()
    if origen.lower() == 's':
        print("Saliendo del programa...")
        break

    destino = input("Ciudad de Destino (Argentina) (o presione 's' para salir): ").strip()
    if destino.lower() == 's':
        print("Saliendo del programa...")
        break

    vehiculo = elegir_medio_transporte()
    calcular_viaje(origen, destino, vehiculo)