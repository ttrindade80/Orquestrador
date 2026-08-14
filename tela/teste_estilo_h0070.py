"""Testes focais dos refinamentos de apresentação H-0070."""

from __future__ import annotations

from tela.estilo import CATEGORIAS_ESTILO, ControladorTelaEstilo
from tela.loader import RuntimeEstilo
from tela.renderizacao.conteudo_externo import (
    _linhas_apresentacao_hierarquia_com_mapa,
)
from tela.renderizacao.estilo import (
    SEPARADOR_NOME_AMOSTRA,
    amostra_de_preset,
)
from tela.renderizacao.texto_ansi import _largura_sem_ansi


def _filhos(controlador, categoria):
    pai = next(
        no for no in controlador.conteudo.nos
        if no.campos.get("categoria") == categoria
    )
    return list(pai.filhos)


def _linhas_estilo(controlador, corrente, selecoes):
    estilo = RuntimeEstilo().global_vigente
    return _linhas_apresentacao_hierarquia_com_mapa(
        controlador.conteudo,
        content_w=240,
        no_corrente_id=corrente,
        indicador=estilo.selecionado_simbolo,
        indicador_off=estilo.selecionado_off,
        selecoes=selecoes,
        incluir_selecao=True,
        incluido_on=estilo.incluido_on,
        incluido_off=estilo.incluido_off,
    )


def test_filhos_sem_ordinais_cursor_e_indicadores_preservados():
    controlador = ControladorTelaEstilo(RuntimeEstilo())
    filhos = _filhos(controlador, "borda")
    corrente = filhos[0].id
    linhas = {
        entrada["id"]: entrada["linhas"][0]
        for entrada in _linhas_estilo(controlador, corrente, {corrente})
    }

    for no in filhos:
        linha = linhas[no.id]
        assert not any(
            marcador in linha for marcador in ("A) ", "B) ", "C) ")
        )

    titulo_corrente = filhos[0].campos["titulo"]
    titulo_off = filhos[1].campos["titulo"]
    inicio_corrente = linhas[corrente].index(titulo_corrente)
    inicio_off = linhas[filhos[1].id].index(titulo_off)
    assert inicio_corrente == inicio_off
    assert linhas[corrente][inicio_corrente - 1] == " "
    assert "→" in linhas[corrente][:inicio_corrente]
    assert "→" not in linhas[filhos[1].id][:inicio_off]
    assert "●" in linhas[corrente]
    assert "○" in linhas[filhos[1].id]
    # O recuo de um filho continua materializado antes da região do cursor.
    assert linhas[corrente].index("→") >= 4


def test_amostras_de_cada_categoria_comecam_na_mesma_coluna_visual():
    controlador = ControladorTelaEstilo(RuntimeEstilo())
    assert tuple(c.nome for c in controlador.categorias) == CATEGORIAS_ESTILO

    for categoria in controlador.categorias:
        inicios = []
        for preset in categoria.presets:
            no = next(
                filho for filho in _filhos(controlador, categoria.nome)
                if filho.campos["preset"] == preset.nome
            )
            titulo = no.campos["titulo"]
            amostra = amostra_de_preset(categoria.nome, preset.dados)
            assert titulo.endswith(amostra)
            prefixo = titulo[: -len(amostra)] if amostra else titulo
            inicios.append(_largura_sem_ansi(prefixo))
            assert prefixo.endswith(SEPARADOR_NOME_AMOSTRA)
        assert len(set(inicios)) == 1

    # Os presets coloridos exercitam ANSI dentro da amostra sem alterar a
    # largura visual calculada para a coluna comum.
    chips = _filhos(controlador, "chip")
    assert any("\x1b[" in no.campos["titulo"] for no in chips)
    assert all(
        _largura_sem_ansi(no.campos["titulo"])
        >= _largura_sem_ansi(no.campos["titulo"].split(SEPARADOR_NOME_AMOSTRA)[0])
        for no in chips
    )
