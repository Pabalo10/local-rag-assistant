import requests
import json
import random
from .config import MODEL_NAME, OLLAMA_URL, MI_ALIAS


def consultar_llm(prompt_sistema, prompt_usuario):
    """Envía la consulta a Ollama."""
    full_prompt = (
        f"<|im_start|>system\n{prompt_sistema}<|im_end|>\n"
        f"<|im_start|>user\n{prompt_usuario}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False,
        "options": {"temperature": 0.5},
    }

    try:
        resp = requests.post(OLLAMA_URL, json=payload)
        if resp.status_code == 200:
            return resp.json().get("response", "").strip()
        else:
            print(f"⚠️ ERROR OLLAMA ({resp.status_code}): {resp.text}")
            return None
    except Exception as e:
        print(f"❌ ERROR CRÍTICO CONEXIÓN: {e}")
        return None


def generar_respuesta_negociacion(remitente, mensaje_recibido, necesidades, sobras):
    sugerencia = ""
    if sobras and necesidades:
        r_doy = random.choice(list(sobras.keys()))
        r_pido = random.choice(list(necesidades.keys()))
        sugerencia = f"Si rechazas o no cuadra, di: 'Te doy 1 {r_doy} por 1 {r_pido}'."

    sistema = f"""
    Eres '{MI_ALIAS}'. Negocias recursos.
    
    TUS SOBRAS (Lo que puedes enviar): {json.dumps(sobras)}
    TUS NECESIDADES (Lo que pides): {json.dumps(necesidades)}
    
    Remitente del mensaje: '{remitente}'.
    
    REGLAS ESTRICTAS:
    1. Si el remitente es 'Sistema', 'System' o 'Butler', significa que YA TE HAN PAGADO. Responde con "accion": "ENVIAR_PAQUETE" y en "recursos_a_enviar" pon el recurso que tienes de sobra y crees que le debes al que te pagó.
    2. Si el remitente es un jugador y propone un trato EXACTO (ej. 'te doy 1 trigo por 1 piedra') y tienes esa piedra en TUS SOBRAS y necesitas ese trigo -> ACEPTA usando "accion": "ENVIAR_PAQUETE" y en "recursos_a_enviar" pon tu recurso sobrante.
    3. Si la oferta no es exacta, no te interesa, o te piden algo que no tienes en TUS SOBRAS -> Responde SOLO CON CARTA ("accion": "CARTA") haciendo contraoferta. NUNCA envíes paquetes como contraoferta.

    {sugerencia}
    
    RESPONDE SOLO JSON:
    {{
        "pensamiento": "tu razonamiento",
        "mensaje": "texto para el otro",
        "accion": "CARTA" o "ENVIAR_PAQUETE",
        "recursos_a_enviar": {{ "recurso_sobrante": 1 }} (Solo si envías paquete YA, si no vacio)
    }}
    """

    usuario = f"Mensaje recibido: '{mensaje_recibido}'. Genera JSON."
    respuesta_raw = consultar_llm(sistema, usuario)

    decision_defecto = {
        "pensamiento": "Fallo IA",
        "mensaje": "No entendí la oferta. ¿Me cambias 1 que necesite por 1 que me sobre?",
        "accion": "CARTA",
        "recursos_a_enviar": {},
    }

    if not respuesta_raw:
        return decision_defecto

    try:
        inicio = respuesta_raw.find("{")
        fin = respuesta_raw.rfind("}") + 1
        if inicio != -1 and fin != -1:
            return json.loads(respuesta_raw[inicio:fin])
        return decision_defecto
    except:
        return decision_defecto


def generar_oferta_inicial(destino, necesidades, sobras):
    """Genera una oferta inicial aleatoria 1 a 1."""
    if not sobras or not necesidades:
        return None

    recurso_doy = random.choice(list(sobras.keys()))
    recurso_pido = random.choice(list(necesidades.keys()))

    sistema = f"""
    Eres '{MI_ALIAS}'. Quieres comerciar con '{destino}'.
    
    TU OFERTA: Das 1 unidad de {recurso_doy}.
    TU DEMANDA: Pides 1 unidad de {recurso_pido}.
    
    Redacta una carta de UNA sola frase proponiendo este cambio exacto. Sé directo y amable.
    """

    usuario = f"Escribe la carta para '{destino}'."
    respuesta = consultar_llm(sistema, usuario)

    if not respuesta:
        return (
            f"Hola {destino}. Te cambio 1 {recurso_doy} por 1 {recurso_pido}. ¿Trato?"
        )
    return respuesta
