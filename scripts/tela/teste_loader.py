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
    TIPOS_CORPO_VALIDOS,
    TelaArquivoNaoEncontrado,
    TelaCampoObrigatorioAusente,
    TelaElementoSemId,
    TelaElementoSemTipo,
    TelaEstruturaInvalida,
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
    _registrar(
        "tela.corpo presente",
        isinstance(tela.get("corpo"), dict),
    )
    _registrar(
        "tela.corpo.arranjo preservado",
        tela.get("corpo", {}).get("arranjo") == "sobreposto",
        "arranjo={0!r}".format(tela.get("corpo", {}).get("arranjo")),
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
        "chip_estilo.tela_destino == 'pendente' carregado sem erro",
        isinstance(chip_estilo, dict)
        and chip_estilo.get("acao", {}).get("tela_destino") == "pendente",
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
        "lancador_principal.itens e lista com 1 item (H-0010A)",
        isinstance(itens_lancador, list) and len(itens_lancador) == 1,
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
