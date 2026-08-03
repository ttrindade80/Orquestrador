"""Carregamento e materialização do estilo global."""

import json
from dataclasses import dataclass

from tela.carregamento.caminho_base import _para_base
from tela.carregamento.erros import EstiloErro


@dataclass(frozen=True)
class EstiloResolvido:
    """Representacao de runtime do estilo global resolvido (H-0039 D6.2).

    ``frozen=True`` impede alteracao acidental em runtime (contrato_estilo.md
    R-4). Os 20 campos cobrem borda (7), chip (5), indicadores (6),
    ``cor_inativo`` (1; H-0041 P04) e ``cor_alerta`` (1; H-0044 / ADR-0037).
    Nenhum campo pode ser omitido -- a configuracao parcialmente resolvida
    nao pode produzir instancia de ``EstiloResolvido``.
    """

    # Borda -- 7 campos (contrato_estilo.md secao 3.1).
    canto_superior_esquerdo: str
    canto_superior_direito: str
    canto_inferior_esquerdo: str
    canto_inferior_direito: str
    traco_superior: str
    traco_inferior: str
    lateral: str
    # Chip -- 5 campos (contrato_estilo.md secao 3.2).
    caractere_esquerdo: str
    caractere_direito: str
    cor_texto: str
    caixa_alta: bool
    cor_fundo: str
    # Indicadores -- 6 campos (contrato_estilo.md secao 3.3).
    concluido_on: str
    concluido_off: str
    selecionado_simbolo: str
    selecionado_off: str
    incluido_on: str
    incluido_off: str
    # Estados dinamicos de cor -- secao 3.5 (H-0041 P04 / H-0044).
    # Defaults somente para construtores manuais de teste; ``carregar_estilo``
    # exige ambos os campos no JSON (sem fallback silencioso).
    cor_inativo: str = "padrão"
    cor_alerta: str = "padrão"


def carregar_estilo(caminho_base=None):
    """Carrega, valida e materializa ``config/estilo.json`` (H-0039 / ADR-0030).

    Le o arquivo uma unica vez por inicializacao da execucao, valida toda a
    estrutura (secoes obrigatórias, ``preset_default``, catálogos, tipos,
    comprimento de caracteres conforme R-6 via ``len(valor) == 1``), resolve
    os presets ativos e devolve um ``EstiloResolvido`` integralmente válido.

    Falha antes de disponibilizar qualquer estilo parcial: toda condicao
    invalida levanta ``EstiloErro``. Nao existe fallback silencioso para
    preset inexistente (V-14 a V-17). O renderer nunca chama esta funcao --
    ele recebe o objeto ja resolvido.

    ``caminho_base`` segue a convenção de ``carregar_tela``: quando ``None``,
    usa a raiz do repositorio derivada de
    ``Path(__file__).resolve().parent.parent``.
    """
    base = _para_base(caminho_base)
    caminho = base / "config" / "estilo.json"

    # V-01: arquivo ausente -- erro explicito, encerramento imediato.
    if not caminho.is_file():
        raise EstiloErro(
            "Arquivo de estilo ausente: {0}".format(caminho)
        )

    # V-02: conteudo nao e JSON valido.
    try:
        texto = caminho.read_text(encoding="utf-8")
    except OSError as exc:
        raise EstiloErro(
            "Falha ao ler arquivo de estilo {0}: {1}".format(caminho, exc)
        )
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise EstiloErro(
            "JSON invalido em {0}: {1}".format(caminho, exc)
        )

    if not isinstance(dados, dict):
        raise EstiloErro(
            "Raiz de {0} deve ser um objeto JSON; encontrado: {1}".format(
                caminho, type(dados).__name__
            )
        )

    # V-03 a V-05: secoes obrigatórias.
    for secao in ("borda", "chip", "indicadores"):
        if secao not in dados:
            raise EstiloErro(
                "Secao obrigatoria ausente em config/estilo.json: {0!r}".format(
                    secao
                )
            )

    borda_cfg = dados["borda"]
    chip_cfg = dados["chip"]
    indicadores_cfg = dados["indicadores"]

    borda = _resolver_borda(borda_cfg)
    chip = _resolver_chip(chip_cfg)
    concluido_on, concluido_off, selecionado_simbolo, selecionado_off, \
        incluido_on, incluido_off = _resolver_indicadores(indicadores_cfg)
    cor_inativo = _resolver_cor_inativo(dados)
    cor_alerta = _resolver_cor_alerta(dados)

    # V-29: so se chega aqui com todos os campos materializados; a construcao
    # abaixo falharia com TypeError se algum campo estivesse ausente, mas as
    # validacoes acima ja garantem presenca e tipo de cada valor.
    return EstiloResolvido(
        canto_superior_esquerdo=borda["canto_superior_esquerdo"],
        canto_superior_direito=borda["canto_superior_direito"],
        canto_inferior_esquerdo=borda["canto_inferior_esquerdo"],
        canto_inferior_direito=borda["canto_inferior_direito"],
        traco_superior=borda["traco_superior"],
        traco_inferior=borda["traco_inferior"],
        lateral=borda["lateral"],
        caractere_esquerdo=chip["caractere_esquerdo"],
        caractere_direito=chip["caractere_direito"],
        cor_texto=chip["cor_texto"],
        caixa_alta=chip["caixa_alta"],
        cor_fundo=chip["cor_fundo"],
        concluido_on=concluido_on,
        concluido_off=concluido_off,
        selecionado_simbolo=selecionado_simbolo,
        selecionado_off=selecionado_off,
        incluido_on=incluido_on,
        incluido_off=incluido_off,
        cor_inativo=cor_inativo,
        cor_alerta=cor_alerta,
    )


def _resolver_cor_inativo(dados):
    """Le e valida ``cor_inativo`` (contrato_estilo.md secao 3.5 / H-0041 P04).

    Segue o mesmo mecanismo de tipo das demais cores semanticas (V-26:
    deve ser texto). Ausencia ou tipo invalido levantam ``EstiloErro`` --
    sem fallback silencioso. O valor permanece como nome semantico; a
    traducao para sequencia de terminal e responsabilidade do renderer (R-7).
    """
    if "cor_inativo" not in dados:
        raise EstiloErro(
            "Campo obrigatorio ausente em config/estilo.json: 'cor_inativo'"
        )
    cor_inativo = dados["cor_inativo"]
    if not isinstance(cor_inativo, str):  # V-26
        raise EstiloErro(
            "cor_inativo deve ser texto; encontrado: {0}".format(
                type(cor_inativo).__name__
            )
        )
    return cor_inativo


def _resolver_cor_alerta(dados):
    """Le e valida ``cor_alerta`` (contrato_estilo.md secao 3.5 / H-0044).

    Validacao proporcional a ``cor_inativo``: campo obrigatorio, tipo texto,
    sem fallback. O valor permanece como nome semantico; a traducao ANSI e
    responsabilidade do renderer (R-7).
    """
    if "cor_alerta" not in dados:
        raise EstiloErro(
            "Campo obrigatorio ausente em config/estilo.json: 'cor_alerta'"
        )
    cor_alerta = dados["cor_alerta"]
    if not isinstance(cor_alerta, str):  # V-26
        raise EstiloErro(
            "cor_alerta deve ser texto; encontrado: {0}".format(
                type(cor_alerta).__name__
            )
        )
    return cor_alerta


def _exigir_secao(cfg, secao, caminho_logico):
    """Devolve ``cfg[secao]`` exigindo que seja dict; senao EstiloErro."""
    if not isinstance(cfg, dict):
        raise EstiloErro(
            "{0} deve ser um objeto; encontrado: {1}".format(
                caminho_logico, type(cfg).__name__
            )
        )
    sub = cfg.get(secao)
    if not isinstance(sub, dict):
        raise EstiloErro(
            "{0}.{1} ausente ou nao e objeto".format(caminho_logico, secao)
        )
    return sub


def _resolver_preset_default(cfg, caminho_logico):
    """Exige ``preset_default`` presente e string (V-06..V-09)."""
    if "preset_default" not in cfg:
        raise EstiloErro(
            "{0}.preset_default ausente (sem fallback)".format(caminho_logico)
        )
    valor = cfg["preset_default"]
    if not isinstance(valor, str):
        raise EstiloErro(
            "{0}.preset_default deve ser texto; encontrado: {1}".format(
                caminho_logico, type(valor).__name__
            )
        )
    return valor


def _resolver_catalogo(cfg, caminho_logico):
    """Exige ``presets`` presente e nao vazio (V-10..V-13)."""
    if "presets" not in cfg:
        raise EstiloErro(
            "{0}.presets ausente (catalogo obrigatorio)".format(caminho_logico)
        )
    presets = cfg["presets"]
    if not isinstance(presets, dict) or not presets:
        raise EstiloErro(
            "{0}.presets vazio ou nao e objeto (catalogo obrigatorio)".format(
                caminho_logico
            )
        )
    return presets


def _resolver_preset_ativo(presets, preset_default, caminho_logico):
    """Devolve o preset ativo, sem fallback silencioso (V-14..V-17)."""
    ativo = presets.get(preset_default)
    if not isinstance(ativo, dict):
        raise EstiloErro(
            "{0}.preset_default {1!r} nao existe no catalogo "
            "(sem fallback)".format(caminho_logico, preset_default)
        )
    return ativo


def _campo_obrigatorio(preset, campo, caminho_logico):
    """Exige campo presente (V-18..V-23)."""
    if campo not in preset:
        raise EstiloErro(
            "Campo obrigatorio ausente: {0}.{1}".format(caminho_logico, campo)
        )
    return preset[campo]


def _validar_caractere(valor, caminho_logico):
    """Valida string de comprimento 1 (R-6 via ``len() == 1``).

    Cobre V-24 (nao string), V-27 (``len != 1``) e V-28 (string vazia). O
    limite tecnico de code point -- e nao largura visual de terminal -- e o
    aprovado pelo handoff H-0039 D6.6 e ADR-0030 D9.
    """
    if not isinstance(valor, str):
        raise EstiloErro(
            "{0} deve ser texto; encontrado: {1}".format(
                caminho_logico, type(valor).__name__
            )
        )
    if len(valor) != 1:
        raise EstiloErro(
            "{0} deve ter exatamente 1 caractere (R-6); "
            "encontrado: {1!r} (len={2})".format(
                caminho_logico, valor, len(valor)
            )
        )
    return valor


def _resolver_borda(borda_cfg):
    """Resolve o preset ativo de borda e materializa os 7 campos."""
    if not isinstance(borda_cfg, dict):
        raise EstiloErro("Secao 'borda' deve ser um objeto")
    preset_default = _resolver_preset_default(borda_cfg, "borda")
    presets = _resolver_catalogo(borda_cfg, "borda")
    ativo = _resolver_preset_ativo(presets, preset_default, "borda.presets")

    campos = {}
    for campo in (
        "canto_superior_esquerdo", "canto_superior_direito",
        "canto_inferior_esquerdo", "canto_inferior_direito",
        "traco_superior", "traco_inferior", "lateral",
    ):
        valor = _campo_obrigatorio(ativo, campo, "borda.presets[{0!r}]".format(
            preset_default
        ))
        campos[campo] = _validar_caractere(
            valor, "borda.presets[{0!r}].{1}".format(preset_default, campo)
        )
    return campos


def _resolver_chip(chip_cfg):
    """Resolve o preset ativo de chip e materializa os 5 campos."""
    if not isinstance(chip_cfg, dict):
        raise EstiloErro("Secao 'chip' deve ser um objeto")
    preset_default = _resolver_preset_default(chip_cfg, "chip")
    presets = _resolver_catalogo(chip_cfg, "chip")
    ativo = _resolver_preset_ativo(presets, preset_default, "chip.presets")

    caractere_esquerdo = _campo_obrigatorio(
        ativo, "caractere_esquerdo",
        "chip.presets[{0!r}]".format(preset_default),
    )
    caractere_direito = _campo_obrigatorio(
        ativo, "caractere_direito",
        "chip.presets[{0!r}]".format(preset_default),
    )
    cor_texto = _campo_obrigatorio(
        ativo, "cor_texto", "chip.presets[{0!r}]".format(preset_default),
    )
    cor_fundo = _campo_obrigatorio(
        ativo, "cor_fundo", "chip.presets[{0!r}]".format(preset_default),
    )
    if "caixa_alta" not in ativo:
        raise EstiloErro(
            "Campo obrigatorio ausente: chip.presets[{0!r}].caixa_alta".format(
                preset_default
            )
        )
    caixa_alta = ativo["caixa_alta"]
    if not isinstance(caixa_alta, bool):  # V-25
        raise EstiloErro(
            "chip.presets[{0!r}].caixa_alta deve ser booleano; encontrado: "
            "{1}".format(preset_default, type(caixa_alta).__name__)
        )
    if not isinstance(cor_texto, str):  # V-26
        raise EstiloErro(
            "chip.presets[{0!r}].cor_texto deve ser texto".format(
                preset_default
            )
        )
    if not isinstance(cor_fundo, str):  # V-26
        raise EstiloErro(
            "chip.presets[{0!r}].cor_fundo deve ser texto".format(
                preset_default
            )
        )

    return {
        "caractere_esquerdo": _validar_caractere(
            caractere_esquerdo,
            "chip.presets[{0!r}].caractere_esquerdo".format(preset_default),
        ),
        "caractere_direito": _validar_caractere(
            caractere_direito,
            "chip.presets[{0!r}].caractere_direito".format(preset_default),
        ),
        "cor_texto": cor_texto,
        "caixa_alta": caixa_alta,
        "cor_fundo": cor_fundo,
    }


def _resolver_indicadores(indicadores_cfg):
    """Materializa os 6 campos de indicadores.

    - ``concluido``: par direto ``on``/``off``.
    - ``selecionado``: preset ativo -> ``simbolo``; campo direto ``off``.
    - ``incluido``: preset ativo -> ``on``/``off``.
    """
    if not isinstance(indicadores_cfg, dict):
        raise EstiloErro("Secao 'indicadores' deve ser um objeto")

    # --- concluido (par direto) ---
    concluido = _exigir_secao(indicadores_cfg, "concluido", "indicadores")
    concluido_on = _campo_obrigatorio(
        concluido, "on", "indicadores.concluido"
    )  # V-22
    concluido_off = _campo_obrigatorio(
        concluido, "off", "indicadores.concluido"
    )  # V-22
    concluido_on = _validar_caractere(concluido_on, "indicadores.concluido.on")
    concluido_off = _validar_caractere(
        concluido_off, "indicadores.concluido.off"
    )

    # --- selecionado (preset + campo direto off) ---
    selecionado = _exigir_secao(
        indicadores_cfg, "selecionado", "indicadores"
    )
    sel_default = _resolver_preset_default(
        selecionado, "indicadores.selecionado"
    )  # V-08
    sel_presets = _resolver_catalogo(
        selecionado, "indicadores.selecionado"
    )  # V-12
    sel_ativo = _resolver_preset_ativo(
        sel_presets, sel_default, "indicadores.selecionado.presets"
    )  # V-16
    simbolo = _campo_obrigatorio(
        sel_ativo, "simbolo", "indicadores.selecionado.presets[{0!r}]".format(
            sel_default
        ),
    )  # V-20
    selecionado_simbolo = _validar_caractere(
        simbolo,
        "indicadores.selecionado.presets[{0!r}].simbolo".format(sel_default),
    )
    selecionado_off = _campo_obrigatorio(
        selecionado, "off", "indicadores.selecionado"
    )  # V-23
    selecionado_off = _validar_caractere(
        selecionado_off, "indicadores.selecionado.off"
    )

    # --- incluido (preset on/off) ---
    incluido = _exigir_secao(indicadores_cfg, "incluido", "indicadores")
    inc_default = _resolver_preset_default(
        incluido, "indicadores.incluido"
    )  # V-09
    inc_presets = _resolver_catalogo(
        incluido, "indicadores.incluido"
    )  # V-13
    inc_ativo = _resolver_preset_ativo(
        inc_presets, inc_default, "indicadores.incluido.presets"
    )  # V-17
    inc_on = _campo_obrigatorio(
        inc_ativo, "on", "indicadores.incluido.presets[{0!r}]".format(
            inc_default
        ),
    )  # V-21
    inc_off = _campo_obrigatorio(
        inc_ativo, "off", "indicadores.incluido.presets[{0!r}]".format(
            inc_default
        ),
    )  # V-21
    incluido_on = _validar_caractere(
        inc_on,
        "indicadores.incluido.presets[{0!r}].on".format(inc_default),
    )
    incluido_off = _validar_caractere(
        inc_off,
        "indicadores.incluido.presets[{0!r}].off".format(inc_default),
    )

    return (
        concluido_on, concluido_off,
        selecionado_simbolo, selecionado_off,
        incluido_on, incluido_off,
    )
