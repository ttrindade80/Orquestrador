from tela import controle_execucao as controle_execucao_mod
from tela.controle_execucao import (
    ControleExecucao,
    ControleExecucaoRepresentacao,
)
from tela.registro_acoes import RegistroAcoes


def _controle(modo="executar", recebido=None):
    registro = RegistroAcoes()
    registro.registrar(
        "processo", "processo", ("executar", "dry_run"),
        executor=lambda captura: recebido.append(captura) if recebido is not None else captura,
    )
    return ControleExecucao(
        {"modo_inicial": modo},
        (registro.resolver("processo"),),
        chip_id="chip_controle_execucao",
    )


def test_controle_tem_um_modo_por_instancia_e_insert_alterna():
    primeiro = _controle()
    segundo = _controle("dry_run")
    assert primeiro.modo_atual == "executar"
    assert segundo.modo_atual == "dry_run"
    primeiro.alternar()
    assert primeiro.modo_atual == "dry_run"
    assert segundo.modo_atual == "dry_run"
    primeiro.alternar()
    assert primeiro.modo_atual == "executar"


def test_chip_tem_rotulo_simulacao_e_dry_run_e_destacado():
    controle = _controle("dry_run")
    representacao = controle.representacao_chip()
    assert isinstance(representacao, ControleExecucaoRepresentacao)
    assert representacao.rotulo == "Simulação"
    assert representacao.destacado is True
    assert representacao.chip_id == "chip_controle_execucao"


def test_chip_tem_rotulo_real_e_aparencia_ativa_normal():
    representacao = _controle("executar").representacao_chip()
    assert representacao.rotulo == "Real"
    assert representacao.destacado is False


def test_captura_e_imutavel_e_captura_o_lote_e_modo_no_momento():
    recebido = []
    controle = _controle("executar", recebido)
    lote = ["item_01", "item_02"]
    captura = controle.capturar(lote)
    lote.append("item_03")
    controle.alternar()
    assert type(captura).__name__.startswith("_")
    assert captura.lote_reconciliado == ("item_01", "item_02")
    assert captura.modo_capturado == "executar"
    try:
        captura.modo_capturado = "dry_run"
    except AttributeError:
        pass
    else:
        raise AssertionError("captura deveria ser congelada")
    controle.executar(["item_02"])
    assert recebido[-1].modo_capturado == "dry_run"


def test_captura_eh_privada_e_nao_e_exportada_como_api():
    captura = _controle().capturar(["item_01"])
    assert not hasattr(controle_execucao_mod, "RequisicaoExecucaoCapturada")
    assert "RequisicaoExecucaoCapturada" not in controle_execucao_mod.__all__
    assert "_RequisicaoExecucaoCapturada" not in controle_execucao_mod.__all__
    assert type(captura).__name__.startswith("_")


def test_lote_vazio_nao_chama_executor_nem_cria_captura():
    recebido = []
    controle = _controle(recebido=recebido)
    assert controle.capturar([]) is None
    assert controle.executar([]) is None
    assert recebido == []
