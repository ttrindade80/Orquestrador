"""Demo dedicado da distribuicao matricial de conteudo (H-0035 / ADR-0025).

Ponto de entrada real e executavel do artefato demonstrado. Separado do demo
principal (`demo/demo.py`), reutiliza sua infraestrutura de sessao TTY por
IMPORTACAO (sem duplicar codigo e sem alterar `demo/demo.py`).

USO:
    python demo/demo_distribuicao.py           # abre o catalogo h0035_catalogo
    python demo/demo_distribuicao.py <id_tela>  # abre diretamente uma familia

Navegacao: no catalogo, cada item do lancador leva (chip -> tela_destino) a uma
tela h0035_*. Esc/`s` volta ao catalogo; Esc/`s` no catalogo sai. `b` alterna a
borda. Redimensionar a janela recalcula a distribuicao a cada SIGWINCH; quando a
area e insuficiente, o quadro minimo canonico e exibido e a distribuicao e
reconstruida deterministicamente ao aumentar.

IDENTIDADE SEMANTICA (H-0035 secao 29): para uma tela, `descrever_tela` retorna
nome da tela, familia de distribuicao, formacao, ordem, consumidor testado e o
estado (normal ou quadro minimo). O smoke test verifica esse conteudo material.

Mensagens de erro: id de tela inexistente, JSON invalido e configuracao
`distribuicao_matricial` invalida produzem mensagem material (classe de erro de
dominio) e codigo de saida nao zero, sem renderizacao parcial.

Apenas biblioteca padrao do Python.
"""

import os
import sys

sys.dont_write_bytecode = True

if __name__ == "__main__":
    _raiz_scripts = "/".join(__file__.replace("\\", "/").split("/")[:-2])
    if _raiz_scripts and _raiz_scripts not in sys.path:
        sys.path.insert(0, _raiz_scripts)
    # Ao executar `python demo/demo_distribuicao.py`, o Python coloca `demo/`
    # em sys.path[0], o que impede `from demo.demo import ...` (o pacote-namespace
    # `demo` fica sombreado). Removemos `demo/` do path (como fazem os testes),
    # preservando a raiz do repositorio inserida acima.
    _este_dir = "/".join(__file__.replace("\\", "/").split("/")[:-1])
    while _este_dir in sys.path:
        sys.path.remove(_este_dir)

from tela.loader import carregar_tela, TelaErro
from tela.modelo import construir_modelo, ModeloTela
from tela.renderizador import renderizar_tela, RenderizadorErro

# Reuso por importacao da infraestrutura de sessao TTY do demo principal.
# Nenhuma dessas funcoes e alterada aqui; apenas invocadas.
from demo.demo import (
    processar_comando,
    _ler_tecla_sessao,
    _iniciar_sessao_tui,
    _encerrar_sessao_tui,
    _obter_dimensoes_iniciais,
    _obter_dimensoes_apos_sigwinch,
    _instalar_handler_sigwinch,
    _restaurar_handler_sigwinch,
    _apresentar_quadro,
    _tela_pequena_demais,
    _quadro_minimo_aviso,
    LARGURA_MINIMA_TELA,
    ALTURA_MINIMA_TELA,
)

import select  # noqa: E402

_RAIZ_TELAS_DEMO = os.path.join("config", "telas", "demo")

_CHIPS_CATALOGO_ALPHA = frozenset("ABCDEFGHIJKLMNOP")


def _normalizar_tecla_catalogo(ch, tela_atual):
    """Converte a-p para A-P somente quando na tela do catálogo.

    Garante que teclas minúsculas selecionem o mesmo chip que maiúsculas.
    Fora do catálogo e para teclas fora do intervalo a-p, não altera nada.
    """
    if tela_atual == _TELA_CATALOGO and len(ch) == 1:
        cu = ch.upper()
        if cu in _CHIPS_CATALOGO_ALPHA:
            return cu
    return ch

# Tela raiz de catalogo do demo dedicado (H-0035 secao 27).
_TELA_CATALOGO = "h0035_catalogo"


def criar_estado_inicial(tela_inicial=_TELA_CATALOGO):
    """Estado inicial do demo dedicado (borda curva, sem telas empilhadas)."""
    return {
        "tipo_borda": "curva",
        "saindo": False,
        "tela_atual": tela_inicial,
        "pilha_telas": [],
    }


def _carregar_modelo_por_id(id_tela):
    """Carrega e constroi o ModeloTela para ``id_tela`` da raiz demo."""
    tela_raw = carregar_tela(None, id_tela, _RAIZ_TELAS_DEMO)
    return construir_modelo(tela_raw)


def _consumidor_e_dm(modelo):
    """Retorna (consumidor, config_dm) do primeiro elemento funcional com
    distribuicao_matricial, ou (tipo_do_primeiro_elemento, None)."""
    for elemento in modelo.corpo.elementos:
        dm = getattr(elemento, "distribuicao_matricial", None)
        if dm is not None:
            return elemento.tipo, dm
    for elemento in modelo.corpo.elementos:
        if elemento.tipo in ("dashboard", "console", "lancador"):
            return elemento.tipo, None
    return "(nenhum)", None


def descrever_tela(modelo, largura=None, altura=None):
    """Identidade semantica material da tela (H-0035 secao 29).

    Retorna dict com: nome da tela, familia (politica de formacao), formacao
    (linhas x colunas quando declarada como matriz_fixa), ordem, consumidor
    testado, politica_horizontal, politica_vertical, objetivo e estado.
    """
    consumidor, dm = _consumidor_e_dm(modelo)
    if dm is not None:
        familia = dm["formacao"]["politica"]
        ordem = dm["ordem"]
        pol_h = dm["distribuicao_horizontal"]["politica"]
        pol_v = dm["distribuicao_vertical"]["politica"]
        if familia == "matriz_fixa":
            formacao = "{0}x{1}".format(
                dm["formacao"]["linhas"]["fixo"],
                dm["formacao"]["colunas"]["fixo"],
            )
        else:
            formacao = familia
    else:
        familia = "(sem distribuicao_matricial)"
        ordem = "(n/a)"
        formacao = "(n/a)"
        pol_h = "(n/a)"
        pol_v = "(n/a)"

    cab = modelo.cabecalho
    objetivo = cab.get("descricao", "n/a") if isinstance(cab, dict) else "n/a"

    estado_visual = "normal"
    if largura is not None and altura is not None:
        if _tela_pequena_demais(largura, altura):
            estado_visual = "quadro_minimo"
        else:
            try:
                saida = renderizar_tela(
                    modelo, tipo_borda="curva", largura=largura, altura=altura
                )
                if "terminal pequeno demais" in saida or "tela peq." in saida:
                    estado_visual = "quadro_minimo"
            except RenderizadorErro:
                estado_visual = "quadro_minimo"

    return {
        "nome": modelo.id,
        "familia": familia,
        "formacao": formacao,
        "ordem": ordem,
        "consumidor": consumidor,
        "politica_horizontal": pol_h,
        "politica_vertical": pol_v,
        "objetivo": objetivo,
        "tecla": "n/a",
        "estado": estado_visual,
    }


def _resolver_conteudo(estado, modelo, largura, altura):
    """Resolve o conteudo a apresentar para as dimensoes correntes.

    Quadro minimo de aviso quando terminal pequeno demais ou quando o renderer
    levanta RenderizadorErro (recuperacao automatica ao aumentar).
    """
    if _tela_pequena_demais(largura, altura):
        return _quadro_minimo_aviso(largura, altura)
    try:
        return renderizar_tela(
            modelo, tipo_borda=estado["tipo_borda"], largura=largura, altura=altura
        )
    except RenderizadorErro:
        return _quadro_minimo_aviso(largura, altura)


def _validar_id_tela(id_tela):
    """Carrega a tela pedida validando existencia e configuracao.

    Lanca TelaErro/RenderizadorErro (erros de dominio) com mensagem material.
    Retorna o ModeloTela quando valido.
    """
    return _carregar_modelo_por_id(id_tela)


def main(argv=None):
    """Entrada principal do demo dedicado.

    Aceita argumento opcional de id de tela para abrir diretamente uma familia.
    Id inexistente/JSON invalido/dm invalida produzem mensagem material e
    codigo de saida nao zero, sem renderizacao parcial.
    """
    if argv is None:
        argv = sys.argv[1:]

    tela_inicial = _TELA_CATALOGO
    if argv:
        tela_inicial = argv[0]

    # Validacao antes de qualquer efeito observavel (sem renderizacao parcial).
    try:
        modelo = _validar_id_tela(tela_inicial)
    except (TelaErro, RenderizadorErro) as exc:
        sys.stderr.write(
            "erro ao abrir tela {0!r}: {1}: {2}\n".format(
                tela_inicial, type(exc).__name__, exc
            )
        )
        return 2

    estado = criar_estado_inicial(tela_inicial)

    if sys.stdin.isatty() and sys.stdout.isatty():
        fd = sys.stdin.fileno()
        largura, altura = _obter_dimensoes_iniciais(fd)
        resize_pendente = [False]
        r_wakeup = None
        w_wakeup = None
        sessao_iniciada = False
        handler_instalado = False
        handler_anterior = None
        atributos_originais = None
        try:
            r_wakeup, w_wakeup = os.pipe()
            os.set_blocking(r_wakeup, False)
            os.set_blocking(w_wakeup, False)
            atributos_originais = _iniciar_sessao_tui(fd)
            sessao_iniciada = True
            handler_anterior = _instalar_handler_sigwinch(w_wakeup, resize_pendente)
            handler_instalado = True
            _apresentar_quadro(
                _resolver_conteudo(estado, modelo, largura, altura), largura
            )
            while True:
                try:
                    prontos, _, _ = select.select([fd, r_wakeup], [], [])
                    if r_wakeup in prontos:
                        while True:
                            try:
                                dados = os.read(r_wakeup, 64)
                                if not dados:
                                    break
                            except BlockingIOError:
                                break
                            except OSError:
                                break
                        resize_pendente[0] = False
                        nova_l, nova_a = _obter_dimensoes_apos_sigwinch(
                            fd, (largura, altura)
                        )
                        if nova_l != largura or nova_a != altura:
                            largura, altura = nova_l, nova_a
                            _apresentar_quadro(
                                _resolver_conteudo(estado, modelo, largura, altura),
                                largura,
                            )
                        if fd not in prontos:
                            continue
                    ch = _ler_tecla_sessao(fd=fd)
                    tela_antes = estado["tela_atual"]
                    ch_cmd = _normalizar_tecla_catalogo(ch, tela_antes)
                    estado = processar_comando(estado, ch_cmd, modelo)
                    if estado["saindo"]:
                        break
                    if estado["tela_atual"] != tela_antes:
                        modelo = _carregar_modelo_por_id(estado["tela_atual"])
                    if ch_cmd == "b" or estado["tela_atual"] != tela_antes:
                        _apresentar_quadro(
                            _resolver_conteudo(estado, modelo, largura, altura),
                            largura,
                        )
                except KeyboardInterrupt:
                    continue
        finally:
            if handler_instalado:
                _restaurar_handler_sigwinch(handler_anterior)
            if r_wakeup is not None:
                try:
                    os.close(r_wakeup)
                except OSError:
                    pass
            if w_wakeup is not None:
                try:
                    os.close(w_wakeup)
                except OSError:
                    pass
            if sessao_iniciada:
                _encerrar_sessao_tui(fd, atributos_originais)
    else:
        # Fora de TTY (pipe/teste/smoke): imprime a tela inicial e sua
        # identidade semantica material, depois processa comandos linha a linha.
        import shutil
        tamanho = shutil.get_terminal_size(fallback=(80, 24))
        largura, altura = tamanho.columns, tamanho.lines
        ident = descrever_tela(modelo, largura, altura)
        sys.stdout.write(
            "identidade: nome={0} familia={1} formacao={2} ordem={3} "
            "consumidor={4} pol_h={5} pol_v={6} estado={7}\n".format(
                ident["nome"], ident["familia"], ident["formacao"],
                ident["ordem"], ident["consumidor"],
                ident["politica_horizontal"], ident["politica_vertical"],
                ident["estado"],
            )
        )
        sys.stdout.write(_resolver_conteudo(estado, modelo, largura, altura))
        for linha in sys.stdin:
            comando = linha.strip()
            tela_antes = estado["tela_atual"]
            cmd = _normalizar_tecla_catalogo(comando, tela_antes)
            estado = processar_comando(estado, cmd, modelo)
            if estado["saindo"]:
                break
            if estado["tela_atual"] != tela_antes:
                modelo = _carregar_modelo_por_id(estado["tela_atual"])
            if cmd == "b" or estado["tela_atual"] != tela_antes:
                ident = descrever_tela(modelo, largura, altura)
                sys.stdout.write(
                    "identidade: nome={0} familia={1} formacao={2} ordem={3} "
                    "consumidor={4} pol_h={5} pol_v={6} estado={7}\n".format(
                        ident["nome"], ident["familia"], ident["formacao"],
                        ident["ordem"], ident["consumidor"],
                        ident["politica_horizontal"], ident["politica_vertical"],
                        ident["estado"],
                    )
                )
                sys.stdout.write(
                    _resolver_conteudo(estado, modelo, largura, altura)
                )
    return 0


if __name__ == "__main__":
    sys.exit(main())
