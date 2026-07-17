"""Testes do demo dedicado da distribuicao matricial (H-0035 / ADR-0025).

Executavel via:
    python demo/teste_demo_distribuicao.py

Cobre (contrato H-0035 secao 37.7): catalogo dedicado; selecao de todas as
configuracoes; identidade semantica; comando de entrada; quadro minimo;
recuperacao; demo principal preservado. Inclui smoke fora de TTY e prova em
pseudo-terminal (pty) com selecao de familia, quadro minimo e recuperacao por
redimensionamento.

Apenas biblioteca padrao do Python.
"""

import json
import os
import signal
import subprocess
import sys
from pathlib import Path

_BASE_PADRAO = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(_BASE_PADRAO))
_this_dir = str(Path(__file__).resolve().parent)
while _this_dir in sys.path:
    sys.path.remove(_this_dir)

from demo.demo_distribuicao import (  # noqa: E402
    criar_estado_inicial,
    descrever_tela,
    _carregar_modelo_por_id,
    _resolver_conteudo,
    _normalizar_tecla_catalogo,
    main,
    _TELA_CATALOGO,
)
from demo.demo import (  # noqa: E402
    processar_comando,
    id_conteudo_externo_de,
)
from tela.distribuicao_matricial import calcular_distribuicao  # noqa: E402
from tela.loader import carregar_conteudo_externo  # noqa: E402

_RESULTADOS = []

_RAIZ_TELAS_DEMO = os.path.join("config", "telas", "demo")

# Telas h0035_* de conteudo (o catalogo navega para todas elas).
_TELAS_CONTEUDO = [
    "h0035_pref_linhas", "h0035_pref_colunas", "h0035_matriz_fixa_cabe",
    "h0035_matriz_fixa_quadro_minimo", "h0035_centralizado_h_colunas",
    "h0035_esquerda_margens_min_max", "h0035_h_uniforme",
    "h0035_h_margens_limitadas", "h0035_v_margens_min",
    "h0035_v_margens_min_max", "h0035_v_uniforme", "h0035_um_centralizado",
    "h0035_tres_centralizados", "h0035_quatro_centralizados",
    "h0035_minimo_fixo_excedido", "h0035_uma_linha", "h0035_uma_coluna",
    "h0035_resto_horizontal", "h0035_resto_vertical", "h0035_console_com",
    "h0035_console_sem", "h0035_lancador_com", "h0035_lancador_sem",
    "h0035_dashboard_com", "h0035_dashboard_sem",
]

# Mapeamento ordenado (ordem canonica do catalogo): chip -> tela_destino.
# 1-9 = primeiros nove; A-P = dezesseis restantes.
_MAPEAMENTO_CATALOGO = [
    ("1", "h0035_pref_linhas"),
    ("2", "h0035_pref_colunas"),
    ("3", "h0035_matriz_fixa_cabe"),
    ("4", "h0035_matriz_fixa_quadro_minimo"),
    ("5", "h0035_centralizado_h_colunas"),
    ("6", "h0035_esquerda_margens_min_max"),
    ("7", "h0035_h_uniforme"),
    ("8", "h0035_h_margens_limitadas"),
    ("9", "h0035_v_margens_min"),
    ("A", "h0035_v_margens_min_max"),
    ("B", "h0035_v_uniforme"),
    ("C", "h0035_um_centralizado"),
    ("D", "h0035_tres_centralizados"),
    ("E", "h0035_quatro_centralizados"),
    ("F", "h0035_minimo_fixo_excedido"),
    ("G", "h0035_uma_linha"),
    ("H", "h0035_uma_coluna"),
    ("I", "h0035_resto_horizontal"),
    ("J", "h0035_resto_vertical"),
    ("K", "h0035_console_com"),
    ("L", "h0035_console_sem"),
    ("M", "h0035_lancador_com"),
    ("N", "h0035_lancador_sem"),
    ("O", "h0035_dashboard_com"),
    ("P", "h0035_dashboard_sem"),
]

# Conjunto canonico de chips esperados (todos de um caractere).
_CHIPS_ESPERADOS = frozenset(c for c, _ in _MAPEAMENTO_CATALOGO)

# Titulos renderizados (uppercase) de cada tela, na ordem do catalogo.
_TITULO_RENDERIZADO = {
    "h0035_pref_linhas":               b"H0035 PREF LINHAS",
    "h0035_pref_colunas":              b"H0035 PREF COLUNAS",
    "h0035_matriz_fixa_cabe":          b"H0035 MATRIZ 3X4",
    "h0035_matriz_fixa_quadro_minimo": b"H0035 MATRIZ 4X4",
    "h0035_centralizado_h_colunas":    b"H0035 CENTRO H",
    "h0035_esquerda_margens_min_max":  b"H0035 ESQUERDA",
    "h0035_h_uniforme":                b"H0035 H UNIFORME",
    "h0035_h_margens_limitadas":       b"H0035 H LIMITADAS",
    "h0035_v_margens_min":             b"H0035 V MIN",
    "h0035_v_margens_min_max":         b"H0035 V MINMAX",
    "h0035_v_uniforme":                b"H0035 V UNIFORME",
    "h0035_um_centralizado":           b"H0035 UM CENTRO",
    "h0035_tres_centralizados":        b"H0035 TRES CENTRO",
    "h0035_quatro_centralizados":      b"H0035 QUATRO CENTRO",
    "h0035_minimo_fixo_excedido":      b"H0035 MIN FIXO",
    "h0035_uma_linha":                 b"H0035 UMA LINHA",
    "h0035_uma_coluna":                b"H0035 UMA COLUNA",
    "h0035_resto_horizontal":          b"H0035 RESTO H",
    "h0035_resto_vertical":            b"H0035 RESTO V",
    "h0035_console_com":               b"H0035 CONSOLE COM",
    "h0035_console_sem":               b"H0035 CONSOLE SEM",
    "h0035_lancador_com":              b"H0035 LANCADOR COM",
    "h0035_lancador_sem":              b"H0035 LANCADOR SEM",
    "h0035_dashboard_com":             b"H0035 DASH COM",
    "h0035_dashboard_sem":             b"H0035 DASH SEM",
}


def _registrar(nome, passou, detalhe=""):
    status = "PASSOU" if passou else "FALHOU"
    linha = "[{0}] {1}".format(status, nome)
    if detalhe:
        linha += " - {0}".format(detalhe)
    print(linha)
    _RESULTADOS.append((nome, passou))


def _config_dm_fixture(id_tela):
    """Retorna o dict distribuicao_matricial do primeiro elemento funcional."""
    caminho = os.path.join(_RAIZ_TELAS_DEMO, id_tela + ".json")
    with open(caminho, encoding="utf-8") as f:
        raw = json.load(f)
    for elem in raw.get("corpo", {}).get("elementos", []):
        dm = elem.get("distribuicao_matricial")
        if dm is not None:
            return dm
    return None


def _contar_nos_dados(dados):
    """Conta recursivamente nos de um documento externo (dados + filhos)."""
    total = 0
    for no in dados:
        total += 1
        total += _contar_nos_dados(no.get("filhos", []) or [])
    return total


def _n_campos_fixture(id_tela):
    """Conta participantes do primeiro elemento com DM.

    H-0036: para o console cujos dados de runtime foram separados para um
    documento externo (``itens`` removido do JSON estrutural), a contagem vem
    do documento externo associado pelo catalogo do demo.py — provando o
    carregamento separado dos dois arquivos.
    """
    caminho = os.path.join(_RAIZ_TELAS_DEMO, id_tela + ".json")
    with open(caminho, encoding="utf-8") as f:
        raw = json.load(f)
    for elem in raw.get("corpo", {}).get("elementos", []):
        if elem.get("distribuicao_matricial") is None:
            continue
        tipo = elem.get("tipo", "")
        if tipo == "dashboard":
            return len(elem.get("campos", []))
        if tipo in ("console", "lancador"):
            itens = elem.get("itens", [])
            if itens:
                return len(itens)
            # console H-0036 separado: contar dados do documento externo.
            id_conteudo = id_conteudo_externo_de(id_tela)
            if id_conteudo is not None:
                doc = carregar_conteudo_externo(None, id_conteudo, _RAIZ_TELAS_DEMO)
                return _contar_nos_dados(doc.get("dados", []))
            return 0
    return 0


def teste_catalogo_dedicado():
    print("")
    print("== Catalogo dedicado h0035_catalogo ==")
    estado = criar_estado_inicial()
    _registrar("estado inicial abre o catalogo",
               estado["tela_atual"] == _TELA_CATALOGO)
    modelo = _carregar_modelo_por_id(_TELA_CATALOGO)
    lanc = [e for e in modelo.corpo.elementos if e.tipo == "lancador"]
    _registrar("catalogo tem um lancador de navegacao", len(lanc) == 1)
    destinos = set()
    for item in lanc[0]._campos_inertes.get("itens", []):
        destinos.add(item.get("tela_destino"))
    faltantes = set(_TELAS_CONTEUDO) - destinos
    _registrar("catalogo navega para todas as telas de conteudo",
               not faltantes, "faltantes: {0}".format(sorted(faltantes)))


def teste_selecao_de_todas():
    print("")
    print("== Selecao de todas as configuracoes ==")
    modelo_cat = _carregar_modelo_por_id(_TELA_CATALOGO)
    todas_ok = True
    for id_tela in _TELAS_CONTEUDO:
        chip = None
        for e in modelo_cat.corpo.elementos:
            if e.tipo != "lancador":
                continue
            for item in e._campos_inertes.get("itens", []):
                if item.get("tela_destino") == id_tela:
                    chip = item.get("chip")
        estado = criar_estado_inicial()
        novo = processar_comando(estado, chip, modelo_cat)
        if novo["tela_atual"] != id_tela:
            todas_ok = False
            _registrar("selecao navega para {0}".format(id_tela), False,
                       "chip={0} -> {1}".format(chip, novo["tela_atual"]))
    _registrar("selecao de todas as configuracoes via chip", todas_ok)


def teste_identidade_semantica():
    print("")
    print("== Identidade semantica material ==")
    m1 = _carregar_modelo_por_id("h0035_pref_colunas")
    id1 = descrever_tela(m1, 80, 24)
    ok1 = (
        id1["nome"] == "h0035_pref_colunas"
        and id1["familia"] == "preferencia_colunas"
        and id1["ordem"] == "por_coluna"
        and id1["consumidor"] == "dashboard"
        and id1["estado"] == "normal"
        and "politica_horizontal" in id1
        and "politica_vertical" in id1
        and "objetivo" in id1
    )
    _registrar("identidade pref_colunas material completa", ok1, str(id1))

    m2 = _carregar_modelo_por_id("h0035_matriz_fixa_cabe")
    id2 = descrever_tela(m2, 80, 24)
    ok2 = (
        id2["familia"] == "matriz_fixa"
        and id2["formacao"] == "3x4"
        and id2["consumidor"] == "dashboard"
        and id2["politica_horizontal"] == "uniforme"
        and id2["politica_vertical"] == "uniforme"
    )
    _registrar("identidade matriz_fixa formacao 3x4 H+V uniformes", ok2, str(id2))

    m3 = _carregar_modelo_por_id("h0035_lancador_com")
    id3 = descrever_tela(m3, 80, 24)
    _registrar("identidade lancador consumidor correto",
               id3["consumidor"] == "lancador", str(id3))

    m4 = _carregar_modelo_por_id("h0035_console_com")
    id4 = descrever_tela(m4, 80, 24)
    _registrar("identidade console consumidor correto",
               id4["consumidor"] == "console", str(id4))

    # Objetivo vem do campo descricao do cabecalho.
    m5 = _carregar_modelo_por_id("h0035_pref_linhas")
    id5 = descrever_tela(m5, 80, 24)
    _registrar("identidade objetivo nao vazio",
               bool(id5.get("objetivo")) and id5["objetivo"] != "n/a",
               "objetivo={0!r}".format(id5.get("objetivo")))


def teste_quadro_minimo_e_recuperacao():
    print("")
    print("== Quadro minimo e recuperacao ==")
    modelo = _carregar_modelo_por_id("h0035_matriz_fixa_quadro_minimo")
    estado = criar_estado_inicial("h0035_matriz_fixa_quadro_minimo")
    # Area pequena -> quadro minimo canonico.
    peq = _resolver_conteudo(estado, modelo, 42, 14)
    _registrar("quadro minimo acionado em area pequena",
               "terminal pequeno demais" in peq)
    id_peq = descrever_tela(modelo, 42, 14)
    _registrar("identidade reporta estado quadro_minimo",
               id_peq["estado"] == "quadro_minimo", str(id_peq))
    # Area grande -> recuperacao deterministica (renderiza a grade).
    grande = _resolver_conteudo(estado, modelo, 120, 40)
    _registrar("recuperacao: area grande renderiza a grade (sem aviso)",
               "terminal pequeno demais" not in grande
               and "H0035 MATRIZ 4X4" in grande)
    # Determinismo: mesma entrada, mesma saida.
    grande2 = _resolver_conteudo(estado, modelo, 120, 40)
    _registrar("recuperacao deterministica (identica)", grande == grande2)


def teste_comando_de_entrada_e_erros():
    print("")
    print("== Comando de entrada e erros materiais ==")
    proc_ok = subprocess.run(
        [sys.executable, "demo/demo_distribuicao.py", "h0035_pref_linhas"],
        cwd=str(_BASE_PADRAO), input="s\n",
        capture_output=True, text=True,
    )
    _registrar("comando com id valido retorna 0", proc_ok.returncode == 0,
               "rc={0}".format(proc_ok.returncode))
    _registrar("smoke exibe identidade semantica material",
               "identidade: nome=h0035_pref_linhas" in proc_ok.stdout
               and "familia=preferencia_linhas" in proc_ok.stdout
               and "pol_h=" in proc_ok.stdout
               and "pol_v=" in proc_ok.stdout,
               proc_ok.stdout.splitlines()[0] if proc_ok.stdout else "")

    proc_err = subprocess.run(
        [sys.executable, "demo/demo_distribuicao.py", "nao_existe_xyz"],
        cwd=str(_BASE_PADRAO), capture_output=True, text=True,
    )
    _registrar("id inexistente retorna codigo nao zero",
               proc_err.returncode != 0, "rc={0}".format(proc_err.returncode))
    _registrar("id inexistente mensagem material (classe de erro)",
               "TelaArquivoNaoEncontrado" in proc_err.stderr,
               proc_err.stderr.strip().splitlines()[-1] if proc_err.stderr else "")
    _registrar("id inexistente sem renderizacao parcial (sem caixa na stdout)",
               "╭" not in proc_err.stdout)


def teste_demo_principal_preservado():
    print("")
    print("== Demo principal preservado ==")
    est_principal = subprocess.run(
        [sys.executable, "demo/demo.py"],
        cwd=str(_BASE_PADRAO), input="s\n",
        capture_output=True, text=True,
    )
    _registrar("demo principal continua funcional (exit 0)",
               est_principal.returncode == 0)
    _registrar("demo principal nao virou catalogo h0035",
               "H0035 CATALOGO" not in est_principal.stdout
               and "ORQUESTRADOR" in est_principal.stdout)


def _ler_pty_ate_ocioso(fd_master, timeout_total, ocioso):
    import select as _sel
    import time as _t
    dados = b""
    fim = _t.monotonic() + timeout_total
    ultimo_dado = None
    while _t.monotonic() < fim:
        restante = fim - _t.monotonic()
        prontos, _, _ = _sel.select(
            [fd_master], [], [], min(0.1, max(0.0, restante))
        )
        if prontos:
            try:
                chunk = os.read(fd_master, 4096)
            except (BlockingIOError, OSError):
                chunk = b""
            if chunk:
                dados += chunk
                ultimo_dado = _t.monotonic()
                continue
        if ultimo_dado is not None and (_t.monotonic() - ultimo_dado) >= ocioso:
            break
    return dados


def teste_separacao_h0036_console():
    """Regressao H-0036: separacao estrutural/externo dos consoles h0035.

    Prova que ``itens`` foi removido do JSON estrutural, que o conteudo esta no
    documento externo associado (carregamento separado dos dois arquivos), que
    a distribuicao_matricial de h0035_console_com foi preservada e que nao ha
    duplicacao entre estrutural e externo.
    """
    print("")
    print("== H-0036: separacao estrutural/externo dos consoles ==")
    for id_tela, id_conteudo, n_esperado, textos in [
        ("h0035_console_com", "h0035_console_com_conteudo", 12, ["P01 linha", "P12 linha"]),
        ("h0035_console_sem", "h0035_console_sem_conteudo", 2, ["Linha alfa", "Linha bravo"]),
    ]:
        caminho = os.path.join(_RAIZ_TELAS_DEMO, id_tela + ".json")
        with open(caminho, encoding="utf-8") as f:
            raw = json.load(f)
        console = next(
            (e for e in raw["corpo"]["elementos"] if e.get("tipo") == "console"),
            None,
        )
        _registrar(
            "{0}: JSON estrutural sem campo 'itens'".format(id_tela),
            console is not None and "itens" not in console,
        )
        _registrar(
            "{0}: catalogo associa ao documento externo {1}".format(id_tela, id_conteudo),
            id_conteudo_externo_de(id_tela) == id_conteudo,
        )
        doc = carregar_conteudo_externo(None, id_conteudo, _RAIZ_TELAS_DEMO)
        _registrar(
            "{0}: documento externo tem {1} nos".format(id_tela, n_esperado),
            _contar_nos_dados(doc.get("dados", [])) == n_esperado,
            "obtido={0}".format(_contar_nos_dados(doc.get("dados", []))),
        )
        # Nao-duplicacao: os textos do conteudo nao estao no JSON estrutural.
        estrutural_txt = json.dumps(raw, ensure_ascii=False)
        externo_txt = json.dumps(doc, ensure_ascii=False)
        _registrar(
            "{0}: conteudo nao duplicado no estrutural".format(id_tela),
            all(t not in estrutural_txt for t in textos)
            and all(t in externo_txt for t in textos),
        )
    # distribuicao_matricial de h0035_console_com preservada no estrutural.
    dm = _config_dm_fixture("h0035_console_com")
    _registrar(
        "h0035_console_com: distribuicao_matricial preservada no estrutural",
        dm is not None
        and dm.get("formacao", {}).get("politica") == "preferencia_colunas",
        "dm={0}".format(dm.get("formacao") if dm else None),
    )
    # h0035_console_sem permanece sem distribuicao_matricial.
    _registrar(
        "h0035_console_sem: permanece sem distribuicao_matricial",
        _config_dm_fixture("h0035_console_sem") is None,
    )


def teste_pseudo_tty():
    print("")
    print("-- Pseudo-TTY: selecao -> quadro minimo -> recuperacao --")
    try:
        import pty as _pty
        import struct as _struct
        import fcntl as _fcntl
        import termios as _termios
    except ImportError:
        _registrar("PTY indisponivel na plataforma (pulado)", True)
        return

    master_fd = None
    slave_fd = None
    proc = None
    COLS_N, LINS_N = 80, 24
    COLS_R, LINS_R = 30, 5
    try:
        master_fd, slave_fd = _pty.openpty()
        win = _struct.pack("HHHH", LINS_N, COLS_N, 0, 0)
        _fcntl.ioctl(slave_fd, _termios.TIOCSWINSZ, win)
        proc = subprocess.Popen(
            [sys.executable, "demo/demo_distribuicao.py", "h0035_pref_linhas"],
            stdin=slave_fd, stdout=slave_fd, stderr=slave_fd,
            cwd=str(_BASE_PADRAO), close_fds=True,
        )
        os.close(slave_fd)
        slave_fd = None
        os.set_blocking(master_fd, False)

        saida_ini = _ler_pty_ate_ocioso(master_fd, 3.0, 0.3)
        vivo_ini = proc.poll() is None
        _registrar(
            "PTY: familia pref_linhas renderizada (processo ativo, titulo presente)",
            vivo_ini and b"H0035 PREF LINHAS" in saida_ini,
            "vivo={0} bytes={1}".format(vivo_ini, len(saida_ini)),
        )

        win_r = _struct.pack("HHHH", LINS_R, COLS_R, 0, 0)
        _fcntl.ioctl(master_fd, _termios.TIOCSWINSZ, win_r)
        os.kill(proc.pid, signal.SIGWINCH)
        saida_red = _ler_pty_ate_ocioso(master_fd, 3.0, 0.3)
        _registrar(
            "PTY: reducao produz quadro minimo ('terminal pequeno demais')",
            b"terminal pequeno demais" in saida_red
            and b"H0035 PREF LINHAS" not in saida_red,
            "bytes={0}".format(len(saida_red)),
        )

        win_a = _struct.pack("HHHH", LINS_N, COLS_N, 0, 0)
        _fcntl.ioctl(master_fd, _termios.TIOCSWINSZ, win_a)
        os.kill(proc.pid, signal.SIGWINCH)
        saida_amp = _ler_pty_ate_ocioso(master_fd, 3.0, 0.3)
        _registrar(
            "PTY: ampliacao recupera a tela normal ('H0035 PREF LINHAS' de volta)",
            b"H0035 PREF LINHAS" in saida_amp
            and b"terminal pequeno demais" not in saida_amp,
            "bytes={0}".format(len(saida_amp)),
        )
    finally:
        try:
            if proc is not None and proc.poll() is None:
                proc.send_signal(signal.SIGTERM)
                try:
                    proc.wait(timeout=2.0)
                except subprocess.TimeoutExpired:
                    proc.kill()
        except Exception:
            pass
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


def teste_estrutura_catalogo():
    print("")
    print("== Estrutura do catalogo: chips de um caractere ==")
    modelo_cat = _carregar_modelo_por_id(_TELA_CATALOGO)
    lanc = [e for e in modelo_cat.corpo.elementos if e.tipo == "lancador"]
    _registrar("catalogo tem exatamente um lancador", len(lanc) == 1)
    if not lanc:
        return
    itens = lanc[0]._campos_inertes.get("itens", [])
    _registrar(
        "catalogo tem exatamente 25 entradas de conteudo",
        len(itens) == 25,
        "encontrado: {0}".format(len(itens)),
    )
    chips = [item.get("chip", "") for item in itens if isinstance(item, dict)]
    _registrar(
        "exatamente 25 comandos presentes",
        len(chips) == 25,
        "encontrado: {0}".format(len(chips)),
    )
    todos_um_char = all(len(c) == 1 for c in chips)
    _registrar(
        "cada comando possui exatamente um caractere",
        todos_um_char,
        "chips invalidos: {0}".format([c for c in chips if len(c) != 1]),
    )
    chips_unicos = len(chips) == len(set(chips))
    _registrar(
        "comandos sao unicos (sem duplicatas)",
        chips_unicos,
        "duplicatas: {0}".format(
            [c for c in chips if chips.count(c) > 1] if not chips_unicos else []
        ),
    )
    conjunto_obtido = set(chips)
    _registrar(
        "conjunto exato: '1'-'9' e 'A'-'P'",
        conjunto_obtido == _CHIPS_ESPERADOS,
        "diferenca: {0}".format(conjunto_obtido.symmetric_difference(_CHIPS_ESPERADOS)),
    )
    chips_dois_digitos = [c for c in chips if c in {str(n) for n in range(10, 26)}]
    _registrar(
        "inexistencia de comandos '10'-'25'",
        not chips_dois_digitos,
        "encontrados: {0}".format(chips_dois_digitos),
    )


def teste_selecao_integral_25_telas():
    print("")
    print("== Selecao integral das 25 telas (chip, identidade, retorno) ==")
    modelo_cat = _carregar_modelo_por_id(_TELA_CATALOGO)
    id_item_1 = _MAPEAMENTO_CATALOGO[0][1]
    todas_ok = True
    for chip, tela_id in _MAPEAMENTO_CATALOGO:
        estado = criar_estado_inicial()
        novo = processar_comando(estado, chip, modelo_cat)
        chegou = novo["tela_atual"] == tela_id
        if not chegou:
            todas_ok = False
            _registrar(
                "selecao chip={0} chega em {1}".format(chip, tela_id),
                False,
                "obtido={0}".format(novo["tela_atual"]),
            )
            continue
        modelo_dest = _carregar_modelo_por_id(tela_id)
        ident = descrever_tela(modelo_dest, 80, 24)
        identidade_ok = ident["nome"] == tela_id
        if not identidade_ok:
            todas_ok = False
            _registrar(
                "identidade semantica chip={0}".format(chip),
                False,
                "nome={0}".format(ident["nome"]),
            )
        if chip != "1":
            nao_e_item1 = novo["tela_atual"] != id_item_1
            if not nao_e_item1:
                todas_ok = False
                _registrar(
                    "chip={0} nao abre item_1 (ausencia de prefixo)".format(chip),
                    False,
                )
        retorno = processar_comando(novo, "s", modelo_dest)
        retornou = retorno["tela_atual"] == _TELA_CATALOGO
        if not retornou:
            todas_ok = False
            _registrar(
                "retorno ao catalogo apos chip={0}".format(chip),
                False,
                "obtido={0}".format(retorno["tela_atual"]),
            )
    _registrar(
        "selecao integral: 25 chips navegam, identificam e retornam",
        todas_ok,
    )


def teste_casos_de_fronteira():
    print("")
    print("== Casos de fronteira explicitamente requeridos ==")
    modelo_cat = _carregar_modelo_por_id(_TELA_CATALOGO)
    _1 = _MAPEAMENTO_CATALOGO[0]    # chip="1", item 1
    _9 = _MAPEAMENTO_CATALOGO[8]    # chip="9", item 9
    _A = _MAPEAMENTO_CATALOGO[9]    # chip="A", item 10
    _K = _MAPEAMENTO_CATALOGO[19]   # chip="K", item 20
    _P = _MAPEAMENTO_CATALOGO[24]   # chip="P", item 25

    for rotulo, chip, tela_esperada in [
        ("tecla_1 -> item_1", "1", _1[1]),
        ("tecla_9 -> item_9", "9", _9[1]),
        ("tecla_A -> item_10", "A", _A[1]),
        ("tecla_K -> item_20", "K", _K[1]),
        ("tecla_P -> item_25", "P", _P[1]),
    ]:
        estado = criar_estado_inicial()
        novo = processar_comando(estado, chip, modelo_cat)
        _registrar(rotulo, novo["tela_atual"] == tela_esperada,
                   "obtido={0}".format(novo["tela_atual"]))

    for rotulo, entrada, tela_esperada in [
        ("tecla_a (minuscula) -> item_10", "a", _A[1]),
        ("tecla_p (minuscula) -> item_25", "p", _P[1]),
    ]:
        ch_norm = _normalizar_tecla_catalogo(entrada, _TELA_CATALOGO)
        estado = criar_estado_inicial()
        novo = processar_comando(estado, ch_norm, modelo_cat)
        _registrar(rotulo, novo["tela_atual"] == tela_esperada,
                   "entrada={0!r} normalizado={1!r} obtido={2}".format(
                       entrada, ch_norm, novo["tela_atual"]))


def teste_regressao_defeito():
    print("")
    print("== Regressao: defeito de dois digitos e de prefixo ==")
    modelo_cat = _carregar_modelo_por_id(_TELA_CATALOGO)
    lanc = [e for e in modelo_cat.corpo.elementos if e.tipo == "lancador"]
    itens = lanc[0]._campos_inertes.get("itens", []) if lanc else []
    chips = [item.get("chip", "") for item in itens if isinstance(item, dict)]

    _registrar(
        "regressao: nenhum chip possui dois caracteres",
        all(len(c) == 1 for c in chips),
        "chips de dois chars: {0}".format([c for c in chips if len(c) != 1]),
    )
    _registrar(
        "regressao: nenhum chip e '10' a '25'",
        not any(c in {str(n) for n in range(10, 26)} for c in chips),
    )
    _registrar(
        "regressao: chips sao unicos (sem colisao entre teclas)",
        len(chips) == len(set(chips)),
    )

    item_10 = _MAPEAMENTO_CATALOGO[9]
    item_25 = _MAPEAMENTO_CATALOGO[24]

    estado = criar_estado_inicial()
    nav_A = processar_comando(estado, "A", modelo_cat)
    _registrar(
        "regressao: 'A' abre item_10 ({0})".format(item_10[1]),
        nav_A["tela_atual"] == item_10[1],
        "obtido={0}".format(nav_A["tela_atual"]),
    )
    nav_P = processar_comando(criar_estado_inicial(), "P", modelo_cat)
    _registrar(
        "regressao: 'P' abre item_25 ({0})".format(item_25[1]),
        nav_P["tela_atual"] == item_25[1],
        "obtido={0}".format(nav_P["tela_atual"]),
    )

    nav_1_prefixo = processar_comando(criar_estado_inicial(), "1", modelo_cat)
    id_item_1 = _MAPEAMENTO_CATALOGO[0][1]
    _registrar(
        "regressao: '1' nao e prefixo de '10'-'19' (abre exatamente item_1)",
        nav_1_prefixo["tela_atual"] == id_item_1,
        "obtido={0}".format(nav_1_prefixo["tela_atual"]),
    )
    nav_2_prefixo = processar_comando(criar_estado_inicial(), "2", modelo_cat)
    id_item_2 = _MAPEAMENTO_CATALOGO[1][1]
    _registrar(
        "regressao: '2' nao e prefixo de '20'-'25' (abre exatamente item_2)",
        nav_2_prefixo["tela_atual"] == id_item_2,
        "obtido={0}".format(nav_2_prefixo["tela_atual"]),
    )

    chip_catalogo_por_tela = {}
    for item in itens:
        if isinstance(item, dict):
            chip_catalogo_por_tela[item.get("tela_destino")] = item.get("chip")
    estado_a = criar_estado_inicial()
    novo_a = processar_comando(estado_a, "A", modelo_cat)
    chip_exibido = chip_catalogo_por_tela.get(novo_a["tela_atual"], "")
    _registrar(
        "regressao: chip exibido para item_10 coincide com tecla aceita ('A')",
        chip_exibido == "A",
        "chip_exibido={0!r}".format(chip_exibido),
    )


def teste_fixtures_geometria():
    """Verificacoes geometricas independentes dos fixtures (quarto patch).

    Usa calcular_distribuicao diretamente com min_ws/min_hs conhecidos.
    Valores esperados calculados independentemente do algoritmo de producao.
    """
    print("")
    print("== Fixtures: geometria e formacoes observaveis ==")

    # --- Contagem de participantes ---
    requisitos_contagem = [
        ("h0035_pref_linhas", 12),
        ("h0035_pref_colunas", 12),
        ("h0035_matriz_fixa_cabe", 12),
        ("h0035_matriz_fixa_quadro_minimo", 16),
        ("h0035_centralizado_h_colunas", 12),
        ("h0035_esquerda_margens_min_max", 12),
        ("h0035_h_uniforme", 12),
        ("h0035_h_margens_limitadas", 12),
        ("h0035_v_margens_min", 12),
        ("h0035_v_margens_min_max", 12),
        ("h0035_v_uniforme", 12),
        ("h0035_resto_horizontal", 7),
        ("h0035_resto_vertical", 7),
        ("h0035_console_com", 12),
        ("h0035_lancador_com", 12),
        ("h0035_dashboard_com", 12),
    ]
    contagens_ok = True
    for id_tela, n_esperado in requisitos_contagem:
        n = _n_campos_fixture(id_tela)
        if n < n_esperado:
            contagens_ok = False
            _registrar(
                "contagem {0}".format(id_tela),
                False,
                "esperado>={0} obtido={1}".format(n_esperado, n),
            )
    _registrar("todos os fixtures com cardinalidade minima", contagens_ok)

    # --- pref_linhas: >= 2 formacoes distintas em areas diferentes ---
    # min_ws = [13]*12 ("P01: Dado P01" = 13 chars)
    dm_pl = _config_dm_fixture("h0035_pref_linhas")
    min_ws_13 = [13] * 12
    min_hs_1 = [1] * 12
    # area_w=78 (80-col terminal - 2 bordas): 3x4 (57<=78, 1x12=169>78, 2x6=85>78)
    res_pl_78 = calcular_distribuicao(78, 22, 12, dm_pl, min_ws_13, min_hs_1)
    # area_w=120: 2x6 (85<=120)
    res_pl_120 = calcular_distribuicao(120, 22, 12, dm_pl, min_ws_13, min_hs_1)
    form_pl_78 = res_pl_78["formacao"]
    form_pl_120 = res_pl_120["formacao"]
    _registrar(
        "pref_linhas: 2 formacoes distintas (78 vs 120 cols)",
        form_pl_78 != form_pl_120 and not res_pl_78["fallback"],
        "w=78->{0} w=120->{1}".format(form_pl_78, form_pl_120),
    )
    _registrar(
        "pref_linhas: w=78 -> formacao (3,4)",
        form_pl_78 == (3, 4),
        str(form_pl_78),
    )
    _registrar(
        "pref_linhas: w=120 -> formacao (2,6)",
        form_pl_120 == (2, 6),
        str(form_pl_120),
    )

    # --- pref_colunas: >= 2 formacoes distintas em alturas diferentes ---
    dm_pc = _config_dm_fixture("h0035_pref_colunas")
    # area_h=22: pref_colunas min=1 -> 1 col primeiro que cabe (1x12, h=12<=22)
    res_pc_h22 = calcular_distribuicao(78, 22, 12, dm_pc, min_ws_13, min_hs_1)
    # area_h=4: 12x1 precisa h=12>4, 6x2 precisa h=6>4, 4x3 precisa h=4<=4 OK
    res_pc_h4 = calcular_distribuicao(78, 4, 12, dm_pc, min_ws_13, min_hs_1)
    form_pc_h22 = res_pc_h22["formacao"]
    form_pc_h4 = res_pc_h4["formacao"]
    _registrar(
        "pref_colunas: 2 formacoes distintas (h=22 vs h=4)",
        form_pc_h22 != form_pc_h4,
        "h=22->{0} h=4->{1}".format(form_pc_h22, form_pc_h4),
    )

    # --- matriz_fixa_cabe: formacao 3x4 preservada ---
    dm_mc = _config_dm_fixture("h0035_matriz_fixa_cabe")
    res_mc = calcular_distribuicao(100, 20, 12, dm_mc, min_ws_13, min_hs_1)
    _registrar(
        "matriz_fixa_cabe: formacao 3x4 preservada",
        res_mc["formacao"] == (3, 4) and not res_mc["fallback"],
        str(res_mc["formacao"]),
    )

    # --- dois eixos simultaneos (matriz_fixa_cabe H+V uniforme) ---
    # Valores calculados independentemente (ver analise no comentario do patch):
    # Pair A (w=100, h=20): spare_w=43, 5 slots H, base=8 rem=3 -> m_ini=9
    #   spare_h=15, 4 slots V, base=3 rem=3 -> m_sup=3, vao_v0=5 -> celulas[4].y=9
    # Pair B (w=70, h=10): spare_w=13, base=2 rem=3 -> m_ini=3
    #   spare_h=5, base=1 rem=1 -> m_sup=1, vao_v0=2 -> celulas[4].y=4
    res_A = calcular_distribuicao(100, 20, 12, dm_mc, min_ws_13, min_hs_1)
    res_B = calcular_distribuicao(70, 10, 12, dm_mc, min_ws_13, min_hs_1)
    _registrar(
        "dois eixos: formacao (3,4) em ambos os pares",
        res_A["formacao"] == (3, 4) and res_B["formacao"] == (3, 4),
        "{0} / {1}".format(res_A["formacao"], res_B["formacao"]),
    )
    x_A = res_A["celulas"][0]["x"]
    x_B = res_B["celulas"][0]["x"]
    _registrar(
        "dois eixos: eixo H ativo (celula[0].x cresce com largura)",
        x_A > x_B,
        "x_A={0} x_B={1}".format(x_A, x_B),
    )
    _registrar(
        "dois eixos: x_A=9 (valor independente w=100, 5 slots, base=8 rem=3)",
        x_A == 9,
        "obtido={0}".format(x_A),
    )
    _registrar(
        "dois eixos: x_B=3 (valor independente w=70, 5 slots, base=2 rem=3)",
        x_B == 3,
        "obtido={0}".format(x_B),
    )
    y_A = res_A["celulas"][4]["y"]
    y_B = res_B["celulas"][4]["y"]
    _registrar(
        "dois eixos: eixo V ativo (celula[4].y cresce com altura)",
        y_A > y_B,
        "y_A={0} y_B={1}".format(y_A, y_B),
    )
    _registrar(
        "dois eixos: y_A=9 (valor independente h=20, 4 slots V, base=3 rem=3)",
        y_A == 9,
        "obtido={0}".format(y_A),
    )
    _registrar(
        "dois eixos: y_B=4 (valor independente h=10, 4 slots V, base=1 rem=1)",
        y_B == 4,
        "obtido={0}".format(y_B),
    )

    # --- h_uniforme: politica_horizontal=uniforme, m_ini crece com largura ---
    # Fixture: pref_linhas linhas={min:3,max:3}, 12 partic, uniforme H
    # Formation fixa: 3 linhas x ceil(12/3)=4 colunas
    # min_w_total = 4*13 + 3*1(vaos) + 1+1(margins) = 57
    # At w=100: spare=43, 5 slots, base=8, rem=3 -> m_ini=9
    # At w=70:  spare=13, 5 slots, base=2, rem=3 -> m_ini=3
    dm_hu = _config_dm_fixture("h0035_h_uniforme")
    res_hu_100 = calcular_distribuicao(100, 20, 12, dm_hu, min_ws_13, min_hs_1)
    res_hu_70 = calcular_distribuicao(70, 20, 12, dm_hu, min_ws_13, min_hs_1)
    _registrar(
        "h_uniforme: politica declarada como uniforme",
        dm_hu["distribuicao_horizontal"]["politica"] == "uniforme",
    )
    _registrar(
        "h_uniforme: formacao 3x4 em ambas as larguras",
        res_hu_100["formacao"] == (3, 4) and res_hu_70["formacao"] == (3, 4),
        "{0} / {1}".format(res_hu_100["formacao"], res_hu_70["formacao"]),
    )
    x_hu_100 = res_hu_100["celulas"][0]["x"]
    x_hu_70 = res_hu_70["celulas"][0]["x"]
    _registrar(
        "h_uniforme: margem_esq cresce com largura (pol_h=uniforme ativa)",
        x_hu_100 > x_hu_70,
        "x(100)={0} x(70)={1}".format(x_hu_100, x_hu_70),
    )
    _registrar(
        "h_uniforme: x(100)=9 (independente: spare=43, 5 slots, base=8 rem=3)",
        x_hu_100 == 9,
        "obtido={0}".format(x_hu_100),
    )
    _registrar(
        "h_uniforme: x(70)=3 (independente: spare=13, 5 slots, base=2 rem=3)",
        x_hu_70 == 3,
        "obtido={0}".format(x_hu_70),
    )

    # --- v_uniforme: politica_vertical=uniforme, celula[3].y cresce com altura ---
    # Fixture: pref_linhas linhas={min:4,max:4}, 12 partic, vao_v=1, uniforme V
    # Formation fixa: 4 linhas x ceil(12/4)=3 colunas
    # total_min_h = 4*1 + 3*1(vaos_v) + 0+0 = 7
    # Slots V: [m_sup(0), vao_v0(1), vao_v1(2), vao_v2(3), m_inf(4)], todos=[0,4,1,2,3]
    # At h=30: spare=23, base=4, rem=3 -> vaos_v=[6,6,6], m_sup=4
    #          celulas[3].y = m_sup + linhas[0] + vaos_v[0] = 4 + 1 + 6 = 11
    # At h=15: spare=8, base=1, rem=3 -> vaos_v=[3,3,3], m_sup=1
    #          celulas[3].y = 1 + 1 + 3 = 5
    dm_vu = _config_dm_fixture("h0035_v_uniforme")
    min_ws_13_12 = [13] * 12
    min_hs_1_12 = [1] * 12
    res_vu_h30 = calcular_distribuicao(78, 30, 12, dm_vu, min_ws_13_12, min_hs_1_12)
    res_vu_h15 = calcular_distribuicao(78, 15, 12, dm_vu, min_ws_13_12, min_hs_1_12)
    _registrar(
        "v_uniforme: politica declarada como uniforme",
        dm_vu["distribuicao_vertical"]["politica"] == "uniforme",
    )
    _registrar(
        "v_uniforme: formacao 4x3 em ambas as alturas",
        res_vu_h30["formacao"] == (4, 3) and res_vu_h15["formacao"] == (4, 3),
        "{0} / {1}".format(res_vu_h30["formacao"], res_vu_h15["formacao"]),
    )
    y_vu_h30 = res_vu_h30["celulas"][3]["y"]
    y_vu_h15 = res_vu_h15["celulas"][3]["y"]
    _registrar(
        "v_uniforme: celula[3].y cresce com altura (pol_v=uniforme ativa)",
        y_vu_h30 > y_vu_h15,
        "y(h=30)={0} y(h=15)={1}".format(y_vu_h30, y_vu_h15),
    )
    _registrar(
        "v_uniforme: y(h=30)=11 (independente: spare=23, 5 slots, base=4 rem=3)",
        y_vu_h30 == 11,
        "obtido={0}".format(y_vu_h30),
    )
    _registrar(
        "v_uniforme: y(h=15)=5 (independente: spare=8, 5 slots, base=1 rem=3)",
        y_vu_h15 == 5,
        "obtido={0}".format(y_vu_h15),
    )

    # --- matriz_fixa_quadro_minimo: fallback em area pequena, formacao (4,4) ampla ---
    # min_w = 4*20 + 3*1 + 1+1 = 85 (minimo_fixo=20)
    dm_qm = _config_dm_fixture("h0035_matriz_fixa_quadro_minimo")
    min_ws_20 = [20] * 16
    min_hs_1_16 = [1] * 16
    res_qm_peq = calcular_distribuicao(40, 10, 16, dm_qm, min_ws_20, min_hs_1_16)
    res_qm_amp = calcular_distribuicao(120, 40, 16, dm_qm, min_ws_20, min_hs_1_16)
    _registrar(
        "matriz 4x4: fallback em area pequena (40x10)",
        res_qm_peq["fallback"],
        "fallback={0}".format(res_qm_peq["fallback"]),
    )
    _registrar(
        "matriz 4x4: formacao (4,4) em area ampla (120x40)",
        res_qm_amp["formacao"] == (4, 4) and not res_qm_amp["fallback"],
        str(res_qm_amp["formacao"]),
    )
    # Segunda reducao e recuperacao sao deterministicas.
    res_qm_peq2 = calcular_distribuicao(40, 10, 16, dm_qm, min_ws_20, min_hs_1_16)
    res_qm_amp2 = calcular_distribuicao(120, 40, 16, dm_qm, min_ws_20, min_hs_1_16)
    _registrar(
        "matriz 4x4: fallback deterministico (segunda reducao = primeira)",
        res_qm_peq["fallback"] == res_qm_peq2["fallback"],
    )
    _registrar(
        "matriz 4x4: recuperacao deterministica (segunda ampliacao = primeira)",
        res_qm_amp["formacao"] == res_qm_amp2["formacao"],
    )

    # --- esquerda_margens_min_max: limites min/max respeitados ---
    dm_em = _config_dm_fixture("h0035_esquerda_margens_min_max")
    # At w=78, pref_linhas min=1 -> formacao (3,4)
    res_em = calcular_distribuicao(78, 22, 12, dm_em, min_ws_13, min_hs_1)
    _registrar(
        "esquerda_margens: sem fallback em 78x22",
        not res_em["fallback"],
    )
    if not res_em["fallback"]:
        m_esq = res_em["grade"]["margem_esq"]
        m_dir = res_em["grade"]["margem_dir"]
        vaos = res_em["grade"]["vaos_h"]
        _registrar(
            "esquerda_margens: m_esq dentro de [1,2]",
            1 <= m_esq <= 2,
            "m_esq={0}".format(m_esq),
        )
        _registrar(
            "esquerda_margens: m_dir dentro de [1,8]",
            1 <= m_dir <= 8,
            "m_dir={0}".format(m_dir),
        )
        _registrar(
            "esquerda_margens: vaos dentro de [2,4]",
            all(2 <= v <= 4 for v in vaos),
            "vaos={0}".format(vaos),
        )

    # --- resto horizontal: vaos recebem resto > margens ---
    # 7 partic "P0N: D0N" = 8 chars, 1 linha x 7 colunas
    # At area_w=78: spare=14, 8 slots, base=1, rem=6 -> vaos[0..5]=3, m_ini=m_fim=2
    dm_rh = _config_dm_fixture("h0035_resto_horizontal")
    min_ws_8 = [8] * 7
    min_hs_1_7 = [1] * 7
    res_rh = calcular_distribuicao(78, 10, 7, dm_rh, min_ws_8, min_hs_1_7)
    _registrar(
        "resto_horizontal: formacao 1x7 em 78x10",
        res_rh["formacao"] == (1, 7) and not res_rh["fallback"],
        str(res_rh["formacao"]),
    )
    if not res_rh["fallback"] and res_rh["formacao"] == (1, 7):
        vao_h0 = res_rh["grade"]["vaos_h"][0]
        m_esq_rh = res_rh["grade"]["margem_esq"]
        _registrar(
            "resto_horizontal: vaos[0]=3 (rem=6 distribui extras aos 6 vaos)",
            vao_h0 == 3,
            "vaos_h[0]={0}".format(vao_h0),
        )
        _registrar(
            "resto_horizontal: margem_esq=2 (nao recebe extra resto)",
            m_esq_rh == 2,
            "margem_esq={0}".format(m_esq_rh),
        )
        _registrar(
            "resto_horizontal: resto observavel (vaos > margem_esq)",
            vao_h0 > m_esq_rh,
            "vaos[0]={0} m_esq={1}".format(vao_h0, m_esq_rh),
        )

    # --- resto vertical: margem_sup recebe resto (ao_primeiro) ---
    # 7 partic "P0N: D0N" = 8 chars, 3 linhas x 3 colunas (9 celulas, 7 usadas)
    # At area_h=20: spare=17, 4 slots V, base=4, rem=1 -> m_sup=5, m_inf=4
    dm_rv = _config_dm_fixture("h0035_resto_vertical")
    res_rv = calcular_distribuicao(78, 20, 7, dm_rv, min_ws_8, min_hs_1_7)
    _registrar(
        "resto_vertical: formacao 3x3 em 78x20",
        res_rv["formacao"] == (3, 3) and not res_rv["fallback"],
        str(res_rv["formacao"]),
    )
    if not res_rv["fallback"] and res_rv["formacao"] == (3, 3):
        m_sup = res_rv["grade"]["margem_sup"]
        m_inf = res_rv["grade"]["margem_inf"]
        _registrar(
            "resto_vertical: m_sup=5 (ao_primeiro: m_sup recebe o resto)",
            m_sup == 5,
            "m_sup={0}".format(m_sup),
        )
        _registrar(
            "resto_vertical: m_inf=4 (nao recebe o resto)",
            m_inf == 4,
            "m_inf={0}".format(m_inf),
        )
        _registrar(
            "resto_vertical: resto observavel (m_sup > m_inf)",
            m_sup > m_inf,
            "m_sup={0} m_inf={1}".format(m_sup, m_inf),
        )

    # --- consumidores com/sem DM distinguiveis ---
    m_con_com = _carregar_modelo_por_id("h0035_console_com")
    id_con_com = descrever_tela(m_con_com, 80, 24)
    m_con_sem = _carregar_modelo_por_id("h0035_console_sem")
    id_con_sem = descrever_tela(m_con_sem, 80, 24)
    _registrar(
        "console_com: familia indica DM presente",
        id_con_com["familia"] != "(sem distribuicao_matricial)",
        id_con_com["familia"],
    )
    _registrar(
        "console_sem: familia indica DM ausente",
        id_con_sem["familia"] == "(sem distribuicao_matricial)",
        id_con_sem["familia"],
    )
    _registrar(
        "console com/sem: familias inequivocamente distintas",
        id_con_com["familia"] != id_con_sem["familia"],
    )

    m_lan_com = _carregar_modelo_por_id("h0035_lancador_com")
    id_lan_com = descrever_tela(m_lan_com, 80, 24)
    m_lan_sem = _carregar_modelo_por_id("h0035_lancador_sem")
    id_lan_sem = descrever_tela(m_lan_sem, 80, 24)
    _registrar(
        "lancador com/sem: familias inequivocamente distintas",
        id_lan_com["familia"] != id_lan_sem["familia"],
    )

    m_dash_com = _carregar_modelo_por_id("h0035_dashboard_com")
    id_dash_com = descrever_tela(m_dash_com, 80, 24)
    m_dash_sem = _carregar_modelo_por_id("h0035_dashboard_sem")
    id_dash_sem = descrever_tela(m_dash_sem, 80, 24)
    _registrar(
        "dashboard com/sem: familias inequivocamente distintas",
        id_dash_com["familia"] != id_dash_sem["familia"],
    )


def teste_pseudo_tty_catalogo():
    print("")
    print("-- Pseudo-TTY catalogo: 25 teclas + a e p minusculos sem Enter --")
    try:
        import pty as _pty
        import struct as _struct
        import fcntl as _fcntl
        import termios as _termios
    except ImportError:
        _registrar("PTY catalogo: indisponivel na plataforma (pulado)", True)
        return

    COLS, LINS = 120, 40

    # Pares (tecla_byte, tela_esperada) na ordem canonica do catalogo.
    # Inclui explicitamente: 1, 9, A, a, K, P, p.
    _TECLAS_PTY = [
        (b"1", "h0035_pref_linhas"),
        (b"2", "h0035_pref_colunas"),
        (b"3", "h0035_matriz_fixa_cabe"),
        (b"4", "h0035_matriz_fixa_quadro_minimo"),
        (b"5", "h0035_centralizado_h_colunas"),
        (b"6", "h0035_esquerda_margens_min_max"),
        (b"7", "h0035_h_uniforme"),
        (b"8", "h0035_h_margens_limitadas"),
        (b"9", "h0035_v_margens_min"),
        (b"A", "h0035_v_margens_min_max"),
        (b"a", "h0035_v_margens_min_max"),
        (b"B", "h0035_v_uniforme"),
        (b"C", "h0035_um_centralizado"),
        (b"D", "h0035_tres_centralizados"),
        (b"E", "h0035_quatro_centralizados"),
        (b"F", "h0035_minimo_fixo_excedido"),
        (b"G", "h0035_uma_linha"),
        (b"H", "h0035_uma_coluna"),
        (b"I", "h0035_resto_horizontal"),
        (b"J", "h0035_resto_vertical"),
        (b"K", "h0035_console_com"),
        (b"L", "h0035_console_sem"),
        (b"M", "h0035_lancador_com"),
        (b"N", "h0035_lancador_sem"),
        (b"O", "h0035_dashboard_com"),
        (b"P", "h0035_dashboard_sem"),
        (b"p", "h0035_dashboard_sem"),
    ]

    master_fd = None
    slave_fd = None
    proc = None
    try:
        master_fd, slave_fd = _pty.openpty()
        win = _struct.pack("HHHH", LINS, COLS, 0, 0)
        _fcntl.ioctl(slave_fd, _termios.TIOCSWINSZ, win)
        proc = subprocess.Popen(
            [sys.executable, "demo/demo_distribuicao.py"],
            stdin=slave_fd, stdout=slave_fd, stderr=slave_fd,
            cwd=str(_BASE_PADRAO), close_fds=True,
        )
        os.close(slave_fd)
        slave_fd = None
        os.set_blocking(master_fd, False)

        saida_ini = _ler_pty_ate_ocioso(master_fd, 3.0, 0.3)
        vivo = proc.poll() is None
        _registrar(
            "PTY catalogo: catalogo inicial renderizado (H0035 CATALOGO presente)",
            vivo and b"H0035 CATALOGO" in saida_ini,
            "vivo={0} bytes={1}".format(vivo, len(saida_ini)),
        )
        if not vivo:
            return

        teclas_falha = []
        for tecla_b, tela_id in _TECLAS_PTY:
            titulo_b = _TITULO_RENDERIZADO[tela_id]
            os.write(master_fd, tecla_b)
            saida = _ler_pty_ate_ocioso(master_fd, 2.0, 0.2)
            if titulo_b not in saida:
                teclas_falha.append("{0}->{1}".format(
                    tecla_b.decode("latin-1"), tela_id))
            os.write(master_fd, b"s")
            _ler_pty_ate_ocioso(master_fd, 1.0, 0.2)

        _registrar(
            "PTY catalogo: todas as 27 teclas navegam sem Enter",
            not teclas_falha,
            "falhas={0}".format(teclas_falha) if teclas_falha else "todas ok",
        )
        for rotulo, tecla_b, tela_id in [
            ("PTY: tecla_1 navega (fronteira digitos inf.)", b"1",
             "h0035_pref_linhas"),
            ("PTY: tecla_9 navega (fronteira digitos sup.)", b"9",
             "h0035_v_margens_min"),
            ("PTY: tecla_A navega (item 10, fronteira letras inf.)", b"A",
             "h0035_v_margens_min_max"),
            ("PTY: tecla_a (minuscula) navega igual a A", b"a",
             "h0035_v_margens_min_max"),
            ("PTY: tecla_K navega (item 20)", b"K",
             "h0035_console_com"),
            ("PTY: tecla_P navega (item 25, fronteira letras sup.)", b"P",
             "h0035_dashboard_sem"),
            ("PTY: tecla_p (minuscula) navega igual a P", b"p",
             "h0035_dashboard_sem"),
        ]:
            tecla_str = tecla_b.decode("latin-1")
            _registrar(
                rotulo,
                not any(f.startswith("{0}->".format(tecla_str)) for f in teclas_falha),
            )
    finally:
        try:
            if proc is not None and proc.poll() is None:
                proc.send_signal(signal.SIGTERM)
                try:
                    proc.wait(timeout=2.0)
                except subprocess.TimeoutExpired:
                    proc.kill()
        except Exception:
            pass
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


def main_testes():
    print("Diagnostico H-0035 - demo dedicado de distribuicao matricial")
    print("Base padrao: {0}".format(_BASE_PADRAO))
    print("Python: {0}".format(sys.version.split()[0]))

    teste_estrutura_catalogo()
    teste_catalogo_dedicado()
    teste_selecao_de_todas()
    teste_selecao_integral_25_telas()
    teste_casos_de_fronteira()
    teste_regressao_defeito()
    teste_identidade_semantica()
    teste_quadro_minimo_e_recuperacao()
    teste_fixtures_geometria()
    teste_separacao_h0036_console()
    teste_comando_de_entrada_e_erros()
    teste_demo_principal_preservado()
    teste_pseudo_tty()
    teste_pseudo_tty_catalogo()

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
    sys.exit(main_testes())
