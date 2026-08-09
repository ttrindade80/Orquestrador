"""Testes do catalogo e do ponto de entrada com conteudo externo (H-0036).

Executavel via:
    python demo/teste_demo_console.py

Cobre os criterios de aceite testaveis do H-0036 relativos ao ``demo.py``
(secoes 17, 18, 19.5 e 19.6 do handoff): catalogo de associacao cenario ->
{JSON estrutural, JSON externo}; carregamento separado dos dois documentos;
tres apresentacoes acessiveis pelo ponto de entrada real; identidade semantica
material; ausencia de mistura entre cenarios; placeholder preservado em
cenarios sem conteudo; smoke tests por cenario com prova de conteudo material.

Responsabilidade distinta dos testes focais (loader/modelo/renderizador) e do
diagnostico: aqui a fronteira sob teste e o ponto de entrada ``demo/demo.py`` e
seu catalogo interno.

Apenas biblioteca padrao do Python.
"""

import os
import re
import subprocess
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
    _preparar_estado_h0053,
    processar_comando,
    renderizar_estado,
    _tela_inicial_de_argv,
)
from demo.demo_navegacao import main as demo_navegacao_main  # noqa: E402
from tela import navegacao  # noqa: E402
from tela.renderizador import renderizar_tela  # noqa: E402
from tela.renderizacao.console import _linhas_console  # noqa: E402
from tela.loader import carregar_estilo  # noqa: E402

# H-0039: estilo global resolvido, carregado uma vez para os testes que
# chamam renderizar_tela diretamente.
_ESTILO = carregar_estilo()

_RESULTADOS = []

_RAIZ_TELAS_DEMO = os.path.join("config", "telas", "demo")

# Smoke matrix (secao 19.6). Cada cenario declara, de forma independente da
# saida auditada, o esperado material: identidade semantica exclusiva, conteudo
# incorreto de outro cenario que NAO pode aparecer, e a regra de placeholder.
_SMOKE = [
    {
        "cenario": "h0036_console_hierarquia",
        "estrutural": "h0036_console_hierarquia",
        "externo": "h0036_hierarquia_conteudo",
        "identidade": "H-0036",
        "identidade_extra": "Fluxo H-0036 hierarquia",
        "conteudo_incorreto": "Parametros",
        "placeholder": "AUSENTE",
    },
    {
        "cenario": "h0036_console_tabela",
        "estrutural": "h0036_console_tabela",
        "externo": "h0036_tabela_conteudo",
        "identidade": "tabela H-0036",
        "identidade_extra": "Entradas",
        "conteudo_incorreto": "Fluxo H-0036 hierarquia",
        "placeholder": "AUSENTE",
    },
    {
        "cenario": "h0036_console_conjuntos",
        "estrutural": "h0036_console_conjuntos",
        "externo": "h0036_conjuntos_conteudo",
        "identidade": "Parametros",
        "identidade_extra": "H-0036",
        "conteudo_incorreto": "Entradas",
        "placeholder": "AUSENTE",
    },
    {
        "cenario": "h0035_console_com",
        "estrutural": "h0035_console_com",
        "externo": "h0035_console_com_conteudo",
        "identidade": "P01 linha",
        "identidade_extra": "P12 linha",
        "conteudo_incorreto": "Linha alfa",
        "placeholder": "AUSENTE",
    },
    {
        "cenario": "h0035_console_sem",
        "estrutural": "h0035_console_sem",
        "externo": "h0035_console_sem_conteudo",
        "identidade": "Linha alfa",
        "identidade_extra": "Linha bravo",
        "conteudo_incorreto": "P01 linha",
        "placeholder": "AUSENTE",
    },
    {
        "cenario": "h0037_console_nao_verboso",
        "estrutural": "h0037_console_nao_verboso",
        "externo": "h0037_dois_niveis_conteudo",
        "identidade": "H-0037 conteudo_dois_niveis",
        "identidade_extra": "somente_nao_verboso",
        "conteudo_incorreto": "H-0037 alternavel_tres_niveis",
        "placeholder": "AUSENTE",
    },
    {
        "cenario": "h0037_console_verboso_dois_niveis",
        "estrutural": "h0037_console_verboso_dois_niveis",
        "externo": "h0037_dois_niveis_conteudo",
        "identidade": "H-0037 conteudo_dois_niveis",
        "identidade_extra": "somente_verboso",
        "conteudo_incorreto": "H-0037 alternavel_tres_niveis",
        "placeholder": "AUSENTE",
    },
    {
        "cenario": "h0037_console_alternavel_tres_niveis",
        "estrutural": "h0037_console_alternavel_tres_niveis",
        "externo": "h0037_tres_niveis_conteudo",
        "identidade": "H-0037 alternavel_tres_niveis",
        "identidade_extra": "Politica alternavel",
        "conteudo_incorreto": "H-0037 conteudo_dois_niveis",
        "placeholder": "AUSENTE",
    },
    {
        "cenario": "h0037_console_tabela_alternavel",
        "estrutural": "h0037_console_tabela_alternavel",
        "externo": "h0037_tabela_conteudo",
        "identidade": "H-0037 tabela_alternavel",
        "identidade_extra": "Politica",
        "conteudo_incorreto": "H-0037 conteudo_dois_niveis",
        "placeholder": "AUSENTE",
    },
]


def _registrar(nome, passou, detalhe=""):
    status = "PASSOU" if passou else "FALHOU"
    linha = "[{0}] {1}".format(status, nome)
    if detalhe:
        linha += " - {0}".format(detalhe)
    print(linha)
    _RESULTADOS.append((nome, passou))


def teste_catalogo():
    print("")
    print("== Catalogo de associacao cenario -> conteudo externo ==")
    esperado = {
        "h0036_console_hierarquia": "h0036_hierarquia_conteudo",
        "h0036_console_tabela": "h0036_tabela_conteudo",
        "h0036_console_conjuntos": "h0036_conjuntos_conteudo",
        "h0052_tabela_passiva": "h0036_tabela_conteudo",
        "h0035_console_com": "h0035_console_com_conteudo",
        "h0035_console_sem": "h0035_console_sem_conteudo",
        "h0037_console_nao_verboso": "h0037_dois_niveis_conteudo",
        "h0037_console_verboso_dois_niveis": "h0037_dois_niveis_conteudo",
        "h0037_console_alternavel_tres_niveis": "h0037_tres_niveis_conteudo",
        "h0037_console_tabela_alternavel": "h0037_tabela_conteudo",
        "h0053_arvore_colapsavel": "h0053_arvore_colapsavel_conteudo",
    }
    _registrar("catalogo associa os cenarios com conteudo",
               _CATALOGO_CONTEUDO_EXTERNO == esperado,
               "obtido={0}".format(_CATALOGO_CONTEUDO_EXTERNO))
    _registrar("cenario com conteudo: associacao correta (hierarquia)",
               id_conteudo_externo_de("h0036_console_hierarquia")
               == "h0036_hierarquia_conteudo")
    # Ausencia representada explicitamente (chave ausente -> None).
    for id_tela in ("demo", "h0030_console_unico", "destino_minimo"):
        _registrar("cenario sem conteudo '{0}': ausencia explicita (None)".format(id_tela),
                   id_conteudo_externo_de(id_tela) is None)


def teste_carregamento_separado_por_cenario():
    print("")
    print("== Carregamento separado dos dois documentos por cenario ==")
    for caso in _SMOKE:
        modelo = _carregar_modelo_por_id(caso["cenario"])
        # Arquivo estrutural correto (id da tela).
        _registrar("{0}: JSON estrutural correto (id={1})".format(
                       caso["cenario"], caso["estrutural"]),
                   modelo.id == caso["estrutural"])
        # Documento externo correto e presente.
        _registrar("{0}: documento externo carregado e associado".format(caso["cenario"]),
                   modelo.conteudo_externo is not None)
        # Conteudo semantico do documento externo (identidade material).
        raw_ext = getattr(modelo.conteudo_externo, "_raw", {})
        import json as _json
        ext_txt = _json.dumps(raw_ext, ensure_ascii=False)
        estr_txt = _json.dumps(modelo._raw, ensure_ascii=False)
        _registrar("{0}: identidade no documento externo, nao no estrutural".format(caso["cenario"]),
                   caso["identidade"] in ext_txt and caso["identidade"] not in estr_txt)


def teste_apresentacoes_acessiveis():
    print("")
    print("== Tres apresentacoes acessiveis pelo demo.py ==")
    for cenario, apresentacao in [
        ("h0036_console_hierarquia", "hierarquia"),
        ("h0036_console_tabela", "tabela"),
        ("h0036_console_conjuntos", "conjuntos_campos"),
    ]:
        modelo = _carregar_modelo_por_id(cenario)
        _registrar("{0}: apresentacao {1} acessivel".format(cenario, apresentacao),
                   modelo.conteudo_externo.apresentacao == apresentacao)
        saida = renderizar_tela(modelo, estilo=_ESTILO, largura=70, altura=26)
        _registrar("{0}: renderiza sem placeholder".format(cenario),
                   "(console)" not in saida)


def teste_ausencia_de_mistura():
    print("")
    print("== Ausencia de mistura de conteudo entre cenarios ==")
    saidas = {}
    for caso in _SMOKE:
        modelo = _carregar_modelo_por_id(caso["cenario"])
        saidas[caso["cenario"]] = renderizar_tela(modelo, estilo=_ESTILO, largura=70, altura=28)
    for caso in _SMOKE:
        saida = saidas[caso["cenario"]]
        _registrar("{0}: conteudo de outro cenario ausente ({1!r})".format(
                       caso["cenario"], caso["conteudo_incorreto"]),
                   caso["conteudo_incorreto"] not in saida,
                   "vazamento detectado" if caso["conteudo_incorreto"] in saida else "")
    # Troca de cenario nao mantem conteudo residual: apos abrir um cenario com
    # conteudo, abrir um cenario sem conteudo produz placeholder e nenhuma marca.
    _carregar_modelo_por_id("h0036_console_hierarquia")
    modelo_sem = _carregar_modelo_por_id("h0030_console_unico")
    saida_sem = renderizar_tela(modelo_sem, estilo=_ESTILO, largura=60, altura=20)
    _registrar("troca para cenario sem conteudo: placeholder presente, sem residuo",
               "(console)" in saida_sem
               and "H-0036" not in saida_sem
               and modelo_sem.conteudo_externo is None)


def teste_smoke_por_cenario():
    print("")
    print("== Smoke tests semanticos por cenario ==")
    for caso in _SMOKE:
        modelo = _carregar_modelo_por_id(caso["cenario"])
        saida = renderizar_tela(modelo, estilo=_ESTILO, largura=72, altura=30)
        identidade_ok = caso["identidade"] in saida and caso["identidade_extra"] in saida
        incorreto_ausente = caso["conteudo_incorreto"] not in saida
        placeholder_regra = ("(console)" not in saida)  # todos os smoke sao AUSENTE
        _registrar(
            "smoke {0}: identidade material presente".format(caso["cenario"]),
            identidade_ok,
            "identidade={0!r}".format(caso["identidade"]),
        )
        _registrar(
            "smoke {0}: conteudo incorreto ausente".format(caso["cenario"]),
            incorreto_ausente,
        )
        _registrar(
            "smoke {0}: placeholder {1}".format(caso["cenario"], caso["placeholder"]),
            placeholder_regra,
        )


def teste_ponto_de_entrada_real():
    print("")
    print("== Ponto de entrada real: python demo/demo.py <cenario> ==")
    # argv resolve a tela inicial.
    _registrar("_tela_inicial_de_argv sem argumento -> 'demo'",
               _tela_inicial_de_argv(["demo.py"]) == "demo")
    _registrar("_tela_inicial_de_argv com argumento -> cenario",
               _tela_inicial_de_argv(["demo.py", "h0036_console_hierarquia"])
               == "h0036_console_hierarquia")
    _registrar("_tela_inicial_de_argv ignora flags",
               _tela_inicial_de_argv(["demo.py", "--x", "h0036_console_tabela"])
               == "h0036_console_tabela")

    # Execucao real do ponto de entrada por cenario H-0036 (fora de TTY).
    for caso in _SMOKE:
        proc = subprocess.run(
            [sys.executable, "demo/demo.py", caso["cenario"]],
            cwd=str(_BASE_PADRAO), input="s\n",
            capture_output=True, text=True,
            env={**os.environ, "COLUMNS": "72", "LINES": "30",
                 "PYTHONDONTWRITEBYTECODE": "1"},
        )
        _registrar("demo.py {0}: exit 0".format(caso["cenario"]),
                   proc.returncode == 0, "rc={0}".format(proc.returncode))
        _registrar("demo.py {0}: identidade material na saida".format(caso["cenario"]),
                   caso["identidade"] in proc.stdout,
                   "identidade={0!r} ausente".format(caso["identidade"])
                   if caso["identidade"] not in proc.stdout else "")
        _registrar("demo.py {0}: placeholder ausente com conteudo".format(caso["cenario"]),
                   "(console)" not in proc.stdout)
        _registrar("demo.py {0}: conteudo de outro cenario ausente".format(caso["cenario"]),
                   caso["conteudo_incorreto"] not in proc.stdout)

    # Ponto de entrada sem argumento preserva a tela raiz (placeholder no console).
    proc0 = subprocess.run(
        [sys.executable, "demo/demo.py"],
        cwd=str(_BASE_PADRAO), input="s\n",
        capture_output=True, text=True,
        env={**os.environ, "COLUMNS": "80", "LINES": "30",
             "PYTHONDONTWRITEBYTECODE": "1"},
    )
    _registrar("demo.py sem argumento: tela raiz ORQUESTRADOR",
               proc0.returncode == 0 and "ORQUESTRADOR" in proc0.stdout)
    _registrar("demo.py sem argumento: placeholder '(console)' presente (sem conteudo)",
               "(console)" in proc0.stdout and "H-0036" not in proc0.stdout)


def teste_h0053_arvore_colapsavel_carrega_renderiza_e_alterna_ramo():
    modelo = _carregar_modelo_por_id("h0053_arvore_colapsavel")
    console = navegacao.lista_foco(modelo)[0]
    estado_base = criar_estado_inicial()
    assert "ramos_fechados" not in estado_base
    estado = _preparar_estado_h0053(estado_base, modelo)
    estado.update({
        "estilo": _ESTILO,
        "foco_console": 0,
        "cursores": {console.id: 0},
    })
    assert estado["ramos_fechados"][console.id] == frozenset()
    assert "ramos_fechados" not in modelo._raw
    assert "ramos_fechados" not in console._campos_inertes

    aberta = renderizar_estado(estado, modelo, largura=90, altura=30)
    _registrar(
        "H-0053: política e conteúdo externo carregados",
        modelo.conteudo_externo is not None
        and navegacao.tipo_navegacao_efetivo(console) == "arvore_colapsavel",
    )
    _registrar(
        "H-0053: árvore aberta renderiza sem placeholder e com chip",
        "(console)" not in aberta
        and "1. Fundamentos" in aberta
        and "1.2.1" in aberta
        and "[✥] Navegar" in aberta
        and "[Esc] Sair" in aberta
        and "[Esc] Voltar" not in aberta,
    )
    barra_aberta = next(linha for linha in aberta.splitlines() if "[?] Ajuda" in linha)
    _registrar(
        "H-0053: ramo aberto mostra Recolher e Ajuda por último",
        "[␣] Recolher" in barra_aberta
        and barra_aberta.index("[␣] Recolher") < barra_aberta.index("[?] Ajuda"),
    )

    fechada = processar_comando(estado, " ", modelo)
    quadro_fechado = renderizar_estado(fechada, modelo, largura=90, altura=30)
    _registrar(
        "H-0053: Espaço fecha o ramo sem seleção",
        fechada.get("ramos_fechados", {}).get(console.id) == frozenset({"secao_1"})
        and "1.1" not in quadro_fechado
        and "1.2" not in quadro_fechado
        and "1.2.1" not in quadro_fechado
        and "2. Estado" in quadro_fechado
        and fechada.get("selecoes", {}) == {},
    )
    barra_fechada = next(linha for linha in quadro_fechado.splitlines() if "[?] Ajuda" in linha)
    _registrar(
        "H-0053: ramo recolhido mostra Expandir ativo",
        "[␣] Expandir" in barra_fechada
        and "\x1b[90m[␣] Expandir\x1b[39m" not in barra_fechada,
    )

    reaberta = processar_comando(fechada, " ", modelo)
    quadro_reaberto = renderizar_estado(reaberta, modelo, largura=90, altura=30)
    _registrar(
        "H-0053: segundo Espaço reabre o mesmo ramo corrente",
        reaberta.get("ramos_fechados", {}).get(console.id) == frozenset()
        and reaberta.get("cursores", {}).get(console.id) == 0
        and "1.1" in quadro_reaberto
        and "1.2" in quadro_reaberto
        and "1.2.1" in quadro_reaberto,
    )

    folha = estado
    for _ in range(3):
        folha = processar_comando(folha, "\x1b[B", modelo)
    quadro_folha = renderizar_estado(folha, modelo, largura=90, altura=30)
    quadro_folha_sem_ansi = re.sub(r"\x1b\[[0-9;]*m", "", quadro_folha)
    barra_folha = next(
        linha for linha in quadro_folha_sem_ansi.splitlines()
        if "[?] Ajuda" in linha
    )
    _registrar(
        "H-0053: folha mostra Expandir inativo e Espaço não seleciona",
        "[␣] Expandir" in barra_folha
        and "\x1b[90m" in quadro_folha
        and navegacao.estado_chip_arvore(
            dict(folha, modelo=modelo)
        ) == {
            "console_id": console.id,
            "item_id": "item_1_2_1",
            "texto": "Expandir",
            "ativo": False,
        }
        and processar_comando(folha, " ", modelo)["cursores"] == folha["cursores"]
        and processar_comando(folha, " ", modelo).get("selecoes", {}) == {},
    )


def teste_h0053_fixture_hierarquia_e_multiline():
    modelo = _carregar_modelo_por_id("h0053_arvore_colapsavel")
    console = navegacao.lista_foco(modelo)[0]
    barra = modelo.barra_de_menus["chips"]
    assert barra[-1]["tecla"] == "?"
    assert barra[-1]["texto"] == "Ajuda"
    assert barra[-1]["regra_ativo"] == "sempre"
    assert any(
        chip["tipo"] == "acao"
        and chip["tecla"] == "␣"
        and chip["texto"] == "Expandir"
        for chip in barra
    )

    conteudo = modelo.conteudo_externo
    assert [no.id for no in conteudo.nos] == ["secao_1", "secao_2"]
    assert [no.id for no in conteudo.nos[0].filhos] == [
        "subsecao_1_1", "subsecao_1_2"
    ]
    assert [no.id for no in conteudo.nos[0].filhos[1].filhos] == [
        "item_1_2_1"
    ]
    assert [no.id for no in conteudo.nos[1].filhos] == ["subsecao_2_1"]
    assert "a)" not in str(conteudo._raw)

    linhas = _linhas_console(console, 80, verboso=True)
    assert len(linhas) > 6
    assert any("1. " in linha for linha in linhas)
    assert any("1.1 " in linha for linha in linhas)
    assert any("1.2 " in linha for linha in linhas)
    assert any("1.2.1 " in linha for linha in linhas)
    assert any("2. " in linha for linha in linhas)
    assert any("2.1 " in linha for linha in linhas)


def teste_h0053_reconcilia_cursor_antes_do_chip_e_renderer():
    modelo = _carregar_modelo_por_id("h0053_arvore_colapsavel")
    console = navegacao.lista_foco(modelo)[0]
    estado = dict(
        criar_estado_inicial(),
        estilo=_ESTILO,
        foco_console=0,
        cursores={},
    )

    reconciliado = _preparar_estado_h0053(estado, modelo)
    assert reconciliado["cursores"] == {console.id: 0}

    contexto = navegacao.estado_chip_arvore(
        dict(reconciliado, modelo=modelo)
    )
    quadro = renderizar_estado(reconciliado, modelo, largura=90, altura=30)
    simbolo = _ESTILO.selecionado_simbolo
    linha_marcada = [
        linha for linha in quadro.splitlines()
        if simbolo in linha and "1. Fundamentos" in linha
    ]
    corrente = navegacao.sequencia_visivel_arvore(
        console, dict(reconciliado, modelo=modelo)
    )[reconciliado["cursores"][console.id]]

    assert contexto["item_id"] == corrente.id
    assert contexto["item_id"] == console.conteudo_externo.nos[0].id
    assert len(linha_marcada) == 1


def teste_h0053_renderer_nao_inventa_cursor_zero_sem_reconciliacao():
    modelo = _carregar_modelo_por_id("h0053_arvore_colapsavel")
    lista = navegacao.lista_foco(modelo)

    quadro = renderizar_tela(
        modelo,
        _ESTILO,
        largura=90,
        altura=30,
        foco_console=0,
        cursores={},
        lista_foco=lista,
        largura_navegacao=90,
    )
    linhas_nos = [
        linha for linha in quadro.splitlines()
        if "1. Fundamentos" in linha
    ]

    assert linhas_nos
    assert all(_ESTILO.selecionado_simbolo not in linha for linha in linhas_nos)
    assert navegacao.estado_chip_arvore({
        "modelo": modelo,
        "foco_console": 0,
        "cursores": {},
    }) is None


def teste_h0053_dispatch_de_espaco_redesenha_a_sessao_sem_tty(
    monkeypatch, capsys
):
    """Exerce o dispatch da sessão e prova o redesenho do estado de árvore."""
    class LinhaComEspaco(str):
        def strip(self, chars=None):
            if self == " \n":
                return " "
            return super().strip(chars)

    class Entrada:
        def isatty(self):
            return False

        def __iter__(self):
            return iter([LinhaComEspaco(" \n"), LinhaComEspaco(" \n"), "s\n"])

    monkeypatch.setattr(sys, "stdin", Entrada())
    assert demo_navegacao_main([
        "demo_navegacao.py",
        "--tela",
        "config/telas/demo/h0053_arvore_colapsavel.json",
    ]) == 0
    saida = capsys.readouterr().out

    assert saida.count("1.2.1") == 2
    assert saida.count("1.1") == 2


def main():
    print("Testes H-0036 - catalogo e ponto de entrada com conteudo externo")
    print("Base padrao: {0}".format(_BASE_PADRAO))
    print("Python: {0}".format(sys.version.split()[0]))

    teste_catalogo()
    teste_carregamento_separado_por_cenario()
    teste_apresentacoes_acessiveis()
    teste_ausencia_de_mistura()
    teste_smoke_por_cenario()
    teste_ponto_de_entrada_real()

    print("")
    print("== Resumo ==")
    total = len(_RESULTADOS)
    passaram = sum(1 for _, ok in _RESULTADOS if ok)
    falharam = total - passaram
    print("Total de verificacoes: {0}".format(total))
    print("Passaram: {0}".format(passaram))
    print("Falharam: {0}".format(falharam))
    if falharam:
        print("")
        print("Verificacoes falhadas:")
        for nome, ok in _RESULTADOS:
            if not ok:
                print("  - {0}".format(nome))
    return 0 if falharam == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
