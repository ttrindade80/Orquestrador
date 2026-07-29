"""Testes de integracao do ponto de entrada TTY do H-0041 (demo_selecao).

Valida o carregamento e a estrutura do ponto de entrada dedicado
``demo/demo_selecao.py`` sobre a fixture D-SEL-22 (oito itens), bem como a
resolucao de caminho/raiz e o argv. Nao abre sessao TTY real (responsabilidade
exclusiva do usuario em terminal, D-SEL-23).
"""

import sys

sys.dont_write_bytecode = True

from pathlib import Path

# Padrao dos testes da demo: insere a raiz do repositorio no sys.path e remove
# o propio diretorio demo, de modo que ``demo.demo_selecao`` seja importavel
# como modulo da raiz (a demo nao e um pacote com __init__.py).
_BASE_PADRAO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE_PADRAO))
_this_dir = str(Path(__file__).resolve().parent)
while _this_dir in sys.path:
    sys.path.remove(_this_dir)

import os  # noqa: E402
import pytest  # noqa: E402

import demo.demo_selecao as demo_selecao  # noqa: E402
import demo.demo as _demo  # noqa: E402
from tela import navegacao  # noqa: E402


_CAMINHO_FIXTURE = os.path.join(
    "config", "telas", "demo", "h0041_selecao_multipla_oito_itens.json"
)


def test_carregar_modelo_por_caminho_oito_itens():
    # CA: carregamento da fixture de oito itens sem excecao.
    modelo = demo_selecao.carregar_modelo_por_caminho(_CAMINHO_FIXTURE)
    assert modelo is not None
    console = modelo.corpo.elementos[0]
    itens = console._campos_inertes["itens"]
    assert len(itens) == 8


def test_seis_navegaveis_na_ordem_contratada():
    # D-SEL-22: seis alvos navegaveis na ordem item_01..07 (exceto 04/08).
    modelo = demo_selecao.carregar_modelo_por_caminho(_CAMINHO_FIXTURE)
    console = modelo.corpo.elementos[0]
    ids = [i["id"] for i in navegacao.itens_navegaveis(console)]
    assert ids == ["item_01", "item_02", "item_03", "item_05", "item_06", "item_07"]


def test_quatro_selecionaveis():
    # D-SEL-22: quatro selecionaveis (item_01,03,05,07).
    modelo = demo_selecao.carregar_modelo_por_caminho(_CAMINHO_FIXTURE)
    console = modelo.corpo.elementos[0]
    from tela import selecao
    assert selecao.itens_selecionaveis(console) == [
        "item_01", "item_03", "item_05", "item_07"
    ]


def test_politica_selecao_multipla():
    # A fixture declara politica_selecao: multipla.
    modelo = demo_selecao.carregar_modelo_por_caminho(_CAMINHO_FIXTURE)
    console = modelo.corpo.elementos[0]
    assert navegacao._console_declarou_selecao_multipla(console)


def test_chip_enter_regra_ativo_selecao_vazia():
    # QA-H0041-002 (P02): chip_enter declara regra_ativo=selecao_vazia
    # (estado logico independente do rotulo Todos/Executar).
    modelo = demo_selecao.carregar_modelo_por_caminho(_CAMINHO_FIXTURE)
    chips = (modelo.barra_de_menus or {}).get("chips") or []
    chip_enter = next(c for c in chips if c.get("id") == "chip_enter")
    assert chip_enter.get("regra_ativo") == "selecao_vazia"
    assert chip_enter.get("forma_exibicao") == "rotulo_dinamico_selecao"


def test_resolver_caminho_dentro_da_raiz_demo():
    # Resolucao de caminho dentro de config/telas/demo retorna raiz demo.
    raiz, id_tela = demo_selecao._resolver_caminho_tela(_CAMINHO_FIXTURE)
    # _resolver_caminho_tela normaliza para caminho absoluto; compara ambos
    # absolutos para independencia do diretorio corrente do teste.
    assert os.path.abspath(raiz) == os.path.abspath(_demo._RAIZ_TELAS_DEMO)
    assert id_tela == "h0041_selecao_multipla_oito_itens"


def test_parse_argv_tela_obrigatoria():
    # --tela e obrigatorio.
    args = demo_selecao._parse_argv(
        ["demo.demo_selecao", "--tela", _CAMINHO_FIXTURE]
    )
    assert args.tela == _CAMINHO_FIXTURE


def test_parse_argv_sem_tela_falha():
    # Ausencia de --tela levanta SystemExit (argparse required=True).
    with pytest.raises(SystemExit):
        demo_selecao._parse_argv(["demo.demo_selecao"])


def test_estado_inicial_foco_primeiro_console():
    # O ponto de entrada deve estabelecer foco no primeiro console ao iniciar.
    modelo = demo_selecao.carregar_modelo_por_caminho(_CAMINHO_FIXTURE)
    lista = navegacao.lista_foco(modelo)
    estado = _demo.criar_estado_inicial()
    lista_foco_inicial = navegacao.lista_foco(modelo)
    if lista_foco_inicial:
        estado = dict(estado, foco_console=0)
        cursores = dict(estado.get("cursores", {}))
        cursores[lista_foco_inicial[0].id] = 0
        estado = dict(estado, cursores=cursores)
    assert estado["foco_console"] == 0
    assert estado["cursores"][lista[0].id] == 0
    assert estado["selecoes"] == {}


def test_h0041_p04_pty_enter_todos_ponto_de_entrada_real():
    """H0041-MANUAL-R02-001: Enter/Todos pelo ponto de entrada TTY real.

    Abre ``python -m demo.demo_selecao --tela <fixture>`` em PTY com tamanho
    deterministico, aguarda o primeiro quadro, envia Enter real (``\\r``,
    convertido a ``\\n`` por ICRNL sob cbreak) e confirma no quadro seguinte:
    quatro ``tg`` incluidos, rotulo ``Executar`` com capitalizacao normal e
    cor_inativo aplicada — apos uma unica tecla.
    """
    import fcntl
    import pty
    import select
    import signal
    import struct
    import subprocess
    import termios
    import time

    from tela.renderizador import _ANSI_RESET_FG, _codigo_ansi_de_cor
    from tela.loader import carregar_estilo

    cols, lines = 80, 28
    master_fd = None
    slave_fd = None
    proc = None
    try:
        master_fd, slave_fd = pty.openpty()
        winsz = struct.pack("HHHH", lines, cols, 0, 0)
        fcntl.ioctl(slave_fd, termios.TIOCSWINSZ, winsz)

        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        proc = subprocess.Popen(
            [
                sys.executable, "-m", "demo.demo_selecao",
                "--tela", _CAMINHO_FIXTURE,
            ],
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            cwd=str(_BASE_PADRAO),
            env=env,
            close_fds=True,
        )
        os.close(slave_fd)
        slave_fd = None

        def _ler_ate(timeout_total, ocioso, predicado=None):
            deadline = time.time() + timeout_total
            buf = b""
            ultimo = time.time()
            while time.time() < deadline:
                pronto, _, _ = select.select([master_fd], [], [], 0.05)
                if pronto:
                    try:
                        chunk = os.read(master_fd, 4096)
                    except OSError:
                        break
                    if not chunk:
                        break
                    buf += chunk
                    ultimo = time.time()
                    if predicado is not None and predicado(buf):
                        return buf
                elif time.time() - ultimo >= ocioso and buf:
                    if predicado is None or predicado(buf):
                        return buf
            return buf

        saida_inicial = _ler_ate(
            4.0, 0.35,
            predicado=lambda b: b"Todos" in b and b"Item um" in b,
        )
        assert proc.poll() is None, "demo_selecao encerrou antes do 1o quadro"
        assert b"Todos" in saida_inicial
        assert b"Item um" in saida_inicial
        assert saida_inicial.count(b"\xe2\x97\x8f") == 0  # ● utf-8

        # Enter real: teclado envia CR; ICRNL sob cbreak entrega LF ao app.
        os.write(master_fd, b"\r")

        saida_apos = _ler_ate(
            4.0, 0.35,
            predicado=lambda b: b"Executar" in b and b.count(b"\xe2\x97\x8f") >= 4,
        )
        assert proc.poll() is None, "demo_selecao encerrou apos Enter"
        texto = saida_apos.decode("utf-8", errors="replace")
        assert texto.count("●") >= 4
        assert "Executar" in texto
        assert "executar" not in texto
        estilo = carregar_estilo()
        codigo = _codigo_ansi_de_cor(estilo.cor_inativo)
        assert codigo and codigo in texto
        assert _ANSI_RESET_FG in texto

        # Encerramento limpo: Esc (selecao ativa limpa) + Esc (sair).
        os.write(master_fd, b"\x1b")
        _ler_ate(2.0, 0.2)
        os.write(master_fd, b"\x1b")
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=2)
            raise AssertionError("timeout ao encerrar demo_selecao via Esc")
        assert proc.returncode == 0
    finally:
        if proc is not None and proc.poll() is None:
            try:
                os.kill(proc.pid, signal.SIGTERM)
            except OSError:
                pass
            try:
                proc.wait(timeout=2)
            except Exception:
                proc.kill()
        if slave_fd is not None:
            try:
                os.close(slave_fd)
            except OSError:
                pass
        if master_fd is not None:
            try:
                os.close(master_fd)
            except OSError:
                pass
