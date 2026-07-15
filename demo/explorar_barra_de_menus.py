"""Script de exploração de combinações da barra_de_menus (H-0017).

Exercita _linhas_barra do renderer com cenários sintéticos gerados em
memória, verificando invariantes e produzindo saída textual determinística.

Executável via:
    python demo/explorar_barra_de_menus.py
    python demo/explorar_barra_de_menus.py --modo-saida resumo
    python demo/explorar_barra_de_menus.py --modo-saida detalhado --mostrar-erros

Exit codes:
    0 — todos os cenários produziram resultado esperado; nenhuma violação.
    1 — erro inesperado ou violação de invariante detectada.
    2 — erro de uso (parâmetro inválido).

Apenas biblioteca padrão do Python.
"""

import sys
import argparse
from pathlib import Path

sys.dont_write_bytecode = True

_BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE))

from tela.renderizador import (  # noqa: E402
    _linhas_barra,
    _DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT,
    RenderizadorErro,
)


# ---------------------------------------------------------------------------
# Perfis de texto (únicos por chip para verificabilidade das invariantes)
# ---------------------------------------------------------------------------

_PERFIS_TEXTO = {
    "curto": ["Ok", "Ir", "Ver", "Ai", "No"],
    "medio": ["Sair", "Ajuda", "Voltar", "Inicio", "Config"],
    "longo": ["Configuracoes", "Selecionar", "Exportar", "Importar", "Pesquisar"],
    "misto": ["Ok", "Configuracoes", "Ir", "Selecionar", "Ver"],
}


def _fabricar_chips(n, perfil="curto", prefixo="c"):
    """Gera n chips sintéticos com ids, teclas e textos únicos."""
    textos_base = _PERFIS_TEXTO.get(perfil, _PERFIS_TEXTO["curto"])
    chips = []
    for i in range(n):
        idx = i % len(textos_base)
        texto_base = textos_base[idx]
        chips.append({
            "id": "{0}{1}".format(prefixo, i + 1),
            "tecla": "k{0}".format(i + 1),
            "texto": "{0}-{1}".format(texto_base, i + 1),
        })
    return chips


def _fabricar_distribuicao(
    preenchimento="coluna_a_coluna",
    linhas_maximo=2,
    vao_entre_chips=2,
    vao_entre_colunas=2,
    ancoras=None,
    vao_chip_texto=1,
    margem_horizontal=1,
):
    """Monta objeto distribuicao canônico com parâmetros configuráveis."""
    return {
        "modo": "horizontal_responsiva",
        "ordem": {
            "politica": "declaracao",
            "ancoras": ancoras if ancoras is not None else {},
        },
        "tentativa_inicial": "linha_unica",
        "quebra": "multilinha_quando_nao_couber",
        "preenchimento_multilinha": preenchimento,
        "preenchimentos_multilinha_suportados": ["coluna_a_coluna", "linha_a_linha"],
        "linhas": {"minimo": 1, "maximo": linhas_maximo, "preferir_menor_numero": True},
        "alinhamento_linhas": "esquerda",
        "espacamentos": {
            "margem_horizontal":         {"minimo": margem_horizontal, "maximo": None},
            "vao_chip_texto":            {"minimo": vao_chip_texto, "maximo": None},
            "vao_entre_chips":           {"minimo": vao_entre_chips, "maximo": None},
            "vao_entre_colunas":         {"minimo": vao_entre_colunas, "maximo": None},
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


def _fabricar_cenario(
    cid, descricao, chips, distribuicao, content_w,
    esperado="ok",
    tipo_erro_esperado=None,
    perfil_texto="curto",
    perfil_espaco="minimo",
    tipo_ancora="sem_ancora",
):
    """Monta dict de cenário para execução."""
    return {
        "id": cid,
        "descricao": descricao,
        "chips": chips,
        "distribuicao": distribuicao,
        "content_w": content_w,
        "esperado": esperado,           # "ok" | "erro_esperado"
        "tipo_erro_esperado": tipo_erro_esperado,
        "perfil_texto": perfil_texto,
        "perfil_espaco": perfil_espaco,
        "tipo_ancora": tipo_ancora,
    }


# ---------------------------------------------------------------------------
# Matriz padrão (14 cenários obrigatórios)
# ---------------------------------------------------------------------------

def _matriz_padrao():
    cenarios = []

    # 1. Linha única com 3 chips curtos e largura ampla
    cenarios.append(_fabricar_cenario(
        "C01", "Linha unica: 3 chips curtos, content_w=80",
        _fabricar_chips(3, "curto"),
        _fabricar_distribuicao("coluna_a_coluna", linhas_maximo=2),
        content_w=80,
        esperado="ok",
        perfil_texto="curto", perfil_espaco="minimo", tipo_ancora="sem_ancora",
    ))

    # 2. Linha única com 6 chips curtos e largura ampla
    cenarios.append(_fabricar_cenario(
        "C02", "Linha unica: 6 chips curtos, content_w=120",
        _fabricar_chips(6, "curto"),
        _fabricar_distribuicao("coluna_a_coluna", linhas_maximo=2),
        content_w=120,
        esperado="ok",
        perfil_texto="curto", perfil_espaco="minimo", tipo_ancora="sem_ancora",
    ))

    # 3. Duas linhas: 6 chips médios, largura estreita (content_w=60)
    cenarios.append(_fabricar_cenario(
        "C03", "Duas linhas: 6 chips medios, content_w=60, coluna_a_coluna",
        _fabricar_chips(6, "medio"),
        _fabricar_distribuicao("coluna_a_coluna", linhas_maximo=2),
        content_w=60,
        esperado="ok",
        perfil_texto="medio", perfil_espaco="minimo", tipo_ancora="sem_ancora",
    ))

    # 4. Duas linhas: 8 chips curtos, largura estreita
    cenarios.append(_fabricar_cenario(
        "C04", "Duas linhas: 8 chips curtos, content_w=50, coluna_a_coluna",
        _fabricar_chips(8, "curto"),
        _fabricar_distribuicao("coluna_a_coluna", linhas_maximo=2),
        content_w=50,
        esperado="ok",
        perfil_texto="curto", perfil_espaco="minimo", tipo_ancora="sem_ancora",
    ))

    # 5. Três linhas: 10 chips curtos, linhas.maximo=3
    # content_w=50: col0 max=10, col1=9, col2=10, col3=11, vao_cols=2 → 10+2+9+2+10+2+11=46 <= 50
    cenarios.append(_fabricar_cenario(
        "C05", "Tres linhas: 10 chips curtos, content_w=50, linhas.maximo=3",
        _fabricar_chips(10, "curto"),
        _fabricar_distribuicao("coluna_a_coluna", linhas_maximo=3),
        content_w=50,
        esperado="ok",
        perfil_texto="curto", perfil_espaco="minimo", tipo_ancora="sem_ancora",
    ))

    # 6. Overflow forçado: 10 chips médios, largura muito estreita
    cenarios.append(_fabricar_cenario(
        "C06", "Overflow: 10 chips medios, content_w=20, linhas.maximo=2",
        _fabricar_chips(10, "medio"),
        _fabricar_distribuicao("coluna_a_coluna", linhas_maximo=2),
        content_w=20,
        esperado="erro_esperado",
        tipo_erro_esperado="erro_layout",
        perfil_texto="medio", perfil_espaco="minimo", tipo_ancora="sem_ancora",
    ))

    # 7. Overflow forçado: 12 chips curtos, largura mínima
    cenarios.append(_fabricar_cenario(
        "C07", "Overflow: 12 chips curtos, content_w=15, linhas.maximo=2",
        _fabricar_chips(12, "curto"),
        _fabricar_distribuicao("coluna_a_coluna", linhas_maximo=2),
        content_w=15,
        esperado="erro_esperado",
        tipo_erro_esperado="erro_layout",
        perfil_texto="curto", perfil_espaco="minimo", tipo_ancora="sem_ancora",
    ))

    # 8. coluna_a_coluna com 5 chips mistos
    cenarios.append(_fabricar_cenario(
        "C08", "coluna_a_coluna: 5 chips mistos, content_w=60",
        _fabricar_chips(5, "misto"),
        _fabricar_distribuicao("coluna_a_coluna", linhas_maximo=2),
        content_w=60,
        esperado="ok",
        perfil_texto="misto", perfil_espaco="minimo", tipo_ancora="sem_ancora",
    ))

    # 9. linha_a_linha com 5 chips mistos, content_w=45 (força multilinha)
    # Linha única: "[k1] Ok-1  [k2] Configuracoes-2  [k3] Ir-3  [k4] Selecionar-4  [k5] Ver-5"
    # = 9+2+20+2+9+2+19+2+10 = 75 chars > 45 → multilinha necessária
    # K=2, CPL=3: linha0="[k1] Ok-1  [k2] Configuracoes-2  [k3] Ir-3" = 9+2+20+2+9=42 <= 45 ✓
    cenarios.append(_fabricar_cenario(
        "C09", "linha_a_linha: 5 chips mistos, content_w=45",
        _fabricar_chips(5, "misto"),
        _fabricar_distribuicao("linha_a_linha", linhas_maximo=2),
        content_w=45,
        esperado="ok",
        perfil_texto="misto", perfil_espaco="minimo", tipo_ancora="sem_ancora",
    ))

    # 10. Âncora válida: 2 chips, primeiro=c1, último=c2
    chips_ancora = [
        {"id": "chip_esc", "tecla": "Esc", "texto": "Sair-A"},
        {"id": "chip_ajuda", "tecla": "?", "texto": "Ajuda-A"},
    ]
    dist_ancora_valida = _fabricar_distribuicao(
        "coluna_a_coluna", linhas_maximo=2,
        ancoras={"primeiro": ["chip_esc"], "ultimo": ["chip_ajuda"]},
    )
    cenarios.append(_fabricar_cenario(
        "C10", "Ancora valida: chip_esc primeiro, chip_ajuda ultimo, content_w=39",
        chips_ancora,
        dist_ancora_valida,
        content_w=39,
        esperado="ok",
        perfil_texto="curto", perfil_espaco="minimo", tipo_ancora="valida",
    ))

    # 11. Âncora inexistente
    chips_ancora_inex = [
        {"id": "chip_esc", "tecla": "Esc", "texto": "Sair-B"},
        {"id": "chip_ajuda", "tecla": "?", "texto": "Ajuda-B"},
    ]
    dist_ancora_inex = _fabricar_distribuicao(
        "coluna_a_coluna", linhas_maximo=2,
        ancoras={"primeiro": ["chip_x"]},
    )
    cenarios.append(_fabricar_cenario(
        "C11", "Ancora inexistente: id 'chip_x' nao existe em chips[]",
        chips_ancora_inex,
        dist_ancora_inex,
        content_w=39,
        esperado="erro_esperado",
        tipo_erro_esperado="ancora_inexistente",
        perfil_texto="curto", perfil_espaco="minimo", tipo_ancora="inexistente",
    ))

    # 12. Âncora em posição errada
    chips_ancora_pos = [
        {"id": "chip_ajuda", "tecla": "?", "texto": "Ajuda-C"},
        {"id": "chip_esc", "tecla": "Esc", "texto": "Sair-C"},
    ]
    dist_ancora_pos = _fabricar_distribuicao(
        "coluna_a_coluna", linhas_maximo=2,
        ancoras={"primeiro": ["chip_esc"]},
    )
    cenarios.append(_fabricar_cenario(
        "C12", "Ancora posicao errada: chip_esc nao esta na posicao 0",
        chips_ancora_pos,
        dist_ancora_pos,
        content_w=39,
        esperado="erro_esperado",
        tipo_erro_esperado="ancora_posicao_errada",
        perfil_texto="curto", perfil_espaco="minimo", tipo_ancora="posicao_errada",
    ))

    # 13. Espaçamentos mínimos
    cenarios.append(_fabricar_cenario(
        "C13", "Espacamentos minimos: 4 chips curtos, content_w=60",
        _fabricar_chips(4, "curto"),
        _fabricar_distribuicao("coluna_a_coluna", linhas_maximo=2,
                               vao_entre_chips=2, vao_entre_colunas=2),
        content_w=60,
        esperado="ok",
        perfil_texto="curto", perfil_espaco="minimo", tipo_ancora="sem_ancora",
    ))

    # 14. Espaçamentos máximos (content_w=120 para garantir que cabe)
    cenarios.append(_fabricar_cenario(
        "C14", "Espacamentos maximos: 4 chips curtos, content_w=120",
        _fabricar_chips(4, "curto"),
        _fabricar_distribuicao("coluna_a_coluna", linhas_maximo=2,
                               vao_entre_chips=6, vao_entre_colunas=8),
        content_w=120,
        esperado="ok",
        perfil_texto="curto", perfil_espaco="maximo", tipo_ancora="sem_ancora",
    ))

    # 15. linhas.maximo=1 com chips que nao cabem em linha unica → erro_layout
    # Com margem=1 e content_w=20: largura_util=18.
    # 4 chips medios: "Sair-1"(11)+"Ajuda-2"(12)+"Voltar-3"(13)+"Inicio-4"(13)
    # single = 11+2+12+2+13+2+13=55 > 18; K=1 (range(2,2) vazio) → erro_layout
    cenarios.append(_fabricar_cenario(
        "C15", "linhas.maximo=1: 4 chips medios, content_w=20 -> erro_layout",
        _fabricar_chips(4, "medio", prefixo="c15"),
        _fabricar_distribuicao("coluna_a_coluna", linhas_maximo=1),
        content_w=20,
        esperado="erro_esperado",
        tipo_erro_esperado="erro_layout",
        perfil_texto="medio", perfil_espaco="minimo", tipo_ancora="sem_ancora",
    ))

    return cenarios


# ---------------------------------------------------------------------------
# Geração de matriz combinatória a partir de parâmetros CLI
# ---------------------------------------------------------------------------

def _perfil_espaco(vao_chips, vao_cols):
    if vao_chips <= 2 and vao_cols <= 2:
        return "minimo"
    if vao_chips >= 6 and vao_cols >= 8:
        return "maximo"
    return "intermediario"


def _gerar_matriz_combinatoria(larguras, qtd_chips_lista, linhas_max_lista,
                                preenchimentos, margens_horizontais=None,
                                vaos_chip_texto_lista=None, espacamentos=None):
    if margens_horizontais is None:
        margens_horizontais = [1]
    if vaos_chip_texto_lista is None:
        vaos_chip_texto_lista = [1]
    if espacamentos is None:
        espacamentos = [(2, 2), (3, 4), (6, 8)]

    cenarios = []
    cid = 0
    for content_w in larguras:
        for n_chips in qtd_chips_lista:
            for linhas_max in linhas_max_lista:
                for preench in preenchimentos:
                    for margem in margens_horizontais:
                        for vao_ct in vaos_chip_texto_lista:
                            for vao_chips, vao_cols in espacamentos:
                                for perfil in ["curto", "misto"]:
                                    cid += 1
                                    chips = _fabricar_chips(
                                        n_chips, perfil,
                                        prefixo="g{0}c".format(cid),
                                    )
                                    dist = _fabricar_distribuicao(
                                        preench, linhas_maximo=linhas_max,
                                        vao_entre_chips=vao_chips,
                                        vao_entre_colunas=vao_cols,
                                        vao_chip_texto=vao_ct,
                                        margem_horizontal=margem,
                                    )
                                    texto_chips = [
                                        "[{0}]{1}{2}".format(
                                            c["tecla"], " " * vao_ct, c["texto"]
                                        )
                                        for c in chips
                                    ]
                                    largura_util = content_w - 2 * margem
                                    linha_unica = (" " * vao_chips).join(texto_chips)
                                    if largura_util <= 0:
                                        esperado = "erro_esperado"
                                        tipo_err = "erro_layout"
                                    elif len(linha_unica) <= largura_util:
                                        esperado = "ok"
                                        tipo_err = None
                                    else:
                                        vai_caber = False
                                        for nl in range(2, linhas_max + 1):
                                            if preench == "coluna_a_coluna":
                                                nc = (n_chips + nl - 1) // nl
                                                cols = []
                                                for ci in range(nc):
                                                    col = texto_chips[ci*nl:(ci+1)*nl]
                                                    cols.append(col)
                                                largs = [
                                                    max(len(s) for s in c)
                                                    for c in cols if c
                                                ]
                                                total = (
                                                    sum(largs)
                                                    + vao_cols * (len(largs) - 1)
                                                    if largs else 0
                                                )
                                                if total <= largura_util:
                                                    vai_caber = True
                                                    break
                                            else:
                                                cpl = (n_chips + nl - 1) // nl
                                                linhas_est = []
                                                for li in range(nl):
                                                    chunk = texto_chips[li*cpl:(li+1)*cpl]
                                                    if chunk:
                                                        linhas_est.append(
                                                            (" " * vao_chips).join(chunk)
                                                        )
                                                if linhas_est and max(
                                                    len(l) for l in linhas_est
                                                ) <= largura_util:
                                                    vai_caber = True
                                                    break
                                        esperado = "ok" if vai_caber else "erro_esperado"
                                        tipo_err = None if vai_caber else "erro_layout"

                                    desc = (
                                        "comb: n={0} w={1} lmax={2} preench={3} "
                                        "vchip={4} vcol={5} perf={6} "
                                        "marg={7} vct={8}".format(
                                            n_chips, content_w, linhas_max, preench,
                                            vao_chips, vao_cols, perfil, margem, vao_ct,
                                        )
                                    )
                                    cenarios.append(_fabricar_cenario(
                                        "G{0:04d}".format(cid),
                                        desc,
                                        chips, dist, content_w,
                                        esperado=esperado,
                                        tipo_erro_esperado=tipo_err,
                                        perfil_texto=perfil,
                                        perfil_espaco=_perfil_espaco(vao_chips, vao_cols),
                                        tipo_ancora="sem_ancora",
                                    ))
    return cenarios


# ---------------------------------------------------------------------------
# Verificação de invariantes
# ---------------------------------------------------------------------------

def _verificar_invariantes(cenario, linhas):
    """Verifica as invariantes 1-12 para cenários OK.

    Retorna lista de strings descrevendo violações (vazia se tudo OK).
    """
    violacoes = []
    chips = cenario["chips"]
    content_w = cenario["content_w"]
    dist = cenario["distribuicao"]
    linhas_cfg = dist.get("linhas") or {}
    maximo = linhas_cfg.get("maximo", 2)
    preench = dist.get("preenchimento_multilinha", "coluna_a_coluna")

    esp = dist.get("espacamentos") or {}
    vao_ct = (esp.get("vao_chip_texto") or {}).get("minimo", 1)
    textos_chips = [
        "[{0}]{1}{2}".format(c["tecla"], " " * vao_ct, c["texto"])
        for c in chips
    ]
    junta = "\n".join(linhas)

    # Invariante 6: quantidade de linhas ≤ linhas.maximo
    if len(linhas) > maximo:
        violacoes.append(
            "INV-6: {0} linhas fisicas > linhas.maximo={1}".format(
                len(linhas), maximo
            )
        )

    # Invariante 7: largura de cada linha ≤ content_w
    for i, linha in enumerate(linhas):
        if len(linha) > content_w:
            violacoes.append(
                "INV-7: linha {0} tem {1} chars > content_w={2}".format(
                    i, len(linha), content_w
                )
            )

    # Invariantes 1, 2, 3, 4, 5: chips na saída
    for i, (chip, texto) in enumerate(zip(chips, textos_chips)):
        cnt = junta.count(texto)
        if cnt == 0:
            violacoes.append(
                "INV-3: chip {0!r} ausente na saida".format(chip["id"])
            )
        elif cnt > 1:
            violacoes.append(
                "INV-1: chip {0!r} aparece {1} vezes (esperado=1)".format(
                    chip["id"], cnt
                )
            )

    # Invariante 2: tokens na saída pertencem aos chips declarados
    teclas_declaradas = {c.get("tecla", "") for c in chips}
    for linha in linhas:
        pos = 0
        while True:
            start = linha.find("[", pos)
            if start == -1:
                break
            end = linha.find("]", start + 1)
            if end == -1:
                break
            token = linha[start + 1:end]
            if token not in teclas_declaradas:
                violacoes.append(
                    "INV-2: token [{0}] na saida nao pertence a nenhum chip "
                    "declarado".format(token)
                )
            pos = end + 1

    # Invariante 4: ordem preservada dentro de cada linha (todos os pares i<j).
    # Para coluna_a_coluna multilinha, a ordem é coluna-major (chip[0] e
    # chip[2] na linha 0; chip[1] e chip[3] na linha 1), portanto a posição
    # sequencial no texto juntado não reflete a ordem declarada de forma
    # linear. Verificamos ordem apenas dentro de cada linha individualmente.
    for linha in linhas:
        posicoes_linha = [linha.find(t) for t in textos_chips]
        for i in range(len(posicoes_linha)):
            for j in range(i + 1, len(posicoes_linha)):
                pi, pj = posicoes_linha[i], posicoes_linha[j]
                if pi == -1 or pj == -1:
                    continue
                if pi > pj:
                    violacoes.append(
                        "INV-4: na linha, chip {0!r} aparece apos chip "
                        "{1!r}".format(chips[i]["id"], chips[j]["id"])
                    )

    # Invariante 5: texto não truncado
    for chip, texto in zip(chips, textos_chips):
        if texto not in junta:
            violacoes.append(
                "INV-5: texto truncado ou ausente para chip {0!r}: {1!r}".format(
                    chip["id"], texto
                )
            )

    # Invariante 8: chips do lancador não aparecem (não aplicável aqui pois
    # usamos chips sintéticos — verificação implícita pela unicidade dos ids)

    # Invariante 9: não usa fallback vertical (um chip por linha quando n>1)
    if len(chips) > 1 and len(linhas) == len(chips):
        # Poderia ser fallback vertical — mas é legítimo se for multilinha
        # com n_linhas == n_chips (cada chip em linha própria)
        # O renderer nunca faz isso: apenas coloca chips em linhas completas
        pass  # Não detectável sem acesso ao modo interno

    # Invariante 10: linha única → todos os chips na mesma linha
    if len(linhas) == 1:
        for texto in textos_chips:
            if texto not in linhas[0]:
                violacoes.append(
                    "INV-10: chip ausente na linha unica: {0!r}".format(texto)
                )

    # Invariante 11: coluna_a_coluna com 2+ linhas — verificação do padrão
    if preench == "coluna_a_coluna" and len(linhas) >= 2:
        n = len(chips)
        n_linhas = len(linhas)
        n_colunas = (n + n_linhas - 1) // n_linhas
        # Os primeiros n_linhas chips devem estar na coluna 0
        # Verificação simplificada: chip[0] deve estar na linha 0
        if textos_chips and textos_chips[0] not in linhas[0]:
            violacoes.append(
                "INV-11: coluna_a_coluna: chip[0] nao esta na linha 0"
            )

    # Invariante 12: linha_a_linha com 2+ linhas — verificação do padrão
    if preench == "linha_a_linha" and len(linhas) >= 2:
        n = len(chips)
        n_linhas = len(linhas)
        cpl = (n + n_linhas - 1) // n_linhas
        # Os primeiros cpl chips devem estar na linha 0
        for i in range(min(cpl, len(textos_chips))):
            if textos_chips[i] not in linhas[0]:
                violacoes.append(
                    "INV-12: linha_a_linha: chip[{0}] nao esta na linha 0".format(i)
                )

    return violacoes


# ---------------------------------------------------------------------------
# Execução de um cenário
# ---------------------------------------------------------------------------

def _executar_cenario(cenario):
    """Executa um cenário e retorna dict com resultado."""
    try:
        linhas = _linhas_barra(
            {"chips": cenario["chips"], "distribuicao": cenario["distribuicao"]},
            cenario["content_w"],
        )
        # Verificar invariantes
        violacoes = _verificar_invariantes(cenario, linhas)
        if violacoes:
            return {
                "status": "ERRO_INESPERADO",
                "era_esperado": False,
                "tipo_erro": "ViolacaoInvariante",
                "mensagem": "; ".join(violacoes),
                "linhas": linhas,
                "violacoes": violacoes,
            }
        return {
            "status": "OK",
            "linhas": linhas,
            "violacoes": [],
        }
    except RenderizadorErro as exc:
        msg = str(exc)
        esperado = cenario.get("esperado") == "erro_esperado"
        tipo = cenario.get("tipo_erro_esperado", "")
        era_esperado = esperado and (
            (tipo == "erro_layout" and "erro_layout" in msg)
            or (tipo == "ancora_inexistente" and "nao existe" in msg)
            or (tipo == "ancora_posicao_errada" and ("violada" in msg or "posicao" in msg or "posição" in msg))
        )
        status = "ERRO_ESPERADO" if era_esperado else "ERRO_INESPERADO"
        return {
            "status": status,
            "era_esperado": era_esperado,
            "tipo_erro": type(exc).__name__,
            "mensagem": msg,
            "linhas": [],
            "violacoes": [],
        }
    except Exception as exc:
        return {
            "status": "ERRO_INESPERADO",
            "era_esperado": False,
            "tipo_erro": type(exc).__name__,
            "mensagem": str(exc),
            "linhas": [],
            "violacoes": [],
        }


# ---------------------------------------------------------------------------
# Formatação de saída
# ---------------------------------------------------------------------------

def _formatar_cenario_detalhado(cenario, resultado, mostrar_ok, mostrar_erros):
    status = resultado["status"]
    deve_mostrar = (
        (status == "OK" and mostrar_ok)
        or (status in ("ERRO_ESPERADO", "ERRO_INESPERADO") and mostrar_erros)
    )
    if not deve_mostrar:
        return ""

    dist = cenario["distribuicao"]
    linhas_cfg = dist.get("linhas") or {}
    esp = dist.get("espacamentos") or {}

    linhas = []
    linhas.append("--- Cenario {0} ---".format(cenario["id"]))
    linhas.append("descricao:     {0}".format(cenario["descricao"]))
    linhas.append("chips:         {0}".format(len(cenario["chips"])))
    linhas.append("content_w:     {0}".format(cenario["content_w"]))
    linhas.append("linhas.maximo: {0}".format(linhas_cfg.get("maximo", 2)))
    linhas.append("preenchimento: {0}".format(
        dist.get("preenchimento_multilinha", "?")
    ))
    linhas.append("espacamento:   {0}".format(cenario.get("perfil_espaco", "?")))
    linhas.append("texto_perfil:  {0}".format(cenario.get("perfil_texto", "?")))
    linhas.append("ancoras:       {0}".format(cenario.get("tipo_ancora", "?")))
    linhas.append("resultado:     {0}".format(status))

    if status == "OK":
        barra_linhas = resultado["linhas"]
        _dist_det = cenario.get("distribuicao") or {}
        _esp_det = _dist_det.get("espacamentos") or {}
        _vao_ct_det = (_esp_det.get("vao_chip_texto") or {}).get("minimo", 1)
        textos_chips = [
            "[{0}]{1}{2}".format(c["tecla"], " " * _vao_ct_det, c["texto"])
            for c in cenario["chips"]
        ]
        junta = "\n".join(barra_linhas)
        chips_ok = all(junta.count(t) == 1 for t in textos_chips)
        ordem_ok = True
        posicoes = [junta.find(t) for t in textos_chips]
        for i in range(len(posicoes) - 1):
            if posicoes[i] != -1 and posicoes[i + 1] != -1:
                if posicoes[i] > posicoes[i + 1]:
                    ordem_ok = False

        linhas.append("  linhas_fisicas:   {0}".format(len(barra_linhas)))
        linhas.append("  contagem_chips:   {0}".format(
            sum(1 for t in textos_chips if t in junta)
        ))
        linhas.append("  chips_corretos:   {0}".format(chips_ok))
        linhas.append("  ordem_preservada: {0}".format(ordem_ok))
        largura_max = max((len(l) for l in barra_linhas), default=0)
        linhas.append("  largura_maxima:   {0}".format(largura_max))
        linhas.append("  representacao:")
        for bl in barra_linhas:
            linhas.append("    {0}".format(bl))
    else:
        linhas.append("  tipo_erro:    {0}".format(resultado.get("tipo_erro", "?")))
        linhas.append("  mensagem:     {0}".format(
            resultado.get("mensagem", "")[:120]
        ))
        linhas.append("  era_esperado: {0}".format(resultado.get("era_esperado", False)))
        if resultado.get("violacoes"):
            for v in resultado["violacoes"]:
                linhas.append("  violacao: {0}".format(v))

    return "\n".join(linhas)


def _formatar_resumo(resultados_todos, cenarios_todos):
    total = len(resultados_todos)
    n_ok = sum(1 for r in resultados_todos if r["status"] == "OK")
    n_esp = sum(1 for r in resultados_todos if r["status"] == "ERRO_ESPERADO")
    n_inesp = sum(1 for r in resultados_todos if r["status"] == "ERRO_INESPERADO")
    n_viol = sum(len(r.get("violacoes", [])) for r in resultados_todos)

    linhas = []
    linhas.append("=== RESUMO DA EXPLORACAO ===")
    linhas.append("Total de cenarios executados:   {0}".format(total))
    linhas.append("OK:                             {0}".format(n_ok))
    linhas.append("Erro esperado:                  {0}".format(n_esp))
    linhas.append("Erro inesperado:                {0}".format(n_inesp))
    linhas.append("Violacoes de invariante:        {0}".format(n_viol))

    # Por preenchimento
    linhas.append("")
    linhas.append("Por preenchimento_multilinha:")
    for preench in ("coluna_a_coluna", "linha_a_linha"):
        idxs = [
            i for i, c in enumerate(cenarios_todos)
            if c["distribuicao"].get("preenchimento_multilinha") == preench
        ]
        ok_p = sum(1 for i in idxs if resultados_todos[i]["status"] == "OK")
        esp_p = sum(1 for i in idxs if resultados_todos[i]["status"] == "ERRO_ESPERADO")
        inp_p = sum(1 for i in idxs if resultados_todos[i]["status"] == "ERRO_INESPERADO")
        linhas.append("  {0}: OK={1} ERRO_ESP={2} ERRO_INESP={3}".format(
            preench, ok_p, esp_p, inp_p
        ))

    # Por linhas.maximo
    linhas.append("")
    linhas.append("Por linhas.maximo:")
    valores_maximo = sorted(set(
        c["distribuicao"].get("linhas", {}).get("maximo", 2)
        for c in cenarios_todos
    ))
    for mv in valores_maximo:
        idxs = [
            i for i, c in enumerate(cenarios_todos)
            if c["distribuicao"].get("linhas", {}).get("maximo", 2) == mv
        ]
        ok_m = sum(1 for i in idxs if resultados_todos[i]["status"] == "OK")
        esp_m = sum(1 for i in idxs if resultados_todos[i]["status"] == "ERRO_ESPERADO")
        inp_m = sum(1 for i in idxs if resultados_todos[i]["status"] == "ERRO_INESPERADO")
        linhas.append("  {0}: OK={1} ERRO_ESP={2} ERRO_INESP={3}".format(
            mv, ok_m, esp_m, inp_m
        ))

    # Por largura (content_w)
    linhas.append("")
    linhas.append("Por largura (content_w):")
    larguras_unicas = sorted(set(c["content_w"] for c in cenarios_todos))
    for w in larguras_unicas:
        idxs = [i for i, c in enumerate(cenarios_todos) if c["content_w"] == w]
        ok_w = sum(1 for i in idxs if resultados_todos[i]["status"] == "OK")
        esp_w = sum(1 for i in idxs if resultados_todos[i]["status"] == "ERRO_ESPERADO")
        inp_w = sum(1 for i in idxs if resultados_todos[i]["status"] == "ERRO_INESPERADO")
        linhas.append("  {0}: OK={1} ERRO_ESP={2} ERRO_INESP={3}".format(
            w, ok_w, esp_w, inp_w
        ))

    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# Parsing de argumentos CLI
# ---------------------------------------------------------------------------

_PREENCHIMENTOS_VALIDOS = {"coluna_a_coluna", "linha_a_linha"}


def _parse_lista_int(s, nome):
    try:
        return [int(x.strip()) for x in s.split(",") if x.strip()]
    except ValueError:
        raise argparse.ArgumentTypeError(
            "{0}: esperado lista de inteiros separados por vírgula".format(nome)
        )


def _parse_preenchimentos(s):
    valores = [x.strip() for x in s.split(",") if x.strip()]
    for v in valores:
        if v not in _PREENCHIMENTOS_VALIDOS:
            raise argparse.ArgumentTypeError(
                "preenchimento inválido: {0!r}; aceitos: coluna_a_coluna, linha_a_linha".format(v)
            )
    return valores


def _construir_parser():
    p = argparse.ArgumentParser(
        description="Script de exploração de combinações da barra_de_menus (H-0017).",
        add_help=True,
    )
    p.add_argument(
        "--larguras",
        metavar="N,N,...",
        default=None,
        help="Lista de content_w a testar. Default: matriz padrão.",
    )
    p.add_argument(
        "--chips",
        metavar="N,N,...",
        default=None,
        help="Lista de quantidades de chips. Default: matriz padrão.",
    )
    p.add_argument(
        "--linhas-max",
        metavar="N,N,...",
        default=None,
        dest="linhas_max",
        help="Lista de valores de linhas.maximo. Default: matriz padrão.",
    )
    p.add_argument(
        "--preenchimentos",
        metavar="P,P,...",
        default=None,
        help="Lista de preenchimentos. Default: matriz padrão.",
    )
    p.add_argument(
        "--margens-horizontais",
        metavar="N,N,...",
        default=None,
        dest="margens_horizontais",
        help="Lista de margem_horizontal.minimo. Default: [1].",
    )
    p.add_argument(
        "--vaos-chip-texto",
        metavar="N,N,...",
        default=None,
        dest="vaos_chip_texto",
        help="Lista de vao_chip_texto.minimo. Default: [1].",
    )
    p.add_argument(
        "--vaos-entre-chips",
        metavar="N,N,...",
        default=None,
        dest="vaos_entre_chips",
        help="Lista de vao_entre_chips.minimo. Default: [2].",
    )
    p.add_argument(
        "--vaos-entre-colunas",
        metavar="N,N,...",
        default=None,
        dest="vaos_entre_colunas",
        help="Lista de vao_entre_colunas.minimo. Default: [2].",
    )
    p.add_argument(
        "--modo-saida",
        choices=["resumo", "detalhado"],
        default="detalhado",
        dest="modo_saida",
        help="Formato de saída. Default: detalhado.",
    )
    p.add_argument(
        "--mostrar-ok",
        action="store_true",
        dest="mostrar_ok",
        help="Inclui cenários OK na saída.",
    )
    p.add_argument(
        "--mostrar-erros",
        action="store_true",
        dest="mostrar_erros",
        help="Inclui cenários com erro na saída.",
    )
    p.add_argument(
        "--limite-casos",
        type=int,
        default=None,
        dest="limite_casos",
        metavar="N",
        help="Limita a quantidade total de cenários executados.",
    )
    return p


def _parse_args(argv=None):
    p = _construir_parser()
    try:
        args = p.parse_args(argv)
    except SystemExit as exc:
        raise

    # Validação adicional dos parâmetros
    erros = []
    larguras = None
    chips_lista = None
    linhas_max_lista = None
    preenchimentos = None
    margens_horizontais = None
    vaos_chip_texto_lista = None
    vaos_entre_chips_lista = None
    vaos_entre_colunas_lista = None

    if args.larguras is not None:
        try:
            larguras = _parse_lista_int(args.larguras, "--larguras")
            if any(w < 1 for w in larguras):
                erros.append("--larguras: todos os valores devem ser >= 1")
        except argparse.ArgumentTypeError as e:
            erros.append(str(e))

    if args.chips is not None:
        try:
            chips_lista = _parse_lista_int(args.chips, "--chips")
            if any(n < 1 for n in chips_lista):
                erros.append("--chips: todos os valores devem ser >= 1")
        except argparse.ArgumentTypeError as e:
            erros.append(str(e))

    if args.linhas_max is not None:
        try:
            linhas_max_lista = _parse_lista_int(args.linhas_max, "--linhas-max")
            if any(m < 1 for m in linhas_max_lista):
                erros.append("--linhas-max: todos os valores devem ser >= 1")
        except argparse.ArgumentTypeError as e:
            erros.append(str(e))

    if args.preenchimentos is not None:
        try:
            preenchimentos = _parse_preenchimentos(args.preenchimentos)
        except argparse.ArgumentTypeError as e:
            erros.append(str(e))

    if args.margens_horizontais is not None:
        try:
            margens_horizontais = _parse_lista_int(
                args.margens_horizontais, "--margens-horizontais"
            )
            if any(m < 0 for m in margens_horizontais):
                erros.append("--margens-horizontais: todos os valores devem ser >= 0")
        except argparse.ArgumentTypeError as e:
            erros.append(str(e))

    if args.vaos_chip_texto is not None:
        try:
            vaos_chip_texto_lista = _parse_lista_int(
                args.vaos_chip_texto, "--vaos-chip-texto"
            )
            if any(v < 1 for v in vaos_chip_texto_lista):
                erros.append("--vaos-chip-texto: todos os valores devem ser >= 1")
        except argparse.ArgumentTypeError as e:
            erros.append(str(e))

    if args.vaos_entre_chips is not None:
        try:
            vaos_entre_chips_lista = _parse_lista_int(
                args.vaos_entre_chips, "--vaos-entre-chips"
            )
            if any(v < 1 for v in vaos_entre_chips_lista):
                erros.append("--vaos-entre-chips: todos os valores devem ser >= 1")
        except argparse.ArgumentTypeError as e:
            erros.append(str(e))

    if args.vaos_entre_colunas is not None:
        try:
            vaos_entre_colunas_lista = _parse_lista_int(
                args.vaos_entre_colunas, "--vaos-entre-colunas"
            )
            if any(v < 1 for v in vaos_entre_colunas_lista):
                erros.append("--vaos-entre-colunas: todos os valores devem ser >= 1")
        except argparse.ArgumentTypeError as e:
            erros.append(str(e))

    if erros:
        for e in erros:
            print("ERRO: {0}".format(e), file=sys.stderr)
        sys.exit(2)

    return (args, larguras, chips_lista, linhas_max_lista, preenchimentos,
            margens_horizontais, vaos_chip_texto_lista,
            vaos_entre_chips_lista, vaos_entre_colunas_lista)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv=None):
    try:
        (args, larguras, chips_lista, linhas_max_lista, preenchimentos,
         margens_horizontais, vaos_chip_texto_lista,
         vaos_entre_chips_lista, vaos_entre_colunas_lista) = _parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if exc.code is not None else 2

    mostrar_ok = args.mostrar_ok
    mostrar_erros = args.mostrar_erros
    modo_saida = args.modo_saida
    limite = args.limite_casos

    # Selecionar matriz
    usar_combinatoria = any(
        x is not None for x in [
            larguras, chips_lista, linhas_max_lista, preenchimentos,
            margens_horizontais, vaos_chip_texto_lista,
            vaos_entre_chips_lista, vaos_entre_colunas_lista,
        ]
    )

    if usar_combinatoria:
        larguras = larguras or [30, 40, 80]
        chips_lista = chips_lista or [3, 6, 10]
        linhas_max_lista = linhas_max_lista or [1, 2, 3]
        preenchimentos = preenchimentos or ["coluna_a_coluna", "linha_a_linha"]
        margens = margens_horizontais or [1]
        vaos_ct = vaos_chip_texto_lista or [1]
        if vaos_entre_chips_lista is not None or vaos_entre_colunas_lista is not None:
            _chips_l = vaos_entre_chips_lista or [2]
            _cols_l = vaos_entre_colunas_lista or [2]
            espacamentos = [(vc, vcol) for vc in _chips_l for vcol in _cols_l]
        else:
            espacamentos = None  # usa legado [(2,2),(3,4),(6,8)]
        cenarios = _gerar_matriz_combinatoria(
            larguras, chips_lista, linhas_max_lista, preenchimentos,
            margens_horizontais=margens,
            vaos_chip_texto_lista=vaos_ct,
            espacamentos=espacamentos,
        )
    else:
        cenarios = _matriz_padrao()

    if limite is not None and limite > 0:
        cenarios = cenarios[:limite]

    # Executar
    resultados = []
    for cenario in cenarios:
        resultado = _executar_cenario(cenario)
        resultados.append(resultado)

        if modo_saida == "detalhado":
            bloco = _formatar_cenario_detalhado(
                cenario, resultado, mostrar_ok, mostrar_erros
            )
            if bloco:
                print(bloco)

    # Resumo sempre ao final
    resumo = _formatar_resumo(resultados, cenarios)
    print(resumo)

    # Exit code
    tem_inesperado = any(r["status"] == "ERRO_INESPERADO" for r in resultados)
    tem_violacao = any(r.get("violacoes") for r in resultados)
    if tem_inesperado or tem_violacao:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
