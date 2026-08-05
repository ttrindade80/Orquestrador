import importlib.util
from pathlib import Path


_spec = importlib.util.spec_from_file_location(
    "teste_executor_h0050",
    Path(__file__).with_name("executor_controle_execucao.py"),
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
executar = _mod.executar
documento_resultado_observavel = _mod.documento_resultado_observavel
from tela.controle_execucao import ControleExecucao
from tela.execucao_focal import resultado_semanticamente_valido
from tela.registro_acoes import RegistroAcoes


def test_executor_consumes_only_capture_and_fixture():
    registro = RegistroAcoes()
    registro.registrar(
        "processo", "processo", ("executar", "dry_run"), executor=lambda captura: captura
    )
    controle = ControleExecucao(
        {"modo_inicial": "dry_run"}, (registro.resolver("processo"),)
    )
    captura = controle.capturar(("item_02", "item_01"))
    fixture = {
        "itens": [
            {"id": "item_01", "valor": "A"},
            {"id": "item_02", "valor": "B"},
        ]
    }
    resultado = executar(captura, fixture)
    assert resultado["modo"] == "dry_run"
    assert resultado["lote_reconciliado"] == ["item_02", "item_01"]
    assert resultado["resultado"] == "DRY_RUN"
    assert resultado_semanticamente_valido(resultado["resultado_bruto"])
    bruto = documento_resultado_observavel(resultado)
    assert resultado_semanticamente_valido(bruto)
    assert '"modo":"dry_run"' in bruto or '"valor":"dry_run"' in bruto
    assert "item_02" in bruto and "item_01" in bruto


def test_executor_modo_real_sem_marcador_dry_run():
    class _Captura:
        lote_reconciliado = ("item_01",)
        modo_capturado = "executar"

    resultado = executar(
        _Captura(),
        {"itens": [{"id": "item_01", "valor": "x"}]},
    )
    assert resultado["modo"] == "executar"
    assert resultado["resultado"] == "EXECUTADO"
    assert "DRY_RUN" not in resultado["resultado"]
    assert resultado_semanticamente_valido(resultado["resultado_bruto"])
    assert '"valor":"executar"' in resultado["resultado_bruto"]
