"""Carregamento, materialização e aplicação controlada do estilo global."""

import copy
import json
import os
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass

from tela.carregamento.caminho_base import _para_base
from tela.carregamento.erros import EstiloErro


@dataclass(frozen=True)
class EstiloResolvido:
    """Representacao de runtime do estilo global resolvido (H-0039 D6.2).

    ``frozen=True`` impede alteracao acidental em runtime (contrato_estilo.md
    R-4). Os campos cobrem borda (7), chip (7), indicadores (6),
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
    # Campos opcionais de assimetria de fundo do chip (contrato 3.2).
    cor_fundo_esquerdo: str = None
    cor_fundo_direito: str = None


CAMINHOS_PRESET_DEFAULT_PERMITIDOS = (
    ("borda", "preset_default"),
    ("chip", "preset_default"),
    ("indicadores", "selecionado", "preset_default"),
    ("indicadores", "incluido", "preset_default"),
)
"""Caminhos que podem ser alterados por um candidato do ITEM-0010."""


@dataclass(frozen=True)
class _EstadoEstiloRuntime:
    """Estado privado trocado integralmente no runtime."""

    baseline: dict
    candidato: dict
    global_vigente: EstiloResolvido


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
    return materializar_configuracao_estilo(
        _ler_configuracao_estilo(caminho_base)
    )


def _ler_configuracao_estilo(caminho_base=None):
    """Le o documento completo de estilo sem descartar campos extras."""
    base = _para_base(caminho_base)
    caminho = base / "config" / "estilo.json"

    if not caminho.is_file():
        raise EstiloErro("Arquivo de estilo ausente: {0}".format(caminho))
    try:
        texto = caminho.read_text(encoding="utf-8")
    except OSError as exc:
        raise EstiloErro(
            "Falha ao ler arquivo de estilo {0}: {1}".format(caminho, exc)
        ) from exc
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise EstiloErro(
            "JSON invalido em {0}: {1}".format(caminho, exc)
        ) from exc
    if not isinstance(dados, dict):
        raise EstiloErro(
            "Raiz de {0} deve ser um objeto JSON; encontrado: {1}".format(
                caminho, type(dados).__name__
            )
        )
    return dados


def carregar_configuracao_estilo(caminho_base=None):
    """Retorna snapshot completo e validado da configuração persistida."""
    dados = _ler_configuracao_estilo(caminho_base)
    materializar_configuracao_estilo(dados)
    return copy.deepcopy(dados)


def materializar_configuracao_estilo(configuracao):
    """Valida e resolve uma configuração completa somente em memória."""
    if not isinstance(configuracao, Mapping):
        raise EstiloErro(
            "Configuracao de estilo deve ser um objeto; encontrado: {0}".format(
                type(configuracao).__name__
            )
        )
    dados = dict(configuracao)
    for secao in ("borda", "chip", "indicadores"):
        if secao not in dados:
            raise EstiloErro(
                "Secao obrigatoria ausente em config/estilo.json: {0!r}".format(
                    secao
                )
            )

    borda = _resolver_borda(dados["borda"])
    chip = _resolver_chip(dados["chip"])
    concluido_on, concluido_off, selecionado_simbolo, selecionado_off, \
        incluido_on, incluido_off = _resolver_indicadores(dados["indicadores"])
    cor_inativo = _resolver_cor_inativo(dados)
    cor_alerta = _resolver_cor_alerta(dados)

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
        cor_fundo_esquerdo=chip["cor_fundo_esquerdo"],
        cor_fundo_direito=chip["cor_fundo_direito"],
        concluido_on=concluido_on,
        concluido_off=concluido_off,
        selecionado_simbolo=selecionado_simbolo,
        selecionado_off=selecionado_off,
        incluido_on=incluido_on,
        incluido_off=incluido_off,
        cor_inativo=cor_inativo,
        cor_alerta=cor_alerta,
    )


def criar_candidato_estilo(baseline):
    """Cria candidato independente a partir de um snapshot completo."""
    if not isinstance(baseline, Mapping):
        raise EstiloErro(
            "Baseline de estilo deve ser um objeto; encontrado: {0}".format(
                type(baseline).__name__
            )
        )
    candidato = copy.deepcopy(dict(baseline))
    materializar_configuracao_estilo(candidato)
    return candidato


def _normalizar_caminho_preset(caminho):
    if isinstance(caminho, str):
        partes = tuple(caminho.split("."))
    elif isinstance(caminho, (tuple, list)):
        partes = tuple(caminho)
    else:
        partes = ()
    if partes not in CAMINHOS_PRESET_DEFAULT_PERMITIDOS:
        raise EstiloErro(
            "Caminho de candidato nao editavel: {0!r}".format(caminho)
        )
    return partes


def definir_preset_candidato(candidato, caminho, preset):
    """Altera somente um dos quatro ``preset_default`` permitidos."""
    if not isinstance(candidato, dict):
        raise EstiloErro(
            "Candidato de estilo deve ser um objeto mutavel; encontrado: {0}".format(
                type(candidato).__name__
            )
        )
    partes = _normalizar_caminho_preset(caminho)
    if not isinstance(preset, str):
        raise EstiloErro("preset_default do candidato deve ser texto")

    secao = candidato
    for parte in partes[:-1]:
        secao = secao.get(parte)
        if not isinstance(secao, dict):
            raise EstiloErro(
                "Estrutura ausente no candidato em {0!r}".format(partes)
            )
    catalogo = secao.get("presets")
    if not isinstance(catalogo, dict) or preset not in catalogo:
        raise EstiloErro(
            "Preset {0!r} nao existe no catalogo de {1}".format(
                preset, ".".join(partes[:-1])
            )
        )
    secao[partes[-1]] = preset
    return candidato


def comparar_configuracoes_estilo(esquerda, direita):
    """Compara documentos completos sem depender de ordenação textual."""
    if not isinstance(esquerda, Mapping) or not isinstance(direita, Mapping):
        raise EstiloErro("Comparacao exige duas configuracoes objeto")
    return dict(esquerda) == dict(direita)


def materializar_estilo_local(candidato):
    """Materializa um candidato sem persistir e sem publicar globalmente."""
    return materializar_configuracao_estilo(candidato)


def _exigir_candidato_dict(candidato):
    if not isinstance(candidato, Mapping):
        raise EstiloErro(
            "Candidato de estilo deve ser um objeto; encontrado: {0}".format(
                type(candidato).__name__
            )
        )
    documento = copy.deepcopy(dict(candidato))
    materializar_configuracao_estilo(documento)
    return documento


def persistir_configuracao_estilo(candidato, caminho_destino):
    """Persiste candidato completo com substituição atômica no destino dado."""
    if caminho_destino is None:
        raise EstiloErro("Destino de persistencia deve ser fornecido")
    documento = _exigir_candidato_dict(candidato)
    destino = os.fspath(caminho_destino)
    if not destino:
        raise EstiloErro("Destino de persistencia nao pode ser vazio")

    temporario = None
    try:
        diretorio = os.path.dirname(os.path.abspath(destino))
        os.makedirs(diretorio, exist_ok=True)
        nome = os.path.basename(destino)
        fd, temporario = tempfile.mkstemp(
            prefix=".{0}.".format(nome), suffix=".tmp", dir=diretorio
        )
        with os.fdopen(fd, "w", encoding="utf-8") as arquivo:
            json.dump(
                documento,
                arquivo,
                ensure_ascii=False,
                indent=2,
                allow_nan=False,
            )
            arquivo.write("\n")
            arquivo.flush()
            os.fsync(arquivo.fileno())
        os.replace(temporario, destino)
        temporario = None
    except (OSError, TypeError, ValueError) as exc:
        raise EstiloErro(
            "Falha ao persistir estilo em {0}: {1}".format(destino, exc)
        ) from exc
    finally:
        if temporario is not None:
            try:
                os.unlink(temporario)
            except OSError:
                pass
    return destino


class EstadoEstiloRuntime:
    """Mantém baseline, candidato e materialização global separados."""

    def __init__(self, caminho_base=None):
        self._caminho_base = _para_base(caminho_base)
        baseline = carregar_configuracao_estilo(self._caminho_base)
        global_vigente = materializar_configuracao_estilo(baseline)
        self._estado = _EstadoEstiloRuntime(
            baseline=baseline,
            candidato=copy.deepcopy(baseline),
            global_vigente=global_vigente,
        )

    @property
    def baseline(self):
        return copy.deepcopy(self._estado.baseline)

    @property
    def candidato(self):
        return copy.deepcopy(self._estado.candidato)

    @property
    def global_vigente(self):
        return self._estado.global_vigente

    @property
    def materializacao_global(self):
        return self._estado.global_vigente

    @property
    def caminho_destino(self):
        """Caminho canonico somente-leitura de ``config/estilo.json`` (H-0068).

        Mesma composicao ja usada por ``_ler_configuracao_estilo``. Nao
        resolve caminho de forma independente nem admite atribuicao.
        """
        return self._caminho_base / "config" / "estilo.json"

    def criar_candidato(self):
        candidato = criar_candidato_estilo(self._estado.baseline)
        self._estado = _EstadoEstiloRuntime(
            baseline=self._estado.baseline,
            candidato=candidato,
            global_vigente=self._estado.global_vigente,
        )
        return copy.deepcopy(candidato)

    def materializar_local(self, candidato):
        documento = _exigir_candidato_dict(candidato)
        materializacao = materializar_estilo_local(documento)
        self._estado = _EstadoEstiloRuntime(
            baseline=self._estado.baseline,
            candidato=documento,
            global_vigente=self._estado.global_vigente,
        )
        return materializacao

    def comparar_candidato_baseline(self, candidato=None):
        documento = self._estado.candidato if candidato is None else candidato
        return comparar_configuracoes_estilo(documento, self._estado.baseline)

    def persistir_candidato(self, candidato, caminho_destino):
        """Persiste candidato sem publicar nem promover baseline."""
        documento = _exigir_candidato_dict(candidato)
        self._estado = _EstadoEstiloRuntime(
            baseline=self._estado.baseline,
            candidato=documento,
            global_vigente=self._estado.global_vigente,
        )
        return persistir_configuracao_estilo(documento, caminho_destino)

    def aplicar_candidato(self, candidato, caminho_destino):
        """Persiste e somente depois publica e promove o candidato."""
        documento = _exigir_candidato_dict(candidato)
        materializacao = materializar_estilo_local(documento)
        estado_anterior = self._estado
        self._estado = _EstadoEstiloRuntime(
            baseline=estado_anterior.baseline,
            candidato=documento,
            global_vigente=estado_anterior.global_vigente,
        )
        persistir_configuracao_estilo(documento, caminho_destino)

        # Uma única troca substitui global, baseline e candidato sincronizado.
        self._estado = _EstadoEstiloRuntime(
            baseline=copy.deepcopy(documento),
            candidato=copy.deepcopy(documento),
            global_vigente=materializacao,
        )
        return materializacao


RuntimeEstilo = EstadoEstiloRuntime


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
    """Resolve o preset ativo de chip e materializa campos opcionais."""
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

    campos_fundo_laterais = {}
    for campo in ("cor_fundo_esquerdo", "cor_fundo_direito"):
        valor = ativo.get(campo, cor_fundo)
        if not isinstance(valor, str):
            raise EstiloErro(
                "chip.presets[{0!r}].{1} deve ser texto".format(
                    preset_default, campo
                )
            )
        campos_fundo_laterais[campo] = valor

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
        **campos_fundo_laterais,
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
