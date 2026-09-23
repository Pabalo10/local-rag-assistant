def calcular_estrategia(info):
    """Calcula qué necesitamos y qué nos sobra."""

    inventario = info.get("Recursos", {})
    objetivo = info.get("Objetivo", {})

    necesidades = {}
    sobras = {}

    todos = set(inventario.keys()) | set(objetivo.keys())

    for r in todos:
        actual = inventario.get(r, 0)
        objetivo_c = objetivo.get(r, 0)
        diff = objetivo_c - actual

        if diff > 0:
            necesidades[r] = diff
        elif diff < 0:
            sobras[r] = abs(diff)

    return necesidades, sobras
