"""Teste da demonstracao reproduzivel do H-0072 pelo ponto de entrada real.

Prova que o cenario ``h0072_formatacao_generica_dois_niveis_por_foco`` e
carregado e renderizado por ``demo/demo.py`` (catalogo de associacao
estrutural <-> conteudo externo, ``_carregar_modelo_por_id``,
``criar_estado_inicial``/``processar_comando``/``renderizar_estado``),
nunca apenas por chamada direta ao renderer (contrato_console.md §20.5).

Executavel via:
    python demo/teste_demo_h0072_formatacao_generica.py

Apenas biblioteca padrao do Python + pytest.
"""

import os
import re
import sys
from pathlib import Path

_BASE_PADRAO = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(_BASE_PADRAO))
_this_dir = str(Path(__file__).resolve().parent)
while _this_dir in sys.path:
    sys.path.remove(_this_dir)

from demo.demo import (  # noqa: E402
    _CATALOGO_CONTEUDO_EXTERNO,
    id_conteudo_externo_de,
    _carregar_modelo_por_id,
    criar_estado_inicial,
    processar_comando,
    renderizar_estado,
)
from tela import navegacao  # noqa: E402
from tela.loader import carregar_estilo  # noqa: E402

_ESTILO = carregar_estilo()
_ID_TELA = "h0072_formatacao_generica_dois_niveis_por_foco"


def _sem_ansi(texto):
    return re.sub(r"\x1b\[[0-9;]*m", "", texto)


def teste_catalogo_associa_cenario_h0072():
    assert _CATALOGO_CONTEUDO_EXTERNO[_ID_TELA] == (
        "h0072_formatacao_generica_dois_niveis_por_foco_conteudo"
    )
    assert id_conteudo_externo_de(_ID_TELA) == (
        "h0072_formatacao_generica_dois_niveis_por_foco_conteudo"
    )


def teste_carregamento_via_ponto_de_entrada_real():
    modelo = _carregar_modelo_por_id(_ID_TELA)
    assert modelo.id == _ID_TELA
    assert modelo.conteudo_externo is not None
    consoles = [e for e in modelo.corpo.elementos if e.tipo == "console"]
    assert [c.id for c in consoles] == [
        "console_h0072_texto", "console_h0072_tabela",
        "console_h0072_sem_designador",
    ]
    # As tres formas de designador e as duas apresentacoes estao presentes.
    formatos = {c.id: c.formato_filho_dois_niveis for c in consoles}
    assert formatos["console_h0072_texto"]["designador"]["tipo"] == "decimal_composto"
    assert "prefixo" not in formatos["console_h0072_texto"]["designador"]
    assert "sufixo" not in formatos["console_h0072_texto"]["designador"]
    assert formatos["console_h0072_texto"]["apresentacao"] == "texto"
    assert formatos["console_h0072_tabela"]["designador"]["tipo"] == "alfabetico_maiusculo"
    assert formatos["console_h0072_tabela"]["designador"]["prefixo"] == "("
    assert formatos["console_h0072_tabela"]["designador"]["sufixo"] == ")"
    assert formatos["console_h0072_tabela"]["apresentacao"] == "tabela"
    assert len(formatos["console_h0072_tabela"]["tabela"]["colunas"]) == 2
    assert formatos["console_h0072_sem_designador"]["designador"]["tipo"] == "nenhum"
    assert "prefixo" not in formatos["console_h0072_sem_designador"]["designador"]
    assert "sufixo" not in formatos["console_h0072_sem_designador"]["designador"]


def teste_renderizacao_real_exibe_as_tres_formas_e_ambas_apresentacoes():
    modelo = _carregar_modelo_por_id(_ID_TELA)
    console = navegacao.lista_foco(modelo)[0]
    estado = dict(
        criar_estado_inicial(), estilo=_ESTILO, foco_console=0,
        cursores={console.id: 0}, largura=90, altura=60,
    )
    inicial = processar_comando(estado, "", modelo)
    quadro = _sem_ansi(renderizar_estado(inicial, modelo, largura=90, altura=60))

    # console_h0072_texto: designador decimal_composto sem adornos.
    assert "1.1" in quadro
    assert "Revisar especificação do módulo de autenticação" in quadro

    # console_h0072_tabela: alfabetico_maiusculo com prefixo "(" e sufixo ")".
    assert "(A)" in quadro
    assert "(B)" in quadro

    # Nenhum placeholder residual do console generico.
    assert "(console)" not in quadro


def teste_alternar_foco_percorre_os_tres_consoles_da_demonstracao():
    modelo = _carregar_modelo_por_id(_ID_TELA)
    consoles = navegacao.lista_foco(modelo)
    assert len(consoles) == 3
    estado = dict(criar_estado_inicial(), estilo=_ESTILO, largura=90, altura=60)
    foco1 = processar_comando(estado, "\t", modelo)
    assert foco1["foco_console"] == 0
    foco2 = processar_comando(foco1, "\t", modelo)
    assert foco2["foco_console"] == 1
    foco3 = processar_comando(foco2, "\t", modelo)
    assert foco3["foco_console"] == 2
    volta = processar_comando(foco3, "\t", modelo)
    assert volta["foco_console"] == 0


def teste_console_tabela_exibe_colunas_alinhadas_entre_pais_diferentes():
    modelo = _carregar_modelo_por_id(_ID_TELA)
    consoles = {c.id: c for c in navegacao.lista_foco(modelo)}
    console_tabela = consoles["console_h0072_tabela"]
    estado = dict(
        criar_estado_inicial(), estilo=_ESTILO, foco_console=1,
        cursores={console_tabela.id: 0}, largura=100, altura=60,
    )
    inicial = processar_comando(estado, "", modelo)
    quadro = _sem_ansi(renderizar_estado(inicial, modelo, largura=100, altura=60))
    assert "(A)" in quadro
    assert "(B)" in quadro
    linhas_responsavel = [
        linha for linha in quadro.splitlines()
        if "Camila Duarte" in linha or "Priscila Nogueira" in linha
    ]
    assert len(linhas_responsavel) == 2
    # A coluna "prazo" comeca na mesma posicao horizontal em ambas as linhas
    # (filhos de pais diferentes), pois a largura de coluna e global (§16).
    posicoes = sorted(
        linha.index("12/09") if "12/09" in linha else linha.index("22/09")
        for linha in linhas_responsavel
    )
    assert posicoes[0] == posicoes[1]


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-v"]))
