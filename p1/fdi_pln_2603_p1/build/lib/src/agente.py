import time
import random

from .config import MI_ALIAS
from .api import (
    registrar_alias,
    obtener_info,
    obtener_gente,
    enviar_carta,
    borrar_mail,
    enviar_paquete,
)
from .estrategia import calcular_estrategia
from .llm import generar_respuesta_negociacion, generar_oferta_inicial


def bucle_principal():
    print(f"🚀 Iniciando agente {MI_ALIAS}...")
    registrar_alias()

    ciclos_sin_novedad = 0
    ultimos_contactados = []

    while True:
        try:
            # 1. PERCEPCIÓN
            info = obtener_info()
            if not info:
                time.sleep(5)
                continue

            necesidades, sobras = calcular_estrategia(info)
            buzon = info.get("Buzon", {})

            print(f"\n--- CICLO --- Falta: {necesidades} | Sobra: {sobras}")
            print(f"📬 Tienes {len(buzon)} mensajes en el buzón.")

            # 2. PROCESAR BUZÓN (Carta a Carta)
            if buzon:
                ciclos_sin_novedad = 0
                print(f"📬 Tienes {len(buzon)} mensajes en el buzón.")

                # Vamos a procesar solo el primer mensaje en este ciclo para event-driven
                uid, carta = list(buzon.items())[0]

                remitente = carta.get("remi")
                cuerpo = carta.get("cuerpo")

                print(f"💬 Leyendo carta de {remitente}...")
                decision = generar_respuesta_negociacion(
                    remitente, cuerpo, necesidades, sobras
                )
                print(
                    f"🧠 Pensamiento: {decision.get('pensamiento', 'Sin pensamiento')}"
                )

                if decision.get("accion") == "ENVIAR_PAQUETE" and decision.get(
                    "recursos_a_enviar"
                ):
                    recursos_raw = decision["recursos_a_enviar"]
                    recursos = {}
                    for k, v in recursos_raw.items():
                        try:
                            recursos[k] = int(v)
                        except (ValueError, TypeError):
                            continue

                    if recursos:
                        puede_enviar = all(
                            sobras.get(k, 0) >= v for k, v in recursos.items()
                        )
                        if puede_enviar:
                            # Si es un aviso del sistema, enviamos el paquete al que generó el recurso (asumimos que lo dice en el cuerpo o que el LLM lo sabe gestionar)
                            # Como 'Sistema' no es un destinatario válido para paquetes, si el remitente es Sistema, asumimos que el LLM ha fallado en decirnos a quién enviarlo.
                            # MEJORA: Para no liarnos, si la acción es enviar paquete, siempre se envía al remitente, a menos que sea Sistema, en cuyo caso enviamos una carta de agradecimiento.
                            if remitente in ["Butler", "System", "Sistema"]:
                                print(
                                    "📦 (Aviso del sistema, no enviamos paquete de vuelta a 'Sistema')"
                                )
                                enviar_carta(
                                    MI_ALIAS,
                                    "Registro",
                                    "Recibido recurso por el sistema.",
                                )  # Nos enviamos nota mental o nada
                            else:
                                envio_exitoso = enviar_paquete(remitente, recursos)
                                if envio_exitoso:
                                    enviar_carta(
                                        remitente, "Trato cerrado", decision["mensaje"]
                                    )
                                else:
                                    enviar_carta(
                                        remitente,
                                        "Error",
                                        "La aduana bloqueó el paquete.",
                                    )
                        else:
                            enviar_carta(
                                remitente,
                                "Error",
                                "Quería aceptar, pero no tengo ese recurso o pediste de más.",
                            )
                    else:
                        enviar_carta(
                            remitente,
                            "Error",
                            "No he entendido bien las cantidades del trato.",
                        )
                else:
                    # Si no enviamos paquete, mandamos carta normal
                    enviar_carta(
                        remitente,
                        f"RE: {carta.get('asunto', 'Negociación')}",
                        decision["mensaje"],
                    )

                # Borramos el mail principal que acabamos de contestar
                borrar_mail(uid)

                # 🧹 LIMPIEZA INTELIGENTE: Borramos mensajes antiguos de ESTE remitente (si es un jugador)
                # para limpiar spam, pero NUNCA borramos mensajes del Sistema.
                if remitente not in ["Butler", "System", "Sistema"]:
                    for otro_uid, otra_carta in buzon.items():
                        if otro_uid != uid and otra_carta.get("remi") == remitente:
                            print(f"⏩ Borrando spam de {remitente}.")
                            borrar_mail(otro_uid)

                print("🔄 Recalculando estado con la API...")

            # 3. INICIATIVA (Buscar gente nueva si el buzón está vacío)
            else:
                ciclos_sin_novedad += 1
                if ciclos_sin_novedad % 2 == 0 and necesidades:
                    gente = obtener_gente()
                    posibles_victimas = [
                        p for p in gente if p not in ultimos_contactados
                    ]

                    if not posibles_victimas:
                        ultimos_contactados = []
                        posibles_victimas = gente

                    if posibles_victimas:
                        victima = random.choice(posibles_victimas)
                        ultimos_contactados.append(victima)
                        if len(ultimos_contactados) > 5:
                            ultimos_contactados.pop(0)

                        print(f"📢 Iniciando contacto con {victima}...")
                        mensaje = generar_oferta_inicial(victima, necesidades, sobras)
                        enviar_carta(victima, "Propuesta comercial", mensaje)

            time.sleep(5)

        except KeyboardInterrupt:
            print("\n🛑 Agente detenido.")
            break
        except Exception as e:
            print(f"❌ Error bucle: {e}")
            time.sleep(5)
