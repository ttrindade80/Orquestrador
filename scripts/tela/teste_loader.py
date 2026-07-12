"""Diagnostico do loader/validador de tela.json (H-0001).

Executavel via:
    python tela/teste_loader.py

Cobre os criterios de aceite testaveis do handoff H-0001:
- carregamento do arquivo real config/telas/orquestrador.json;
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
    TelaEstruturaInvalida,
    TelaGrupoInvalido,
    TelaIdIncorreto,
    TelaIdNaoCoincideComArquivo,
    TelaJsonInvalido,
    TelaTipoDesconhecido,
    carregar_tela,
)


_RESULTADOS = []


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
                {"id": "c1", "tipo": "console"},
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
    print("== Carregamento do arquivo real config/telas/orquestrador.json ==")
    try:
        tela = carregar_tela(_BASE_PADRAO, "orquestrador")
    except Exception as exc:  # pragma: no cover - diagnostico
        _registrar("carregar_tela(orquestrador)", False,
                   "{0}: {1}".format(type(exc).__name__, exc))
        return None
    _registrar("carregar_tela(orquestrador)", True)

    _registrar(
        "tela.id == 'orquestrador'",
        tela.get("id") == "orquestrador",
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
    # H-0025: orquestrador real declara distribuicao fracao [2,1,2].
    dist_orq = tela.get("corpo", {}).get("distribuicao")
    _registrar(
        "H-0025: orquestrador declara corpo.distribuicao (fracao [2,1,2])",
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
        and tela.get("_raw", {}).get("id") == "orquestrador",
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
        "lancador_principal.itens e lista com 2 itens (H-0013)",
        isinstance(itens_lancador, list) and len(itens_lancador) == 2,
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

    return tela


def teste_erros(tmp_base):
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


def teste_tipos_validos(tmp_base):
    print("")
    print("== Aceitacao dos tipos validos (taxonomia fechada) ==")
    for tipo in ("console", "lancador", "dashboard"):
        nome_arquivo = "tipo_ok_" + tipo
        _escrever_tela(tmp_base, nome_arquivo,
                       {"schema": "tela.v1", "id": nome_arquivo,
                        "cabecalho": {}, "barra_de_menus": {},
                        "corpo": {"elementos": [
                            {"id": "e1", "tipo": tipo}
                        ]}})
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


def teste_grupo_estrutural(tmp_base):
    print("")
    print("== Grupo estrutural minimo (H-0012) ==")

    print("-- Carregamento do arquivo real config/telas/grupo_minimo.json --")
    try:
        tela = carregar_tela(_BASE_PADRAO, "grupo_minimo")
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
                        "elementos": [{"id": "c_interno", "tipo": "console"}]},
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
    for id_plano in ("orquestrador", "destino_minimo", "stub_b"):
        try:
            carregar_tela(_BASE_PADRAO, id_plano)
            _registrar("lista plana '{0}' carrega sem erro".format(id_plano),
                       True)
        except Exception as exc:  # pragma: no cover - diagnostico
            _registrar("lista plana '{0}' carrega sem erro".format(id_plano),
                       False, "{0}: {1}".format(type(exc).__name__, exc))

    print("")
    print("-- H-0016: os 4 JSONs ativos com distribuicao objeto canônico --")
    for id_tela in ("orquestrador", "grupo_minimo", "destino_minimo", "stub_b"):
        try:
            t = carregar_tela(_BASE_PADRAO, id_tela)
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


def teste_arranjo_corpo_h0019(tmp_base):
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


def teste_distribuicao_corpo_h0025(tmp_base):
    print("")
    print("== H-0025: validacao de corpo.distribuicao (igual/percentual/fracao) ==")

    def _tela_dist(id_tela, distribuicao, n_elementos=3):
        elementos = [
            {"id": "e{0}".format(i), "tipo": "console"} for i in range(n_elementos)
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


def teste_hierarquia_grupos_adr0019(tmp_base):
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
             "elementos": [{"id": "c1", "tipo": "console"}]},
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
                 {"id": "c1", "tipo": "console"},
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
                  "elementos": [{"id": "c1", "tipo": "console"}]},
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
                       "elementos": [{"id": "c1", "tipo": "console"}]},
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
                           {"id": "c1", "tipo": "console"},
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
                            "elementos": [{"id": "c1", "tipo": "console"}]},
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
             "elementos": [{"id": "c1", "tipo": "console"}]},
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
                  "elementos": [{"id": "c1", "tipo": "console"}]},
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
            {"id": "c0", "tipo": "console"},
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
             "elementos": [{"id": "c1", "tipo": "console"}]},
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
             "elementos": [{"id": "c1", "tipo": "console"}]},
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
                 {"id": "c1", "tipo": "console"},
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
                 {"id": "c1", "tipo": "console"},
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
                 {"id": "c1", "tipo": "console"},
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
                 {"id": "c1", "tipo": "console"},
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
             "elementos": [{"id": "c1", "tipo": "console"}]},
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
             "elementos": [{"id": "c1", "tipo": "console"}]},
        ],
    }))
    _espera_excecao(
        "grupo com arranjo invalido ('diagonal') -> TelaGrupoInvalido",
        lambda: carregar_tela(tmp_base, "h_g_arranjo_inv"),
        TelaGrupoInvalido,
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


def main():
    print("Diagnostico H-0001 - loader/validador de tela.json")
    print("Base padrao: {0}".format(_BASE_PADRAO))
    print("Python: {0}".format(sys.version.split()[0]))

    tela_real = teste_caminho_feliz()

    tmp_base = Path(tempfile.mkdtemp(prefix="tela_loader_h0001_"))
    try:
        teste_erros(tmp_base)
        teste_tipos_validos(tmp_base)
        teste_grupo_estrutural(tmp_base)
        teste_arranjo_corpo_h0019(tmp_base)
        teste_distribuicao_corpo_h0025(tmp_base)
        teste_hierarquia_grupos_adr0019(tmp_base)
    finally:
        try:
            shutil.rmtree(tmp_base)
        except OSError:
            pass

    teste_id_incorreto_classe()

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

    if tela_real is not None:
        print("")
        print("== Representacao interna carregada (resumo) ==")
        print("id: {0}".format(tela_real.get("id")))
        print("schema: {0}".format(tela_real.get("schema")))
        print("corpo.arranjo: {0}".format(
            tela_real.get("corpo", {}).get("arranjo")
        ))
        for el in tela_real.get("corpo", {}).get("elementos", []):
            if isinstance(el, dict):
                print("  elemento: id={0!r} tipo={1!r}".format(
                    el.get("id"), el.get("tipo")
                ))

    return 0 if falharam == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
