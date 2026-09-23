import requests
from .config import BUTLER_ADDRESS, MI_ALIAS


def registrar_alias():
    """Registra al agente en el juego."""
    try:
        resp = requests.post(f"{BUTLER_ADDRESS}/alias/{MI_ALIAS}")
        if resp.status_code in [200, 201]:
            print(f"✅ Alias '{MI_ALIAS}' registrado.")
            return True
        print(f"⚠️ Error registro: {resp.text}")
    except Exception as e:
        print(f"❌ Error conexión registro: {e}")
    return False


def obtener_info():
    """Obtiene el estado completo del agente."""
    try:
        resp = requests.get(f"{BUTLER_ADDRESS}/info")
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"❌ Error obteniendo info: {e}")
    return None


def obtener_gente():
    """Devuelve lista de NOMBRES de otros agentes."""
    try:
        resp = requests.get(f"{BUTLER_ADDRESS}/gente")
        resp.raise_for_status()  # Lanza excepción si hay error HTTP
        gente = resp.json()

        # Si por alguna razón gente no es lista, lo convertimos a lista vacía
        if not isinstance(gente, list):
            print(f"⚠️ Respuesta inesperada al obtener gente: {gente}")
            gente = []

        if len(gente) == 0:
            print(":'( No se encontró a nadie")
        else:
            print(f":D Se encontraron {len(gente)} agentes")

        return [
            p.get("alias")
            for p in gente
            if isinstance(p, dict) and p.get("alias") and p.get("alias") != MI_ALIAS
        ]

        # if resp.status_code == 200:
        #    gente = resp.json()
        #    lista_nombres = []
        #    for p in gente:
        #        nombre = p.get("alias")
        #        if nombre and nombre != MI_ALIAS:
        #            lista_nombres.append(nombre)
        #    return lista_nombres

    except Exception as e:
        print(f"⚠️ Error al obtener gente: {e}")
    return []


def enviar_carta(dest, asunto, cuerpo):
    """Envía un mensaje de texto."""
    print(f"🔹 Intentando enviar carta a {dest}")
    payload = {
        "remi": MI_ALIAS,
        "dest": dest,
        "asunto": asunto,
        "cuerpo": cuerpo,
    }
    try:
        resp = requests.post(f"{BUTLER_ADDRESS}/carta", json=payload)
        if resp.status_code in [200, 201]:
            print(f"✉️ Carta enviada a {dest}: {asunto}")
        else:
            print(f"⚠️ Fallo enviando carta a {dest}: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"❌ Fallo enviando carta: {e}")


def borrar_mail(uid):
    """Borra un mail procesado."""
    try:
        requests.delete(f"{BUTLER_ADDRESS}/mail/{uid}")
        print(f"🗑️ Mail {uid} borrado.")
    except:
        pass


def enviar_paquete(dest, recursos):
    """Envía recursos físicos."""
    try:
        resp = requests.post(f"{BUTLER_ADDRESS}/paquete/{dest}", json=recursos)
        if resp.status_code == 200:
            print(f"📦 PAQUETE ENVIADO A {dest}: {recursos}")
            return True
        else:
            print(f"⚠️ Fallo enviando paquete: {resp.text}")

    except Exception as e:
        print(f"❌ Error crítico enviando paquete: {e}")

    return False
