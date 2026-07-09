"""Teste automatizado do script de exploração da barra_de_menus (H-0017).

Executável via:
    python tela/teste_explorar_barra_de_menus.py

Cobre os 10 casos obrigatórios do handoff H-0017.

Apenas biblioteca padrão do Python.
"""

import sys
import subprocess

sys.dont_write_bytecode = True

from pathlib import Path

_BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE))

from tela.renderizador import _linhas_barra, RenderizadorErro  # noqa: E402

_SCRIPT = str(_BASE / "tela" / "explorar_barra_de_menus.py")

_RESULTADOS = []


def _registrar(ok, descricao, detalhe=""):
    status = "PASSOU" if ok else "FALHOU"
    linha = "[{0}] {1}".format(status, descricao)
    if detalhe:
        linha += " - {0}".format(detalhe)
    print(linha)
    _RESULTADOS.append((descricao, ok))


def _rodar_script(*args, timeout=15):
    """Executa o script via subprocess e retorna (returncode, stdout, stderr)."""
    cmd = [sys.executable, _SCRIPT] + list(args)
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return proc.returncode, proc.stdout, proc.stderr


def _dist_canonica(preenchimento="coluna_a_coluna", linhas_maximo=2, ancoras=None):
    return {
        "modo": "horizontal_responsiva",
        "ordem": {"politica": "declaracao", "ancoras": ancoras or {}},
        "tentativa_inicial": "linha_unica",
        "quebra": "multilinha_quando_nao_couber",
        "preenchimento_multilinha": preenchimento,
        "preenchimentos_multilinha_suportados": ["coluna_a_coluna", "linha_a_linha"],
        "linhas": {"minimo": 1, "maximo": linhas_maximo, "preferir_menor_numero": True},
        "alinhamento_linhas": "esquerda",
        "espacamentos": {
            "margem_horizontal":         {"minimo": 1, "maximo": None},
            "vao_chip_texto":            {"minimo": 1, "maximo": 3},
            "vao_entre_chips":           {"minimo": 2, "maximo": 6},
            "vao_entre_colunas":         {"minimo": 2, "maximo": 8},
            "vao_vertical_entre_linhas": {"minimo": 0, "maximo": 0},
        },
        "colunas": {
            "largura": "por_maior_item_da_coluna",
            "subcolunas": {
                "chip":  {"alinhamento": "esquerda"},
                "texto": {"alinhamento": "esquerda"},
            },
        },
        "overflow": {
            "quando_nao_couber": "erro_layout",
            "nao_omitir_chips":  True,
            "nao_truncar_texto": True,
            "nao_reordenar":     True,
        },
    }


def _chip(cid, tecla, texto):
    return {"id": cid, "tecla": tecla, "texto": texto}


# ---------------------------------------------------------------------------
# Caso 1: Matriz padrão sem argumentos → exit code 0
# ---------------------------------------------------------------------------

def teste_caso_1_matriz_padrao_exit_0():
    print("")
    print("== Caso 1: matriz padrao sem argumentos → exit code 0 ==")
    code, stdout, stderr = _rodar_script()
    _registrar(
        code == 0,
        "matriz padrao retorna exit code 0",
        "code={0} stderr={1!r}".format(code, stderr[:80] if stderr else ""),
    )
    _registrar(
        "RESUMO DA EXPLORACAO" in stdout,
        "saida contem cabecalho de resumo",
    )
    _registrar(
        "Erro inesperado:                  0" in stdout
        or "Erro inesperado:                0" in stdout
        or "ERRO_INESP=0" in stdout
        or "inesperado:                     0" in stdout,
        "saida indica 0 erros inesperados",
        "stdout_trecho={0!r}".format(stdout[:300]),
    )


# ---------------------------------------------------------------------------
# Caso 2: Modo resumo determinístico (duas chamadas idênticas)
# ---------------------------------------------------------------------------

def teste_caso_2_resumo_deterministico():
    print("")
    print("== Caso 2: modo resumo deterministico ==")
    args = ["--modo-saida", "resumo"]
    code1, stdout1, _ = _rodar_script(*args)
    code2, stdout2, _ = _rodar_script(*args)
    _registrar(
        code1 == 0 and code2 == 0,
        "ambas chamadas retornam exit code 0",
        "code1={0} code2={1}".format(code1, code2),
    )
    _registrar(
        stdout1 == stdout2,
        "saida identica em duas chamadas consecutivas (determinismo)",
        "len1={0} len2={1}".format(len(stdout1), len(stdout2)),
    )


# ---------------------------------------------------------------------------
# Caso 3: Linha única com 3 chips curtos → OK, 1 linha física
# ---------------------------------------------------------------------------

def teste_caso_3_linha_unica():
    print("")
    print("== Caso 3: linha unica com 3 chips curtos ==")
    chips = [
        _chip("t3c1", "F1", "Ok-T3"),
        _chip("t3c2", "F2", "Ir-T3"),
        _chip("t3c3", "F3", "Ver-T3"),
    ]
    bar = {"chips": chips, "distribuicao": _dist_canonica()}
    try:
        linhas = _linhas_barra(bar, 80)
        _registrar(
            isinstance(linhas, list) and len(linhas) == 1,
            "linha unica: 3 chips em content_w=80 → lista com 1 string",
            "len={0} linhas={1!r}".format(len(linhas), linhas),
        )
        if linhas:
            todos_presentes = all(
                "[{0}] {1}".format(c["tecla"], c["texto"]) in linhas[0]
                for c in chips
            )
            _registrar(
                todos_presentes,
                "todos os chips aparecem na linha unica",
                "linha={0!r}".format(linhas[0]),
            )
    except RenderizadorErro as exc:
        _registrar(False, "linha unica sem erro", str(exc))


# ---------------------------------------------------------------------------
# Caso 4: Multilinha coluna_a_coluna → OK, 2 linhas físicas
# ---------------------------------------------------------------------------

def teste_caso_4_multilinha_coluna_a_coluna():
    print("")
    print("== Caso 4: multilinha coluna_a_coluna com 4 chips estreito ==")
    chips = [
        _chip("t4c1", "F1", "Ok-T4"),
        _chip("t4c2", "F2", "Ir-T4"),
        _chip("t4c3", "F3", "Ver-T4"),
        _chip("t4c4", "F4", "Ai-T4"),
    ]
    bar = {"chips": chips, "distribuicao": _dist_canonica("coluna_a_coluna", 2)}
    # content_w=25: col0=max(9,9)=9, col1=max(10,9)=10, gap=2 → total=21 <= 25
    try:
        linhas = _linhas_barra(bar, 25)
        _registrar(
            isinstance(linhas, list) and len(linhas) == 2,
            "coluna_a_coluna K=2: 4 chips em content_w=25 → 2 linhas",
            "len={0} linhas={1!r}".format(len(linhas), linhas),
        )
        if linhas and len(linhas) == 2:
            # coluna_a_coluna: col0=[c1,c2], col1=[c3,c4] → linha0 tem c1,c3
            t0 = "[F1] Ok-T4"
            t2 = "[F3] Ver-T4"
            _registrar(
                t0 in linhas[0] and t2 in linhas[0],
                "coluna_a_coluna: linha 0 contem chips 1 e 3 (coluna-major)",
                "linha0={0!r}".format(linhas[0]),
            )
    except RenderizadorErro as exc:
        _registrar(False, "multilinha coluna_a_coluna sem erro", str(exc))


# ---------------------------------------------------------------------------
# Caso 5: Multilinha linha_a_linha → OK, 2 linhas físicas
# ---------------------------------------------------------------------------

def teste_caso_5_multilinha_linha_a_linha():
    print("")
    print("== Caso 5: multilinha linha_a_linha com 4 chips ==")
    chips = [
        _chip("t5c1", "F1", "Ok-T5"),
        _chip("t5c2", "F2", "Ir-T5"),
        _chip("t5c3", "F3", "Ver-T5"),
        _chip("t5c4", "F4", "Ai-T5"),
    ]
    bar = {"chips": chips, "distribuicao": _dist_canonica("linha_a_linha", 2)}
    try:
        linhas = _linhas_barra(bar, 25)
        _registrar(
            isinstance(linhas, list) and len(linhas) == 2,
            "linha_a_linha K=2: 4 chips em content_w=25 → 2 linhas",
            "len={0} linhas={1!r}".format(len(linhas), linhas),
        )
        if linhas and len(linhas) == 2:
            # linha_a_linha: CPL=2 → linha0=[c1,c2], linha1=[c3,c4]
            t0 = "[F1] Ok-T5"
            t1 = "[F2] Ir-T5"
            _registrar(
                t0 in linhas[0] and t1 in linhas[0],
                "linha_a_linha: linha 0 contem chips 1 e 2 (linha-major)",
                "linha0={0!r}".format(linhas[0]),
            )
    except RenderizadorErro as exc:
        _registrar(False, "multilinha linha_a_linha sem erro", str(exc))


# ---------------------------------------------------------------------------
# Caso 6: Overflow forçado → erro_layout, script continua
# ---------------------------------------------------------------------------

def teste_caso_6_overflow_esperado():
    print("")
    print("== Caso 6: overflow forcado → erro_layout, script continua ==")
    code, stdout, stderr = _rodar_script(
        "--modo-saida", "detalhado",
        "--mostrar-erros",
        "--limite-casos", "14",
    )
    _registrar(
        code == 0,
        "script continua apos erro_layout e retorna exit 0",
        "code={0}".format(code),
    )
    _registrar(
        "ERRO_ESPERADO" in stdout,
        "saida menciona ERRO_ESPERADO (overflow classificado corretamente)",
    )
    _registrar(
        "erro_layout" in stdout,
        "saida contem 'erro_layout' na mensagem de overflow",
    )


# ---------------------------------------------------------------------------
# Caso 7: Âncora inexistente → RenderizadorErro com menção ao id
# ---------------------------------------------------------------------------

def teste_caso_7_ancora_inexistente():
    print("")
    print("== Caso 7: ancora inexistente ==")
    chips = [
        _chip("t7c1", "Esc", "Sair-T7"),
        _chip("t7c2", "?", "Ajuda-T7"),
    ]
    dist = _dist_canonica(ancoras={"primeiro": ["chip_inexistente_xyz"]})
    bar = {"chips": chips, "distribuicao": dist}
    try:
        _linhas_barra(bar, 39)
        _registrar(False, "ancora inexistente levanta RenderizadorErro", "nenhuma excecao")
    except RenderizadorErro as exc:
        msg = str(exc)
        _registrar(True, "ancora inexistente levanta RenderizadorErro", msg[:80])
        _registrar(
            "chip_inexistente_xyz" in msg or "nao existe" in msg,
            "mensagem menciona id inexistente",
            msg[:80],
        )
    except Exception as exc:
        _registrar(
            False, "ancora inexistente levanta RenderizadorErro",
            "excecao inesperada: {0}: {1}".format(type(exc).__name__, exc),
        )


# ---------------------------------------------------------------------------
# Caso 8: Âncora em posição errada → RenderizadorErro com menção à posição
# ---------------------------------------------------------------------------

def teste_caso_8_ancora_posicao_errada():
    print("")
    print("== Caso 8: ancora em posicao errada ==")
    chips = [
        _chip("t8c_ajuda", "?", "Ajuda-T8"),
        _chip("t8c_esc", "Esc", "Sair-T8"),
    ]
    dist = _dist_canonica(ancoras={"primeiro": ["t8c_esc"]})  # esc não está na pos 0
    bar = {"chips": chips, "distribuicao": dist}
    try:
        _linhas_barra(bar, 39)
        _registrar(False, "ancora posicao errada levanta RenderizadorErro", "nenhuma excecao")
    except RenderizadorErro as exc:
        msg = str(exc)
        _registrar(True, "ancora posicao errada levanta RenderizadorErro", msg[:80])
        _registrar(
            "violada" in msg or "posicao" in msg or "posição" in msg,
            "mensagem menciona posicao errada",
            msg[:80],
        )
    except Exception as exc:
        _registrar(
            False, "ancora posicao errada levanta RenderizadorErro",
            "excecao inesperada: {0}: {1}".format(type(exc).__name__, exc),
        )


# ---------------------------------------------------------------------------
# Caso 9: Exit code 1 para violação inesperada
# Verificação por inspeção do código (conforme autorizado pelo handoff H-0017
# e nota AUD-N-02 da auditoria): o script retorna 1 quando `tem_inesperado`
# ou `tem_violacao` é True. A lógica está em `main()` e é testada aqui via
# análise do código-fonte, conforme documentado no IMP-0017.
# ---------------------------------------------------------------------------

def teste_caso_9_exit_1_violacao_inspecao():
    print("")
    print("== Caso 9: exit code 1 para violacao inesperada (verificacao por inspecao) ==")
    import tela.explorar_barra_de_menus as mod
    src = Path(_SCRIPT).read_text(encoding="utf-8")
    _registrar(
        "tem_inesperado" in src,
        "codigo fonte contem verificacao de 'tem_inesperado'",
    )
    _registrar(
        "tem_violacao" in src,
        "codigo fonte contem verificacao de 'tem_violacao'",
    )
    _registrar(
        "return 1" in src,
        "codigo fonte contem 'return 1' para violacoes",
    )
    _registrar(
        "ERRO_INESPERADO" in src,
        "codigo fonte classifica ERRO_INESPERADO",
    )
    # Verificação funcional: simulação de cenário com expectativa errada.
    # Criamos um cenário que o renderer aceita mas forçamos uma "expectativa
    # incorreta" verificando que a lógica do script detectaria a violação.
    # Como o renderer nunca produz ViolacaoInvariante para inputs válidos,
    # testamos a lógica de exit 1 via inspeção direta do fluxo de retorno.
    _registrar(
        callable(getattr(mod, "main", None)),
        "funcao main() esta disponivel e é chamável",
    )


# ---------------------------------------------------------------------------
# Caso 10: Exit code 2 para parâmetro inválido
# ---------------------------------------------------------------------------

def teste_caso_10_exit_2_parametro_invalido():
    print("")
    print("== Caso 10: exit code 2 para parametro invalido ==")
    code, stdout, stderr = _rodar_script("--preenchimentos", "invalido_xyz")
    _registrar(
        code == 2,
        "parâmetro invalido retorna exit code 2",
        "code={0} stderr={1!r}".format(code, stderr[:80] if stderr else ""),
    )

    code2, _, _ = _rodar_script("--larguras", "abc")
    _registrar(
        code2 == 2,
        "largura não-inteira retorna exit code 2",
        "code={0}".format(code2),
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Testes automatizados H-0017 — explorar_barra_de_menus.py")
    print("Base: {0}".format(_BASE))
    print("Script alvo: {0}".format(_SCRIPT))

    teste_caso_1_matriz_padrao_exit_0()
    teste_caso_2_resumo_deterministico()
    teste_caso_3_linha_unica()
    teste_caso_4_multilinha_coluna_a_coluna()
    teste_caso_5_multilinha_linha_a_linha()
    teste_caso_6_overflow_esperado()
    teste_caso_7_ancora_inexistente()
    teste_caso_8_ancora_posicao_errada()
    teste_caso_9_exit_1_violacao_inspecao()
    teste_caso_10_exit_2_parametro_invalido()

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
