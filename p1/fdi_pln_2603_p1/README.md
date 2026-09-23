# 🤖 Agente Autónomo de Negociación: "Nortenios"

## 👥 Integrantes del equipo

- **Pablo Alonso Romero**
- **Rodrigo Jesús-Portanet Martínez**

Asignatura: Procesamiento del Lenguaje Natural  
Práctica 1 — Agente negociador autóno

Este proyecto implementa un agente autónomo conversacional diseñado para participar en un juego de simulación de comercio y gestión de recursos. El agente, apodado **Nortenios**, se conecta a un servidor central para interactuar con otros jugadores (y con el sistema), utilizando un Modelo de Lenguaje Grande (LLM) local para interpretar ofertas, negociar de forma inteligente y ejecutar intercambios de recursos de manera completamente autónoma.

---

## 🚀 Características Principales

* **Autonomía Total:** 
Un bucle principal infinito se encarga de percibir el entorno, procesar la bandeja de entrada, tomar decisiones y ejecutar acciones sin intervención humana.

* **Inteligencia Artificial Integrada:** 
Utiliza **Ollama** con el modelo `qwen3:8b` para leer los mensajes de otros agentes, interpretar las intenciones y redactar respuestas o contraofertas en lenguaje natural.
* **Toma de Decisiones Estricta:** 
El sistema de prompts guía al LLM mediante reglas rígidas para evitar estafas. Solo acepta tratos exactos (1:1 o según conveniencia) basados en sus necesidades reales y excedentes.
* **Gestión de Inventario Dinámica:** 
Calcula en tiempo real la diferencia entre los recursos actuales y los objetivos para determinar qué le sobra y qué necesita.
* **Filtro Anti-Spam:** 
Limpia automáticamente la bandeja de entrada eliminando mensajes redundantes de jugadores con los que ya está interactuando, priorizando siempre los mensajes vitales del sistema.
* **Proactividad:** 
Si la bandeja de entrada está vacía, el agente toma la iniciativa y envía propuestas comerciales a jugadores con los que no ha contactado recientemente.


---

## ⚙️ Configuración

Antes de lanzar el agente, revisa la sección de configuración al inicio del script (`configuración`) y ajusta las constantes si es necesario:

| Variable | Descripción | Valor por Defecto |
| :--- | :--- | :--- |
| `FDI_PLN__BUTLER_ADDRESS` | URL del servidor central del juego (API del mayordomo). | `http://147.96.84.134:7719` |
| `OLLAMA_URL` | Endpoint local donde la API de Ollama escucha las peticiones. | `http://localhost:11434/api/generate` |
| `MODEL_NAME` | Nombre del modelo LLM a utilizar. | `qwen3:8b` |
| `MI_ALIAS` | El nombre público de tu equipo/agente en la red del juego. | `Nortenios` |

---

## 🏗️ Arquitectura del Agente

El código está modularizado para facilitar su mantenimiento. La estructura del proyecto es la siguiente:

```
FDI-PLN/
│
├── src/
│ └── fdi_pln_2603_p1/  # Paquete principal del agente
│ ├── pycache/          # Caché de Python
│ ├── init.py           # Inicializa el paquete
│ ├── main.py           # Bucle principal de ejecución
│ ├── agent.py          # Lógica principal del agente
│ ├── estrategia.py     # Estrategias de negociación
│ ├── api.py            # Comunicación con la API (GET/POST)
│ ├── llm.py            # Integración con el modelo LLM (Ollama)
│ └── config.py         # Configuración global (URLs, alias, modelo, etc.)
│
├── pyproject.toml      # Configuración del proyecto y dependencias (uv)
├── uv.lock             # Lock de dependencias
└── README.md           # Documentación del proyecto
```

### Principios de diseño

- Separación clara de responsabilidades
- Arquitectura funcional
- Tipado moderno (Python 3.11+)
- Manejo básico de errores
- Flujo de datos consistente
- Código formateado con `uv format`


---

## 🧩 Responsabilidades de cada módulo

- **main.py** → Ejecuta el bucle principal del agente.
- **agente.py** → Coordina la toma de decisiones a partir del estado actual.
- **estrategia.py** → Implementa la lógica de negociación (aceptar, proponer, ignorar).
- **api.py** → Gestiona todas las peticiones HTTP al servidor.
- **llm.py** → Maneja la interacción con el modelo de lenguaje.
- **config.py** → Contiene constantes y parámetros configurables.

### 🔄 Funcionamiento general

En cada ciclo:

1. El agente realiza una petición GET al servidor.
2. Analiza:
   - Inventario actual
   - Objetivo
   - Propuestas recibidas
3. Decide una acción:
   - Aceptar propuesta
   - Enviar propuesta
   - No realizar acción
4. Si procede, envía un POST al servidor.
5. Espera un intervalo y repite el proceso.

---

## 🧠 Uso del LLM

El agente utiliza el modelo:
```bash
qwen3:8b
```

de Ollama

Ejecutado localmente mediante Ollama.

El LLM se emplea para:

- Analizar propuestas en lenguaje natural.
- Generar propuestas estratégicas.
- Tomar decisiones en contextos ambiguos.
- Generar salidas estructuradas en JSON cuando es necesario.


---

## 🔐 Estrategia de negociación

El agente implementa un modelo seguro tipo **handshake**:

1. Si recibe una propuesta exacta 1 a 1 que le interesa:
   - Acepta por carta
   - Solicita que el otro agente envíe primero

2. Cuando el sistema (Butler) confirma la recepción del recurso:
   - Envía automáticamente el recurso acordado

Esto garantiza que:

- Nunca envía recursos como contraoferta
- Nunca envía sin garantía de recepción
- Evita intercambios inseguros

---

# ⚙️ Instalación

## Opción 1 — Instalación desde wheel (modo evaluación)

Para instalar el agente directamente desde el archivo `.whl`:

```bash
uv tool install <ruta_al_archivo.whl>
```

## Opción 2 — Desde el repositorio

Clonar el repositorio y ejecutar:

```bash
uv sync
```

- Después de tener todo instalado, ejecutar:

```bash
uv run fdi-pln-2603-p1
```

para poner en funcionamiento al agente.

Para que el agente se conecte a butler en local, hay que instalar el wheel proporcionado en el Campus Virtual, y ejecutar la instrucción para instalar el wheel, adaptada a la ruta.
Ejecutar:
```bash
fdi-pln-butler server
```

Con la conexión que aparezca, antes de lanzar nuestro agente, hacer:
```bash
export FDI_PLN__BUTLER_ADDRESS="<ruta de conexion>"
```
para posteriormente poder lanzar el agente sin problemas.


---

## 🚧 Posibles Mejoras Futuras (To-Do)

* **Memoria a largo plazo:** Implementar un historial para recordar con qué jugadores se han hecho buenos tratos y con cuáles no, creando una "lista de amigos" y una "lista negra".
* **Negociación Multi-recurso:** Modificar las reglas para permitir intercambios complejos (ej. "Te doy 2 de madera y 1 de piedra por 1 de oro").
* **Manejo de Errores de JSON:** Mejorar la extracción del JSON mediante expresiones regulares (Regex) más robustas en caso de que Ollama devuelva texto extra antes o después de las llaves `{}`.
