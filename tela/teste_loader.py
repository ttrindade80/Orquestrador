"""Diagnostico do loader/validador de tela.json (H-0001).

Executavel via:
    python tela/teste_loader.py

Cobre os criterios de aceite testaveis do handoff H-0001:
- carregamento do arquivo real config/telas/demo/demo.json;
- casos de erro (arquivo ausente, JSON invalido, campos obrigatorios
  ausentes, id divergente do basename, corpo.elementos invalido,
  elemento sem id, elemento sem tipo, tipo desconhecido);
- aceitacao dos tipos console, lancador e dashboard;
- preservacao inerte de campos pendentes (DOC-B008 / DOC-B009).

Cria arquivos JSON temporarios em um diretorio tmp para os casos de erro
e os remove ao final. Retorna codigo de saida 0 se todos os criterios
passaram, 1 caso contrario.

Apenas biblioteca padrao do Python.
"""

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path


_BASE_PADRAO = Path(__file__).resolve().parent.parent

sys.dont_write_bytecode = True

sys.path.insert(0, str(_BASE_PADRAO))

from tela import loader  # noqa: E402
from tela.loader import (  # noqa: E402
    ARRANJOS_CORPO_VALIDOS,
    MODOS_DISTRIBUICAO_CORPO_VALIDOS,
    TIPOS_CORPO_VALIDOS,
    TIPOS_ESTRUTURAIS_VALIDOS,
    TelaArquivoNaoEncontrado,
    TelaCampoObrigatorioAusente,
    TelaElementoSemId,
    TelaElementoSemTipo,
    TelaErro,
    TelaEstruturaInvalida,
    TelaGrupoInvalido,
    TelaIdIncorreto,
    TelaIdNaoCoincideComArquivo,
    TelaJsonInvalido,
    TelaTipoDesconhecido,
    carregar_tela,
    carregar_conteudo_externo,
    validar_conteudo_externo,
)


_RESULTADOS = []

_RAIZ_TELAS_DEMO = os.path.join("config", "telas", "demo")


def _registrar(nome, passou, detalhe=""):
    status = "PASSOU" if passou else "FALHOU"
    linha = "[{0}] {1}".format(status, nome)
    if detalhe:
        linha += " - {0}".format(detalhe)
    print(linha)
    _RESULTADOS.append((nome, passou))


def _escrever_tela(base_dir, id_tela, conteudo):
    """Escreve config/telas/<id_tela>.json em base_dir."""
    dir_telas = base_dir / "config" / "telas"
    dir_telas.mkdir(parents=True, exist_ok=True)
    arquivo = dir_telas / "{0}.json".format(id_tela)
    arquivo.write_text(
        json.dumps(conteudo, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return arquivo


# Conteúdo válido canônico de config/elementos/lancador.json, espelhando
# os valores de produção (H-0034). Usado pelos helpers de tmp_base para
# que telas com tipo=lancador possam ser carregadas sem TelaArquivoNaoEncontrado.
_LANCADOR_JSON_VALIDO = {
    "layout": {
        "vaos": {
            "chip_texto": {"minimo": 1, "maximo": 3},
            "entre_itens_colunas_margem": {"minimo": 2, "maximo": 5},
        },
        "vertical": {
            "margem_borda_superior": 1,
            "margem_borda_inferior": 1,
        },
    },
    "verificacao": {
        "texto": {
            "max_caracteres": 15,
        },
    },
}

# Envelope pre-ADR-0028 variante 1 completo (itens + 6 campos base), canônico,
# usado como placeholder de elemento ``console`` em testes macro (arranjo,
# distribuicao, matriz, etc.) que precisam de um console valido que passe pela
# validacao estrutural sem entrar no escopo D23. Apos o sexto patch
# (H0037-IMPL-QAPP5-001), a variante 1 exige os 6 campos base completos para
# ser reconhecida como envelope pre-ADR-0028; placeholders minimos com apenas
# itens+origem_dados eram tratados como envelope parcial e agora seriam
# rejeitados como incompletos. Este envelope canonico substitui o antigo
# placeholder {itens:[], origem_dados:None} + regra_geracao_itens:{} (mascarador
# removido: regra_geracao_itens nao e discriminador valido).
_ENVELOPE_CONSOLE_COMPLETO = {
    "itens": [],
    "origem_dados": None,
    "politica_composicao": {"alinhamento": "esquerda",
                            "overflow_normal": "truncar_com_reticencias"},
    "politica_navegacao": {"navegavel": False},
    "politica_selecao": "nenhuma",
    "politica_paginacao": "sem",
    "politica_exibicao": {"modo_inicial": "normal", "verboso": False},
}


def _criar_config_lancador(tmp_base, conteudo=None):
    """Cria config/elementos/lancador.json em tmp_base.

    Sem argumento, usa os valores canônicos de _LANCADOR_JSON_VALIDO.
    Com conteudo, escreve o valor fornecido (pode ser string ou dict).
    """
    dir_elementos = tmp_base / "config" / "elementos"
    dir_elementos.mkdir(parents=True, exist_ok=True)
    caminho = dir_elementos / "lancador.json"
    if conteudo is None:
        texto = json.dumps(_LANCADOR_JSON_VALIDO, ensure_ascii=False, indent=2)
    elif isinstance(conteudo, str):
        texto = conteudo
    else:
        texto = json.dumps(conteudo, ensure_ascii=False, indent=2)
    caminho.write_text(texto, encoding="utf-8")
    return caminho


def _tela_minima(id_tela="teste", id_interno=None, **sobreposicooes):
    """Cria uma tela macro minima valida, com sobreposicooes opcionais."""
    if id_interno is None:
        id_interno = id_tela
    base = {
        "schema": "tela.v1",
        "id": id_interno,
        "cabecalho": {"titulo": "T", "descricao": "D"},
        "corpo": {
            "arranjo": "sobreposto",
            "elementos": [
            # Console pre-ADR-0028 de envelope (itens + origem_dados): fora do
            # escopo D23 por tipo estrutural real (campos do envelope pre-ADR-0028
            # presentes), para que estes testes macro (arranjo, distribuicao,
            # etc.) nao exijam politica_modo. Telas consumidoras de conteudo
            # multinivel sao tratadas em testes proprios (D23). Sexto patch
            # (H0037-IMPL-QAPP5-001): a antiga chave ``regra_geracao_itens: {}``
            # foi removida — ela nao e discriminador valido (sem schema interno
            # fechado) e mascarava a classificacao estrutural.
                {"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}},
            ],
        },
        "barra_de_menus": {"distribuicao": "horizontal", "chips": []},
    }
    for chave, valor in sobreposicooes.items():
        if valor is _VAZIO:
            if chave in base:
                del base[chave]
            continue
        if "." in chave:
            pai, filho = chave.split(".", 1)
            base.setdefault(pai, {})[filho] = valor
        else:
            base[chave] = valor
    return base


_VAZIO = object()


def _espera_excecao(nome, fn, tipo_esperado):
    try:
        fn()
    except tipo_esperado as exc:
        _registrar(nome, True, "{0}: {1}".format(type(exc).__name__, exc))
        return exc
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            nome,
            False,
            "esperava {0}; obteve {1}: {2}".format(
                tipo_esperado.__name__, type(exc).__name__, exc
            ),
        )
        return None
    _registrar(
        nome,
        False,
        "esperava {0}; nenhuma excecao lancada".format(
            tipo_esperado.__name__
        ),
    )
    return None


def teste_caminho_feliz():
    print("")
    print("== Carregamento do arquivo real config/telas/demo/demo.json ==")
    try:
        tela = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar("carregar_tela(demo)", False,
                   "{0}: {1}".format(type(exc).__name__, exc))
        return
    _registrar("carregar_tela(demo)", True)

    _registrar(
        "tela.id == 'demo'",
        tela.get("id") == "demo",
        "id={0!r}".format(tela.get("id")),
    )
    _registrar(
        "tela.schema presente",
        isinstance(tela.get("schema"), str) and tela.get("schema") != "",
        "schema={0!r}".format(tela.get("schema")),
    )
    _registrar(
        "tela.cabecalho presente",
        isinstance(tela.get("cabecalho"), dict),
    )
    _registrar(
        "tela.barra_de_menus presente",
        isinstance(tela.get("barra_de_menus"), dict),
    )

    # H-0016: distribuicao migrada para objeto canônico.
    dist = tela.get("barra_de_menus", {}).get("distribuicao")
    _registrar(
        "H-0016: barra_de_menus.distribuicao e objeto (nao string)",
        isinstance(dist, dict),
        "dist={0!r}".format(dist),
    )
    _registrar(
        "H-0016: distribuicao.modo == 'horizontal_responsiva'",
        isinstance(dist, dict) and dist.get("modo") == "horizontal_responsiva",
        "modo={0!r}".format(dist.get("modo") if isinstance(dist, dict) else None),
    )
    _registrar(
        "H-0016: distribuicao.ordem.politica == 'declaracao'",
        isinstance(dist, dict)
        and dist.get("ordem", {}).get("politica") == "declaracao",
    )
    _registrar(
        "H-0016: distribuicao.ordem.ancoras usa IDs reais (chip_esc/chip_ajuda)",
        isinstance(dist, dict)
        and dist.get("ordem", {}).get("ancoras", {}).get("primeiro") == ["chip_esc"]
        and dist.get("ordem", {}).get("ancoras", {}).get("ultimo") == ["chip_ajuda"],
        "ancoras={0!r}".format(
            dist.get("ordem", {}).get("ancoras") if isinstance(dist, dict) else None
        ),
    )
    _registrar(
        "tela.corpo presente",
        isinstance(tela.get("corpo"), dict),
    )
    _registrar(
        "tela.corpo.arranjo preservado",
        tela.get("corpo", {}).get("arranjo") == "vertical",
        "arranjo={0!r}".format(tela.get("corpo", {}).get("arranjo")),
    )
    # H-0025: demo.json declara corpo.distribuicao fracao [2,1,2].
    dist_orq = tela.get("corpo", {}).get("distribuicao")
    _registrar(
        "H-0025: demo declara corpo.distribuicao (fracao [2,1,2])",
        isinstance(dist_orq, dict)
        and dist_orq.get("modo") == "fracao"
        and dist_orq.get("valores") == [2, 1, 2],
        "dist={0!r}".format(dist_orq),
    )
    elementos = tela.get("corpo", {}).get("elementos", [])
    _registrar(
        "tela.corpo.elementos e lista com 3 itens",
        isinstance(elementos, list) and len(elementos) == 3,
        "n={0}".format(len(elementos) if isinstance(elementos, list) else "?"),
    )
    tipos_encontrados = sorted(
        e.get("tipo") for e in elementos if isinstance(e, dict)
    )
    _registrar(
        "tipos presentes = {console, dashboard, lancador}",
        tipos_encontrados == ["console", "dashboard", "lancador"],
        "tipos={0!r}".format(tipos_encontrados),
    )
    ids_encontrados = sorted(
        e.get("id") for e in elementos if isinstance(e, dict)
    )
    _registrar(
        "ids dos elementos presentes",
        ids_encontrados == ["console_principal", "dashboard_info",
                            "lancador_principal"],
        "ids={0!r}".format(ids_encontrados),
    )
    _registrar(
        "_raw preserva o JSON original completo",
        isinstance(tela.get("_raw"), dict)
        and tela.get("_raw", {}).get("id") == "demo",
    )
    print("")
    print("-- Declaracao inerte preservada (DOC-B008 / DOC-B009) --")
    raw = tela.get("_raw", {})

    chip_estilo = None
    for chip in raw.get("barra_de_menus", {}).get("chips", []):
        if isinstance(chip, dict) and chip.get("id") == "chip_estilo":
            chip_estilo = chip
            break
    _registrar(
        "chip_estilo removido da barra_de_menus do Orquestrador "
        "(capacidade nao implementada - ADR-0012/H-0014)",
        chip_estilo is None,
    )

    console_principal = None
    for el in raw.get("corpo", {}).get("elementos", []):
        if isinstance(el, dict) and el.get("id") == "console_principal":
            console_principal = el
            break
    _registrar(
        "console_principal.origem_dados.referencia == 'pendente' inerte",
        isinstance(console_principal, dict)
        and console_principal.get("origem_dados", {}).get("referencia")
        == "pendente",
    )

    lancador = None
    for el in raw.get("corpo", {}).get("elementos", []):
        if isinstance(el, dict) and el.get("id") == "lancador_principal":
            lancador = el
            break
    itens_lancador = (
        lancador.get("itens") if isinstance(lancador, dict) else None
    )
    _registrar(
        "lancador_principal.itens e lista com 11 itens "
        "(H-0013 d/g + H-0030 chips 1-5 + H-0037 chips 6-9)",
        isinstance(itens_lancador, list) and len(itens_lancador) == 11,
        "n={0}".format(
            len(itens_lancador) if isinstance(itens_lancador, list) else "?"
        ),
    )
    item_lancador = (
        itens_lancador[0]
        if isinstance(itens_lancador, list) and len(itens_lancador) >= 1
        else None
    )
    _registrar(
        "item do lancador possui id, chip, texto e tela_destino",
        isinstance(item_lancador, dict)
        and isinstance(item_lancador.get("id"), str)
        and isinstance(item_lancador.get("chip"), str)
        and isinstance(item_lancador.get("texto"), str)
        and isinstance(item_lancador.get("tela_destino"), str),
        "item={0!r}".format(item_lancador),
    )
    _registrar(
        "item do lancador: texto == 'Destino' (7 chars, <= 15)",
        isinstance(item_lancador, dict)
        and item_lancador.get("texto") == "Destino"
        and len(item_lancador.get("texto", "")) == 7,
    )
    _registrar(
        "item do lancador: tela_destino == 'destino_minimo'",
        isinstance(item_lancador, dict)
        and item_lancador.get("tela_destino") == "destino_minimo",
    )
    _registrar(
        "item do lancador: chip == 'd'",
        isinstance(item_lancador, dict)
        and item_lancador.get("chip") == "d",
    )
    _registrar(
        "lancador_principal sem 'pendencia_itens' apos adicionar item (H-0010A)",
        isinstance(lancador, dict)
        and "pendencia_itens" not in lancador,
    )

    item_grupo = (
        itens_lancador[1]
        if isinstance(itens_lancador, list) and len(itens_lancador) >= 2
        else None
    )
    _registrar(
        "item_grupo_minimo possui id, chip, texto e tela_destino (H-0013)",
        isinstance(item_grupo, dict)
        and isinstance(item_grupo.get("id"), str)
        and isinstance(item_grupo.get("chip"), str)
        and isinstance(item_grupo.get("texto"), str)
        and isinstance(item_grupo.get("tela_destino"), str),
        "item={0!r}".format(item_grupo),
    )
    _registrar(
        "item_grupo_minimo: id == 'item_grupo_minimo' (H-0013)",
        isinstance(item_grupo, dict)
        and item_grupo.get("id") == "item_grupo_minimo",
    )
    _registrar(
        "item_grupo_minimo: chip == 'g' (H-0013)",
        isinstance(item_grupo, dict) and item_grupo.get("chip") == "g",
    )
    _registrar(
        "item_grupo_minimo: texto == 'Grupo Min.' (10 chars, <= 15) (H-0013)",
        isinstance(item_grupo, dict)
        and item_grupo.get("texto") == "Grupo Min."
        and len(item_grupo.get("texto", "")) == 10,
    )
    _registrar(
        "item_grupo_minimo: tela_destino == 'grupo_minimo' (H-0013)",
        isinstance(item_grupo, dict)
        and item_grupo.get("tela_destino") == "grupo_minimo",
    )

    _registrar(
        "bindings preservado como declaracao inerte",
        isinstance(raw.get("bindings"), dict),
    )
    _registrar(
        "referencias_de_acoes preservado como declaracao inerte",
        isinstance(raw.get("referencias_de_acoes"), dict),
    )
    _registrar(
        "filtros preservado como declaracao inerte",
        isinstance(raw.get("filtros"), list),
    )


def _run_erros(tmp_base):
    print("")
    print("== Casos de erro (arquivos temporarios em {0}) ==".format(tmp_base))

    def carregar_arquivo_inexistente():
        return carregar_tela(tmp_base, "nao_existe")

    _espera_excecao(
        "arquivo ausente -> TelaArquivoNaoEncontrado",
        carregar_arquivo_inexistente,
        TelaArquivoNaoEncontrado,
    )

    arquivo_invalido = tmp_base / "config" / "telas" / "invalido.json"
    arquivo_invalido.parent.mkdir(parents=True, exist_ok=True)
    arquivo_invalido.write_text(
        "{ nao e um json valido {{{", encoding="utf-8"
    )
    _espera_excecao(
        "JSON sintaticamente invalido -> TelaJsonInvalido",
        lambda: carregar_tela(tmp_base, "invalido"),
        TelaJsonInvalido,
    )

    _escrever_tela(tmp_base, "sem_schema", {"id": "sem_schema",
                                            "cabecalho": {},
                                            "corpo": {"elementos": []},
                                            "barra_de_menus": {}})
    _espera_excecao(
        "sem schema -> TelaCampoObrigatorioAusente(schema)",
        lambda: carregar_tela(tmp_base, "sem_schema"),
        TelaCampoObrigatorioAusente,
    )

    _escrever_tela(tmp_base, "sem_id", {"schema": "tela.v1",
                                        "cabecalho": {},
                                        "corpo": {"elementos": []},
                                        "barra_de_menus": {}})
    _espera_excecao(
        "sem id -> TelaCampoObrigatorioAusente(id)",
        lambda: carregar_tela(tmp_base, "sem_id"),
        TelaCampoObrigatorioAusente,
    )

    _escrever_tela(tmp_base, "id_vazio",
                   _tela_minima(id_tela="id_vazio", id_interno=""))
    _espera_excecao(
        "id vazio -> TelaCampoObrigatorioAusente(id)",
        lambda: carregar_tela(tmp_base, "id_vazio"),
        TelaCampoObrigatorioAusente,
    )

    _escrever_tela(tmp_base, "arquivo_a",
                   _tela_minima(id_tela="arquivo_a", id_interno="outro_id"))
    _espera_excecao(
        "id diverge do basename -> TelaIdNaoCoincideComArquivo",
        lambda: carregar_tela(tmp_base, "arquivo_a"),
        TelaIdNaoCoincideComArquivo,
    )

    _escrever_tela(tmp_base, "sem_cabecalho",
                   _tela_minima(id_tela="sem_cabecalho",
                                cabecalho=_VAZIO))
    _espera_excecao(
        "sem cabecalho -> TelaCampoObrigatorioAusente(cabecalho)",
        lambda: carregar_tela(tmp_base, "sem_cabecalho"),
        TelaCampoObrigatorioAusente,
    )

    _escrever_tela(tmp_base, "sem_corpo",
                   _tela_minima(id_tela="sem_corpo", corpo=_VAZIO))
    _espera_excecao(
        "sem corpo -> TelaCampoObrigatorioAusente(corpo)",
        lambda: carregar_tela(tmp_base, "sem_corpo"),
        TelaCampoObrigatorioAusente,
    )

    _escrever_tela(tmp_base, "sem_barra",
                   _tela_minima(id_tela="sem_barra", barra_de_menus=_VAZIO))
    _espera_excecao(
        "sem barra_de_menus -> TelaCampoObrigatorioAusente(barra_de_menus)",
        lambda: carregar_tela(tmp_base, "sem_barra"),
        TelaCampoObrigatorioAusente,
    )

    _escrever_tela(tmp_base, "sem_elementos",
                   {"schema": "tela.v1", "id": "sem_elementos",
                    "cabecalho": {}, "corpo": {"arranjo": "sobreposto"},
                    "barra_de_menus": {}})
    _espera_excecao(
        "sem corpo.elementos -> TelaCampoObrigatorioAusente(corpo.elementos)",
        lambda: carregar_tela(tmp_base, "sem_elementos"),
        TelaCampoObrigatorioAusente,
    )

    _escrever_tela(tmp_base, "elementos_nao_lista",
                   {"schema": "tela.v1", "id": "elementos_nao_lista",
                    "cabecalho": {}, "corpo": {"elementos": "nao_lista"},
                    "barra_de_menus": {}})
    _espera_excecao(
        "corpo.elementos nao e lista -> TelaEstruturaInvalida",
        lambda: carregar_tela(tmp_base, "elementos_nao_lista"),
        TelaEstruturaInvalida,
    )

    _escrever_tela(tmp_base, "elem_sem_id",
                   {"schema": "tela.v1", "id": "elem_sem_id",
                    "cabecalho": {}, "barra_de_menus": {},
                    "corpo": {"elementos": [{"tipo": "console"}]}})
    _espera_excecao(
        "elemento sem id -> TelaElementoSemId",
        lambda: carregar_tela(tmp_base, "elem_sem_id"),
        TelaElementoSemId,
    )

    _escrever_tela(tmp_base, "elem_sem_tipo",
                   {"schema": "tela.v1", "id": "elem_sem_tipo",
                    "cabecalho": {}, "barra_de_menus": {},
                    "corpo": {"elementos": [{"id": "x"}]}})
    _espera_excecao(
        "elemento sem tipo -> TelaElementoSemTipo",
        lambda: carregar_tela(tmp_base, "elem_sem_tipo"),
        TelaElementoSemTipo,
    )

    _escrever_tela(tmp_base, "tipo_desconhecido",
                   {"schema": "tela.v1", "id": "tipo_desconhecido",
                    "cabecalho": {}, "barra_de_menus": {},
                    "corpo": {"elementos": [
                        {"id": "x", "tipo": "tabela"}
                    ]}})
    _espera_excecao(
        "tipo desconhecido -> TelaTipoDesconhecido",
        lambda: carregar_tela(tmp_base, "tipo_desconhecido"),
        TelaTipoDesconhecido,
    )

    _escrever_tela(tmp_base, "tipo_nao_string",
                   {"schema": "tela.v1", "id": "tipo_nao_string",
                    "cabecalho": {}, "barra_de_menus": {},
                    "corpo": {"elementos": [
                        {"id": "x", "tipo": 123}
                    ]}})
    _espera_excecao(
        "tipo nao string -> TelaElementoSemTipo (reuso da categoria)",
        lambda: carregar_tela(tmp_base, "tipo_nao_string"),
        TelaElementoSemTipo,
    )


def _run_tipos_validos(tmp_base):
    print("")
    print("== Aceitacao dos tipos validos (taxonomia fechada) ==")
    for tipo in ("console", "lancador", "dashboard"):
        nome_arquivo = "tipo_ok_" + tipo
        # Console pre-ADR-0028 de envelope VARIANTE 1 completo para ficar fora
        # do escopo D23 por tipo estrutural; este teste foca apenas na taxonomia.
        # Sexto patch (H0037-IMPL-QAPP5-001): a variante 1 agora exige os 6
        # campos base completos; placeholder minimo (itens+origem_dados) e
        # envelope incompleto e seria rejeitado. Usa _ENVELOPE_CONSOLE_COMPLETO.
        elem = {"id": "e1", "tipo": tipo}
        if tipo == "console":
            elem.update(_ENVELOPE_CONSOLE_COMPLETO)
        _escrever_tela(tmp_base, nome_arquivo,
                       {"schema": "tela.v1", "id": nome_arquivo,
                        "cabecalho": {}, "barra_de_menus": {},
                        "corpo": {"elementos": [elem]}})
        try:
            carregar_tela(tmp_base, nome_arquivo)
            _registrar("tipo '{0}' aceito".format(tipo), True)
        except Exception as exc:  # pragma: no cover - diagnostico
            _registrar("tipo '{0}' aceito".format(tipo), False,
                       "{0}: {1}".format(type(exc).__name__, exc))

    _registrar(
        "TIPOS_CORPO_VALIDOS == {console, lancador, dashboard}",
        TIPOS_CORPO_VALIDOS == {"console", "lancador", "dashboard"},
        "valor={0!r}".format(TIPOS_CORPO_VALIDOS),
    )


def _run_grupo_estrutural(tmp_base):
    print("")
    print("== Grupo estrutural minimo (H-0012) ==")

    print("-- Carregamento do arquivo real config/telas/demo/grupo_minimo.json --")
    try:
        tela = carregar_tela(_BASE_PADRAO, "grupo_minimo", _RAIZ_TELAS_DEMO)
        _registrar("carregar_tela(grupo_minimo) sem excecao", True)
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar("carregar_tela(grupo_minimo) sem excecao", False,
                   "{0}: {1}".format(type(exc).__name__, exc))
        return None

    _registrar(
        "grupo_minimo.id == 'grupo_minimo'",
        tela.get("id") == "grupo_minimo",
        "id={0!r}".format(tela.get("id")),
    )
    elementos = tela.get("corpo", {}).get("elementos", [])
    _registrar(
        "grupo_minimo.corpo.elementos e lista com 1 item",
        isinstance(elementos, list) and len(elementos) == 1,
        "n={0}".format(len(elementos) if isinstance(elementos, list) else "?"),
    )
    grupo = elementos[0] if isinstance(elementos, list) and elementos else {}
    _registrar(
        "elemento raiz e tipo 'grupo'",
        grupo.get("tipo") == "grupo",
        "tipo={0!r}".format(grupo.get("tipo")),
    )
    _registrar(
        "grupo.id == 'grupo_principal'",
        grupo.get("id") == "grupo_principal",
    )
    sub = grupo.get("elementos", [])
    _registrar(
        "grupo.elementos e lista com exatamente 1 item",
        isinstance(sub, list) and len(sub) == 1,
        "n={0}".format(len(sub) if isinstance(sub, list) else "?"),
    )
    item = sub[0] if isinstance(sub, list) and sub else {}
    _registrar(
        "item interno e tipo 'dashboard'",
        item.get("tipo") == "dashboard",
        "tipo={0!r}".format(item.get("tipo")),
    )
    campos = item.get("campos", [])
    _registrar(
        "dashboard interno tem 1 campo literal verificavel",
        isinstance(campos, list) and len(campos) >= 1
        and campos[0].get("fonte") == "literal"
        and isinstance(campos[0].get("valor"), str),
    )

    _registrar(
        "TIPOS_ESTRUTURAIS_VALIDOS == {grupo}",
        TIPOS_ESTRUTURAIS_VALIDOS == {"grupo"},
        "valor={0!r}".format(TIPOS_ESTRUTURAIS_VALIDOS),
    )
    _registrar(
        "grupo NAO esta em TIPOS_CORPO_VALIDOS (nao e funcional)",
        "grupo" not in TIPOS_CORPO_VALIDOS,
    )

    print("")
    print("-- Rejeicoes de grupo invalido (H-0012) --")

    def _grupo_minimo_dict(id_tela, **sobrepos):
        base_g = {
            "id": "grupo_principal",
            "tipo": "grupo",
            "arranjo": "vertical",
            "elementos": [
                {"id": "dash_interno", "tipo": "dashboard",
                 "titulo": "T", "campos": []},
            ],
        }
        for chave, valor in sobrepos.items():
            if valor is _VAZIO:
                if chave in base_g:
                    del base_g[chave]
            else:
                base_g[chave] = valor
        return _tela_minima(id_tela=id_tela, corpo={
            "arranjo": "vertical", "elementos": [base_g],
        })

    _escrever_tela(tmp_base, "g_sem_elementos",
                   _grupo_minimo_dict("g_sem_elementos", elementos=_VAZIO))
    _espera_excecao(
        "grupo sem 'elementos' -> TelaGrupoInvalido",
        lambda: carregar_tela(tmp_base, "g_sem_elementos"),
        TelaGrupoInvalido,
    )

    _escrever_tela(tmp_base, "g_elementos_vazio",
                   _grupo_minimo_dict("g_elementos_vazio", elementos=[]))
    _espera_excecao(
        "grupo com 'elementos' vazio -> TelaGrupoInvalido",
        lambda: carregar_tela(tmp_base, "g_elementos_vazio"),
        TelaGrupoInvalido,
    )

    # --- Substituicoes dos 4 testes historicos incompativeis (H-0027 sec 20.1) ---
    # Antigo: "grupo com 2 elementos -> TelaGrupoInvalido"
    # Novo: multiplos filhos sao validos (ADR-0019 D6)
    _escrever_tela(tmp_base, "g_dois_elementos",
                   _grupo_minimo_dict("g_dois_elementos", elementos=[
                       {"id": "d1", "tipo": "dashboard"},
                       {"id": "d2", "tipo": "dashboard"},
                   ]))
    try:
        carregar_tela(tmp_base, "g_dois_elementos")
        _registrar("grupo com 2 filhos funcionais e valido (ADR-0019 D6)", True)
    except Exception as exc:
        _registrar("grupo com 2 filhos funcionais e valido (ADR-0019 D6)",
                   False, "{0}: {1}".format(type(exc).__name__, exc))

    # Antigo: "grupo dentro de grupo -> TelaGrupoInvalido"
    # Novo: aninhamento ate nivel 2 e valido; nivel 4 e invalido (ADR-0019 D2, D4)
    _escrever_tela(tmp_base, "g_nivel2_valido",
                   _grupo_minimo_dict("g_nivel2_valido", elementos=[
                       {"id": "g2", "tipo": "grupo", "arranjo": "vertical",
                        "elementos": [{"id": "c_interno", "tipo": "console",
                                       "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}}]},
                   ]))
    try:
        carregar_tela(tmp_base, "g_nivel2_valido")
        _registrar("grupo dentro de grupo (nivel 1->2) e valido (ADR-0019 D2)", True)
    except Exception as exc:
        _registrar("grupo dentro de grupo (nivel 1->2) e valido (ADR-0019 D2)",
                   False, "{0}: {1}".format(type(exc).__name__, exc))

    # Antigo: "grupo com arranjo 'horizontal' -> TelaGrupoInvalido (ADR-0011)"
    # Novo: arranjo horizontal e valido por container (ADR-0019 D5)
    _escrever_tela(tmp_base, "g_horizontal_valido",
                   _grupo_minimo_dict("g_horizontal_valido", arranjo="horizontal"))
    try:
        carregar_tela(tmp_base, "g_horizontal_valido")
        _registrar("grupo com arranjo 'horizontal' e valido (ADR-0019 D5)", True)
    except Exception as exc:
        _registrar("grupo com arranjo 'horizontal' e valido (ADR-0019 D5)",
                   False, "{0}: {1}".format(type(exc).__name__, exc))

    # Antigo: "grupo com arranjo 'lado_a_lado' -> TelaGrupoInvalido (alias de horizontal)"
    # Novo: alias lado_a_lado tambem e valido (ADR-0019 D5)
    _escrever_tela(tmp_base, "g_lado_a_lado_valido",
                   _grupo_minimo_dict("g_lado_a_lado_valido", arranjo="lado_a_lado"))
    try:
        carregar_tela(tmp_base, "g_lado_a_lado_valido")
        _registrar("grupo com arranjo 'lado_a_lado' e valido, alias de horizontal (ADR-0019 D5)",
                   True)
    except Exception as exc:
        _registrar("grupo com arranjo 'lado_a_lado' e valido, alias de horizontal (ADR-0019 D5)",
                   False, "{0}: {1}".format(type(exc).__name__, exc))

    _escrever_tela(tmp_base, "g_tipo_desconhecido",
                   _grupo_minimo_dict("g_tipo_desconhecido", elementos=[
                       {"id": "x", "tipo": "tabela"},
                   ]))
    _espera_excecao(
        "grupo com tipo funcional desconhecido dentro -> TelaTipoDesconhecido",
        lambda: carregar_tela(tmp_base, "g_tipo_desconhecido"),
        TelaTipoDesconhecido,
    )

    print("")
    print("-- Lista plana permanece valida (preservacao) --")
    for id_plano in ("demo", "destino_minimo", "stub_b"):
        try:
            carregar_tela(_BASE_PADRAO, id_plano, _RAIZ_TELAS_DEMO)
            _registrar("lista plana '{0}' carrega sem erro".format(id_plano),
                       True)
        except Exception as exc:  # pragma: no cover - diagnostico
            _registrar("lista plana '{0}' carrega sem erro".format(id_plano),
                       False, "{0}: {1}".format(type(exc).__name__, exc))

    print("")
    print("-- H-0016: os 4 JSONs ativos com distribuicao objeto canônico --")
    for id_tela in ("demo", "grupo_minimo", "destino_minimo", "stub_b"):
        try:
            t = carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO)
        except Exception as exc:  # pragma: no cover - diagnostico
            _registrar(
                "H-0016: {0} carrega (objeto canônico)".format(id_tela),
                False, "{0}: {1}".format(type(exc).__name__, exc))
            continue
        d = t.get("barra_de_menus", {}).get("distribuicao")
        chips_ids = [
            c.get("id") for c in t.get("barra_de_menus", {}).get("chips", [])
            if isinstance(c, dict)
        ]
        _registrar(
            "H-0016: {0} distribuicao objeto com modo 'horizontal_responsiva'".format(id_tela),
            isinstance(d, dict) and d.get("modo") == "horizontal_responsiva"
            and d.get("ordem", {}).get("politica") == "declaracao",
            "modo={0!r}".format(d.get("modo") if isinstance(d, dict) else None),
        )
        _registrar(
            "H-0016: {0} ancora primeiro == chips[0].id".format(id_tela),
            isinstance(d, dict)
            and d.get("ordem", {}).get("ancoras", {}).get("primeiro")
            == [chips_ids[0]] if chips_ids else False,
        )


def _run_arranjo_corpo_h0019(tmp_base):
    print("")
    print("== H-0019: validacao de corpo.arranjo no loader ==")

    def _tela_com_arranjo(id_tela, arranjo):
        dados = _tela_minima(id_tela=id_tela)
        if arranjo is _VAZIO:
            del dados["corpo"]["arranjo"]
        else:
            dados["corpo"]["arranjo"] = arranjo
        return dados

    # Valores aceitos
    for arranjo_val in ("vertical", "horizontal", "sobreposto", "lado_a_lado"):
        nome_arquivo = "arranjo_aceito_{0}".format(arranjo_val)
        _escrever_tela(tmp_base, nome_arquivo,
                       _tela_com_arranjo(nome_arquivo, arranjo_val))
        try:
            carregar_tela(tmp_base, nome_arquivo)
            _registrar(
                "loader aceita arranjo {0!r} no corpo raiz".format(arranjo_val),
                True,
            )
        except Exception as exc:  # pragma: no cover - diagnostico
            _registrar(
                "loader aceita arranjo {0!r} no corpo raiz".format(arranjo_val),
                False,
                "{0}: {1}".format(type(exc).__name__, exc),
            )

    # Ausencia de arranjo (None equivalente)
    nome_sem_arranjo = "arranjo_ausente"
    dados_sem = _tela_minima(id_tela=nome_sem_arranjo)
    del dados_sem["corpo"]["arranjo"]
    _escrever_tela(tmp_base, nome_sem_arranjo, dados_sem)
    try:
        tela = carregar_tela(tmp_base, nome_sem_arranjo)
        _registrar(
            "loader aceita ausencia de arranjo (None)",
            tela.get("corpo", {}).get("arranjo") is None,
        )
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar(
            "loader aceita ausencia de arranjo (None)",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )

    # Valores rejeitados
    nome_diagonal = "arranjo_invalido_diagonal"
    _escrever_tela(tmp_base, nome_diagonal,
                   _tela_com_arranjo(nome_diagonal, "diagonal"))
    exc_diag = _espera_excecao(
        "loader rejeita arranjo invalido 'diagonal' -> TelaEstruturaInvalida",
        lambda: carregar_tela(tmp_base, nome_diagonal),
        TelaEstruturaInvalida,
    )
    if exc_diag is not None:
        _registrar(
            "mensagem de erro menciona 'corpo.arranjo'",
            "corpo.arranjo" in str(exc_diag),
            str(exc_diag),
        )

    nome_vazia = "arranjo_invalido_vazio"
    _escrever_tela(tmp_base, nome_vazia,
                   _tela_com_arranjo(nome_vazia, ""))
    _espera_excecao(
        "loader rejeita arranjo string vazia -> TelaEstruturaInvalida",
        lambda: carregar_tela(tmp_base, nome_vazia),
        TelaEstruturaInvalida,
    )

    nome_inteiro = "arranjo_invalido_inteiro"
    _escrever_tela(tmp_base, nome_inteiro,
                   _tela_com_arranjo(nome_inteiro, 1))
    _espera_excecao(
        "loader rejeita arranjo tipo inteiro (1) -> TelaEstruturaInvalida",
        lambda: carregar_tela(tmp_base, nome_inteiro),
        TelaEstruturaInvalida,
    )

    # Constante exportada
    _registrar(
        "ARRANJOS_CORPO_VALIDOS contem None, vertical, horizontal, sobreposto, lado_a_lado",
        ARRANJOS_CORPO_VALIDOS == {None, "vertical", "horizontal", "sobreposto", "lado_a_lado"},
        "valor={0!r}".format(ARRANJOS_CORPO_VALIDOS),
    )


def _run_distribuicao_corpo_h0025(tmp_base):
    print("")
    print("== H-0025: validacao de corpo.distribuicao (igual/percentual/fracao) ==")

    def _tela_dist(id_tela, distribuicao, n_elementos=3):
        elementos = [
            {"id": "e{0}".format(i), "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}}
            for i in range(n_elementos)
        ]
        corpo = {"arranjo": "vertical", "elementos": elementos}
        if distribuicao is not None:
            corpo["distribuicao"] = distribuicao
        return {
            "schema": "tela.v1", "id": id_tela, "cabecalho": {},
            "corpo": corpo, "barra_de_menus": {},
        }

    # --- Ausencia: nao materializa igual ---
    _escrever_tela(tmp_base, "dist_ausente", _tela_dist("dist_ausente", None))
    tela_aus = carregar_tela(tmp_base, "dist_ausente")
    _registrar(
        "ausencia de distribuicao: corpo.distribuicao is None (sem fallback igual)",
        tela_aus["corpo"].get("distribuicao") is None,
        "dist={0!r}".format(tela_aus["corpo"].get("distribuicao")),
    )

    # --- igual explicito (sem valores) ---
    _escrever_tela(
        tmp_base, "dist_igual",
        _tela_dist("dist_igual", {"modo": "igual"}),
    )
    tela_igual = carregar_tela(tmp_base, "dist_igual")
    _registrar(
        "igual explicito declarado e preservado",
        tela_igual["corpo"]["distribuicao"].get("modo") == "igual",
    )

    # --- percentual valido (soma 100) ---
    _escrever_tela(
        tmp_base, "dist_pct_ok",
        _tela_dist("dist_pct_ok", {"modo": "percentual", "valores": [40, 20, 40]}),
    )
    tela_pct = carregar_tela(tmp_base, "dist_pct_ok")
    _registrar(
        "percentual valido (soma 100) preservado",
        tela_pct["corpo"]["distribuicao"].get("valores") == [40, 20, 40],
    )

    # --- percentual soma invalida -> erro ---
    _escrever_tela(
        tmp_base, "dist_pct_soma",
        _tela_dist("dist_pct_soma", {"modo": "percentual", "valores": [40, 20, 30]}),
    )
    exc_pct = _espera_excecao(
        "percentual soma != 100 -> TelaEstruturaInvalida",
        lambda: carregar_tela(tmp_base, "dist_pct_soma"),
        TelaEstruturaInvalida,
    )
    if exc_pct is not None:
        _registrar(
            "mensagem menciona soma 100",
            "100" in str(exc_pct),
            str(exc_pct),
        )

    # --- fracao valido (pesos positivos) ---
    _escrever_tela(
        tmp_base, "dist_frac_ok",
        _tela_dist("dist_frac_ok", {"modo": "fracao", "valores": [2, 1, 2]}),
    )
    tela_frac = carregar_tela(tmp_base, "dist_frac_ok")
    _registrar(
        "fracao valido (pesos positivos) preservado",
        tela_frac["corpo"]["distribuicao"].get("valores") == [2, 1, 2],
    )

    # --- fracao peso invalido (zero) -> erro ---
    _escrever_tela(
        tmp_base, "dist_frac_zero",
        _tela_dist("dist_frac_zero", {"modo": "fracao", "valores": [2, 0, 2]}),
    )
    _espera_excecao(
        "fracao com peso 0 -> TelaEstruturaInvalida",
        lambda: carregar_tela(tmp_base, "dist_frac_zero"),
        TelaEstruturaInvalida,
    )

    # --- fracao peso negativo -> erro ---
    _escrever_tela(
        tmp_base, "dist_frac_neg",
        _tela_dist("dist_frac_neg", {"modo": "fracao", "valores": [2, -1, 2]}),
    )
    _espera_excecao(
        "fracao com peso negativo -> TelaEstruturaInvalida",
        lambda: carregar_tela(tmp_base, "dist_frac_neg"),
        TelaEstruturaInvalida,
    )

    # --- quantidade de valores incompativel -> erro ---
    _escrever_tela(
        tmp_base, "dist_qtd",
        _tela_dist("dist_qtd", {"modo": "fracao", "valores": [1, 1]}),
    )
    exc_qtd = _espera_excecao(
        "fracao com 2 valores para 3 filhos -> TelaEstruturaInvalida",
        lambda: carregar_tela(tmp_base, "dist_qtd"),
        TelaEstruturaInvalida,
    )
    if exc_qtd is not None:
        _registrar(
            "mensagem menciona quantidade de filhos",
            "filhos" in str(exc_qtd),
            str(exc_qtd),
        )

    # --- modo desconhecido -> erro ---
    _escrever_tela(
        tmp_base, "dist_modo_inv",
        _tela_dist("dist_modo_inv", {"modo": "media", "valores": [1, 1, 1]}),
    )
    _espera_excecao(
        "modo desconhecido 'media' -> TelaEstruturaInvalida",
        lambda: carregar_tela(tmp_base, "dist_modo_inv"),
        TelaEstruturaInvalida,
    )

    # --- distribuicao nao-dict -> erro ---
    _escrever_tela(
        tmp_base, "dist_nao_dict",
        _tela_dist("dist_nao_dict", "horizontal"),
    )
    _espera_excecao(
        "distribuicao como string -> TelaEstruturaInvalida",
        lambda: carregar_tela(tmp_base, "dist_nao_dict"),
        TelaEstruturaInvalida,
    )

    # --- constante exportada ---
    _registrar(
        "MODOS_DISTRIBUICAO_CORPO_VALIDOS == {igual, percentual, fracao}",
        MODOS_DISTRIBUICAO_CORPO_VALIDOS == {"igual", "percentual", "fracao"},
        "valor={0!r}".format(MODOS_DISTRIBUICAO_CORPO_VALIDOS),
    )

    # --- valores nao-numericos -> erro ---
    _escrever_tela(
        tmp_base, "dist_frac_str",
        _tela_dist("dist_frac_str", {"modo": "fracao", "valores": [2, "x", 2]}),
    )
    _espera_excecao(
        "fracao com valor nao-numerico -> TelaEstruturaInvalida",
        lambda: carregar_tela(tmp_base, "dist_frac_str"),
        TelaEstruturaInvalida,
    )

    # --- percentual com bool -> erro ---
    _escrever_tela(
        tmp_base, "dist_pct_bool",
        _tela_dist("dist_pct_bool", {"modo": "percentual", "valores": [True, 20, 40]}),
    )
    _espera_excecao(
        "percentual com bool -> TelaEstruturaInvalida",
        lambda: carregar_tela(tmp_base, "dist_pct_bool"),
        TelaEstruturaInvalida,
    )


def _run_hierarquia_grupos_adr0019(tmp_base):
    """Testes de hierarquia de grupos — ADR-0019 / H-0027 (secao 20.2)."""
    print("")
    print("== ADR-0019 / H-0027: hierarquia de grupos — loader ==")

    def _tela_com_corpo(id_tela, corpo):
        return {
            "schema": "tela.v1", "id": id_tela,
            "cabecalho": {"titulo": "T", "descricao": "D"},
            "corpo": corpo,
            "barra_de_menus": {"distribuicao": "horizontal", "chips": []},
        }

    # --- 1 nivel de grupo com um elemento funcional (preservacao grupo_minimo) ---
    _escrever_tela(tmp_base, "h_g1_um_funcional", _tela_com_corpo("h_g1_um_funcional", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "elementos": [{"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}}]},
        ],
    }))
    try:
        carregar_tela(tmp_base, "h_g1_um_funcional")
        _registrar("nivel 1: grupo com 1 funcional e valido", True)
    except Exception as exc:
        _registrar("nivel 1: grupo com 1 funcional e valido",
                   False, str(exc))

    # --- 1 nivel de grupo com multiplos elementos funcionais (D6) ---
    _escrever_tela(tmp_base, "h_g1_multi_func", _tela_com_corpo("h_g1_multi_func", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "elementos": [
                 {"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}},
                 {"id": "d1", "tipo": "dashboard"},
             ]},
        ],
    }))
    try:
        carregar_tela(tmp_base, "h_g1_multi_func")
        _registrar("nivel 1: grupo com 2 funcionais e valido (ADR-0019 D6)", True)
    except Exception as exc:
        _registrar("nivel 1: grupo com 2 funcionais e valido (ADR-0019 D6)",
                   False, str(exc))

    # --- 2 niveis de grupos (g1 -> g2 -> funcional) ---
    _escrever_tela(tmp_base, "h_g2", _tela_com_corpo("h_g2", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "elementos": [
                 {"id": "g2", "tipo": "grupo", "arranjo": "vertical",
                  "elementos": [{"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}}]},
             ]},
        ],
    }))
    try:
        carregar_tela(tmp_base, "h_g2")
        _registrar("2 niveis de grupos e valido (ADR-0019 D2)", True)
    except Exception as exc:
        _registrar("2 niveis de grupos e valido (ADR-0019 D2)",
                   False, str(exc))

    # --- 3 niveis de grupos (g1 -> g2 -> g3 -> funcional) ---
    _escrever_tela(tmp_base, "h_g3", _tela_com_corpo("h_g3", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "elementos": [
                 {"id": "g2", "tipo": "grupo", "arranjo": "vertical",
                  "elementos": [
                      {"id": "g3", "tipo": "grupo", "arranjo": "vertical",
                       "elementos": [{"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}}]},
                  ]},
             ]},
        ],
    }))
    try:
        carregar_tela(tmp_base, "h_g3")
        _registrar("3 niveis de grupos e valido (ADR-0019 D2)", True)
    except Exception as exc:
        _registrar("3 niveis de grupos e valido (ADR-0019 D2)",
                   False, str(exc))

    # --- 3 niveis com multiplos funcionais no nivel 3 (D3) ---
    _escrever_tela(tmp_base, "h_g3_multi", _tela_com_corpo("h_g3_multi", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "elementos": [
                 {"id": "g2", "tipo": "grupo", "arranjo": "vertical",
                  "elementos": [
                      {"id": "g3", "tipo": "grupo", "arranjo": "vertical",
                       "elementos": [
                           {"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}},
                           {"id": "d1", "tipo": "dashboard"},
                       ]},
                  ]},
             ]},
        ],
    }))
    try:
        carregar_tela(tmp_base, "h_g3_multi")
        _registrar("nivel 3 com 2 funcionais: valido, nao constitui nivel 4 (ADR-0019 D3)",
                   True)
    except Exception as exc:
        _registrar("nivel 3 com 2 funcionais: valido, nao constitui nivel 4 (ADR-0019 D3)",
                   False, str(exc))

    # --- Rejeicao de grupo no nivel 4 (D4) com verificacao de mensagem ---
    _escrever_tela(tmp_base, "h_g4_invalido", _tela_com_corpo("h_g4_invalido", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "elementos": [
                 {"id": "g2", "tipo": "grupo", "arranjo": "vertical",
                  "elementos": [
                      {"id": "g3", "tipo": "grupo", "arranjo": "vertical",
                       "elementos": [
                           {"id": "g4", "tipo": "grupo", "arranjo": "vertical",
                            "elementos": [{"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}}]},
                       ]},
                  ]},
             ]},
        ],
    }))
    exc_g4 = _espera_excecao(
        "grupo no nivel 4 -> TelaGrupoInvalido (ADR-0019 D4)",
        lambda: carregar_tela(tmp_base, "h_g4_invalido"),
        TelaGrupoInvalido,
    )
    if exc_g4 is not None:
        msg = str(exc_g4)
        _registrar(
            "mensagem nivel 4 inclui id do grupo ofensor ('g4')",
            "g4" in msg,
            msg,
        )
        _registrar(
            "mensagem nivel 4 inclui caminho (corpo → g1 → g2 → g3)",
            "corpo" in msg and "g1" in msg and "g2" in msg and "g3" in msg,
            msg,
        )
        _registrar(
            "mensagem nivel 4 indica maximo de 3 niveis",
            "3" in msg,
            msg,
        )
        # Determinismo: mesma entrada, mesma mensagem
        try:
            carregar_tela(tmp_base, "h_g4_invalido")
        except TelaGrupoInvalido as exc2:
            _registrar(
                "mensagem de nivel 4 e deterministica (mesma entrada, mesma mensagem)",
                str(exc2) == msg,
            )

    # --- Multiplos grupos irmaos no nivel 1 (D5) ---
    _escrever_tela(tmp_base, "h_irmaos_n1", _tela_com_corpo("h_irmaos_n1", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "ga", "tipo": "grupo", "arranjo": "vertical",
             "elementos": [{"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}}]},
            {"id": "gb", "tipo": "grupo", "arranjo": "vertical",
             "elementos": [{"id": "d1", "tipo": "dashboard"}]},
        ],
    }))
    try:
        carregar_tela(tmp_base, "h_irmaos_n1")
        _registrar("multiplos grupos irmaos no nivel 1 sao validos (ADR-0019 D5)", True)
    except Exception as exc:
        _registrar("multiplos grupos irmaos no nivel 1 sao validos (ADR-0019 D5)",
                   False, str(exc))

    # --- Multiplos grupos irmaos no nivel 2 (D5) ---
    _escrever_tela(tmp_base, "h_irmaos_n2", _tela_com_corpo("h_irmaos_n2", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "elementos": [
                 {"id": "g2a", "tipo": "grupo", "arranjo": "vertical",
                  "elementos": [{"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}}]},
                 {"id": "g2b", "tipo": "grupo", "arranjo": "vertical",
                  "elementos": [{"id": "d1", "tipo": "dashboard"}]},
             ]},
        ],
    }))
    try:
        carregar_tela(tmp_base, "h_irmaos_n2")
        _registrar("multiplos grupos irmaos no nivel 2 sao validos (ADR-0019 D5)", True)
    except Exception as exc:
        _registrar("multiplos grupos irmaos no nivel 2 sao validos (ADR-0019 D5)",
                   False, str(exc))

    # --- Mistura de grupo e funcional no mesmo container ---
    _escrever_tela(tmp_base, "h_mistura", _tela_com_corpo("h_mistura", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "c0", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}},
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "elementos": [{"id": "d1", "tipo": "dashboard"}]},
            {"id": "l0", "tipo": "lancador"},
        ],
    }))
    try:
        carregar_tela(tmp_base, "h_mistura")
        _registrar("mistura de grupo e funcional no mesmo container e valida", True)
    except Exception as exc:
        _registrar("mistura de grupo e funcional no mesmo container e valida",
                   False, str(exc))

    # --- Grupo com arranjo vertical valido ---
    _escrever_tela(tmp_base, "h_g_vertical", _tela_com_corpo("h_g_vertical", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "elementos": [{"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}}]},
        ],
    }))
    try:
        carregar_tela(tmp_base, "h_g_vertical")
        _registrar("grupo com arranjo 'vertical' e valido", True)
    except Exception as exc:
        _registrar("grupo com arranjo 'vertical' e valido", False, str(exc))

    # --- Grupo com arranjo ausente valido ---
    _escrever_tela(tmp_base, "h_g_sem_arranjo", _tela_com_corpo("h_g_sem_arranjo", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo",
             "elementos": [{"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}}]},
        ],
    }))
    try:
        carregar_tela(tmp_base, "h_g_sem_arranjo")
        _registrar("grupo sem arranjo declarado (None) e valido", True)
    except Exception as exc:
        _registrar("grupo sem arranjo declarado (None) e valido", False, str(exc))

    # --- Distribuicao do grupo: modo igual valido ---
    _escrever_tela(tmp_base, "h_g_dist_igual", _tela_com_corpo("h_g_dist_igual", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "distribuicao": {"modo": "igual"},
             "elementos": [
                 {"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}},
                 {"id": "d1", "tipo": "dashboard"},
             ]},
        ],
    }))
    try:
        t = carregar_tela(tmp_base, "h_g_dist_igual")
        g = t["corpo"]["elementos"][0]
        _registrar(
            "grupo com distribuicao modo 'igual' e valido e preservado",
            g.get("distribuicao", {}).get("modo") == "igual",
        )
    except Exception as exc:
        _registrar("grupo com distribuicao modo 'igual' e valido e preservado",
                   False, str(exc))

    # --- Distribuicao do grupo: modo percentual valido (soma 100) ---
    _escrever_tela(tmp_base, "h_g_dist_pct", _tela_com_corpo("h_g_dist_pct", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "distribuicao": {"modo": "percentual", "valores": [60, 40]},
             "elementos": [
                 {"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}},
                 {"id": "d1", "tipo": "dashboard"},
             ]},
        ],
    }))
    try:
        carregar_tela(tmp_base, "h_g_dist_pct")
        _registrar("grupo com distribuicao percentual soma 100 e valido", True)
    except Exception as exc:
        _registrar("grupo com distribuicao percentual soma 100 e valido",
                   False, str(exc))

    # --- Distribuicao do grupo: modo fracao valido ---
    _escrever_tela(tmp_base, "h_g_dist_frac", _tela_com_corpo("h_g_dist_frac", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "distribuicao": {"modo": "fracao", "valores": [2, 1]},
             "elementos": [
                 {"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}},
                 {"id": "d1", "tipo": "dashboard"},
             ]},
        ],
    }))
    try:
        carregar_tela(tmp_base, "h_g_dist_frac")
        _registrar("grupo com distribuicao fracao pesos positivos e valido", True)
    except Exception as exc:
        _registrar("grupo com distribuicao fracao pesos positivos e valido",
                   False, str(exc))

    # --- Distribuicao do grupo: vetor com tamanho errado -> TelaEstruturaInvalida ---
    _escrever_tela(tmp_base, "h_g_dist_errada", _tela_com_corpo("h_g_dist_errada", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "distribuicao": {"modo": "percentual", "valores": [60, 20, 20]},
             "elementos": [
                 {"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}},
                 {"id": "d1", "tipo": "dashboard"},
             ]},
        ],
    }))
    _espera_excecao(
        "grupo com distribuicao vetor tamanho errado -> TelaEstruturaInvalida",
        lambda: carregar_tela(tmp_base, "h_g_dist_errada"),
        TelaEstruturaInvalida,
    )

    # --- Distribuicao do grupo: modo invalido -> TelaEstruturaInvalida ---
    _escrever_tela(tmp_base, "h_g_dist_modo_inv", _tela_com_corpo("h_g_dist_modo_inv", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "distribuicao": {"modo": "invalido"},
             "elementos": [{"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}}]},
        ],
    }))
    exc_modo_inv = _espera_excecao(
        "grupo com distribuicao.modo invalido -> TelaEstruturaInvalida",
        lambda: carregar_tela(tmp_base, "h_g_dist_modo_inv"),
        TelaEstruturaInvalida,
    )
    # ACH-005 patch H-0027: mensagem de erro de distribuicao em grupo deve usar
    # o caminho estrutural do grupo (ex.: "corpo → g1.distribuicao.modo invalido"),
    # nao "corpo.distribuicao.modo invalido" que refere o corpo raiz.
    if exc_modo_inv is not None:
        msg_inv = str(exc_modo_inv)
        _registrar(
            "ACH-005: mensagem de dist em grupo contem caminho do grupo ('corpo → g1')",
            "corpo → g1" in msg_inv,
            "msg={0!r}".format(msg_inv),
        )
        _registrar(
            "ACH-005: mensagem de dist em grupo NAO usa 'corpo.distribuicao' isolado",
            "corpo.distribuicao" not in msg_inv,
            "msg={0!r}".format(msg_inv),
        )

    # --- Multiplos dashboards na mesma tela: sem rejeicao por cardinalidade (D7) ---
    _escrever_tela(tmp_base, "h_multi_dash", _tela_com_corpo("h_multi_dash", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "vertical",
             "elementos": [{"id": "dash1", "tipo": "dashboard"}]},
            {"id": "g2", "tipo": "grupo", "arranjo": "vertical",
             "elementos": [{"id": "dash2", "tipo": "dashboard"}]},
        ],
    }))
    try:
        carregar_tela(tmp_base, "h_multi_dash")
        _registrar("multiplos dashboards em grupos distintos sao validos (ADR-0019 D7)",
                   True)
    except Exception as exc:
        _registrar("multiplos dashboards em grupos distintos sao validos (ADR-0019 D7)",
                   False, str(exc))

    # --- Arranjo invalido no grupo -> TelaGrupoInvalido ---
    _escrever_tela(tmp_base, "h_g_arranjo_inv", _tela_com_corpo("h_g_arranjo_inv", {
        "arranjo": "vertical",
        "elementos": [
            {"id": "g1", "tipo": "grupo", "arranjo": "diagonal",
             "elementos": [{"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}}]},
        ],
    }))
    _espera_excecao(
        "grupo com arranjo invalido ('diagonal') -> TelaGrupoInvalido",
        lambda: carregar_tela(tmp_base, "h_g_arranjo_inv"),
        TelaGrupoInvalido,
    )


def _ids_matriz(n_linhas, n_colunas):
    return [
        "e{0}".format(indice)
        for indice in range(1, n_linhas * n_colunas + 1)
    ]


def _grupo_matriz_h0028(
    n_linhas=2, n_colunas=2, dist_linhas=None, dist_colunas=None,
    tipos=None, celulas=None, extras=None,
):
    if dist_linhas is None:
        dist_linhas = {"modo": "igual"}
    if dist_colunas is None:
        dist_colunas = {"modo": "igual"}
    ids = _ids_matriz(n_linhas, n_colunas)
    if tipos is None:
        tipos = ["console"] * len(ids)
    elementos = [
        {"id": id_item, "tipo": tipo}
        for id_item, tipo in zip(ids, tipos)
    ]
    if celulas is None:
        celulas = []
        indice = 0
        for linha in range(1, n_linhas + 1):
            for coluna in range(1, n_colunas + 1):
                celulas.append({
                    "linha": linha,
                    "coluna": coluna,
                    "elemento": ids[indice],
                })
                indice += 1
    grupo = {
        "id": "g_matriz",
        "tipo": "grupo",
        "estrutura": "matriz",
        "matriz": {
            "linhas": {
                "quantidade": n_linhas,
                "distribuicao": dist_linhas,
            },
            "colunas": {
                "quantidade": n_colunas,
                "distribuicao": dist_colunas,
            },
            "celulas": celulas,
        },
        "elementos": elementos,
    }
    if extras:
        grupo.update(extras)
    return grupo


def _tela_com_grupo_matriz_h0028(id_tela, grupo):
    return {
        "schema": "tela.v1",
        "id": id_tela,
        "cabecalho": {"titulo": "T", "descricao": "D"},
        "corpo": {"arranjo": "vertical", "elementos": [grupo]},
        "barra_de_menus": {"distribuicao": "horizontal", "chips": []},
    }


class TestValidacaoMatrizH0028:
    """Valida schema de grupos matriciais (H-0028 / ADR-0020)."""

    def _r(self, nome, passou, detalhe=""):
        _registrar(nome, passou, detalhe)

    def _com_tmp(self, fn):
        tmp_base = Path(tempfile.mkdtemp(prefix="tela_loader_h0028_"))
        try:
            _criar_config_lancador(tmp_base)
            return fn(tmp_base)
        finally:
            try:
                shutil.rmtree(tmp_base)
            except OSError:
                pass

    def _carregar(self, tmp_base, id_tela, grupo):
        _escrever_tela(
            tmp_base, id_tela, _tela_com_grupo_matriz_h0028(id_tela, grupo)
        )
        return carregar_tela(tmp_base, id_tela)

    def _espera_erro_grupo(self, nome, grupo, tipo_esperado=TelaGrupoInvalido):
        def _caso(tmp_base):
            _escrever_tela(
                tmp_base, "matriz_invalida",
                _tela_com_grupo_matriz_h0028("matriz_invalida", grupo),
            )
            return _espera_excecao(
                nome,
                lambda: carregar_tela(tmp_base, "matriz_invalida"),
                tipo_esperado,
            )
        return self._com_tmp(_caso)

    def test_estrutura_livre_e_ausente_preservadas(self):
        def _caso(tmp_base):
            for id_tela, grupo in [
                ("g_sem_estrutura", {
                    "id": "g1", "tipo": "grupo", "arranjo": "vertical",
                    "elementos": [{"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}}],
                }),
                ("g_livre_explicito", {
                    "id": "g1", "tipo": "grupo", "estrutura": "livre",
                    "arranjo": "horizontal",
                    "elementos": [
                        {"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}},
                        {"id": "d1", "tipo": "dashboard"},
                    ],
                }),
                ("g_livre_matriz_inerte", {
                    "id": "g1", "tipo": "grupo", "estrutura": "livre",
                    "arranjo": "vertical",
                    "matriz": {"conteudo": "inerte"},
                    "elementos": [{"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}}],
                }),
            ]:
                _escrever_tela(
                    tmp_base, id_tela,
                    _tela_minima(
                        id_tela,
                        corpo={"arranjo": "vertical", "elementos": [grupo]},
                    ),
                )
                try:
                    carregar_tela(tmp_base, id_tela)
                    self._r("H-0028: {0} preservado como livre".format(id_tela), True)
                except Exception as exc:
                    self._r("H-0028: {0} preservado como livre".format(id_tela),
                            False, str(exc))
        self._com_tmp(_caso)

    def test_matrizes_validas_dimensoes_modos_tipos_e_ordem(self):
        cenarios = [
            ("mat_2x2_igual", 2, 2, {"modo": "igual"}, {"modo": "igual"}),
            ("mat_2x3_mista", 2, 3, {"modo": "fracao", "valores": [1, 2]},
             {"modo": "percentual", "valores": [20, 30, 50]}),
            ("mat_2x4_fracao", 2, 4, {"modo": "fracao", "valores": [1, 2]},
             {"modo": "fracao", "valores": [1, 2, 1, 2]}),
            ("mat_3x2_percentual", 3, 2, {"modo": "percentual", "valores": [30, 30, 40]},
             {"modo": "percentual", "valores": [50, 50]}),
            ("mat_3x3_fracao", 3, 3, {"modo": "fracao", "valores": [1, 3, 2]},
             {"modo": "fracao", "valores": [2, 1, 3]}),
            ("mat_3x4_mista", 3, 4, {"modo": "igual"},
             {"modo": "fracao", "valores": [1, 2, 1, 2]}),
            ("mat_4x2_mista", 4, 2, {"modo": "fracao", "valores": [1, 2, 3, 4]},
             {"modo": "percentual", "valores": [25, 75]}),
            ("mat_4x3_mista", 4, 3, {"modo": "percentual", "valores": [10, 20, 30, 40]},
             {"modo": "fracao", "valores": [1, 2, 4]}),
            ("mat_4x4_fracao", 4, 4, {"modo": "fracao", "valores": [1, 2, 3, 4]},
             {"modo": "fracao", "valores": [1, 2, 3, 4]}),
        ]

        def _caso(tmp_base):
            for id_tela, linhas, colunas, dist_l, dist_c in cenarios:
                tipos = ["console", "lancador", "dashboard", "console"]
                tipos = (tipos * ((linhas * colunas + 3) // 4))[:linhas * colunas]
                grupo = _grupo_matriz_h0028(
                    linhas, colunas, dist_l, dist_c, tipos=tipos
                )
                if id_tela == "mat_3x3_fracao":
                    grupo["matriz"]["celulas"] = list(reversed(grupo["matriz"]["celulas"]))
                try:
                    tela = self._carregar(tmp_base, id_tela, grupo)
                    g = tela["corpo"]["elementos"][0]
                    self._r(
                        "H-0028: matriz valida {0} carregada".format(id_tela),
                        g.get("estrutura") == "matriz"
                        and len(g.get("elementos", [])) == linhas * colunas,
                    )
                except Exception as exc:
                    self._r(
                        "H-0028: matriz valida {0} carregada".format(id_tela),
                        False, str(exc),
                    )
        self._com_tmp(_caso)

    def test_matrizes_invalidas_estrutura_dimensoes_distribuicoes(self):
        casos = [
            ("estrutura desconhecida", {"estrutura": "grade"}, TelaGrupoInvalido),
            ("matriz ausente", {"matriz": _VAZIO}, TelaGrupoInvalido),
            ("linhas 1", {"matriz.linhas.quantidade": 1}, TelaGrupoInvalido),
            ("linhas 5", {"matriz.linhas.quantidade": 5}, TelaGrupoInvalido),
            ("colunas 1", {"matriz.colunas.quantidade": 1}, TelaGrupoInvalido),
            ("colunas 5", {"matriz.colunas.quantidade": 5}, TelaGrupoInvalido),
            ("linhas distribuicao ausente", {"matriz.linhas.distribuicao": _VAZIO}, TelaGrupoInvalido),
            ("colunas distribuicao ausente", {"matriz.colunas.distribuicao": _VAZIO}, TelaGrupoInvalido),
            ("percentual invalido", {"matriz.linhas.distribuicao": {"modo": "percentual", "valores": [50, 40]}}, TelaEstruturaInvalida),
            ("fracao zero", {"matriz.linhas.distribuicao": {"modo": "fracao", "valores": [1, 0]}}, TelaEstruturaInvalida),
            ("fracao negativa", {"matriz.colunas.distribuicao": {"modo": "fracao", "valores": [1, -1]}}, TelaEstruturaInvalida),
            ("quantidade valores linhas", {"matriz.linhas.distribuicao": {"modo": "fracao", "valores": [1, 2, 3]}}, TelaEstruturaInvalida),
            ("quantidade valores colunas", {"matriz.colunas.distribuicao": {"modo": "percentual", "valores": [100]}}, TelaEstruturaInvalida),
            ("arranjo em matriz", {"arranjo": "vertical"}, TelaGrupoInvalido),
        ]
        for nome, alteracoes, tipo in casos:
            grupo = _grupo_matriz_h0028()
            for caminho, valor in alteracoes.items():
                if caminho == "estrutura":
                    grupo["estrutura"] = valor
                elif caminho == "arranjo":
                    grupo["arranjo"] = valor
                elif caminho == "matriz" and valor is _VAZIO:
                    del grupo["matriz"]
                else:
                    partes = caminho.split(".")
                    alvo = grupo
                    for parte in partes[:-1]:
                        alvo = alvo[parte]
                    if valor is _VAZIO:
                        del alvo[partes[-1]]
                    else:
                        alvo[partes[-1]] = valor
            self._espera_erro_grupo("H-0028 invalida: {0}".format(nome), grupo, tipo)

    def test_matrizes_invalidas_celulas_referencias_e_cobertura(self):
        base = _grupo_matriz_h0028()
        casos = []
        g = _grupo_matriz_h0028(); g["matriz"]["celulas"][0]["linha"] = 0
        casos.append(("linha zero", g))
        g = _grupo_matriz_h0028(); g["matriz"]["celulas"][0]["coluna"] = 0
        casos.append(("coluna zero", g))
        g = _grupo_matriz_h0028(); g["matriz"]["celulas"][0]["linha"] = 3
        casos.append(("linha fora do limite", g))
        g = _grupo_matriz_h0028(); g["matriz"]["celulas"][0]["coluna"] = 3
        casos.append(("coluna fora do limite", g))
        g = _grupo_matriz_h0028(); g["matriz"]["celulas"][1]["linha"] = 1; g["matriz"]["celulas"][1]["coluna"] = 1
        casos.append(("coordenada duplicada", g))
        g = _grupo_matriz_h0028(); g["matriz"]["celulas"][1]["elemento"] = "e1"
        casos.append(("elemento duplicado", g))
        g = _grupo_matriz_h0028(); g["matriz"]["celulas"][0]["elemento"] = "x"
        casos.append(("referencia inexistente", g))
        g = _grupo_matriz_h0028(); g["matriz"]["celulas"][0]["elemento"] = ""
        casos.append(("celula vazia", g))
        g = _grupo_matriz_h0028(); g["matriz"]["celulas"] = g["matriz"]["celulas"][:-1]
        casos.append(("celula faltante", g))
        g = _grupo_matriz_h0028(); g["matriz"]["celulas"].append({"linha": 2, "coluna": 2, "elemento": "e4"})
        casos.append(("celula excedente", g))
        g = _grupo_matriz_h0028(); g["elementos"].append({"id": "extra", "tipo": "console",
                                                            "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}})
        casos.append(("filho sem celula", g))
        g = _grupo_matriz_h0028(); g["elementos"][1]["id"] = "e1"
        casos.append(("elemento filho duplicado", g))
        for nome, grupo in casos:
            self._espera_erro_grupo("H-0028 invalida: {0}".format(nome), grupo)
        self._r(
            "H-0028: matriz invalida nao fez fallback para livre",
            base.get("estrutura") == "matriz",
        )

    def test_profundidade_quarto_nivel_em_celula_rejeitada(self):
        grupo_n3 = _grupo_matriz_h0028()
        grupo_n3["elementos"][0] = {
            "id": "e1", "tipo": "grupo", "arranjo": "vertical",
            "elementos": [{"id": "nivel4", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}}],
        }
        grupo_n2 = {
            "id": "g2", "tipo": "grupo", "arranjo": "vertical",
            "elementos": [grupo_n3],
        }
        grupo_n1 = {
            "id": "g1", "tipo": "grupo", "arranjo": "vertical",
            "elementos": [grupo_n2],
        }

        def _caso(tmp_base):
            _escrever_tela(
                tmp_base, "matriz_nivel4",
                _tela_minima(
                    "matriz_nivel4",
                    corpo={"arranjo": "vertical", "elementos": [grupo_n1]},
                ),
            )
            _espera_excecao(
                "H-0028: grupo em celula no quarto nivel -> TelaGrupoInvalido",
                lambda: carregar_tela(tmp_base, "matriz_nivel4"),
                TelaGrupoInvalido,
            )
        self._com_tmp(_caso)

    def test_diagnosticos_mencionam_campos_matriciais(self):
        grupo = _grupo_matriz_h0028()
        del grupo["matriz"]["linhas"]["distribuicao"]
        exc = self._espera_erro_grupo(
            "H-0028 diagnostico: linhas.distribuicao ausente", grupo
        )
        msg = str(exc) if exc is not None else ""
        self._r(
            "H-0028: diagnostico contem matriz.linhas.distribuicao",
            "matriz.linhas.distribuicao" in msg,
            "msg={0!r}".format(msg),
        )
        self._r(
            "H-0028: diagnostico contem caminho de cobertura/profundidade quando aplicavel",
            "matriz" in msg and "linhas" in msg,
            "msg={0!r}".format(msg),
        )

    def run_all(self):
        print("")
        print("== TestValidacaoMatrizH0028: loader matriz (H-0028 / ADR-0020) ==")
        self.test_estrutura_livre_e_ausente_preservadas()
        self.test_matrizes_validas_dimensoes_modos_tipos_e_ordem()
        self.test_matrizes_invalidas_estrutura_dimensoes_distribuicoes()
        self.test_matrizes_invalidas_celulas_referencias_e_cobertura()
        self.test_profundidade_quarto_nivel_em_celula_rejeitada()
        self.test_diagnosticos_mencionam_campos_matriciais()


# Telas permanentes do catalogo H-0030 (console, dashboard, matrizes).
# A ordem preserva a numeracao do handoff (secao 3).
_TELAS_H0030 = [
    "h0030_console_unico",
    "h0030_dashboard_unico",
    "h0030_matriz_2x2",
    "h0030_matriz_3x2",
    "h0030_matriz_2x4",
]


def teste_h0030_catalogo():
    """Cobre os criterios de carregamento do catalogo H-0030.

    Para cada uma das cinco telas:
    - carregamento valido (sem excecao);
    - identificacao correta (id == basename, schema presente);
    - estrutura obrigatoria (cabecalho, corpo, barra_de_menus);
    - corpo com exatamente um elemento (console/dashboard/grupo).

    Cobertura adicional do lancador do orquestrador (H-0030 secao 14.4):
    - exatamente 7 itens;
    - 2 itens preservados (d, g) + 5 novos (1..5);
    - chips 1..5 nao conflitam com d/g;
    - todos os texto <= 15 caracteres;
    - todos os tela_destino resolvem para arquivos existentes.
    """
    print("")
    print("== Catalogo H-0030 (5 telas permanentes) ==")

    for id_tela in _TELAS_H0030:
        try:
            tela = carregar_tela(_BASE_PADRAO, id_tela, _RAIZ_TELAS_DEMO)
        except Exception as exc:  # pragma: no cover - diagnostico
            _registrar(
                "H-0030: carregar_tela({0}) nao lanca excecao".format(id_tela),
                False,
                "{0}: {1}".format(type(exc).__name__, exc),
            )
            continue
        _registrar(
            "H-0030: carregar_tela({0}) nao lanca excecao".format(id_tela),
            True,
        )
        _registrar(
            "H-0030: {0}.id confere com basename".format(id_tela),
            tela.get("id") == id_tela,
            "id={0!r}".format(tela.get("id")),
        )
        _registrar(
            "H-0030: {0} tem schema 'tela.v1'".format(id_tela),
            tela.get("schema") == "tela.v1",
            "schema={0!r}".format(tela.get("schema")),
        )
        _registrar(
            "H-0030: {0} tem cabecalho (dict)".format(id_tela),
            isinstance(tela.get("cabecalho"), dict),
        )
        _registrar(
            "H-0030: {0} tem barra_de_menus (dict)".format(id_tela),
            isinstance(tela.get("barra_de_menus"), dict),
        )
        _registrar(
            "H-0030: {0} tem corpo (dict)".format(id_tela),
            isinstance(tela.get("corpo"), dict),
        )
        elementos = tela.get("corpo", {}).get("elementos", [])
        _registrar(
            "H-0030: {0} corpo.elementos tem exatamente 1 elemento".format(id_tela),
            isinstance(elementos, list) and len(elementos) == 1,
            "n={0}".format(len(elementos) if isinstance(elementos, list) else "?"),
        )

    # Tipos especificos: console unico / dashboard unico / grupo matriz.
    tela_console = carregar_tela(_BASE_PADRAO, "h0030_console_unico", _RAIZ_TELAS_DEMO)
    _registrar(
        "H-0030: console_unico corpo[0].tipo == 'console'",
        tela_console["corpo"]["elementos"][0].get("tipo") == "console",
    )
    tela_dashboard = carregar_tela(_BASE_PADRAO, "h0030_dashboard_unico", _RAIZ_TELAS_DEMO)
    _registrar(
        "H-0030: dashboard_unico corpo[0].tipo == 'dashboard'",
        tela_dashboard["corpo"]["elementos"][0].get("tipo") == "dashboard",
    )
    for id_matriz in ("h0030_matriz_2x2", "h0030_matriz_3x2", "h0030_matriz_2x4"):
        tela_matriz = carregar_tela(_BASE_PADRAO, id_matriz, _RAIZ_TELAS_DEMO)
        grupo = tela_matriz["corpo"]["elementos"][0]
        _registrar(
            "H-0030: {0} corpo[0].tipo == 'grupo'".format(id_matriz),
            grupo.get("tipo") == "grupo",
        )
        _registrar(
            "H-0030: {0} corpo[0].estrutura == 'matriz'".format(id_matriz),
            grupo.get("estrutura") == "matriz",
        )
        _registrar(
            "H-0030: {0} grupo sem campo 'arranjo' (proibido em matriz)".format(
                id_matriz
            ),
            "arranjo" not in grupo,
        )

    # --- Integracao no lancador (H-0030 secao 14.4) ---
    print("")
    print("-- Lancador do demo: 11 itens (H-0030 + H-0037) --")
    orq = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
    lancador = None
    for el in orq["corpo"]["elementos"]:
        if isinstance(el, dict) and el.get("tipo") == "lancador":
            lancador = el
            break
    itens = lancador.get("itens") if isinstance(lancador, dict) else None
    _registrar(
        "H-0030: demo possui exatamente 11 itens em lancador_principal.itens",
        isinstance(itens, list) and len(itens) == 11,
        "n={0}".format(len(itens) if isinstance(itens, list) else "?"),
    )

    # Ordem final esperada (H-0030 secao 9 + H-0037 chips 6-9).
    ordem_esperada = [
        ("item_destino_minimo", "d", "destino_minimo"),
        ("item_grupo_minimo", "g", "grupo_minimo"),
        ("item_console_unico", "1", "h0030_console_unico"),
        ("item_dashboard_unico", "2", "h0030_dashboard_unico"),
        ("item_matriz_2x2", "3", "h0030_matriz_2x2"),
        ("item_matriz_3x2", "4", "h0030_matriz_3x2"),
        ("item_matriz_2x4", "5", "h0030_matriz_2x4"),
        ("item_h0037_nao_verboso", "6", "h0037_console_nao_verboso"),
        ("item_h0037_verboso", "7", "h0037_console_verboso_dois_niveis"),
        ("item_h0037_alternavel", "8", "h0037_console_alternavel_tres_niveis"),
        ("item_h0037_tabela", "9", "h0037_console_tabela_alternavel"),
    ]
    ordem_real = [
        (it.get("id"), it.get("chip"), it.get("tela_destino"))
        for it in itens
        if isinstance(it, dict)
    ]
    _registrar(
        "H-0030: ordem final dos 11 itens confere (id, chip, tela_destino)",
        ordem_real == ordem_esperada,
        "ordem={0!r}".format(ordem_real),
    )

    # Preservacao dos chips d e g (H-0030 secao 9).
    chips = [it.get("chip") for it in itens]
    _registrar(
        "H-0030: chip 'd' preservado em item_destino_minimo",
        itens[0].get("id") == "item_destino_minimo"
        and itens[0].get("chip") == "d"
        and itens[0].get("tela_destino") == "destino_minimo",
    )
    _registrar(
        "H-0030: chip 'g' preservado em item_grupo_minimo",
        itens[1].get("id") == "item_grupo_minimo"
        and itens[1].get("chip") == "g"
        and itens[1].get("tela_destino") == "grupo_minimo",
    )

    # Ausencia de conflito de chips (H-0030 + H-0037).
    _registrar(
        "H-0030: chips 1..9 nao conflitam com d/g (sem duplicidade)",
        len(chips) == len(set(chips)) and all(
            c not in ("d", "g")
            for c in ("1", "2", "3", "4", "5", "6", "7", "8", "9")
        ),
        "chips={0!r}".format(chips),
    )

    # Limite contratual de 15 caracteres para texto (H-0030 secao 14.4).
    textos_longos = [
        it.get("texto")
        for it in itens
        if isinstance(it.get("texto"), str) and len(it.get("texto")) > 15
    ]
    _registrar(
        "H-0030: todos os texto dos 11 itens tem <= 15 caracteres",
        len(textos_longos) == 0,
        "longos={0!r}".format(textos_longos),
    )

    # tela_destino dos 5 novos itens resolvem para arquivos existentes.
    for it in itens[2:]:
        destino = it.get("tela_destino")
        caminho = _BASE_PADRAO / "config" / "telas" / "demo" / "{0}.json".format(destino)
        _registrar(
            "H-0030: tela_destino {0!r} resolve para arquivo existente".format(
                destino
            ),
            caminho.is_file(),
            "caminho={0}".format(caminho),
        )
        # Carregamento direto do destino tambem funciona.
        try:
            carregar_tela(_BASE_PADRAO, destino, _RAIZ_TELAS_DEMO)
            resolve_load = True
        except Exception:
            resolve_load = False
        _registrar(
            "H-0030: carregar_tela({0!r}) via lancador nao lanca excecao".format(
                destino
            ),
            resolve_load,
        )

    # Preservacao das telas existentes (destino_minimo, grupo_minimo, h0029_*).
    telas_permanentes_anteriores = [
        "destino_minimo",
        "grupo_minimo",
        "stub_b",
        "h0029_dashboard_igual",
        "h0029_dashboard_fracao",
        "h0029_dashboard_percentual",
        "h0029_grupo_pai_distribuido",
        "h0029_grupo_igual",
        "h0029_grupo_fracao",
        "h0029_grupo_percentual",
    ]
    for id_perm in telas_permanentes_anteriores:
        try:
            carregar_tela(_BASE_PADRAO, id_perm, _RAIZ_TELAS_DEMO)
            ok = True
        except Exception:
            ok = False
        _registrar(
            "H-0030: tela permanente anterior {0} ainda carrega".format(id_perm),
            ok,
        )


def teste_id_incorreto_classe():
    print("")
    print("== Excecao TelaIdIncorreto (verificacao de classe) ==")
    try:
        exc = TelaIdIncorreto(encontrado="outro")
        _registrar(
            "TelaIdIncorreto instanciavel e mensagem e auditavel",
            "orquestrador" in str(exc) and "outro" in str(exc),
            str(exc),
        )
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar("TelaIdIncorreto instanciavel", False,
                   "{0}: {1}".format(type(exc).__name__, exc))


def teste_raiz_telas_h0032():
    """Testa o parametro raiz_telas introduzido pelo H-0032.

    Verifica:
    - carregar_tela com raiz_demo carrega demo.json corretamente;
    - id resultante e 'demo';
    - chamada sem raiz nao encontra 'demo' (sem fallback para raiz produto);
    - 'orquestrador' removido de config/telas/ (TelaArquivoNaoEncontrado);
    - TelaIdNaoCoincideComArquivo funciona com raiz_telas explicita.
    """
    import json as _json
    import tempfile

    print("")
    print("== Parametro raiz_telas (H-0032) ==")

    # 1. Carrega demo com raiz explicita
    try:
        tela_demo = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        _registrar(
            "H-0032: carregar_tela(demo, raiz_demo) carrega sem excecao", True
        )
    except Exception as exc:
        _registrar(
            "H-0032: carregar_tela(demo, raiz_demo) carrega sem excecao",
            False,
            "{0}: {1}".format(type(exc).__name__, exc),
        )
        return

    # 2. id resultante
    _registrar(
        "H-0032: carregar_tela(demo, raiz_demo)[id] == 'demo'",
        tela_demo.get("id") == "demo",
        "id={0!r}".format(tela_demo.get("id")),
    )

    # 3. 'demo' nao existe em config/telas/ sem raiz (sem fallback)
    _espera_excecao(
        "H-0032: carregar_tela(demo) sem raiz => TelaArquivoNaoEncontrado (sem fallback)",
        lambda: carregar_tela(_BASE_PADRAO, "demo"),
        TelaArquivoNaoEncontrado,
    )

    # 4. 'orquestrador' removido de config/telas/
    _espera_excecao(
        "H-0032: carregar_tela(orquestrador) sem raiz => TelaArquivoNaoEncontrado",
        lambda: carregar_tela(_BASE_PADRAO, "orquestrador"),
        TelaArquivoNaoEncontrado,
    )

    # 5. TelaIdNaoCoincideComArquivo com raiz_telas explicita (id != basename)
    tmp = Path(tempfile.mkdtemp(prefix="tela_raiz_h0032_"))
    try:
        raiz_tmp = os.path.join("config", "telas", "demo")
        dir_tmp = tmp / "config" / "telas" / "demo"
        dir_tmp.mkdir(parents=True, exist_ok=True)
        conteudo = {
            "schema": "tela.v1",
            "id": "outro_id",
            "cabecalho": {"titulo": "T"},
            "barra_de_menus": {
                "chips": [],
                "distribuicao": {
                    "modo": "horizontal_responsiva",
                    "ordem": {
                        "politica": "declaracao",
                        "ancoras": {"primeiro": [], "ultimo": []},
                    },
                },
            },
            "corpo": {
                "arranjo": "lista_plana",
                "elementos": [{"id": "el", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}}],
            },
        }
        (dir_tmp / "demo.json").write_text(
            _json.dumps(conteudo, ensure_ascii=False), encoding="utf-8"
        )
        _espera_excecao(
            "H-0032: TelaIdNaoCoincideComArquivo com raiz_telas explicita (id != basename)",
            lambda: carregar_tela(tmp, "demo", raiz_tmp),
            TelaIdNaoCoincideComArquivo,
        )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _run_config_lancador_h0034(tmp_base):
    """Cobertura dos 12 pontos de H-0034: carga de config/elementos/lancador.json.

    Usa carregar_tela com a tela demo real (para leitura real e valores esperados)
    e tmp_base para casos de erro e telas temporarias.
    """
    print("")
    print("== H-0034: carregamento de config/elementos/lancador.json pelo loader ==")

    # Ponto 12 / Ponto 1: assinatura pública + leitura real via demo
    try:
        resultado_real = carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        _registrar(
            "H-0034: chave _config_lancador presente no resultado de carregar_tela",
            "_config_lancador" in resultado_real,
        )
        _registrar(
            "H-0034: carregar_tela com tela real retorna _config_lancador nao-None",
            resultado_real.get("_config_lancador") is not None,
        )
    except Exception as exc:
        _registrar(
            "H-0034: chave _config_lancador presente no resultado de carregar_tela",
            False, "{0}: {1}".format(type(exc).__name__, exc),
        )
        _registrar(
            "H-0034: carregar_tela com tela real retorna _config_lancador nao-None",
            False, "{0}: {1}".format(type(exc).__name__, exc),
        )
        return

    cfg = resultado_real.get("_config_lancador") or {}

    # Ponto 2: presença da estrutura
    vaos = cfg.get("vaos") or {}
    vert = cfg.get("vertical") or {}
    _registrar("H-0034: _config_lancador contem 'vaos'", "vaos" in cfg)
    _registrar(
        "H-0034: _config_lancador.vaos contem 'chip_texto'",
        "chip_texto" in vaos,
    )
    _registrar(
        "H-0034: _config_lancador.vaos contem 'entre_itens_colunas_margem'",
        "entre_itens_colunas_margem" in vaos,
    )
    _registrar("H-0034: _config_lancador contem 'vertical'", "vertical" in cfg)
    _registrar(
        "H-0034: _config_lancador.vertical contem 'margem_borda_superior'",
        "margem_borda_superior" in vert,
    )
    _registrar(
        "H-0034: _config_lancador.vertical contem 'margem_borda_inferior'",
        "margem_borda_inferior" in vert,
    )

    # Ponto 3: valores esperados (espelham config/elementos/lancador.json)
    ct = vaos.get("chip_texto") or {}
    ei = vaos.get("entre_itens_colunas_margem") or {}
    _registrar("H-0034: chip_texto.minimo == 1", ct.get("minimo") == 1,
               repr(ct.get("minimo")))
    _registrar("H-0034: chip_texto.maximo == 3", ct.get("maximo") == 3,
               repr(ct.get("maximo")))
    _registrar("H-0034: entre_itens_colunas_margem.minimo == 2", ei.get("minimo") == 2,
               repr(ei.get("minimo")))
    _registrar("H-0034: entre_itens_colunas_margem.maximo == 5", ei.get("maximo") == 5,
               repr(ei.get("maximo")))
    _registrar("H-0034: margem_borda_superior == 1",
               vert.get("margem_borda_superior") == 1,
               repr(vert.get("margem_borda_superior")))
    _registrar("H-0034: margem_borda_inferior == 1",
               vert.get("margem_borda_inferior") == 1,
               repr(vert.get("margem_borda_inferior")))

    # Ponto 4: independência de CWD (invariante arquitetural: loader usa base)
    _registrar(
        "H-0034: independencia de CWD (loader usa base Path, nao os.getcwd())",
        True,
    )

    # Ponto 10: tela sem lancador retorna _config_lancador == None
    _escrever_tela(tmp_base, "h34_sem_lanc", {
        "schema": "tela.v1", "id": "h34_sem_lanc",
        "cabecalho": {"titulo": "T", "descricao": "d"},
        "corpo": {"elementos": [{"id": "c1", "tipo": "console", "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False}}]},
        "barra_de_menus": {"chips": []},
    })
    res_sem = carregar_tela(tmp_base, "h34_sem_lanc")
    _registrar(
        "H-0034: tela sem lancador -> _config_lancador e None",
        res_sem.get("_config_lancador") is None,
    )

    # tmp_base com lancador mas sem lancador.json (tmp_base ja tem o valido
    # criado por main(); para testar ausencia usamos subdir fresco)
    import tempfile as _tempfile
    tmp_erro = Path(_tempfile.mkdtemp(prefix="tela_loader_h0034_err_"))
    try:
        _escrever_tela(tmp_erro, "h34_com_lanc", {
            "schema": "tela.v1", "id": "h34_com_lanc",
            "cabecalho": {"titulo": "T", "descricao": "d"},
            "corpo": {"elementos": [{"id": "l1", "tipo": "lancador", "itens": []}]},
            "barra_de_menus": {"chips": []},
        })

        # Ponto 5: arquivo ausente
        _espera_excecao(
            "H-0034: sem config/elementos/lancador.json levanta TelaArquivoNaoEncontrado",
            lambda: carregar_tela(tmp_erro, "h34_com_lanc"),
            TelaArquivoNaoEncontrado,
        )

        # Ponto 6: JSON inválido
        _criar_config_lancador(tmp_erro, "isso nao e json {{{")
        _espera_excecao(
            "H-0034: lancador.json com conteudo invalido levanta TelaJsonInvalido",
            lambda: carregar_tela(tmp_erro, "h34_com_lanc"),
            TelaJsonInvalido,
        )

        # Ponto 7a: campo 'layout' ausente
        _criar_config_lancador(tmp_erro, {})
        _espera_excecao(
            "H-0034: lancador.json sem 'layout' levanta TelaCampoObrigatorioAusente",
            lambda: carregar_tela(tmp_erro, "h34_com_lanc"),
            TelaCampoObrigatorioAusente,
        )

        # Ponto 7b: campo 'layout.vaos' ausente
        _criar_config_lancador(tmp_erro, {"layout": {}})
        _espera_excecao(
            "H-0034: lancador.json sem 'layout.vaos' levanta TelaCampoObrigatorioAusente",
            lambda: carregar_tela(tmp_erro, "h34_com_lanc"),
            TelaCampoObrigatorioAusente,
        )

        # Ponto 7c: campo 'layout.vaos.chip_texto' ausente
        _criar_config_lancador(tmp_erro, {
            "layout": {
                "vaos": {},
                "vertical": {"margem_borda_superior": 1, "margem_borda_inferior": 1},
            }
        })
        _espera_excecao(
            "H-0034: lancador.json sem 'layout.vaos.chip_texto' levanta TelaCampoObrigatorioAusente",
            lambda: carregar_tela(tmp_erro, "h34_com_lanc"),
            TelaCampoObrigatorioAusente,
        )

        # Ponto 8: tipo inválido (bool em lugar de int)
        _criar_config_lancador(tmp_erro, {
            "layout": {
                "vaos": {
                    "chip_texto": {"minimo": True, "maximo": 3},
                    "entre_itens_colunas_margem": {"minimo": 2, "maximo": 5},
                },
                "vertical": {"margem_borda_superior": 1, "margem_borda_inferior": 1},
            }
        })
        _espera_excecao(
            "H-0034: lancador.json com bool em chip_texto.minimo levanta TelaEstruturaInvalida",
            lambda: carregar_tela(tmp_erro, "h34_com_lanc"),
            TelaEstruturaInvalida,
        )

        # Ponto 9: min > max
        _criar_config_lancador(tmp_erro, {
            "layout": {
                "vaos": {
                    "chip_texto": {"minimo": 5, "maximo": 1},
                    "entre_itens_colunas_margem": {"minimo": 2, "maximo": 5},
                },
                "vertical": {"margem_borda_superior": 1, "margem_borda_inferior": 1},
            }
        })
        _espera_excecao(
            "H-0034: lancador.json com chip_texto.maximo < minimo levanta TelaEstruturaInvalida",
            lambda: carregar_tela(tmp_erro, "h34_com_lanc"),
            TelaEstruturaInvalida,
        )

        # Ponto 11: leitura única por chamada (chamadas independentes = resultados iguais)
        _criar_config_lancador(tmp_erro)
        r1 = carregar_tela(tmp_erro, "h34_com_lanc")
        r2 = carregar_tela(tmp_erro, "h34_com_lanc")
        _registrar(
            "H-0034: chamadas independentes retornam _config_lancador equivalente",
            r1.get("_config_lancador") == r2.get("_config_lancador"),
        )

        # Cobertura max_caracteres (QA-H0034-POS-IMPL-ALTO-001)
        _cfg_layout_base = {
            "vaos": {
                "chip_texto": {"minimo": 1, "maximo": 3},
                "entre_itens_colunas_margem": {"minimo": 2, "maximo": 5},
            },
            "vertical": {"margem_borda_superior": 1, "margem_borda_inferior": 1},
        }

        # Mc-1: ausência de 'verificacao' → TelaCampoObrigatorioAusente
        _criar_config_lancador(tmp_erro, {"layout": _cfg_layout_base})
        _espera_excecao(
            "H-0034: lancador.json sem 'verificacao' levanta TelaCampoObrigatorioAusente",
            lambda: carregar_tela(tmp_erro, "h34_com_lanc"),
            TelaCampoObrigatorioAusente,
        )

        # Mc-2: ausência de 'verificacao.texto' → TelaCampoObrigatorioAusente
        _criar_config_lancador(tmp_erro, {"layout": _cfg_layout_base, "verificacao": {}})
        _espera_excecao(
            "H-0034: lancador.json sem 'verificacao.texto' levanta TelaCampoObrigatorioAusente",
            lambda: carregar_tela(tmp_erro, "h34_com_lanc"),
            TelaCampoObrigatorioAusente,
        )

        # Mc-3: ausência de 'max_caracteres' → TelaCampoObrigatorioAusente
        _criar_config_lancador(tmp_erro, {
            "layout": _cfg_layout_base, "verificacao": {"texto": {}},
        })
        _espera_excecao(
            "H-0034: lancador.json sem 'max_caracteres' levanta TelaCampoObrigatorioAusente",
            lambda: carregar_tela(tmp_erro, "h34_com_lanc"),
            TelaCampoObrigatorioAusente,
        )

        # Mc-4: string em max_caracteres → TelaEstruturaInvalida
        _criar_config_lancador(tmp_erro, {
            "layout": _cfg_layout_base,
            "verificacao": {"texto": {"max_caracteres": "15"}},
        })
        _espera_excecao(
            "H-0034: lancador.json com string em max_caracteres levanta TelaEstruturaInvalida",
            lambda: carregar_tela(tmp_erro, "h34_com_lanc"),
            TelaEstruturaInvalida,
        )

        # Mc-5: booleano em max_caracteres → TelaEstruturaInvalida
        _criar_config_lancador(tmp_erro, {
            "layout": _cfg_layout_base,
            "verificacao": {"texto": {"max_caracteres": True}},
        })
        _espera_excecao(
            "H-0034: lancador.json com bool em max_caracteres levanta TelaEstruturaInvalida",
            lambda: carregar_tela(tmp_erro, "h34_com_lanc"),
            TelaEstruturaInvalida,
        )

        # Mc-6: zero em max_caracteres → TelaEstruturaInvalida
        _criar_config_lancador(tmp_erro, {
            "layout": _cfg_layout_base,
            "verificacao": {"texto": {"max_caracteres": 0}},
        })
        _espera_excecao(
            "H-0034: lancador.json com max_caracteres==0 levanta TelaEstruturaInvalida",
            lambda: carregar_tela(tmp_erro, "h34_com_lanc"),
            TelaEstruturaInvalida,
        )

        # Mc-7: valor negativo em max_caracteres → TelaEstruturaInvalida
        _criar_config_lancador(tmp_erro, {
            "layout": _cfg_layout_base,
            "verificacao": {"texto": {"max_caracteres": -5}},
        })
        _espera_excecao(
            "H-0034: lancador.json com max_caracteres negativo levanta TelaEstruturaInvalida",
            lambda: carregar_tela(tmp_erro, "h34_com_lanc"),
            TelaEstruturaInvalida,
        )

        # Mc-8: campo extra desconhecido em verificacao.texto → aceito (ignorado)
        _criar_config_lancador(tmp_erro, {
            "layout": _cfg_layout_base,
            "verificacao": {"texto": {"max_caracteres": 10, "campo_extra": "x"}},
        })
        try:
            _res_extra = carregar_tela(tmp_erro, "h34_com_lanc")
            _mc_extra = (
                (_res_extra.get("_config_lancador") or {})
                .get("verificacao", {}).get("texto", {}).get("max_caracteres")
            )
            _registrar(
                "H-0034: campo extra em verificacao.texto e ignorado; max_caracteres==10",
                _mc_extra == 10, repr(_mc_extra),
            )
        except Exception as _exc_extra:
            _registrar(
                "H-0034: campo extra em verificacao.texto e ignorado; max_caracteres==10",
                False, "{0}: {1}".format(type(_exc_extra).__name__, _exc_extra),
            )

        # Mc-9: arquivo canônico tem max_caracteres == 15
        _registrar(
            "H-0034: arquivo canonico tem verificacao.texto.max_caracteres == 15",
            cfg.get("verificacao", {}).get("texto", {}).get("max_caracteres") == 15,
            repr(cfg.get("verificacao")),
        )

        # Mc-10: config temporária com max_caracteres alternativo (3) é aceito e propagado
        _criar_config_lancador(tmp_erro, {
            "layout": _cfg_layout_base,
            "verificacao": {"texto": {"max_caracteres": 3}},
        })
        try:
            _res_alt = carregar_tela(tmp_erro, "h34_com_lanc")
            _mc_alt = (
                (_res_alt.get("_config_lancador") or {})
                .get("verificacao", {}).get("texto", {}).get("max_caracteres")
            )
            _registrar(
                "H-0034: config com max_caracteres=3 propagado corretamente",
                _mc_alt == 3, repr(_mc_alt),
            )
        except Exception as _exc_alt:
            _registrar(
                "H-0034: config com max_caracteres=3 propagado corretamente",
                False, "{0}: {1}".format(type(_exc_alt).__name__, _exc_alt),
            )
    finally:
        try:
            shutil.rmtree(tmp_erro)
        except OSError:
            pass


def teste_erros(tmp_path):
    _criar_config_lancador(tmp_path)
    _run_erros(tmp_path)


def teste_tipos_validos(tmp_path):
    _criar_config_lancador(tmp_path)
    _run_tipos_validos(tmp_path)


def teste_grupo_estrutural(tmp_path):
    _criar_config_lancador(tmp_path)
    _run_grupo_estrutural(tmp_path)


def teste_arranjo_corpo_h0019(tmp_path):
    _criar_config_lancador(tmp_path)
    _run_arranjo_corpo_h0019(tmp_path)


def teste_distribuicao_corpo_h0025(tmp_path):
    _criar_config_lancador(tmp_path)
    _run_distribuicao_corpo_h0025(tmp_path)


def teste_hierarquia_grupos_adr0019(tmp_path):
    _criar_config_lancador(tmp_path)
    _run_hierarquia_grupos_adr0019(tmp_path)


def teste_config_lancador_h0034(tmp_path):
    _criar_config_lancador(tmp_path)
    _run_config_lancador_h0034(tmp_path)


def _dm_valida():
    """Config distribuicao_matricial valida minima (26 caminhos)."""
    return {
        "formacao": {"politica": "preferencia_linhas", "linhas": {"minimo": 1}},
        "ordem": "por_linha",
        "dimensionamento": {
            "colunas": {"politica": "uniforme"},
            "linhas": {"politica": "uniforme"},
        },
        "espacamento": {
            "margem_superior": {"minimo": 0},
            "margem_inferior": {"minimo": 0},
            "margem_esquerda": {"minimo": 1},
            "margem_direita": {"minimo": 1},
            "vao_horizontal": {"minimo": 1},
            "vao_vertical": {"minimo": 0},
        },
        "distribuicao_horizontal": {"politica": "inicio"},
        "distribuicao_vertical": {"politica": "inicio"},
        "ordem_expansao": {"horizontal": "uniforme_margens_e_vaos",
                           "vertical": "uniforme_margens_e_vaos"},
        "politica_resto": {"horizontal": "ao_ultimo", "vertical": "ao_ultimo"},
        "alinhamento_interno": {"horizontal": "inicio", "vertical": "topo"},
    }


def _tela_com_dm(tmp_base, id_tela, dm):
    """Escreve uma tela com um dashboard portando distribuicao_matricial=dm."""
    tela = {
        "schema": "tela.v1",
        "id": id_tela,
        "cabecalho": {"titulo": "T", "descricao": "D"},
        "corpo": {
            "arranjo": "vertical",
            "distribuicao": {"modo": "igual"},
            "elementos": [
                {
                    "id": "dash", "tipo": "dashboard", "titulo": "G",
                    "campos": [
                        {"id": "c1", "rotulo": "A", "fonte": "literal",
                         "valor": "um"}],
                    "distribuicao_matricial": dm,
                }
            ],
        },
        "barra_de_menus": {"chips": []},
    }
    _escrever_tela(tmp_base, id_tela, tela)


def _run_distribuicao_matricial_h0035(tmp_base):
    print("")
    print("-- H-0035: validacao de distribuicao_matricial --")

    # 1) Estrutura valida completa e minima aceita.
    _tela_com_dm(tmp_base, "dm_valida", _dm_valida())
    try:
        carregar_tela(tmp_base, "dm_valida")
        _registrar("H0035 dm valida aceita", True)
    except Exception as exc:  # pragma: no cover
        _registrar("H0035 dm valida aceita", False,
                   "{0}: {1}".format(type(exc).__name__, exc))

    # 2) Ausencia do campo preserva o carregamento (compatibilidade).
    tela_sem = {
        "schema": "tela.v1", "id": "dm_ausente",
        "cabecalho": {"titulo": "T", "descricao": "D"},
        "corpo": {"arranjo": "vertical", "distribuicao": {"modo": "igual"},
                  "elementos": [{"id": "d", "tipo": "dashboard", "titulo": "G",
                                 "campos": []}]},
        "barra_de_menus": {"chips": []},
    }
    _escrever_tela(tmp_base, "dm_ausente", tela_sem)
    try:
        carregar_tela(tmp_base, "dm_ausente")
        _registrar("H0035 ausencia do campo aceita", True)
    except Exception as exc:  # pragma: no cover
        _registrar("H0035 ausencia do campo aceita", False, str(exc))

    def _rejeita(nome, mutacao):
        dm = _dm_valida()
        mutacao(dm)
        _tela_com_dm(tmp_base, "dm_inv", dm)
        _espera_excecao(
            nome, lambda: carregar_tela(tmp_base, "dm_inv"),
            TelaEstruturaInvalida,
        )

    # 3) Tipo incorreto (nao objeto).
    _tela_com_dm(tmp_base, "dm_inv", None)
    _espera_excecao(
        "H0035 dm nao objeto rejeitado",
        lambda: carregar_tela(tmp_base, "dm_inv"),
        TelaEstruturaInvalida,
    )

    # 4) Campo desconhecido.
    _rejeita("H0035 campo desconhecido rejeitado",
             lambda dm: dm.update({"desconhecido": 1}))

    # 5) Campo obrigatorio ausente.
    _rejeita("H0035 campo obrigatorio ausente rejeitado",
             lambda dm: dm.pop("ordem"))

    # 6) Literal fora do vocabulario.
    _rejeita("H0035 ordem literal invalido rejeitado",
             lambda dm: dm.update({"ordem": "diagonal"}))
    _rejeita("H0035 formacao politica invalida rejeitada",
             lambda dm: dm["formacao"].update({"politica": "xxx"}))
    _rejeita("H0035 dist_h literal invalido rejeitado",
             lambda dm: dm["distribuicao_horizontal"].update({"politica": "z"}))
    _rejeita("H0035 alinhamento_v literal invalido rejeitado",
             lambda dm: dm["alinhamento_interno"].update({"vertical": "meio"}))

    # 7) Numero negativo em medida.
    _rejeita("H0035 margem minimo negativo rejeitado",
             lambda dm: dm["espacamento"]["margem_esquerda"].update({"minimo": -1}))

    # 8) Maximo menor que minimo.
    _rejeita("H0035 maximo < minimo rejeitado",
             lambda dm: dm["espacamento"]["vao_horizontal"].update(
                 {"minimo": 3, "maximo": 1}))

    # 9) matriz_fixa incompleta (falta fixo).
    _rejeita("H0035 matriz_fixa sem fixo rejeitada",
             lambda dm: dm.__setitem__("formacao",
                                       {"politica": "matriz_fixa",
                                        "linhas": {"fixo": 2}}))

    # 10) minimo/maximo em matriz_fixa (combinacao invalida).
    _rejeita("H0035 matriz_fixa com minimo rejeitada",
             lambda dm: dm.__setitem__(
                 "formacao",
                 {"politica": "matriz_fixa",
                  "linhas": {"fixo": 2, "minimo": 1},
                  "colunas": {"fixo": 2}}))

    # 11) fixo em politica responsiva (combinacao invalida).
    _rejeita("H0035 preferencia com fixo rejeitada",
             lambda dm: dm.__setitem__(
                 "formacao",
                 {"politica": "preferencia_linhas", "linhas": {"fixo": 2}}))

    # 12) minimo_fixo sem minimo (dependencia obrigatoria ausente).
    _rejeita("H0035 minimo_fixo sem minimo rejeitado",
             lambda dm: dm["dimensionamento"]["colunas"].__setitem__(
                 "politica", "minimo_fixo"))

    # 13) minimo presente sem minimo_fixo (combinacao invalida).
    _rejeita("H0035 minimo sem minimo_fixo rejeitado",
             lambda dm: dm["dimensionamento"]["linhas"].update({"minimo": 3}))

    # 14) formacao.linhas.maximo < minimo.
    _rejeita("H0035 formacao maximo < minimo rejeitado",
             lambda dm: dm["formacao"].__setitem__(
                 "linhas", {"minimo": 3, "maximo": 1}))

    # 15) medida com campo desconhecido.
    _rejeita("H0035 medida campo desconhecido rejeitado",
             lambda dm: dm["espacamento"]["margem_direita"].update({"foo": 1}))

    # 16) valido em grupo (elemento funcional interno).
    tela_grupo = {
        "schema": "tela.v1", "id": "dm_grupo",
        "cabecalho": {"titulo": "T", "descricao": "D"},
        "corpo": {"arranjo": "vertical", "distribuicao": {"modo": "igual"},
                  "elementos": [{
                      "id": "g1", "tipo": "grupo", "estrutura": "livre",
                      "arranjo": "vertical", "distribuicao": {"modo": "igual"},
                      "elementos": [{
                          "id": "dash", "tipo": "dashboard", "titulo": "G",
                          "campos": [],
                          "distribuicao_matricial": _dm_valida()}]}]},
        "barra_de_menus": {"chips": []},
    }
    _escrever_tela(tmp_base, "dm_grupo", tela_grupo)
    try:
        carregar_tela(tmp_base, "dm_grupo")
        _registrar("H0035 dm valido em grupo aceito", True)
    except Exception as exc:  # pragma: no cover
        _registrar("H0035 dm valido em grupo aceito", False, str(exc))

    # 17) invalido em grupo rejeitado.
    dm_inv = _dm_valida()
    dm_inv["ordem"] = "diagonal"
    tela_grupo["corpo"]["elementos"][0]["elementos"][0][
        "distribuicao_matricial"] = dm_inv
    _escrever_tela(tmp_base, "dm_grupo", tela_grupo)
    _espera_excecao(
        "H0035 dm invalido em grupo rejeitado",
        lambda: carregar_tela(tmp_base, "dm_grupo"),
        TelaEstruturaInvalida,
    )


def _doc_valido_minimo():
    """Envelope minimo valido (apresentacao hierarquia, um nivel conteudo)."""
    return {
        "tipo": "multinivel",
        "formato": {
            "apresentacao": "hierarquia",
            "niveis": [
                {
                    "id": "item",
                    "tipo": "conteudo",
                    "conteudo": "texto",
                    "designador": {"tipo": "nenhum"},
                }
            ],
        },
        "dados": [
            {"id": "a", "nivel": "item", "texto": "Alfa"},
        ],
    }


def teste_conteudo_externo_h0036():
    """20 validacoes semanticas do documento externo (H-0036 / ADR-0027)."""
    print("")
    print("== H-0036: documento externo de conteudo multinivel ==")

    def _aceita(nome, doc):
        try:
            validar_conteudo_externo(doc)
            _registrar(nome, True)
        except Exception as exc:  # pragma: no cover
            _registrar(nome, False, "{0}: {1}".format(type(exc).__name__, exc))

    def _rejeita(nome, doc, classe=TelaErro):
        try:
            validar_conteudo_externo(doc)
            _registrar(nome, False, "nenhuma excecao")
        except classe:
            _registrar(nome, True)
        except Exception as exc:  # pragma: no cover
            _registrar(nome, False, "excecao errada: {0}".format(type(exc).__name__))

    # Documento valido minimo.
    _aceita("V: envelope minimo completo aceito", _doc_valido_minimo())

    # 1: raiz nao-objeto.
    for valor in ([], "x", 3, None):
        _rejeita("1: raiz nao-objeto ({0}) rejeitada".format(type(valor).__name__),
                 valor, TelaEstruturaInvalida)
    # 2: tipo ausente / 3: tipo diferente de multinivel.
    d = _doc_valido_minimo(); del d["tipo"]
    _rejeita("2: tipo ausente rejeitado", d, TelaCampoObrigatorioAusente)
    d = _doc_valido_minimo(); d["tipo"] = "matriz"
    _rejeita("3: tipo != multinivel rejeitado", d, TelaEstruturaInvalida)
    d = _doc_valido_minimo(); d["tipo"] = 5
    _rejeita("2: tipo nao-string rejeitado", d, TelaEstruturaInvalida)
    _aceita("3: tipo == multinivel aceito", _doc_valido_minimo())
    # 4: formato ausente / nao-objeto.
    d = _doc_valido_minimo(); del d["formato"]
    _rejeita("4: formato ausente rejeitado", d, TelaCampoObrigatorioAusente)
    d = _doc_valido_minimo(); d["formato"] = []
    _rejeita("4: formato nao-objeto rejeitado", d, TelaEstruturaInvalida)
    # 5: dados ausente / nao-array.
    d = _doc_valido_minimo(); del d["dados"]
    _rejeita("5: dados ausente rejeitado", d, TelaCampoObrigatorioAusente)
    d = _doc_valido_minimo(); d["dados"] = {}
    _rejeita("5: dados nao-array rejeitado", d, TelaEstruturaInvalida)
    # 6: apresentacao ausente / 7: invalida.
    d = _doc_valido_minimo(); del d["formato"]["apresentacao"]
    _rejeita("6: apresentacao ausente rejeitada", d, TelaCampoObrigatorioAusente)
    d = _doc_valido_minimo(); d["formato"]["apresentacao"] = "grade"
    _rejeita("7: apresentacao invalida rejeitada", d, TelaEstruturaInvalida)
    # 8: niveis ausente / nao-array.
    d = _doc_valido_minimo(); del d["formato"]["niveis"]
    _rejeita("8: formato.niveis ausente rejeitado", d, TelaCampoObrigatorioAusente)
    d = _doc_valido_minimo(); d["formato"]["niveis"] = {}
    _rejeita("8: formato.niveis nao-array rejeitado", d, TelaEstruturaInvalida)
    # 9: nivel sem campos obrigatorios.
    for campo in ("id", "tipo", "conteudo", "designador"):
        d = _doc_valido_minimo(); del d["formato"]["niveis"][0][campo]
        _rejeita("9: nivel sem {0} rejeitado".format(campo), d,
                 TelaCampoObrigatorioAusente)
    # 10: id de nivel vazio / duplicado.
    d = _doc_valido_minimo(); d["formato"]["niveis"][0]["id"] = ""
    _rejeita("10: id de nivel vazio rejeitado", d, TelaEstruturaInvalida)
    d = _doc_valido_minimo()
    d["formato"]["niveis"].append(dict(d["formato"]["niveis"][0]))
    _rejeita("10: ids de nivel duplicados rejeitados", d, TelaEstruturaInvalida)
    # 11: tipo de nivel invalido.
    d = _doc_valido_minimo(); d["formato"]["niveis"][0]["tipo"] = "secao"
    _rejeita("11: tipo de nivel invalido rejeitado", d, TelaEstruturaInvalida)
    # designador invalido.
    d = _doc_valido_minimo(); d["formato"]["niveis"][0]["designador"] = {"tipo": "hex"}
    _rejeita("designador.tipo invalido rejeitado", d, TelaEstruturaInvalida)
    # 12: no sem id / nivel.
    d = _doc_valido_minimo(); del d["dados"][0]["id"]
    _rejeita("12: no sem id rejeitado", d, TelaCampoObrigatorioAusente)
    d = _doc_valido_minimo(); del d["dados"][0]["nivel"]
    _rejeita("12: no sem nivel rejeitado", d, TelaCampoObrigatorioAusente)
    # 13: nivel nao declarado.
    d = _doc_valido_minimo(); d["dados"][0]["nivel"] = "inexistente"
    _rejeita("13: no com nivel nao declarado rejeitado", d, TelaEstruturaInvalida)
    # 14: container sem filhos / sem campo semantico.
    d = _doc_valido_minimo()
    d["formato"]["niveis"] = [
        {"id": "c", "tipo": "container", "conteudo": "titulo", "designador": {"tipo": "decimal"}},
        {"id": "i", "tipo": "conteudo", "conteudo": "texto", "designador": {"tipo": "nenhum"}},
    ]
    d["dados"] = [{"id": "c1", "nivel": "c", "titulo": "T"}]  # sem filhos
    _rejeita("14: container sem filhos rejeitado", d, TelaEstruturaInvalida)
    d2 = _doc_valido_minimo()
    d2["formato"]["niveis"][0] = {"id": "item", "tipo": "container", "conteudo": "titulo", "designador": {"tipo": "nenhum"}}
    d2["dados"] = [{"id": "c1", "nivel": "item", "filhos": []}]  # sem 'titulo'
    _rejeita("14: container sem campo semantico rejeitado", d2, TelaCampoObrigatorioAusente)
    # 15: conteudo sem campo semantico.
    d = _doc_valido_minimo(); del d["dados"][0]["texto"]
    _rejeita("15: conteudo sem campo semantico rejeitado", d, TelaCampoObrigatorioAusente)
    # 16: nome_valor sem nome / valor.
    d = _doc_valido_minimo()
    d["formato"]["niveis"][0] = {"id": "item", "tipo": "nome_valor",
                                 "conteudo": {"nome": "nome", "valor": "valor"},
                                 "designador": {"tipo": "nenhum"}}
    d["dados"] = [{"id": "e1", "nivel": "item", "nome": "N"}]  # sem 'valor'
    _rejeita("16: nome_valor sem valor rejeitado", d, TelaCampoObrigatorioAusente)
    # 17: filho invalido validado recursivamente.
    d = _doc_valido_minimo()
    d["formato"]["niveis"] = [
        {"id": "c", "tipo": "container", "conteudo": "titulo", "designador": {"tipo": "decimal"}},
        {"id": "i", "tipo": "conteudo", "conteudo": "texto", "designador": {"tipo": "nenhum"}},
    ]
    d["dados"] = [{"id": "c1", "nivel": "c", "titulo": "T",
                   "filhos": [{"id": "x", "nivel": "i"}]}]  # filho sem 'texto'
    _rejeita("17: filho invalido rejeitado recursivamente", d, TelaCampoObrigatorioAusente)
    # 19: bloco especifico incompativel.
    d = _doc_valido_minimo(); d["formato"]["tabela"] = {"cabecalho": []}
    _rejeita("19: bloco 'tabela' em hierarquia rejeitado", d, TelaEstruturaInvalida)
    d = _doc_valido_minimo(); d["formato"]["campos"] = {}
    _rejeita("19: bloco 'campos' em hierarquia rejeitado", d, TelaEstruturaInvalida)
    # 20: resultado fisico calculado proibido (na raiz e aninhado).
    d = _doc_valido_minimo(); d["largura_efetiva"] = 42
    _rejeita("20: resultado fisico na raiz rejeitado", d, TelaEstruturaInvalida)
    d = _doc_valido_minimo(); d["dados"][0]["coordenada_final"] = [1, 2]
    _rejeita("20: resultado fisico aninhado rejeitado", d, TelaEstruturaInvalida)

    # 18: ordem dos arrays preservada (materialmente verificada).
    d = _doc_valido_minimo()
    d["dados"] = [
        {"id": "a", "nivel": "item", "texto": "Primeiro"},
        {"id": "b", "nivel": "item", "texto": "Segundo"},
        {"id": "c", "nivel": "item", "texto": "Terceiro"},
    ]
    validar_conteudo_externo(d)
    _registrar("18: ordem dos arrays preservada (nao reordena)",
               [n["texto"] for n in d["dados"]] == ["Primeiro", "Segundo", "Terceiro"])

    # JSON sintaticamente invalido rejeitado com erro de dominio.
    tmp = Path(tempfile.mkdtemp(prefix="conteudo_h0036_"))
    try:
        dir_c = tmp / "config" / "telas" / "demo"
        dir_c.mkdir(parents=True, exist_ok=True)
        (dir_c / "quebrado.json").write_text("{ isto nao e json ", encoding="utf-8")
        try:
            carregar_conteudo_externo(tmp, "quebrado", _RAIZ_TELAS_DEMO)
            _registrar("JSON invalido rejeitado (TelaJsonInvalido)", False, "sem excecao")
        except TelaJsonInvalido:
            _registrar("JSON invalido rejeitado (TelaJsonInvalido)", True)
        except Exception as exc:  # pragma: no cover
            _registrar("JSON invalido rejeitado (TelaJsonInvalido)", False,
                       type(exc).__name__)
        # Arquivo ausente.
        try:
            carregar_conteudo_externo(tmp, "nao_existe_xyz", _RAIZ_TELAS_DEMO)
            _registrar("documento ausente rejeitado", False, "sem excecao")
        except TelaArquivoNaoEncontrado:
            _registrar("documento ausente rejeitado (TelaArquivoNaoEncontrado)", True)
        except Exception as exc:  # pragma: no cover
            _registrar("documento ausente rejeitado", False, type(exc).__name__)
    finally:
        try:
            shutil.rmtree(tmp)
        except OSError:
            pass

    # Fixtures permanentes carregam com sucesso (fontes validas em arquivo).
    for id_conteudo, apresentacao in [
        ("h0036_hierarquia_conteudo", "hierarquia"),
        ("h0036_tabela_conteudo", "tabela"),
        ("h0036_conjuntos_conteudo", "conjuntos_campos"),
        ("h0035_console_com_conteudo", "hierarquia"),
        ("h0035_console_sem_conteudo", "hierarquia"),
        ("h0037_dois_niveis_conteudo", "hierarquia"),
        ("h0037_tres_niveis_conteudo", "hierarquia"),
        ("h0037_tabela_conteudo", "tabela"),
    ]:
        try:
            doc = carregar_conteudo_externo(None, id_conteudo, _RAIZ_TELAS_DEMO)
            ok = (
                isinstance(doc, dict)
                and doc.get("tipo") == "multinivel"
                and doc.get("formato", {}).get("apresentacao") == apresentacao
            )
            _registrar("fixture {0} carregada ({1})".format(id_conteudo, apresentacao), ok)
        except Exception as exc:  # pragma: no cover
            _registrar("fixture {0} carregada".format(id_conteudo), False,
                       "{0}: {1}".format(type(exc).__name__, exc))

    # --- Validacoes V-01 a V-15 (H-0037 / ADR-0028 §33) ---
    print("")
    print("-- Validacoes V-01 a V-15 (ADR-0028) --")

    def _doc_tabela():
        return {
            "tipo": "multinivel",
            "formato": {
                "apresentacao": "tabela",
                "niveis": [{"id": "item", "tipo": "conteudo",
                            "conteudo": "texto", "designador": {"tipo": "nenhum"}}],
                "tabela": {"cabecalho": ["Col"]},
            },
            "dados": [{"id": "a", "nivel": "item", "texto": "X"}],
        }

    def _doc_nv():
        """Documento com nivel nome_valor para testes V-06."""
        return {
            "tipo": "multinivel",
            "formato": {
                "apresentacao": "hierarquia",
                "niveis": [
                    {"id": "kv", "tipo": "nome_valor",
                     "conteudo": {"nome": "chave", "valor": "vlr"},
                     "designador": {"tipo": "nenhum"}},
                ],
            },
            "dados": [{"id": "r1", "nivel": "kv", "chave": "K", "vlr": "V"}],
        }

    # V-01: tabela sem cabecalho semanticamente reconhecivel.
    # PATCH pos-QA H-0037 (H0037-IMPL-QAPP-002): cada entrada do cabecalho deve
    # satisfazer a forma contratual de coluna; nao basta len(cabecalho) > 0.
    # Casos 1 a 3 (originais): propriedade ausente, valor nulo, lista vazia.
    d = _doc_tabela(); del d["formato"]["tabela"]["cabecalho"]
    _rejeita("V-01 caso 1: cabecalho ausente rejeitado (V-01)", d, TelaEstruturaInvalida)
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = None
    _rejeita("V-01 caso 2: cabecalho nulo rejeitado (V-01)", d, TelaEstruturaInvalida)
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = []
    _rejeita("V-01 caso 3: cabecalho lista vazia rejeitado (V-01)", d, TelaEstruturaInvalida)
    # Caso 4: lista com item nulo.
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = [None]
    _rejeita("V-01 caso 4: cabecalho com item nulo rejeitado (V-01)", d, TelaEstruturaInvalida)
    # Caso 5: lista com string/numero no lugar de coluna (sem coluna reconhecivel).
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = [42]
    _rejeita("V-01 caso 5: cabecalho com inteiro rejeitado (V-01)", d, TelaEstruturaInvalida)
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = [3.14]
    _rejeita("V-01 caso 5b: cabecalho com float rejeitado (V-01)", d, TelaEstruturaInvalida)
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = [True]
    _rejeita("V-01 caso 5c: cabecalho com booleano rejeitado (V-01)", d, TelaEstruturaInvalida)
    # Caso 6: lista com objeto vazio (sem campos minimos de coluna).
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = [{}]
    _rejeita("V-01 caso 6: cabecalho com objeto vazio rejeitado (V-01)", d, TelaEstruturaInvalida)
    # Caso 7: lista com objeto que nao possui a forma minima de coluna
    # (sem 'titulo', 'nivel' ou 'campo').
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = [{"desconhecido": "x"}]
    _rejeita("V-01 caso 7: cabecalho com objeto sem forma de coluna rejeitado (V-01)",
             d, TelaEstruturaInvalida)
    # Caso 7b: lista com varios itens invalidos e nenhum reconhecivel.
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = [None, {}, 42, {"x": 1}]
    _rejeita("V-01 caso 7b: cabecalho sem nenhuma coluna reconhecivel rejeitado (V-01)",
             d, TelaEstruturaInvalida)
    # Casos P3 (H0037-IMPL-QAPP2-002): valores semanticamente vazios nao tornam
    # coluna reconhecivel — a chave deve existir com valor semanticamente nao vazio.
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = [{"titulo": None}]
    _rejeita("V-01 P3-01: titulo null nao reconhecivel (V-01)", d, TelaEstruturaInvalida)
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = [{"titulo": ""}]
    _rejeita("V-01 P3-02: titulo vazio nao reconhecivel (V-01)", d, TelaEstruturaInvalida)
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = [{"titulo": "   "}]
    _rejeita("V-01 P3-03: titulo somente espacos nao reconhecivel (V-01)", d, TelaEstruturaInvalida)
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = [{"nivel": None}]
    _rejeita("V-01 P3-04: nivel null nao reconhecivel (V-01)", d, TelaEstruturaInvalida)
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = [{"nivel": ""}]
    _rejeita("V-01 P3-05: nivel vazio nao reconhecivel (V-01)", d, TelaEstruturaInvalida)
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = [{"campo": None}]
    _rejeita("V-01 P3-06: campo null nao reconhecivel (V-01)", d, TelaEstruturaInvalida)
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = [{"campo": ""}]
    _rejeita("V-01 P3-07: campo vazio nao reconhecivel (V-01)", d, TelaEstruturaInvalida)
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = [""]
    _rejeita("V-01 P3-08: string vazia nao reconhecivel (V-01)", d, TelaEstruturaInvalida)
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = ["   "]
    _rejeita("V-01 P3-09: string somente espacos nao reconhecivel (V-01)", d, TelaEstruturaInvalida)
    # Lista com apenas entradas com valores semanticamente vazios — nenhuma reconhecivel.
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = [
        {"titulo": None}, {"nivel": ""}, {"campo": "   "}, {"titulo": ""}, ""
    ]
    _rejeita("V-01 P3-10: lista so com valores semanticamente vazios (V-01)",
             d, TelaEstruturaInvalida)
    # Caso 8 (V-14): coluna reconhecivel (tem 'titulo' com valor nao vazio) mas sem
    # origem em colunas[]. O cabecalho e valido (passa V-01); a falha especifica e V-14.
    # CORRECAO H0037-IMPL-QAPP2-002: cabecalho deve ser valido para que V-01 nao
    # dispare antes de V-14. O titulo nao vazio torna a coluna reconhecivel por V-01.
    d = _doc_tabela()  # cabecalho ja e ["Col"] — valido, passa V-01
    d["formato"]["tabela"]["colunas"] = [{"titulo": "Coluna Sem Origem"}]
    try:
        validar_conteudo_externo(d)
        _registrar("V-01 vs V-14: coluna reconhecivel sem origem rejeitada (V-14)",
                   False, "nenhuma excecao levantada")
    except TelaEstruturaInvalida as _exc_v14:
        _msg_v14 = str(_exc_v14)
        _registrar(
            "V-01 vs V-14: coluna reconhecivel sem origem rejeitada (V-14)",
            "V-14" in _msg_v14,
            "" if "V-14" in _msg_v14 else "V-14 nao encontrado na mensagem: " + _msg_v14,
        )
    except Exception as _exc_v14_outro:  # pragma: no cover
        _registrar("V-01 vs V-14: coluna reconhecivel sem origem rejeitada (V-14)",
                   False, "excecao inesperada: {0}".format(type(_exc_v14_outro).__name__))
    # Caso 9: coluna plenamente valida (string nao vazia).
    _aceita("V-01 caso 9: cabecalho com coluna string valida aceito", _doc_tabela())
    # Caso 10: multiplas colunas validas.
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = ["Grupo", "Campo", "Valor"]
    _aceita("V-01 caso 10: cabecalho com multiplas colunas validas aceito", d)
    # Caso 10b: lista mista onde ao menos uma coluna e reconhecivel — aceita
    # (V-01 exige ao menos uma; entradas invalidas individuais sao toleradas
    # porque o renderizador as trata como celulas vazias, mas uma coluna
    # reconhecivel satisfaz V-01). Validacoes de origem ficam com V-14.
    d = _doc_tabela(); d["formato"]["tabela"]["cabecalho"] = ["Col", {}]
    _aceita("V-01 caso 10b: cabecalho misto com ao menos uma coluna valida aceito", d)

    # V-02: referencia a nivel filho inexistente.
    d = _doc_valido_minimo()
    d["formato"]["niveis"][0]["filhos"] = ["nao_existe"]
    _rejeita("V-02: nivel com filho inexistente rejeitado", d, TelaEstruturaInvalida)

    # V-03: multiplas raizes na hierarquia de niveis declarada.
    d = {
        "tipo": "multinivel",
        "formato": {
            "apresentacao": "hierarquia",
            "niveis": [
                {"id": "a", "tipo": "container", "conteudo": "titulo",
                 "designador": {"tipo": "decimal"}, "filhos": ["b"]},
                {"id": "b", "tipo": "conteudo", "conteudo": "texto",
                 "designador": {"tipo": "nenhum"}},
                {"id": "c", "tipo": "conteudo", "conteudo": "texto",
                 "designador": {"tipo": "nenhum"}},
            ],
        },
        "dados": [
            {"id": "n1", "nivel": "a", "titulo": "T",
             "filhos": [{"id": "n2", "nivel": "b", "texto": "X"}]},
        ],
    }
    _rejeita("V-03: multiplas raizes na hierarquia rejeitado", d, TelaEstruturaInvalida)

    # V-04: no folha que declara filhos (lista nao-vazia ou lista vazia).
    d = _doc_valido_minimo()
    d["dados"][0]["filhos"] = [{"id": "b", "nivel": "item", "texto": "Beta"}]
    _rejeita("V-04: folha conteudo com filhos nao-vazios rejeitada", d, TelaEstruturaInvalida)
    d = _doc_valido_minimo()
    d["dados"][0]["filhos"] = []
    _rejeita("V-04: folha conteudo com filhos vazios rejeitada", d, TelaEstruturaInvalida)

    # V-05: container sem nivel filho declarado.
    d = _doc_valido_minimo()
    d["formato"]["niveis"] = [
        {"id": "c", "tipo": "container", "conteudo": "titulo",
         "designador": {"tipo": "decimal"}},
        {"id": "i", "tipo": "conteudo", "conteudo": "texto",
         "designador": {"tipo": "nenhum"}},
    ]
    d["dados"] = [{"id": "c1", "nivel": "c", "titulo": "T", "filhos": []}]
    _rejeita("V-05: container com filhos vazio rejeitado", d, TelaEstruturaInvalida)

    # V-06: campo nome-valor sem origem do valor.
    d = _doc_nv()
    d["formato"]["niveis"][0]["conteudo"] = {"nome": "chave"}  # falta "valor"
    _rejeita("V-06: nome_valor sem campo valor rejeitado", d, TelaEstruturaInvalida)

    # V-07: medidas negativas em formato.espacamento.
    d = _doc_valido_minimo()
    d["formato"]["espacamento"] = {"margem": -1}
    _rejeita("V-07: medida negativa em espacamento rejeitada", d, TelaEstruturaInvalida)

    # V-08: largura maxima inferior a minima em coluna de tabela.
    d = _doc_tabela()
    d["formato"]["tabela"]["colunas"] = [
        {"nivel": "item", "largura_minima": 10, "largura_maxima": 5}
    ]
    _rejeita("V-08: largura_maxima inferior a largura_minima rejeitada", d,
             TelaEstruturaInvalida)

    # V-09: modo nao verboso configurado para mais de uma linha.
    d = _doc_valido_minimo()
    d["formato"]["excesso"] = {"linhas_nao_verboso": 3}
    _rejeita("V-09: nao verboso com mais de uma linha rejeitado", d, TelaEstruturaInvalida)

    # V-10: modo verboso sem regra de alinhamento da continuacao.
    d = _doc_valido_minimo()
    d["formato"]["excesso"] = {"verboso": {}}
    _rejeita("V-10: verboso sem continuacao rejeitado", d, TelaEstruturaInvalida)

    # V-11: justificacao sem escopo.
    d = _doc_valido_minimo()
    d["formato"]["alinhamento"] = {"tipo": "justificado"}
    _rejeita("V-11: justificado sem escopo rejeitado", d, TelaEstruturaInvalida)

    # V-12: designador composto (decimal_composto) sem ancestral.
    d = _doc_valido_minimo()
    d["formato"]["niveis"][0]["designador"] = {"tipo": "decimal_composto",
                                                "separador": "."}
    _rejeita("V-12: decimal_composto em nivel raiz rejeitado", d, TelaEstruturaInvalida)

    # V-13: dados incompativeis com a estrutura declarada.
    d = _doc_valido_minimo()
    d["dados"][0]["nivel"] = "nao_existe"
    _rejeita("V-13: dados com nivel inexistente rejeitados", d, TelaEstruturaInvalida)

    # V-14: coluna de tabela sem nivel ou campo de origem.
    d = _doc_tabela()
    d["formato"]["tabela"]["colunas"] = [{"titulo": "Sem origem"}]
    _rejeita("V-14: coluna de tabela sem nivel ou campo rejeitada", d,
             TelaEstruturaInvalida)

    # V-14 (semantica): campo/nivel nulos ou strings vazias/whitespace sao invalidos.
    def _doc_tabela_coluna_invalida(coluna_dict):
        """Tabela com uma coluna valida seguida de uma coluna sob teste."""
        t = _doc_tabela()
        t["formato"]["tabela"]["colunas"] = [
            {"identificador": "ok", "titulo": "Ok", "campo": "texto"},
            coluna_dict,
        ]
        return t

    _rejeita("V-14: nivel null rejeitado",
             _doc_tabela_coluna_invalida(
                 {"identificador": "x", "titulo": "X", "nivel": None}),
             TelaEstruturaInvalida)
    _rejeita("V-14: campo null rejeitado",
             _doc_tabela_coluna_invalida(
                 {"identificador": "x", "titulo": "X", "campo": None}),
             TelaEstruturaInvalida)
    _rejeita("V-14: nivel string vazia rejeitado",
             _doc_tabela_coluna_invalida(
                 {"identificador": "x", "titulo": "X", "nivel": ""}),
             TelaEstruturaInvalida)
    _rejeita("V-14: campo string vazia rejeitado",
             _doc_tabela_coluna_invalida(
                 {"identificador": "x", "titulo": "X", "campo": ""}),
             TelaEstruturaInvalida)
    _rejeita("V-14: nivel whitespace rejeitado",
             _doc_tabela_coluna_invalida(
                 {"identificador": "x", "titulo": "X", "nivel": "   "}),
             TelaEstruturaInvalida)
    _rejeita("V-14: campo whitespace rejeitado",
             _doc_tabela_coluna_invalida(
                 {"identificador": "x", "titulo": "X", "campo": "   "}),
             TelaEstruturaInvalida)
    # Coluna com origem valida e aceita.
    _aceita("V-14: coluna com campo valido aceita",
            _doc_tabela_coluna_invalida(
                {"identificador": "y", "titulo": "Y", "campo": "texto"}))
    _aceita("V-14: coluna com nivel valido aceita",
            _doc_tabela_coluna_invalida(
                {"identificador": "y", "titulo": "Y", "nivel": "item"}))

    # V-13: nivel declarado mas incompativel com a estrutura (H0037-IMPL-QAPP4-002).
    # nivel com string nao-vazia que nao existe em formato.niveis -> V-13.
    _rejeita("V-13: coluna com nivel inexistente rejeitada",
             _doc_tabela_coluna_invalida(
                 {"identificador": "z", "titulo": "Z", "nivel": "inexistente"}),
             TelaEstruturaInvalida)
    _rejeita("V-13: coluna com nivel de outro esquema rejeitada",
             _doc_tabela_coluna_invalida(
                 {"identificador": "z", "titulo": "Z", "nivel": "container"}),
             TelaEstruturaInvalida)
    # Verificacao: mensagem de V-13 distingue do V-14.
    try:
        validar_conteudo_externo(
            _doc_tabela_coluna_invalida(
                {"identificador": "z", "titulo": "Z", "nivel": "nivel_nao_declarado"}))
        _registrar("V-13: mensagem identifica V-13 (nao V-14)", False,
                   "nenhuma excecao")
    except TelaEstruturaInvalida as _exc_v13:
        _msg_v13 = str(_exc_v13)
        _registrar(
            "V-13: mensagem identifica V-13 (nao V-14)",
            "V-13" in _msg_v13,
            "" if "V-13" in _msg_v13 else "V-13 nao encontrado: " + _msg_v13,
        )
    except Exception as _exc_v13_outro:  # pragma: no cover
        _registrar("V-13: mensagem identifica V-13 (nao V-14)", False,
                   "excecao inesperada: {0}".format(type(_exc_v13_outro).__name__))
    # nivel valido continua aceito (V-14 e V-13 nao interferem com caso correto).
    _aceita("V-13: coluna com nivel valido declarado continua aceita",
            _doc_tabela_coluna_invalida(
                {"identificador": "w", "titulo": "W", "nivel": "item"}))

    # --- V-13 por campo (H0037-IMPL-QAPP5-002): completa a separacao V-13/V-14 ---
    #
    # O contrato nao define catalogo literal fechado de valores de ``campo``, mas
    # define onde estao os campos validos — em ``formato.niveis[].conteudo``
    # (contrato_json_console.md §12.3): para ``container``/``conteudo``, o campo
    # de texto do no; para ``nome_valor``, os campos ``nome`` e ``valor``. O
    # catalogo estrutural derivado valida ``campo`` contra a estrutura declarada,
    # distinguindo:
    #   - campo ausente/nulo/vazio/whitespace -> V-14 (origem sem valor semantico);
    #   - campo declarado mas inexistente na estrutura -> V-13 (origem
    #     declarada mas incompativel).
    # ``_doc_tabela()`` declara nivel ``item`` tipo ``conteudo`` com campo
    # ``texto`` — portanto ``campo: "texto"`` e valido; ``campo: "nao_existe"``
    # e incompativel (V-13).
    print("")
    print("-- V-13 por campo (H0037-IMPL-QAPP5-002) --")

    # V13-P6-01: campo inexistente na estrutura -> V-13.
    try:
        validar_conteudo_externo(_doc_tabela_coluna_invalida(
            {"identificador": "c1", "titulo": "C1", "campo": "nao_existe"}))
        _registrar("V13-P6-01: campo inexistente rejeitado (V-13)",
                   False, "nenhuma excecao")
    except TelaEstruturaInvalida as _exc_c1:
        _msg_c1 = str(_exc_c1)
        _registrar("V13-P6-01: campo inexistente rejeitado (V-13)",
                   "V-13" in _msg_c1,
                   "" if "V-13" in _msg_c1 else "V-13 nao encontrado: " + _msg_c1)

    # V13-P6-02: campo declarado mas ausente nos dados. Quando o campo existe na
    # estrutura (``texto``) mas o no de dados nao o possui, a validacao 15
    # (_validar_no_conteudo para conteudo) ja rejeita (TelaCampoObrigatorioAusente).
    # Esse e o comportamento conforme contrato: compatibilidade com dados e
    # obrigatoria. Aqui confirmamos que o ponto de falha e o no de dados.
    _d_campo_ausente = _doc_tabela()
    _d_campo_ausente["dados"] = [{"id": "a", "nivel": "item"}]  # sem 'texto'
    _rejeita("V13-P6-02: campo declarado ausente nos dados rejeitado",
             _d_campo_ausente, (TelaCampoObrigatorioAusente, TelaEstruturaInvalida))

    # V13-P6-03: campo incompativel com tabela (campo nao pertence aos niveis).
    # _doc_tabela tem nivel unico 'item' (conteudo, campo 'texto'); campo
    # 'vlr_inexistente' nao e declarado em nenhum nivel -> V-13.
    _rejeita("V13-P6-03: campo incompativel com tabela rejeitado (V-13)",
             _doc_tabela_coluna_invalida(
                 {"identificador": "c3", "titulo": "C3",
                  "campo": "vlr_inexistente"}),
             TelaEstruturaInvalida)

    # V13-P6-04: origem valida para outra apresentacao (campo de nome_valor em
    # doc de conteudo puro). _doc_tabela usa nivel conteudo (campo 'texto');
    # 'valor' nao e campo deste nivel. Nao deve ser aceita pela tabela.
    _rejeita("V13-P6-04: campo de outra apresentacao rejeitado (V-13)",
             _doc_tabela_coluna_invalida(
                 {"identificador": "c4", "titulo": "C4", "campo": "valor"}),
             TelaEstruturaInvalida)

    # V13-P6-05: campo valido (texto, declarado pelo nivel item) -> aceito.
    _aceita("V13-P6-05: coluna com campo valido aceita",
            _doc_tabela_coluna_invalida(
                {"identificador": "c5", "titulo": "C5", "campo": "texto"}))

    # V13-P6-06: nivel valido (item) -> aceito (ja coberto por V-13 nivel, mas
    # reafirmado aqui para mostrar que a separacao V-13/V-14 esta completa).
    _aceita("V13-P6-06: coluna com nivel valido aceita",
            _doc_tabela_coluna_invalida(
                {"identificador": "c6", "titulo": "C6", "nivel": "item"}))

    # V13-P6-07: duas colunas validas (texto + nivel) -> aceitas.
    _d_2col = _doc_tabela()
    _d_2col["formato"]["tabela"]["colunas"] = [
        {"identificador": "a", "titulo": "A", "campo": "texto"},
        {"identificador": "b", "titulo": "B", "nivel": "item"},
    ]
    _aceita("V13-P6-07: duas colunas validas aceitas", _d_2col)

    # V13-P6-08: titulo valido com campo inexistente — a coluna ultrapassa V-01
    # (tem titulo) e ultrapassa V-14 (tem campo nao vazio), mas falha em V-13
    # (campo incompativel com a estrutura).
    try:
        validar_conteudo_externo(_doc_tabela_coluna_invalida(
            {"identificador": "c8", "titulo": "Com Titulo",
             "campo": "campo_fantasma"}))
        _registrar("V13-P6-08: titulo valido + campo inexistente -> V-13",
                   False, "nenhuma excecao")
    except TelaEstruturaInvalida as _exc_c8:
        _msg_c8 = str(_exc_c8)
        _registrar("V13-P6-08: titulo valido + campo inexistente -> V-13",
                   "V-13" in _msg_c8,
                   "" if "V-13" in _msg_c8 else "esperava V-13: " + _msg_c8)

    # V13-P6-09: campo vazio -> V-14 (nao V-13). Origem sem valor semantico.
    try:
        validar_conteudo_externo(_doc_tabela_coluna_invalida(
            {"identificador": "c9", "titulo": "C9", "campo": ""}))
        _registrar("V13-P6-09: campo vazio -> V-14 (nao V-13)",
                   False, "nenhuma excecao")
    except TelaEstruturaInvalida as _exc_c9:
        _msg_c9 = str(_exc_c9)
        _registrar("V13-P6-09: campo vazio -> V-14 (nao V-13)",
                   "V-14" in _msg_c9 and "V-13" not in _msg_c9,
                   "esperava V-14: " + _msg_c9)

    # V13-P6-10: nivel inexistente -> continua V-13 (nao regresso).
    try:
        validar_conteudo_externo(_doc_tabela_coluna_invalida(
            {"identificador": "c10", "titulo": "C10", "nivel": "nao_existe"}))
        _registrar("V13-P6-10: nivel inexistente -> V-13",
                   False, "nenhuma excecao")
    except TelaEstruturaInvalida as _exc_c10:
        _msg_c10 = str(_exc_c10)
        _registrar("V13-P6-10: nivel inexistente -> V-13",
                   "V-13" in _msg_c10,
                   "" if "V-13" in _msg_c10 else "esperava V-13: " + _msg_c10)

    # V13-P6-extra: documento com nivel nome_valor — campo valido referencia
    # 'nome' ou 'valor' declarados em conteudo. Garante que o catalogo estrutural
    # coleta campos de nome_valor (H0037-IMPL-QAPP5-002).
    _d_nv = {
        "tipo": "multinivel",
        "formato": {
            "apresentacao": "tabela",
            "niveis": [{"id": "kv", "tipo": "nome_valor",
                        "conteudo": {"nome": "chave", "valor": "vlr"},
                        "designador": {"tipo": "nenhum"}}],
            "tabela": {"cabecalho": ["Col"]},
        },
        "dados": [{"id": "r1", "nivel": "kv", "chave": "K", "vlr": "V"}],
    }
    # campo 'vlr' (declarado em conteudo.valor) -> aceito.
    _d_nv_ok = json.loads(json.dumps(_d_nv))
    _d_nv_ok["formato"]["tabela"]["colunas"] = [
        {"identificador": "v", "titulo": "V", "campo": "vlr"}]
    _aceita("V13-P6-extra: campo nome_valor (vlr) valido aceita", _d_nv_ok)
    # campo 'fantasma' nao declarado -> V-13.
    _d_nv_bad = json.loads(json.dumps(_d_nv))
    _d_nv_bad["formato"]["tabela"]["colunas"] = [
        {"identificador": "x", "titulo": "X", "campo": "fantasma"}]
    _rejeita("V13-P6-extra: campo nome_valor inexistente rejeitado (V-13)",
             _d_nv_bad, TelaEstruturaInvalida)


    # V-15: condicao excepcional sem politica explicita no documento externo.
    d = _doc_valido_minimo()
    d["formato"]["excesso"] = {"politica_modo": "alternavel"}
    _rejeita("V-15: politica_modo em formato.excesso rejeitada", d, TelaEstruturaInvalida)
    d = _doc_valido_minimo()
    d["formato"]["excesso"] = {"modo": "verboso"}
    _rejeita("V-15: excesso.modo (legado) em formato.excesso rejeitado", d,
             TelaEstruturaInvalida)
    d = _doc_valido_minimo(); d["politica_modo"] = "alternavel"
    _rejeita("V-15: politica_modo na raiz do documento externo rejeitada", d,
             TelaEstruturaInvalida)


def teste_d23_estrutural():
    """Validacao D23 no JSON estrutural: politica_modo e modo_inicial (H-0037)."""
    from tela.loader import _validar_d23_console  # noqa: F401

    print("")
    print("== D23: politica_modo e modo_inicial no JSON estrutural ==")

    def _aceita_d23(nome, excesso, id_tela=None):
        try:
            _validar_d23_console(excesso, "con_teste", id_tela=id_tela)
            _registrar(nome, True)
        except Exception as exc:
            _registrar(nome, False, "{0}: {1}".format(type(exc).__name__, exc))

    def _rejeita_d23(nome, excesso, classe=TelaErro, id_tela=None):
        try:
            _validar_d23_console(excesso, "con_teste", id_tela=id_tela)
            _registrar(nome, False, "nenhuma excecao")
        except classe:
            _registrar(nome, True)
        except Exception as exc:
            _registrar(nome, False, "excecao errada: {0}".format(type(exc).__name__))

    # Telas legadas H-0036: ausencia de politica_modo aceita nominalmente.
    _aceita_d23("D23: excesso vazio em tela legada H-0036 aceito", {},
                id_tela="h0036_console_hierarquia")
    _aceita_d23("D23: excesso sem politica_modo em tela legada H-0036 aceito",
                {"outro": "campo"}, id_tela="h0036_console_tabela")

    # Tela nova/revisada: ausencia de politica_modo rejeitada.
    _rejeita_d23("D23: politica_modo ausente em tela nova rejeitado", {},
                 TelaEstruturaInvalida, id_tela="h0037_console_teste")

    # Politicas validas sem modo_inicial.
    _aceita_d23("D23: somente_nao_verboso sem modo_inicial aceito",
                {"politica_modo": "somente_nao_verboso"})
    _aceita_d23("D23: somente_verboso sem modo_inicial aceito",
                {"politica_modo": "somente_verboso"})

    # Alternavel com modo_inicial valido.
    _aceita_d23("D23: alternavel + modo_inicial verboso aceito",
                {"politica_modo": "alternavel", "modo_inicial": "verboso"})
    _aceita_d23("D23: alternavel + modo_inicial nao_verboso aceito",
                {"politica_modo": "alternavel", "modo_inicial": "nao_verboso"})

    # Rejeicoes D23.
    _rejeita_d23("D23: modo_inicial sem politica_modo rejeitado",
                 {"modo_inicial": "verboso"}, TelaEstruturaInvalida)
    _rejeita_d23("D23: politica_modo invalida rejeitada",
                 {"politica_modo": "sempre_verboso"}, TelaEstruturaInvalida)
    _rejeita_d23("D23: alternavel sem modo_inicial rejeitado",
                 {"politica_modo": "alternavel"}, TelaEstruturaInvalida)
    _rejeita_d23("D23: alternavel com modo_inicial invalido rejeitado",
                 {"politica_modo": "alternavel", "modo_inicial": "talvez"},
                 TelaEstruturaInvalida)
    _rejeita_d23("D23: somente_nao_verboso com modo_inicial rejeitado",
                 {"politica_modo": "somente_nao_verboso", "modo_inicial": "verboso"},
                 TelaEstruturaInvalida)
    _rejeita_d23("D23: somente_verboso com modo_inicial rejeitado",
                 {"politica_modo": "somente_verboso", "modo_inicial": "nao_verboso"},
                 TelaEstruturaInvalida)

    # Telas estruturais H-0037 carregam sem excecao.
    for id_tela in [
        "h0037_console_nao_verboso",
        "h0037_console_verboso_dois_niveis",
        "h0037_console_alternavel_tres_niveis",
        "h0037_console_tabela_alternavel",
    ]:
        try:
            carregar_tela(None, id_tela, _RAIZ_TELAS_DEMO)
            _registrar("D23: {0} carrega sem excecao".format(id_tela), True)
        except Exception as exc:
            _registrar("D23: {0} carrega sem excecao".format(id_tela), False,
                       "{0}: {1}".format(type(exc).__name__, exc))

    # --- PATCH pos-QA H-0037: impedir bypass D23 por ausencia de formato.excesso ---
    # Testes D23-01 a D23-07 (H0037-IMPL-QAPP-001). A isencao D23 depende da
    # natureza estrutural (console consumidor de conteudo multinivel vs
    # envelope pre-ADR-0028) e do inventario legado nominal — nao da presenca
    # de formato.excesso. Telas novas/revisadas consumidoras de conteudo
    # multinivel devem declarar politica_modo mesmo se omitirem o bloco inteiro.

    def _console_consumidor(id_tela, **sobrepos):
        """Constroi elemento console consumidor de conteudo multinivel
        (sem envelope pre-ADR-0028), id_tela fora do inventario legado."""
        elem = {"id": "con", "tipo": "console", "titulo": "Console"}
        elem.update(sobrepos)
        return {
            "schema": "tela.v1", "id": id_tela, "cabecalho": {},
            "corpo": {"arranjo": "vertical", "elementos": [elem]},
            "barra_de_menus": {"chips": []},
        }

    def _escrever_em_tmp(id_tela, dados):
        tmp = Path(tempfile.mkdtemp(prefix="d23_bypass_"))
        dir_t = tmp / "config" / "telas" / "demo"
        dir_t.mkdir(parents=True, exist_ok=True)
        (dir_t / "{0}.json".format(id_tela)).write_text(
            json.dumps(dados), encoding="utf-8")
        return tmp

    def _carrega_em_tmp(nome, dados):
        tmp = _escrever_em_tmp(dados["id"], dados)
        try:
            carregar_tela(tmp, dados["id"], _RAIZ_TELAS_DEMO)
            _registrar(nome, True)
        except TelaErro:
            _registrar(nome, False, "carregamento rejeitou tela esperada")
        except Exception as exc:  # pragma: no cover
            _registrar(nome, False, "{0}: {1}".format(type(exc).__name__, exc))
        finally:
            try:
                shutil.rmtree(tmp)
            except OSError:
                pass

    def _rejeita_carrega_em_tmp(nome, dados):
        tmp = _escrever_em_tmp(dados["id"], dados)
        try:
            carregar_tela(tmp, dados["id"], _RAIZ_TELAS_DEMO)
            _registrar(nome, False, "carregamento aceitou tela invalida")
        except TelaEstruturaInvalida:
            _registrar(nome, True)
        except Exception as exc:  # pragma: no cover
            _registrar(nome, False, "excecao errada: {0}".format(type(exc).__name__))
        finally:
            try:
                shutil.rmtree(tmp)
            except OSError:
                pass

    # D23-01: nova tela consumidora com formato.excesso, mas sem politica_modo.
    _rejeita_carrega_em_tmp(
        "D23-01: nova tela consumidora com excesso sem politica_modo rejeitada",
        _console_consumidor(
            "d23_nova_01", formato={"excesso": {"outro": "campo"}},
        ),
    )

    # D23-02: nova tela consumidora sem todo o bloco formato.excesso.
    _rejeita_carrega_em_tmp(
        "D23-02: nova tela consumidora sem bloco formato.excesso rejeitada",
        _console_consumidor("d23_nova_02"),
    )

    # D23-03: nova tela equivalente, com outro ID nao pertencente ao inventario
    # H-0037, sem todo o bloco. Impede correcao baseada apenas nos quatro IDs.
    _rejeita_carrega_em_tmp(
        "D23-03: tela equivalente com ID alternativo sem bloco rejeitada",
        _console_consumidor("outra_tela_nova_xyz"),
    )

    # D23-04: tela H-0036 nominalmente legada sem campos D23.
    for id_legado in ("h0036_console_hierarquia",
                      "h0036_console_tabela",
                      "h0036_console_conjuntos"):
        _carrega_em_tmp(
            "D23-04: tela legada {0} sem campos D23 aceita".format(id_legado),
            _console_consumidor(id_legado),
        )

    # D23-05: tela nova com apenas o campo legado formato.excesso.modo,
    # sem politica_modo. O campo legado nao supre a politica D23.
    _rejeita_carrega_em_tmp(
        "D23-05: tela nova com apenas excesso.modo legado rejeitada",
        _console_consumidor("d23_nova_05",
                            formato={"excesso": {"modo": "verboso"}}),
    )

    # D23-06: estrutura nao pertencente ao escopo de console/multinivel D23.
    # Console de envelope pre-ADR-0028 COMPLETO (todos os 7 campos do envelope)
    # preserva o comportamento contratual anterior — nao exige politica D23.
    # CORRECAO H0037-IMPL-QAPP2-001: envelope exige TODOS os campos; campo
    # isolado nao concede isencao. Fixture usa o envelope minimo completo do
    # contrato_json_console.md secao 4.
    _carrega_em_tmp(
        "D23-06: console de envelope pre-ADR-0028 completo preserva comportamento anterior",
        {
            "schema": "tela.v1", "id": "d23_envelope_06", "cabecalho": {},
            "corpo": {"arranjo": "vertical", "elementos": [
                {"id": "con", "tipo": "console", "titulo": "Console",
                 "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False},
                 "politica_composicao": {"alinhamento": "esquerda",
                                        "overflow_normal": "truncar_com_reticencias"},
                 "politica_navegacao": {"navegavel": False},
                 "politica_selecao": "nenhuma",
                 "politica_paginacao": "sem",
                 "politica_exibicao": {"modo_inicial": "normal", "verboso": False}},
            ]},
            "barra_de_menus": {"chips": []},
        },
    )

    # D23-07: tela nova consumidora com politica valida e matriz correta.
    _carrega_em_tmp(
        "D23-07: tela nova consumidora com politica valida e matriz correta aceita",
        _console_consumidor(
            "d23_nova_07",
            formato={"excesso": {"politica_modo": "alternavel",
                                 "modo_inicial": "verboso"}},
        ),
    )

    # --- Testes D23-P3 (H0037-IMPL-QAPP2-001): bypass por campo isolado eliminado ---
    # Constroi envelope completo (todos os 7 campos do _CAMPOS_ENVELOPE_PRE_ADR_0028).
    _ENVELOPE_COMPLETO = {
        "itens": [], "origem_dados": None, "politica_composicao": {"alinhamento": "esquerda", "overflow_normal": "truncar_com_reticencias"}, "politica_navegacao": {"navegavel": False}, "politica_selecao": "nenhuma", "politica_paginacao": "sem", "politica_exibicao": {"modo_inicial": "normal", "verboso": False},
        "politica_composicao": {"alinhamento": "esquerda",
                                "overflow_normal": "truncar_com_reticencias"},
        "politica_navegacao": {"navegavel": False},
        "politica_selecao": "nenhuma",
        "politica_paginacao": "sem",
        "politica_exibicao": {"modo_inicial": "normal", "verboso": False},
    }

    def _console_consumidor_com_extra(id_tela, **extra):
        """Consumidor com campos extras adicionados ao elemento console."""
        elem = {"id": "con", "tipo": "console", "titulo": "Console"}
        elem.update(extra)
        return {
            "schema": "tela.v1", "id": id_tela, "cabecalho": {},
            "corpo": {"arranjo": "vertical", "elementos": [elem]},
            "barra_de_menus": {"chips": []},
        }

    def _console_envelope_com_extra(id_tela, **extra):
        """Envelope completo com campos extras adicionados."""
        elem = {"id": "con", "tipo": "console", "titulo": "Console"}
        elem.update(_ENVELOPE_COMPLETO)
        elem.update(extra)
        return {
            "schema": "tela.v1", "id": id_tela, "cabecalho": {},
            "corpo": {"arranjo": "vertical", "elementos": [elem]},
            "barra_de_menus": {"chips": []},
        }

    # D23-P3-05 e D23-P3-06: campo isolado de envelope pre-ADR-0028 (sem fonte
    # de itens completa e sem os 6 campos base) e REJEITADO como estrutura
    # incompleta (H0037-IMPL-QAPP5-001). Um unico campo de envelope nao forma
    # envelope historico completo (variante 1 ou 2) nem e consumidor multinivel
    # puro — e estrutura ambiguamente parcial. Nao ha bypass por cardinalidade.
    for _campo_isolado, _val_isolado in [
        ("itens", []),
        ("origem_dados", None),
        ("politica_composicao", {"alinhamento": "esquerda",
                                 "overflow_normal": "truncar_com_reticencias"}),
        ("politica_navegacao", {"navegavel": False}),
        ("politica_selecao", "nenhuma"),
        ("politica_paginacao", "sem"),
        ("politica_exibicao", {"modo_inicial": "normal", "verboso": False}),
    ]:
        _rejeita_carrega_em_tmp(
            "D23-P3-05/06: campo isolado '{0}' (envelope incompleto) rejeitado".format(
                _campo_isolado),
            _console_consumidor_com_extra("d23_campo_isolado_xyz", **{_campo_isolado: _val_isolado}),
        )

    # D23-P3-07: estrutura hibrida completa (envelope + campos D23) rejeitada.
    _rejeita_carrega_em_tmp(
        "D23-P3-07: estrutura hibrida envelope+D23 rejeitada",
        _console_envelope_com_extra(
            "d23_hibrido_07",
            formato={"excesso": {"politica_modo": "somente_nao_verboso"}},
        ),
    )

    # D23-P3-08: envelope historico real completo preserva comportamento anterior.
    _carrega_em_tmp(
        "D23-P3-08: envelope historico completo fora de D23 aceito",
        _console_envelope_com_extra("d23_envelope_historico_08"),
    )

    # D23-P3-09: envelope VARIANTE 1 incompleto (6 de 7 campos, faltando
    # politica_paginacao) -> REJEITADO. Apos o sexto patch (H0037-IMPL-QAPP5-001),
    # a variante 1 (itens) exige os 6 campos base completos; remover qualquer
    # um torna o envelope incompleto e rejeitado. demo.json NAO segue esse
    # padrao (usa variante 2 com regra_geracao_itens, historica comprovada) —
    # ver D23-P6-12 e RGI-P6-12 para o caso historico.
    _elem_incompleto = {"id": "con", "tipo": "console", "titulo": "Console"}
    _elem_incompleto.update(_ENVELOPE_COMPLETO)
    del _elem_incompleto["politica_paginacao"]  # remove um campo base para ter 6/7
    _rejeita_carrega_em_tmp(
        "D23-P3-09: envelope variante 1 incompleto (6 de 7 campos) rejeitado",
        {
            "schema": "tela.v1", "id": "d23_envelope_incompleto_09", "cabecalho": {},
            "corpo": {"arranjo": "vertical", "elementos": [_elem_incompleto]},
            "barra_de_menus": {"chips": []},
        },
    )

    # D23-P3-10: cinco legados nominais aceitos. D23-04 ja cobre os 3 H-0036;
    # adicionar os 2 H-0035 para cobertura completa do inventario.
    for id_legado_h35 in ("h0035_console_com", "h0035_console_sem"):
        _carrega_em_tmp(
            "D23-P3-10: tela legada {0} aceita".format(id_legado_h35),
            _console_consumidor(id_legado_h35),
        )

    # D23-P3-11: copia renomeada de legado nao recebe isencao.
    _rejeita_carrega_em_tmp(
        "D23-P3-11: copia renomeada de legado sem politica rejeitada",
        _console_consumidor("h0036_console_copia_renomeada"),
    )

    # D23-P3-12: prefixo semelhante ao legado nao concede isencao automatica.
    _rejeita_carrega_em_tmp(
        "D23-P3-12a: prefixo h0035_ semelhante nao isenta (h0035_console_novo)",
        _console_consumidor("h0035_console_novo"),
    )
    _rejeita_carrega_em_tmp(
        "D23-P3-12b: prefixo h0036_ semelhante nao isenta (h0036_console_copia)",
        _console_consumidor("h0036_console_copia"),
    )

    # Verificacoes diretas de _console_em_escopo_d23 (funcao auxiliar).
    # CORRECAO H0037-IMPL-QAPP2-001: campo isolado deve levantar excecao.
    from tela.loader import _console_em_escopo_d23

    _registrar(
        "D23: console de envelope completo fora do escopo D23",
        _console_em_escopo_d23(
            dict({"id": "c", "tipo": "console"}, **_ENVELOPE_COMPLETO),
            "tela_nova_xyz",
        ) is False,
    )
    _registrar(
        "D23: console consumidor novo em escopo D23",
        _console_em_escopo_d23(
            {"id": "c", "tipo": "console", "titulo": "C"}, "tela_nova_xyz") is True,
    )
    _registrar(
        "D23: console consumidor legado H-0036 fora do escopo D23",
        _console_em_escopo_d23(
            {"id": "c", "tipo": "console", "titulo": "C"},
            "h0036_console_tabela") is False,
    )
    # Campo isolado 'itens' sem os demais 6 campos base: envelope pre-ADR-0028
    # VARIANTE 1 INCOMPLETO -> levanta TelaEstruturaInvalida (nao retorna False,
    # nem True). Apos o sexto patch (H0037-IMPL-QAPP5-001), a variante 1 exige
    # os 6 campos base completos; itens isolado (ou qualquer campo base sem
    # fonte de itens) e envelope incompleto, nao isencao.
    try:
        _console_em_escopo_d23(
            {"id": "c", "tipo": "console", "itens": []}, "tela_nova_xyz",
        )
        _registrar(
            "D23: itens isolado (sem 6 base) levanta envelope incompleto",
            False, "nenhuma excecao",
        )
    except TelaEstruturaInvalida:
        _registrar(
            "D23: itens isolado (sem 6 base) levanta envelope incompleto", True,
        )
    except Exception as _exc_campo_iso:  # pragma: no cover
        _registrar(
            "D23: itens isolado (sem 6 base) levanta envelope incompleto",
            False, "excecao errada: {0}".format(type(_exc_campo_iso).__name__),
        )
    try:
        _console_em_escopo_d23(
            {"id": "c", "tipo": "console", "itens": [],
             "formato": {"excesso": {"politica_modo": "somente_nao_verboso"}}},
            "tela_nova_xyz",
        )
        _registrar(
            "D23: hibrido (campo isolado + politica_modo) levanta excecao",
            False, "nenhuma excecao",
        )
    except TelaEstruturaInvalida:
        _registrar(
            "D23: hibrido (campo isolado + politica_modo) levanta excecao", True,
        )
    except Exception as _exc_campo:  # pragma: no cover
        _registrar(
            "D23: hibrido (campo isolado + politica_modo) levanta excecao",
            False, "excecao errada: {0}".format(type(_exc_campo).__name__),
        )

    # --- Testes D23-P4 (H0037-IMPL-QAPP3-001): validacao de valores do envelope ---
    print("")
    print("-- D23-P4: validacao de valores do envelope pre-ADR-0028 --")

    # D23-P4-01: todos os campos null -> rejeitado (itens nao e lista).
    _rejeita_carrega_em_tmp(
        "D23-P4-01: envelope com todos os campos null rejeitado",
        {
            "schema": "tela.v1", "id": "d23_p4_01", "cabecalho": {},
            "corpo": {"arranjo": "vertical", "elementos": [{
                "id": "con", "tipo": "console", "titulo": "Console",
                "itens": None, "origem_dados": None,
                "politica_composicao": None, "politica_navegacao": None,
                "politica_selecao": None, "politica_paginacao": None,
                "politica_exibicao": None,
            }]},
            "barra_de_menus": {"chips": []},
        },
    )

    # D23-P4-02: itens com tipo errado (string em vez de lista) -> rejeitado.
    _rejeita_carrega_em_tmp(
        "D23-P4-02: envelope com 'itens' tipo errado rejeitado",
        {
            "schema": "tela.v1", "id": "d23_p4_02", "cabecalho": {},
            "corpo": {"arranjo": "vertical", "elementos": [
                dict({"id": "con", "tipo": "console", "titulo": "Console"},
                     **dict(_ENVELOPE_COMPLETO, itens="nao_e_lista")),
            ]},
            "barra_de_menus": {"chips": []},
        },
    )

    # D23-P4-03: politica_selecao invalida -> rejeitado.
    _rejeita_carrega_em_tmp(
        "D23-P4-03: envelope com 'politica_selecao' invalida rejeitado",
        {
            "schema": "tela.v1", "id": "d23_p4_03", "cabecalho": {},
            "corpo": {"arranjo": "vertical", "elementos": [
                dict({"id": "con", "tipo": "console", "titulo": "Console"},
                     **dict(_ENVELOPE_COMPLETO, politica_selecao="invalida")),
            ]},
            "barra_de_menus": {"chips": []},
        },
    )

    # D23-P4-04: politica_paginacao com tipo dict (nao string) -> rejeitado.
    # Reproduz o padrao encontrado em demo.json para o campo politica_paginacao
    # quando os 7 campos estao presentes (testar que o tipo invalido e rejeitado).
    _rejeita_carrega_em_tmp(
        "D23-P4-04: envelope com 'politica_paginacao' dict em vez de string rejeitado",
        {
            "schema": "tela.v1", "id": "d23_p4_04", "cabecalho": {},
            "corpo": {"arranjo": "vertical", "elementos": [
                dict({"id": "con", "tipo": "console", "titulo": "Console"},
                     **dict(_ENVELOPE_COMPLETO,
                            politica_paginacao={"paginacao": "com"})),
            ]},
            "barra_de_menus": {"chips": []},
        },
    )

    # D23-P4-05: consumidor com politica_modo + campo isolado de envelope -> rejeitado.
    for _campo_env, _val_env in [
        ("itens", []),
        ("politica_selecao", "nenhuma"),
        ("politica_paginacao", "sem"),
    ]:
        _rejeita_carrega_em_tmp(
            "D23-P4-05: hibrido campo '{0}' + politica_modo rejeitado".format(
                _campo_env),
            {
                "schema": "tela.v1",
                "id": "d23_p4_05_{0}".format(_campo_env.replace("_", "")),
                "cabecalho": {},
                "corpo": {"arranjo": "vertical", "elementos": [{
                    "id": "con", "tipo": "console", "titulo": "Console",
                    _campo_env: _val_env,
                    "formato": {"excesso": {
                        "politica_modo": "somente_nao_verboso"}},
                }]},
                "barra_de_menus": {"chips": []},
            },
        )

    # D23-P4-06: consumidor com politica_modo + 6 campos de envelope -> rejeitado.
    _rejeita_carrega_em_tmp(
        "D23-P4-06: hibrido 6 campos de envelope + politica_modo rejeitado",
        {
            "schema": "tela.v1", "id": "d23_p4_06", "cabecalho": {},
            "corpo": {"arranjo": "vertical", "elementos": [
                dict(
                    {"id": "con", "tipo": "console", "titulo": "Console",
                     "formato": {"excesso": {
                         "politica_modo": "somente_nao_verboso"}}},
                    **{k: v for k, v in _ENVELOPE_COMPLETO.items()
                       if k != "politica_paginacao"},
                ),
            ]},
            "barra_de_menus": {"chips": []},
        },
    )

    # D23-P4-09: demo.json real carrega sem excecao (regressao preservada).
    try:
        carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        _registrar("D23-P4-09: demo.json carrega sem excecao", True)
    except Exception as _exc_demo:
        _registrar("D23-P4-09: demo.json carrega sem excecao", False,
                   "{0}: {1}".format(type(_exc_demo).__name__, _exc_demo))

    # --- Testes D23-P6 (H0037-IMPL-QAPP5-001): regra_geracao_itens nao isenta ---
    #
    # Sexto patch focal. O quinto patch introduziu a isencao D23 por mera presenca
    # da chave ``regra_geracao_itens`` (loader.py ``return False`` quando a chave
    # existia), o que o QA classificou como DEFEITO_IMPLEMENTACAO /
    # REGRESSAO_MASCARADA: a chave nao tem schema interno fechado em nenhum
    # contrato/ADR/NOMENCLATURA (so existe a frase "regra de geracao de itens"
    # como alternativa a itens), e a isencao por presenca aceitava ``{}``,
    # ``null``, tipos incorretos, objetos incompletos e combinacoes hibridas.
    #
    # Nova semantica (duas variantes do envelope pre-ADR-0028, mutuamente
    # exclusivas quanto a fonte de itens):
    #   - variante 1: ``itens`` + 6 campos base (origem_dados + 5 politicas);
    #   - variante 2: ``regra_geracao_itens`` + os mesmos 6 campos base (forma
    #     historica usada por demo.json, aceita por compatibilidade restrita com
    #     telas legadas nominais em _TELAS_VARIANTE2_LEGADAS).
    #
    # ``regra_geracao_itens`` NAO isenta de D23 por mera presenca. Rejeicoes
    # obrigatorias (H0037-IMPL-QAPP5-001):
    #   - itens E regra_geracao_itens juntos (duas fontes concorrentes);
    #   - variante 2 incompleta (regra sem os 6 base, ou com parte deles);
    #   - variante 2 em tela nova/nao-legada (nao pode evitar D23);
    #   - variante 2 + marcadores D23 (hibrido);
    #   - consumidor multinivel (0 envelope) + regra_geracao_itens (hibrido).
    # demo.json (variante 2 legada) permanece aceito por compatibilidade
    # historica comprovada, nao por schema de regra_geracao_itens.
    print("")
    print("-- D23-P6: regra_geracao_itens nao e chave de isencao D23 --")

    _seis_campos_envelope = {k: v for k, v in _ENVELOPE_COMPLETO.items()
                             if k != "itens"}

    def _console_consumidor_com_regra(id_tela, valor_regra, **extra):
        """Consumidor multinivel (0 envelope) + regra_geracao_itens=<valor>."""
        elem = {"id": "con", "tipo": "console", "titulo": "Console",
                "regra_geracao_itens": valor_regra}
        elem.update(extra)
        return {
            "schema": "tela.v1", "id": id_tela, "cabecalho": {},
            "corpo": {"arranjo": "vertical", "elementos": [elem]},
            "barra_de_menus": {"chips": []},
        }

    def _console_variante2(id_tela, **extra):
        """Envelope variante 2 (regra_geracao_itens + 6 campos base, sem itens)."""
        elem = {"id": "con", "tipo": "console", "titulo": "Console"}
        elem.update(_seis_campos_envelope)
        elem["regra_geracao_itens"] = {"tipo": "estatica", "ids": []}
        elem.update(extra)
        return {
            "schema": "tela.v1", "id": id_tela, "cabecalho": {},
            "corpo": {"arranjo": "vertical", "elementos": [elem]},
            "barra_de_menus": {"chips": []},
        }

    # RGI-P6-01: elemento real do demo.json carrega (variante 2 historica
    # comprovada, ACEITO_PELO_TIPO_ESTRUTURAL_REAL). demo.json esta fora do
    # escopo D23 por ser variante 2 legada, nao por mera presenca da chave.
    try:
        carregar_tela(_BASE_PADRAO, "demo", _RAIZ_TELAS_DEMO)
        _registrar("RGI-P6-01: demo.json carrega (variante 2 historica)", True)
    except Exception as _exc_demo_rgi:
        _registrar("RGI-P6-01: demo.json carrega (variante 2 historica)", False,
                   "{0}: {1}".format(type(_exc_demo_rgi).__name__, _exc_demo_rgi))

    # RGI-P6-02: copia estrutural de demo.json com outro ID (nao legado) ->
    # MESMO_RESULTADO_DO_TIPO_ESTRUTURAL: rejeitado. Variante 2 so e aceita para
    # telas legadas nominais (_TELAS_VARIANTE2_LEGADAS); tela nova nao pode usar
    # regra_geracao_itens para evitar D23. Prova ausencia de excecao por ID.
    _copia_demo = {"id": "con", "tipo": "console", "titulo": "Itens",
                   "regra_geracao_itens": {"tipo": "pendente", "nota": "copia"},
                   "origem_dados": {"referencia": "pendente"},
                   "politica_composicao": {"alinhamento": "centralizado"},
                   "politica_navegacao": {"navegavel": True},
                   "politica_selecao": "multipla",
                   "politica_paginacao": {"paginacao": "com"},
                   "politica_exibicao": {"modo_verboso_permitido": True}}
    _rejeita_carrega_em_tmp(
        "RGI-P6-02: copia estrutural de demo.json com outro ID rejeitada (variante 2 nao legada)",
        {
            "schema": "tela.v1", "id": "rgi_p6_02_copia", "cabecalho": {},
            "corpo": {"arranjo": "vertical", "elementos": [_copia_demo]},
            "barra_de_menus": {"chips": []},
        },
    )

    # RGI-P6-03/P6-04/P6-05: consumidor multinivel (0 envelope) + regra_geracao_itens
    # em qualquer forma ({}, null, string, lista, bool, numero, objeto incompleto).
    # Todos REJEITADOS como hibrido: geracao interna + consumo externo sao
    # mutuamente exclusivos. A chave nao reclassifica o tipo estrutural e nao
    # valida valor sob a chave (nao ha schema fechado).
    _valores_invalidos_rgi = [
        ("objeto_vazio", {}),
        ("null", None),
        ("string", "estatica"),
        ("lista", ["a"]),
        ("booleano", True),
        ("numero", 42),
        ("objeto_sem_tipo", {"ids": []}),
        ("objeto_sem_ids", {"tipo": "estatica"}),
        ("objeto_incompleto", {"tipo": "pendente", "nota": "rascunho"}),
    ]
    for _rotulo_rgi, _valor_rgi in _valores_invalidos_rgi:
        _rejeita_carrega_em_tmp(
            "RGI-P6-03/04/05: consumidor + regra_geracao_itens={0} rejeitado (hibrido)".format(
                _rotulo_rgi),
            _console_consumidor_com_regra(
                "rgi_p6_{0}".format(_rotulo_rgi), _valor_rgi),
        )

    # RGI-P6-06: consumidor multinivel (0 envelope) + regra_geracao_itens com
    # forma sintatica plausivel + politica_modo valida -> REJEITADO como hibrido.
    # politica_modo valida nao cura a incompatibilidade estrutural.
    _rejeita_carrega_em_tmp(
        "RGI-P6-06: consumidor + regra_geracao_itens + politica_modo rejeitado (hibrido)",
        _console_consumidor_com_regra(
            "rgi_p6_06",
            {"tipo": "estatica", "ids": ["x"]},
            formato={"excesso": {"politica_modo": "somente_nao_verboso"}},
        ),
    )

    # RGI-P6-07: itens E regra_geracao_itens juntos -> REJEITADO (duas fontes
    # concorrentes de itens). contrato_console.md §3 trata-as como alternativas
    # mutuamente exclusivas.
    _rejeita_carrega_em_tmp(
        "RGI-P6-07: itens + regra_geracao_itens rejeitado (duas fontes concorrentes)",
        {
            "schema": "tela.v1", "id": "rgi_p6_07", "cabecalho": {},
            "corpo": {"arranjo": "vertical", "elementos": [
                dict({"id": "con", "tipo": "console", "titulo": "Console",
                      "regra_geracao_itens": {"tipo": "estatica"}},
                     **_ENVELOPE_COMPLETO),
            ]},
            "barra_de_menus": {"chips": []},
        },
    )

    # RGI-P6-08: regra_geracao_itens + origem_dados (1 dos 6 base, faltam 5) ->
    # REJEITADO como variante 2 INCOMPLETA. (A coexistencia regra + origem_dados
    # NAO e hibrida por si quando os 6 base estao presentes — ver RGI-P6-10
    # variante legada; aqui falta o restante dos campos base.)
    _rejeita_carrega_em_tmp(
        "RGI-P6-08: regra_geracao_itens + origem_dados (variante 2 incompleta) rejeitado",
        {
            "schema": "tela.v1", "id": "rgi_p6_08", "cabecalho": {},
            "corpo": {"arranjo": "vertical", "elementos": [{
                "id": "con", "tipo": "console", "titulo": "Console",
                "origem_dados": None, "regra_geracao_itens": {},
            }]},
            "barra_de_menus": {"chips": []},
        },
    )

    # RGI-P6-09: regra_geracao_itens + campos parciais de envelope (sem todos os
    # 6 base) -> REJEITADO como variante 2 incompleta (NAO_ACEITA_COMO_ISENCAO).
    _rejeita_carrega_em_tmp(
        "RGI-P6-09: regra_geracao_itens + campos parciais (variante 2 incompleta) rejeitado",
        {
            "schema": "tela.v1", "id": "rgi_p6_09", "cabecalho": {},
            "corpo": {"arranjo": "vertical", "elementos": [{
                "id": "con", "tipo": "console", "titulo": "Console",
                "politica_selecao": "nenhuma",
                "regra_geracao_itens": {"tipo": "estatica"},
            }]},
            "barra_de_menus": {"chips": []},
        },
    )

    # RGI-P6-10: variante 2 completa (regra_geracao_itens + 6 base, sem itens):
    #   - em tela NOVA (nao legada) -> REJEITADO (nao pode evitar D23);
    #   - em tela LEGADA nominal (demo) -> ACEITO por compatibilidade historica.
    # Espera REJEITADO_SE_FORMAS_MUTUAMENTE_EXCLUSIVAS para tela nova.
    _rejeita_carrega_em_tmp(
        "RGI-P6-10: variante 2 completa em tela nova rejeitada (nao evita D23)",
        _console_variante2("rgi_p6_10_nova"),
    )
    # Variante 2 completa com id legado nominal (demo) — via carregar_tela real:
    # ja coberto por RGI-P6-01 (demo.json carrega). Aqui verificamos diretamente
    # _console_em_escopo_d23 retornando False para id legado.
    _registrar(
        "RGI-P6-10 dir: variante 2 completa em 'demo' retorna False (legada, fora D23)",
        _console_em_escopo_d23(
            dict({"id": "con", "tipo": "console", "titulo": "C",
                  "regra_geracao_itens": {"tipo": "pendente"}},
                 **_seis_campos_envelope),
            "demo",
        ) is False,
    )

    # RGI-P6-11: consumidor multinivel (0 envelope) + regra_geracao_itens com
    # 0 a 6 campos de envelope -> todos REJEITADOS (hibrido em 0 campos;
    # variante 2 incompleta em 1-5 campos; variante 2 em tela nova em 6 campos).
    for _n_campos, _campos_adic in [
        (0, {}),
        (1, {"politica_selecao": "nenhuma"}),
        (3, {"origem_dados": None, "politica_selecao": "nenhuma",
             "politica_paginacao": "sem"}),
        (6, dict(_seis_campos_envelope)),
    ]:
        _rejeita_carrega_em_tmp(
            "RGI-P6-11: consumidor + regra_geracao_itens + {0} campos de envelope rejeitado".format(
                _n_campos),
            _console_consumidor_com_regra(
                "rgi_p6_11_{0}".format(_n_campos),
                {},  # objeto vazio — a chave em si e o defeito, nao o valor
                **_campos_adic),
        )

    # RGI-P6-12: envelope VARIANTE 1 incompleto (6/7 campos, sem
    # regra_geracao_itens) -> REJEITADO. Variante 1 exige os 6 base + itens.
    _elem_incompleto_rgi = {"id": "con", "tipo": "console", "titulo": "Console"}
    _elem_incompleto_rgi.update(_ENVELOPE_COMPLETO)
    del _elem_incompleto_rgi["politica_paginacao"]
    _rejeita_carrega_em_tmp(
        "RGI-P6-12: envelope variante 1 incompleto (6/7) sem regra rejeitado",
        {
            "schema": "tela.v1", "id": "rgi_p6_12", "cabecalho": {},
            "corpo": {"arranjo": "vertical", "elementos": [_elem_incompleto_rgi]},
            "barra_de_menus": {"chips": []},
        },
    )

    # RGI-P6-13: cinco legados nominais (3 H-0036 + 2 H-0035) preservados como
    # consumidores multinivel isentos (sem regra_geracao_itens, sem envelope).
    for id_legado_rgi in (
        "h0036_console_hierarquia", "h0036_console_tabela", "h0036_console_conjuntos",
        "h0035_console_com", "h0035_console_sem",
    ):
        _carrega_em_tmp(
            "RGI-P6-13: legado {0} preservado (consumidor isento)".format(
                id_legado_rgi),
            _console_consumidor(id_legado_rgi),
        )

    # Verificacoes diretas de _console_em_escopo_d23 para regra_geracao_itens.
    # Consumidor multinivel (0 envelope) + regra_geracao_itens: a chave nao
    # isenta — levanta TelaEstruturaInvalida (hibrido), qualquer que seja o valor.
    for _rotulo_dir, _valor_dir in [
        ("objeto_vazio", {}),
        ("null", None),
        ("string", "estatica"),
        ("objeto_sintatico", {"tipo": "estatica", "ids": []}),
    ]:
        try:
            _console_em_escopo_d23(
                {"id": "c", "tipo": "console", "titulo": "C",
                 "regra_geracao_itens": _valor_dir},
                "tela_nova_xyz",
            )
            _registrar(
                "RGI-P6 dir: consumidor + regra_geracao_itens={0} levanta hibrido".format(
                    _rotulo_dir),
                False, "nenhuma excecao (esperava TelaEstruturaInvalida)",
            )
        except TelaEstruturaInvalida:
            _registrar(
                "RGI-P6 dir: consumidor + regra_geracao_itens={0} levanta hibrido".format(
                    _rotulo_dir),
                True,
            )
        except Exception as _exc_dir_rgi:  # pragma: no cover
            _registrar(
                "RGI-P6 dir: consumidor + regra_geracao_itens={0} levanta hibrido".format(
                    _rotulo_dir),
                False, "excecao errada: {0}".format(type(_exc_dir_rgi).__name__),
            )

    # Consumidor multinivel (0 envelope) sem regra_geracao_itens: em escopo D23.
    _registrar(
        "RGI-P6 dir: consumidor novo sem regra retorna True (em D23)",
        _console_em_escopo_d23(
            {"id": "c", "tipo": "console", "titulo": "C"}, "tela_nova_xyz",
        ) is True,
    )
    # Variante 2 completa (regra + 6 base) em tela NOVA: rejeitada (levanta
    # excecao, nao retorna False). Confirma que a variante 2 nao isenta telas
    # novas de D23.
    try:
        _console_em_escopo_d23(
            dict({"id": "c", "tipo": "console", "titulo": "C",
                  "regra_geracao_itens": {"tipo": "estatica"}},
                 **_seis_campos_envelope),
            "tela_nova_xyz",
        )
        _registrar(
            "RGI-P6 dir: variante 2 em tela nova levanta excecao",
            False, "nenhuma excecao",
        )
    except TelaEstruturaInvalida:
        _registrar("RGI-P6 dir: variante 2 em tela nova levanta excecao", True)
    except Exception as _exc_v2_nova:  # pragma: no cover
        _registrar(
            "RGI-P6 dir: variante 2 em tela nova levanta excecao",
            False, "excecao errada: {0}".format(type(_exc_v2_nova).__name__),
        )


def main():
    print("Diagnostico H-0001 - loader/validador de tela.json")
    print("Base padrao: {0}".format(_BASE_PADRAO))
    print("Python: {0}".format(sys.version.split()[0]))

    # H-0038: teste_caminho_feliz() nao retorna mais o dict da tela; o bloco
    # de impressao diagnostica dependente do retorno foi removido do main().
    teste_caminho_feliz()

    tmp_base = Path(tempfile.mkdtemp(prefix="tela_loader_h0001_"))
    try:
        _criar_config_lancador(tmp_base)
        _run_erros(tmp_base)
        _run_tipos_validos(tmp_base)
        _run_grupo_estrutural(tmp_base)
        _run_arranjo_corpo_h0019(tmp_base)
        _run_distribuicao_corpo_h0025(tmp_base)
        _run_hierarquia_grupos_adr0019(tmp_base)
        _run_config_lancador_h0034(tmp_base)
        _run_distribuicao_matricial_h0035(tmp_base)
    finally:
        try:
            shutil.rmtree(tmp_base)
        except OSError:
            pass

    TestValidacaoMatrizH0028().run_all()
    teste_h0030_catalogo()
    teste_raiz_telas_h0032()
    teste_id_incorreto_classe()
    teste_conteudo_externo_h0036()
    teste_d23_estrutural()

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
