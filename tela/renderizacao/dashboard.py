"""Renderização de dashboards."""



def _linhas_dashboard(elemento):
    """Linhas de conteudo para elemento dashboard a partir de campos[].

    Apenas campos com ``fonte == "literal"`` contribuem com o ``valor``
    como linha de conteudo. Campos com outra ``fonte`` (ex.: ``"pendente"``)
    sao ignorados -- sem texto, sem erro, sem placeholder.
    """
    campos = elemento._campos_inertes.get("campos", []) or []
    linhas = []
    for campo in campos:
        if not isinstance(campo, dict):
            continue
        if campo.get("fonte") == "literal":
            valor = campo.get("valor", "")
            linhas.append(valor)
    return linhas
