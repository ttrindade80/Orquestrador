"""Conteudo runtime deterministico das listas de marcacao H-0058."""


def _itens():
    return [
        {"id": "opcao_1", "texto": "Opção 1"},
        {"id": "opcao_2", "texto": "Opção 2"},
        {"id": "opcao_3", "texto": "Opção 3"},
        {"id": "opcao_4", "texto": "Opção 4"},
        {"id": "opcao_5", "texto": "Opção 5"},
        {"id": "opcao_6", "texto": "Opção 6"},
    ]


def conteudo_popup_h0058_exclusiva():
    return {
        "tipo": "marcacao",
        "instrucao": "Escolha uma opção:",
        "itens": _itens(),
        "marcados": ["opcao_2"],
    }


def conteudo_popup_h0058_multipla():
    return {
        "tipo": "marcacao",
        "instrucao": "Escolha uma ou mais opções:",
        "itens": _itens(),
        "marcados": ["opcao_2", "opcao_4"],
    }
