# RELATORIO_IMPLEMENTACAO_H-0038_PYTEST_PADRAO_UNICO

## 1. Identificacao

```yaml
etapa: IMPLEMENTACAO
papel: implementador
data: 2026-07-21
handoff: docs/handoff/H-0038-adocao-pytest-padrao-unico-testes.md
raiz_operacional: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
relatorio_criado: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0038_PYTEST_PADRAO_UNICO.md
```

## 2. Autoridades

```yaml
handoff_autoridade:
  - docs/handoff/H-0038-adocao-pytest-padrao-unico-testes.md
qa_liberador:
  - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0038_HANDOFF.md
  - status: H1_HANDOFF_APPROVED
qa_historico_preservado:
  - docs/relatorios/RELATORIO_QA_H-0038_HANDOFF.md
levantamentos_preservados:
  - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_PENDENCIAS_CONSOLE_PROCESSO_E_PROMPTS.md
contrato_de_processo_alterado:
  - docs/contratos/contrato_processo_desenvolvimento.md
  - escopo: nova secao 13 declarando o comando canonico de testes
```

## 3. Estado Git inicial real

Comandos executados antes de qualquer alteracao:

```bash
cd "$(git rev-parse --show-toplevel)"
git status --short --untracked-files=all
git branch --show-current
git log -1 --oneline
git diff --cached --name-only
```

Resultado observado:

```yaml
branch: master
HEAD: 23f49d0 docs: aplica nomenclatura modular e leitura seletiva
stage: VAZIO
workspace: COM_CINCO_ARQUIVOS_NAO_RASTREADOS
arquivos_nao_rastreados:
  - docs/handoff/H-0038-adocao-pytest-padrao-unico-testes.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_PENDENCIAS_CONSOLE_PROCESSO_E_PROMPTS.md
  - docs/relatorios/RELATORIO_QA_H-0038_HANDOFF.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0038_HANDOFF.md
divergencia_do_estado_esperado: nao
```

O estado Git inicial confere com o esperado pela secao 1 do prompt e pela
secao 15.4 do handoff (observado, nao presumido).

## 4. Arquivos criados

```text
pytest.ini
conftest.py
docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0038_PYTEST_PADRAO_UNICO.md
```

## 5. Arquivos modificados

```text
demo/teste_diagnostico.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
docs/contratos/contrato_processo_desenvolvimento.md
```

## 6. Arquivos preservados sem alteracao

```text
tela/teste_distribuicao_matricial.py
demo/teste_demo.py
demo/teste_demo_console.py
demo/teste_demo_console_modos.py
demo/teste_demo_distribuicao.py
demo/teste_explorar_barra_de_menus.py
docs/handoff/H-0038-adocao-pytest-padrao-unico-testes.md
docs/relatorios/RELATORIO_QA_H-0038_HANDOFF.md
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0038_HANDOFF.md
docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL.md
docs/relatorios/RELATORIO_LEVANTAMENTO_PENDENCIAS_CONSOLE_PROCESSO_E_PROMPTS.md
```

A preservacao foi confirmada por `git diff --stat` vazio para cada um dos
arquivos acima.

## 7. Configuracao do pytest

Arquivo criado: `pytest.ini` (nao foi criada nenhuma outra configuracao
concorrente em `pyproject.toml`, `setup.cfg` ou `tox.ini`).

Conteudo integral:

```ini
[pytest]
python_files = teste_*.py
testpaths = tela demo
```

Justificativa (alinhada a H-0038 secao 7.2):

- `python_files = teste_*.py`: os dez scripts usam o prefixo portugues
  `teste_`; sem esta diretiva, o pytest coleta zero itens.
- `testpaths = tela demo`: limita a descoberta aos dois diretorios onde os
  dez scripts residem, evitando varredura da arvore completa.

## 8. Implementacao do conftest.py

Arquivo criado: `conftest.py` na raiz do repositorio.

Mecanismo: uma unica fixture `autouse` de escopo `function` chamada
`verificar_resultados_internos`, com o seguinte comportamento material:

1. obtem o modulo do item coletado via `request.module`;
2. localiza `_RESULTADOS` no modulo via `getattr(modulo, "_RESULTADOS", None)`;
3. quando o modulo nao possui `_RESULTADOS`, a fixture opera como no-op
   (apenas `yield` e retorna), nao interferindo no item;
4. quando existe, limpa a lista com `resultados.clear()` antes do `yield`,
   garantindo isolamento entre itens coletados;
5. deixa a funcao de teste executar todas as suas verificacoes internas
   (todas as chamadas a `_registrar` acontecem entre o setup e o teardown,
   sem interromper no primeiro falso);
6. apos o `yield`, inspeciona `_RESULTADOS` e reune todas as entradas cujo
   segundo elemento seja falso;
7. se houver entradas falsas, levanta `AssertionError` com os nomes das
   verificacoes reprovadas (formato legivel: `"verificacoes internas
   reprovadas pelo gate do H-0038: '<nome>', '<nome>'"`).

Propriedades do mecanismo:

- nao depende de `main()` em nenhum arquivo;
- nao altera a logica de `_registrar()` nos dez arquivos;
- nao esconde falha ou excecao nativa do teste: o `yield` esta entre o
  setup e o teardown, de modo que qualquer excecao nativa lancada pela
  funcao de teste reprova o item antes da inspecao;
- trata defensivamente entradas com formato inesperado (nao-tupla ou
  tamanho menor que 2), ignorando-as sem mascarar as demais;
- aceita tanto a ordem canonica `(nome, passou)` (nove arquivos) quanto a
  variante `(descricao, ok)` usada por `demo/teste_explorar_barra_de_menus.py`
  (mesma forma material);
- nenhuma outra politica funcional foi adicionada ao `conftest.py`.

Conteudo resumido do arquivo:

```python
import pytest


def _iter_nomes_falsos(resultados):
    for entrada in resultados:
        if not isinstance(entrada, (tuple, list)) or len(entrada) < 2:
            continue
        nome, passou = entrada[0], entrada[1]
        if not passou:
            yield nome


@pytest.fixture(autouse=True)
def verificar_resultados_internos(request):
    modulo = getattr(request, "module", None)
    resultados = getattr(modulo, "_RESULTADOS", None)
    if resultados is None:
        yield
        return
    try:
        resultados.clear()
    except AttributeError:
        pass
    yield
    nomes_falsos = list(_iter_nomes_falsos(resultados))
    if nomes_falsos:
        lista = ", ".join(repr(n) for n in nomes_falsos)
        raise AssertionError(
            "verificacoes internas reprovadas pelo gate do H-0038: "
            "{0}".format(lista)
        )
```

## 9. Correcoes nos quatro testes

### `demo/teste_diagnostico.py`

- `teste_modo_executavel`: removido o parametro posicional `resultado_esperado`
  (causa do ERROR de setup "fixture 'resultado_esperado' not found"); o
  resultado esperado passou a ser computado internamente por
  `gerar_diagnostico_tela()`, preservando integralmente o subprocesso, a
  comparacao de stdout e os criterios do H-0032.
- `teste_invariantes_anteriores`: removido o `return todos_ok` final
  (produzia `PytestReturnNotNoneWarning`); o calculo interno de `todos_ok`
  permanece para a logica de fluxo, porem nao e mais retornado.
- `teste_gerar_diagnostico`: removidos os `return None` e `return resultado`
  dos caminhos de excecao e sucesso; a funcao agora retorna implicitamente
  `None` (sem `return` explicito).
- `main()`: nao captura mais o retorno de `teste_invariantes_anteriores`,
  `teste_gerar_diagnostico` ou `teste_modo_executavel`; o fluxo permanece
  o mesmo (invariantes -> gerar diagnostico -> modo executavel ->
  proibicoes -> telas h0035 -> pipeline h0036).

### `tela/teste_loader.py`

- `teste_caminho_feliz`: removidos os `return None` e `return tela` finais.
- `main()`: removida a captura `tela_real = teste_caminho_feliz()` e o bloco
  de impressao diagnostica dependente do retorno (`== Representacao interna
  carregada (resumo) ==`), conforme autorizado pela secao 7.1 do handoff
  ("omitir o bloco de impressao").

### `tela/teste_modelo.py`

- `teste_modelo_orquestrador`: removidos os `return None` e `return modelo`
  finais.
- `teste_modelo_grupo_minimo`: removido o `return None` do caminho de
  excecao. Justificativa da inclusao: embora o handoff liste apenas
  `teste_modelo_orquestrador` como fonte historica de warning, esta funcao
  tambem e coletada pelo pytest e tambem produzia
  `PytestReturnNotNoneWarning`; a remocao do `return None` explicito e
  estritamente necessaria para satisfazer o CA-05 dentro do arquivo ja
  autorizado como MODIFICAR.
- `main()`: nao captura mais o retorno de `teste_modelo_orquestrador` e
  nao imprime mais o bloco `== Diagnostico do modelo ==` que dependia do
  retorno.

### `tela/teste_renderizador.py`

- `teste_renderizador_orquestrador`: removidos os `return None` (dois
  caminhos de excecao) e o `return modelo` final.
- `teste_renderizador_destino_minimo`: removidos os `return None` (dois
  caminhos de excecao) e o `return modelo` final.
- `teste_renderizador_grupo_minimo`: removidos os `return None` (dois
  caminhos de excecao) e o `return modelo` final.
- `main()`: nenhuma alteracao necessaria, pois os tres retornos nao eram
  capturados.
- Metodo auxiliar `_modelo_demo` (linha ~7626, dentro de
  `TestDistribuicaoResponsivaH0034`) preservado: e metodo privado
  (prefixo `_`), nao coletado como item pytest, e nao gera warning.

Todas as verificacoes internas de cada funcao foram preservadas
integralmente; apenas os `return <valor>` foram removidos.

## 10. Atualizacao do contrato

Foi adicionada a secao `13. Suíte de testes canônica (H-0038)` ao final de
`docs/contratos/contrato_processo_desenvolvimento.md`, declarando:

```yaml
comando_canonico:
  - PYTHONDONTWRITEBYTECODE=1 python -m pytest

execucao_direta_dos_scripts:
  status: permitida_mas_nao_canonica

gate_oficial:
  quantidade: um
  ferramenta: pytest
```

Nenhuma outra secao do contrato foi alterada (processo, papeis, ciclo, QA,
stage ou commit permanecem intactos). A secao 3 do contrato (autoridade
documental) ja colocava o contrato de processo acima de handoffs; a nova
declaracao supera, por hierarquia, qualquer handoff anterior que tratasse
a execucao direta dos scripts como gate canonico.

## 11. Coleta antes e depois

### Antes (estado historico do handoff H-0038 secao 3)

```yaml
pytest_padrao_atual:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  itens_coletados: 0
  codigo_de_saida: 5
  causa: ausencia de configuracao
```

### Depois (apos a implementacao)

Comando:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest --collect-only -q
```

Resultado consolidado:

```yaml
codigo_de_saida: 0
itens_coletados: 422
diferenca_em_relacao_ao_baseline_de_422: 0
dez_arquivos_descobertos_automaticamente: sim
zero_arquivos_especificados_manualmente: sim
```

Inventario por arquivo (apos implementacao):

```yaml
tela/teste_distribuicao_matricial.py: 25
tela/teste_loader.py: 19
tela/teste_modelo.py: 15
tela/teste_renderizador.py: 292
demo/teste_demo.py: 15
demo/teste_demo_console.py: 6
demo/teste_demo_console_modos.py: 11
demo/teste_demo_distribuicao.py: 14
demo/teste_diagnostico.py: 6
demo/teste_explorar_barra_de_menus.py: 19
total: 422
```

Contagem identica ao baseline historico do H-0038. Nenhuma diferenca a
justificar.

Inventario por classe (metodos `test_*` dentro de classes `Test*`):

```yaml
(modulo / funcoes teste_*): 131
TestDistribuicaoH0018: 35
TestLinhasBarra: 27
TestOcupacaoIntegralCorpoH0033: 22
TestDistribuicaoVerticalH0025: 22
TestCardinalidadeUnitariaH0029: 20
TestHierarquiaGruposH0027: 19
TestDistribuicaoHorizontalH0026: 16
TestPreenchimentoBordeadoH0021: 14
TestDistribuicaoResponsivaH0034: 14
TestArranjoH0019: 13
TestTelasPermanentesH0029: 12
TestPreenchimentoVerticalH0020: 12
TestDistribuicaoMatricialH0035: 12
TestHelperHorizontalH0033Patch2: 10
TestRenderizadorMatrizH0028: 8
TestCatalogoH0030: 8
TestCardinalidadeHorizontalH0033Patch4: 7
TestValidacaoMatrizH0028: 6
TestCardinalidadeHorizontalH0033Patch3: 6
TestModeloCatalogoH0030: 5
TestModeloMatrizH0028: 3
total_classes: 22
```

Confirmacoes CA-10:

- os dez arquivos oficiais sao coletados automaticamente;
- funcoes `teste_*` reais permanecem coletadas (131 itens de modulo);
- metodos `test_*` em classes `Test*` reais permanecem coletados
  (evidencia: `TestHelperHorizontalH0033Patch2` com 10 metodos, citado como
  achado QA-H0038-002 no QA inicial);
- parametrizacoes legitimas permanecem coletadas (sem alteracao nos dez
  arquivos);
- funcoes auxiliares nao aparecem como node IDs — verificado que `main`,
  `_registrar`, `_espera_excecao`, `_finalizar` e `run_all` nao aparecem
  como itens coletados.

## 12. Testes focais

Cada comando abaixo foi executado apos as correcoes:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_diagnostico.py
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_loader.py
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_modelo.py
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_renderizador.py
```

Resultados por arquivo:

```yaml
demo/teste_diagnostico.py:
  codigo_de_saida: 0
  itens_coletados: 6
  passed: 6
  failed: 0
  errors: 0
  warnings_do_projeto: 0

tela/teste_loader.py:
  codigo_de_saida: 0
  itens_coletados: 19
  passed: 19
  failed: 0
  errors: 0
  warnings_do_projeto: 0

tela/teste_modelo.py:
  codigo_de_saida: 0
  itens_coletados: 15
  passed: 15
  failed: 0
  errors: 0
  warnings_do_projeto: 0

tela/teste_renderizador.py:
  codigo_de_saida: 0
  itens_coletados: 292
  passed: 292
  failed: 0
  errors: 0
  warnings_do_projeto: 0
```

Prova adicional: a re-execucao de cada arquivo focal com
`-W error::pytest.PytestReturnNotNoneWarning` (que transformaria qualquer
warning desse tipo em erro de item) retornou codigo zero para os quatro
arquivos, confirmando a ausencia de `PytestReturnNotNoneWarning` do projeto.

## 13. Execucao canonica

Comando:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

Resultado:

```yaml
codigo_de_saida: 0
passed: 422
failed: 0
errors: 0
warnings_do_projeto: 0
warnings_externos_emitidos: 0
PytestReturnNotNoneWarning_do_projeto: 0
falhas_internas_registradas: 0
fixture_conftest_reprovou_algum_item: nao
```

Saida final:

```text
============================= 422 passed in 16.75s =============================
```

Nenhum resumo de warnings foi emitido pelo pytest (nem do projeto, nem de
plugins externos como `anyio` ou `typeguard`). Os plugins `anyio-4.14.2` e
`typeguard-4.5.2` permanecem carregados, mas nao produziram warnings na
suite.

## 14. Prova negativa

Procedimento executado exatamente como prescrito na secao 10, item 3 do
handoff e na secao 11 do prompt.

Arquivo temporario: `tela/teste_h0038_gate_negativo_temporario.py`

Conteudo:

```python
_RESULTADOS = []

def _registrar(nome, passou):
    _RESULTADOS.append((nome, passou))

def teste_gate_negativo_temporario():
    _registrar("prova negativa controlada do H-0038", False)
```

Comando:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

Resultado registrado:

```yaml
arquivo_temporario: tela/teste_h0038_gate_negativo_temporario.py
foi_coletado: sim
item_resultante: tela/teste_h0038_gate_negativo_temporario.py::teste_gate_negativo_temporario
resultado_do_item: ERROR (AssertionError no teardown da fixture verificar_resultados_internos)
codigo_do_pytest: 1
falha_mencionou_verificacao_controlada: sim
mensagem_do_gate: "verificacoes internas reprovadas pelo gate do H-0038: 'prova negativa controlada do H-0038'"
demais_itens_da_suite: 423 passed (nao houve interrupcao prematura)
arquivo_removido: sim
arquivo_ausente_do_git_status_final: sim
stage_vazio: sim
```

Trecho relevante da saida do pytest:

```text
conftest.py:82: AssertionError
AssertionError: verificacoes internas reprovadas pelo gate do H-0038: 'prova negativa controlada do H-0038'
=========================== short test summary info ============================
ERROR tela/teste_h0038_gate_negativo_temporario.py::teste_gate_negativo_temporario
======================== 423 passed, 1 error in 16.64s =========================
```

Aprovada: `_registrar(False)` resultou em falha real do pytest, codigo de
saida 1, mensagem citando a verificacao controlada, e nenhuma dependencia
de `main()`. O arquivo temporario foi removido integralmente, o git status
final nao o lista e o stage permaneceu vazio.

## 15. Warnings por origem

```yaml
warnings_do_projeto:
  PytestReturnNotNoneWarning: 0
  outros: 0

warnings_externos:
  anyio: 0
  typeguard: 0
  ambiente_python: 0
  total: 0

separacao_confirmada: sim
CA_05_satisfeito: sim
```

Nenhum warning foi emitido na execucao canonica. Os 7 warnings
historicos de `PytestReturnNotNoneWarning` citados pelo handoff (H-0038
secao 3) foram eliminados pelas correcoes da secao 9 deste relatorio. O
erro legado `fixture 'resultado_esperado' not found` foi eliminado pela
refatoracao de `teste_modo_executavel` (CA-06 satisfeito).

## 16. Matriz de cobertura

| Script anterior | Verificacoes ou grupos preservados | Itens pytest correspondentes | Conversao de falha interna | Alteracao de cobertura |
| --------------- | ---------------------------------- | ---------------------------- | -------------------------- | ---------------------- |
| `tela/teste_loader.py` | caminho feliz de `demo.json`; erros de carregamento (arquivo ausente, JSON invalido, schema/id/cabecalho/corpo/barra ausentes, elementos invalidos, tipos desconhecidos); tipos validos; grupo estrutural (H-0012); arranjo de corpo (H-0019); distribuicao de corpo (H-0025); hierarquia de grupos (H-0027/ADR-0019); config lancador (H-0034); distribuicao matricial (H-0035); matriz H-0028; catalogo H-0030; raiz de telas H-0032; conteudo externo H-0036; D23 estrutural | 19 | `conftest.py` (fixture autouse) | nenhuma |
| `tela/teste_modelo.py` | modelo da `demo`; modelo de grupo_minimo (H-0012); erros do construtor; hierarquia recursiva (ADR-0019); matriz no modelo (H-0028); catalogo H-0030; parametros_tipo (H-0034); distribuicao_matricial no modelo (H-0035); conteudo externo multinivel (H-0036) | 15 | `conftest.py` (fixture autouse) | nenhuma |
| `tela/teste_renderizador.py` | renderer sobre `demo`, `destino_minimo`, `grupo_minimo`; modelo fabricado; erros; proibicoes de importacao; hardcoding; inercia; alternancia de borda; largura e altura explicitas; linhas de barra; distribuicoes H-0018/H-0025/H-0026; arranjo H-0019; preenchimento H-0020/H-0021; hierarquia H-0027; matriz H-0028; cardinalidade H-0029; catalogo H-0030; responsiva H-0034; ocupacao H-0033; distribuicao matricial H-0035; conteudo externo H-0036; manual H-0037 | 292 | `conftest.py` (fixture autouse) | nenhuma |
| `tela/teste_distribuicao_matricial.py` | formacao preferencias (linhas/colunas/matriz fixa); ordem por linha/coluna; dimensionamento; margens e distribuicao horizontal; vao maximo; resto; coordenadas; cardinalidade unitaria; uma linha/coluna; fallback impossivel; recuperacao; determinismo; sem perda/duplicacao; alinhamento; zero participantes; erros de dominio | 25 | `conftest.py` (fixture autouse) | nenhuma |
| `demo/teste_diagnostico.py` | invariantes H-0001/H-0002/H-0010A; `gerar_diagnostico_tela()` sem excecao; identidade material da saida; determinismo; comparacao estrita com expected output; campos inertes nao vazam; modo executavel `python demo/diagnostico.py`; proibicoes de importacao; telas permanentes H-0035; pipeline H-0036 | 6 | `conftest.py` (fixture autouse) | nenhuma |
| `demo/teste_demo.py` | diagnostico da tela demo via render; casos visuais; inercia de campos | 15 | `conftest.py` (fixture autouse) | nenhuma |
| `demo/teste_demo_console.py` | render do console da demo; modo verboso/normal; conteudo externo | 6 | `conftest.py` (fixture autouse) | nenhuma |
| `demo/teste_demo_console_modos.py` | modos por tela (H-0037); alternancia verbosa | 11 | `conftest.py` (fixture autouse) | nenhuma |
| `demo/teste_demo_distribuicao.py` | distribuicao matricial no demo; regressao de defeito; fixtures de geometria; pseudo-tty catalogo | 14 | `conftest.py` (fixture autouse) | nenhuma |
| `demo/teste_explorar_barra_de_menus.py` | casos de exploracao CLI (exit codes, determinismo, single/multilinha, overflow, ancoras, violacoes de inspecao, parametros invalidos, vaos/margens, matriz padrao, invariantes) | 19 | `conftest.py` (fixture autouse) | nenhuma |

Total pytest apos migracao: 422 itens.

A diferenca entre 2.778 verificacoes internas (`_registrar`) e 422 itens
pytest permanece explicada pela natureza distinta das grandezas (H-0038
secao 8.1):

- `2.778` e a contagem de chamadas individuais a `_registrar()` executadas
  pelos dez scripts quando rodados diretamente; cada chamada e uma
  afirmacao atomica;
- `422` e a contagem de funcoes/metodos coletados pelo pytest; cada item
  pytest agrupa multiplas chamadas a `_registrar()`.

A correspondencia entre falha interna e falha pytest agora e fechada pelo
`conftest.py`: qualquer `_registrar(nome, False)` produz falha real do
item pytest que o contiver (comprovado pela prova negativa da secao 14).
Nenhuma verificacao foi removida ou enfraquecida para obter resultado
verde.

## 17. Desvios ou excecoes

```yaml
excecoes_operacionais: []
desvios_do_escopo_autorizado: []
```

Observacoes relevantes (nao bloqueantes, dentro do escopo autorizado):

1. `tela/teste_modelo.py::teste_modelo_grupo_minimo` tinha `return None`
   explicito em um caminho de excecao. Embora o handoff (H-0038 secao 7.1)
   liste apenas `teste_modelo_orquestrador` como fonte historica de
   `PytestReturnNotNoneWarning` neste arquivo, a remocao do `return None`
   de `teste_modelo_grupo_minimo` foi necessaria para satisfazer o CA-05
   (ausencia de `PytestReturnNotNoneWarning` do projeto). A alteracao esta
   dentro do arquivo ja classificado como MODIFICAR e nao altera o
   comportamento da funcao (o caminho de excecao continua registrando a
   falha via `_registrar` antes de sair). Nao constitui excecao operacional
   de arquivo porque o arquivo ja estava autorizado; e apenas um ajuste
   adicional dentro do mesmo arquivo, consistente com o objetivo do CA-05.
2. As funcoes `teste_*` (com "e" no prefixo) sao coletadas pelo pytest
   9.0.3 neste projeto; a evidencia material esta na coleta (422 itens,
   inclui `teste_caminho_feliz`, `teste_modelo_orquestrador` etc.). Por
   isso os warnings historicos de `PytestReturnNotNoneWarning` existiam e
   foram corrigidos.

## 18. Estado Git final

Comandos executados apos a implementacao:

```bash
git diff --check
git status --short --untracked-files=all
git diff --cached --name-only
```

Resultado observado:

```yaml
diff_check: sem falhas de whitespace (exit 0)
stage: VAZIO
arquivos_rastreados_modificados:
  - demo/teste_diagnostico.py
  - docs/contratos/contrato_processo_desenvolvimento.md
  - tela/teste_loader.py
  - tela/teste_modelo.py
  - tela/teste_renderizador.py
arquivos_nao_rastreados:
  - conftest.py
  - pytest.ini
  - docs/handoff/H-0038-adocao-pytest-padrao-unico-testes.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_PENDENCIAS_CONSOLE_PROCESSO_E_PROMPTS.md
  - docs/relatorios/RELATORIO_QA_H-0038_HANDOFF.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0038_HANDOFF.md
  - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0038_PYTEST_PADRAO_UNICO.md
arquivo_temporario_da_prova_negativa: ausente
arquivo_fora_da_lista_autorizada: nenhum
```

Confere integralmente com o estado Git final esperado pela secao 15 do
prompt e pela secao 12 do handoff.

## 19. Stage vazio

```yaml
stage_vazio: sim
verificacao: git diff --cached --name-only
saida: ""
```

Nada foi adicionado ao stage, conforme exigido pelo CA-09 e pela secao 15
do prompt.

## 20. Conclusao

A implementacao do H-0038 transforma `PYTHONDONTWRITEBYTECODE=1 python -m pytest`
no unico comando canonico de testes, com descoberta automatica dos dez
arquivos oficiais, execucao unificada, codigo de saida zero somente quando
nao ha falhas ou erros, e conversao de `_registrar(False)` em falha real
de item pytest via `conftest.py`. Os criterios de aceite CA-01 a CA-10 e
CA-FALHA-INTERNA-01 a 03 sao satisfeitos. A cobertura material foi
preservada sem regressao: 422 itens pytest cobrindo os mesmos grupos de
verificacao dos dez scripts, com o gate agora operando sobre falhas
internas anteriormente dependentes de `main()`. A prova negativa confirma
o funcionamento do mecanismo.

```text
IMPLEMENTATION_COMPLETED_AWAITING_QA
```
