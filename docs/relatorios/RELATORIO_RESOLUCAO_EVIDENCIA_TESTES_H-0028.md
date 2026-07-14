# RELATORIO_RESOLUCAO_EVIDENCIA_TESTES_H-0028

## 1. Identificação

- handoff: `H-0028-matriz-de-grupos-coordenadas-explicitas`
- implementação: `IMP-0029-matriz-de-grupos-coordenadas-explicitas`
- commit-base: `f00b0bb968847205bb0bcca5259af0ae11af1844`
- etapa: `RESOLVER_EVIDENCIA_TESTES`
- papel: `investigador de evidência de testes`
- raiz Git: `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`
- branch: `master`
- HEAD atual: `f00b0bb` (HEAD não avançou; nenhum commit criado)

---

## 2. Problema investigado

A implementação do H-0028 retornou `IMPLEMENTATION_INCOMPLETE` porque o comando de suite completa exigido pelo handoff (`python3 -m pytest ...`) terminou com `224 passed, 10 errors`. O objetivo desta etapa é determinar:

1. se os 10 erros foram introduzidos pelo H-0028;
2. se já existiam no commit-base `f00b0bb`;
3. se decorrem de testes legados escritos para execução direta, mas coletados indevidamente pelo pytest;
4. se revelam um comando obrigatório incorreto no handoff;
5. se impedem ou não a transição para `QA_IMPLEMENTACAO`.

---

## 3. Comandos definidos no handoff

### 3.1 Suite completa (seções 23.1 e 23.6)

```bash
# executado a partir do diretório scripts/
python3 -m pytest tela/teste_loader.py tela/teste_modelo.py tela/teste_renderizador.py tela/teste_demo.py tela/teste_diagnostico.py tela/teste_explorar_barra_de_menus.py -q --tb=short
```

```text
comando_suite_completa_handoff: python3 -m pytest tela/teste_loader.py tela/teste_modelo.py tela/teste_renderizador.py tela/teste_demo.py tela/teste_diagnostico.py tela/teste_explorar_barra_de_menus.py -q --tb=short
```

### 3.2 Comandos diretos (IMP-0029 seção 18, conforme prática documentada)

```bash
python3 scripts/tela/teste_loader.py
python3 scripts/tela/teste_modelo.py
python3 scripts/tela/teste_renderizador.py
python3 scripts/tela/teste_demo.py
python3 scripts/tela/teste_diagnostico.py
python3 scripts/tela/teste_explorar_barra_de_menus.py
```

```text
comandos_diretos_handoff: seis comandos de execução direta, um por arquivo
```

### 3.3 Natureza do comando pytest no handoff

O handoff apresenta o comando pytest como **critério obrigatório de aprovação**. A seção 26 lista dezesseis critérios de aceite; o critério 12 diz:

> **Suite completa aprovada**: todos os testes (anteriores + novos) passam com resultado `N/N`.

A seção 23.6 especifica que o resultado deve ser "todos os testes anteriores (1004) passando; testes novos passando; novo total = 1004 + N". O critério não apresenta abertura para erros de coleta nem para exclusão de arquivos.

---

## 4. Ambiente de execução

```text
Python: 3.14.6
pytest: 9.0.3
OS: Linux (Arch)
```

---

## 5. Reprodução no baseline

### 5.1 Criação da cópia isolada

```bash
BASELINE_DIR=$(mktemp -d /tmp/h0028-baseline-XXXXXX)
# resultado: /tmp/h0028-baseline-he1oMd
git archive f00b0bb | tar -x -C "$BASELINE_DIR"
```

### 5.2 Resultado do pytest no baseline

```text
BASELINE_PYTEST_RC=1

207 passed, 7 warnings, 10 errors
```

**Erros de coleta (baseline):**

| # | Node ID | Fixture ausente | Arquivo | Linha |
|---|---------|-----------------|---------|-------|
| 1 | `tela/teste_loader.py::teste_erros` | `tmp_base` | `teste_loader.py` | 367 |
| 2 | `tela/teste_loader.py::teste_tipos_validos` | `tmp_base` | `teste_loader.py` | 517 |
| 3 | `tela/teste_loader.py::teste_grupo_estrutural` | `tmp_base` | `teste_loader.py` | 542 |
| 4 | `tela/teste_loader.py::teste_arranjo_corpo_h0019` | `tmp_base` | `teste_loader.py` | 747 |
| 5 | `tela/teste_loader.py::teste_distribuicao_corpo_h0025` | `tmp_base` | `teste_loader.py` | 837 |
| 6 | `tela/teste_loader.py::teste_hierarquia_grupos_adr0019` | `tmp_base` | `teste_loader.py` | 1003 |
| 7 | `tela/teste_demo.py::teste_navegacao_minima` | `modelo` | `teste_demo.py` | 412 |
| 8 | `tela/teste_demo.py::teste_renderizar_estado` | `modelo` | `teste_demo.py` | 582 |
| 9 | `tela/teste_demo.py::teste_renderizar_estado_altura` | `modelo` | `teste_demo.py` | 679 |
| 10 | `tela/teste_diagnostico.py::teste_modo_executavel` | `resultado_esperado` | `teste_diagnostico.py` | 228 |

---

## 6. Reprodução na implementação atual

### 6.1 Resultado do pytest na implementação atual

```text
CURRENT_PYTEST_RC=1

224 passed, 7 warnings, 10 errors
```

**Erros de coleta (atual):**

| # | Node ID | Fixture ausente | Arquivo | Linha |
|---|---------|-----------------|---------|-------|
| 1 | `tela/teste_loader.py::teste_erros` | `tmp_base` | `teste_loader.py` | 367 |
| 2 | `tela/teste_loader.py::teste_tipos_validos` | `tmp_base` | `teste_loader.py` | 517 |
| 3 | `tela/teste_loader.py::teste_grupo_estrutural` | `tmp_base` | `teste_loader.py` | 542 |
| 4 | `tela/teste_loader.py::teste_arranjo_corpo_h0019` | `tmp_base` | `teste_loader.py` | 747 |
| 5 | `tela/teste_loader.py::teste_distribuicao_corpo_h0025` | `tmp_base` | `teste_loader.py` | 837 |
| 6 | `tela/teste_loader.py::teste_hierarquia_grupos_adr0019` | `tmp_base` | `teste_loader.py` | 1003 |
| 7 | `tela/teste_demo.py::teste_navegacao_minima` | `modelo` | `teste_demo.py` | 412 |
| 8 | `tela/teste_demo.py::teste_renderizar_estado` | `modelo` | `teste_demo.py` | 582 |
| 9 | `tela/teste_demo.py::teste_renderizar_estado_altura` | `modelo` | `teste_demo.py` | 679 |
| 10 | `tela/teste_diagnostico.py::teste_modo_executavel` | `resultado_esperado` | `teste_diagnostico.py` | 228 |

---

## 7. Comparação dos resultados

| Item | Baseline `f00b0bb` | Implementação atual | Igual? |
|------|--------------------|---------------------|--------|
| passed | 207 | 224 | Não (+17 novos testes) |
| failed | 0 | 0 | Sim |
| errors | 10 | 10 | Sim |
| skipped | 0 | 0 | Sim |
| código de saída | 1 | 1 | Sim |
| node IDs com erro | 10 listados acima | 10 listados acima | Idênticos |
| arquivos afetados | teste_loader.py, teste_demo.py, teste_diagnostico.py | idem | Idênticos |
| linhas afetadas | 367, 517, 542, 747, 837, 1003, 412, 582, 679, 228 | idem | Idênticas |
| fixtures ausentes | tmp_base, modelo, resultado_esperado | idem | Idênticas |
| mensagens de coleta | fixture 'X' not found | idem | Idênticas |

**Tabela de erros individuais (comparação node ID por node ID):**

| Node ID | Fixture ou causa | Existe no baseline? | Existe no atual? | Relação com H-0028 |
|---------|-----------------|---------------------|-----------------|---------------------|
| `teste_loader.py::teste_erros` | `tmp_base` ausente | Sim (linha 367) | Sim (linha 367) | Nenhuma — pré-existente |
| `teste_loader.py::teste_tipos_validos` | `tmp_base` ausente | Sim (linha 517) | Sim (linha 517) | Nenhuma — pré-existente |
| `teste_loader.py::teste_grupo_estrutural` | `tmp_base` ausente | Sim (linha 542) | Sim (linha 542) | Nenhuma — pré-existente |
| `teste_loader.py::teste_arranjo_corpo_h0019` | `tmp_base` ausente | Sim (linha 747) | Sim (linha 747) | Nenhuma — pré-existente |
| `teste_loader.py::teste_distribuicao_corpo_h0025` | `tmp_base` ausente | Sim (linha 837) | Sim (linha 837) | Nenhuma — pré-existente |
| `teste_loader.py::teste_hierarquia_grupos_adr0019` | `tmp_base` ausente | Sim (linha 1003) | Sim (linha 1003) | Nenhuma — pré-existente |
| `teste_demo.py::teste_navegacao_minima` | `modelo` ausente | Sim (linha 412) | Sim (linha 412) | Nenhuma — arquivo proibido, não modificado |
| `teste_demo.py::teste_renderizar_estado` | `modelo` ausente | Sim (linha 582) | Sim (linha 582) | Nenhuma — arquivo proibido, não modificado |
| `teste_demo.py::teste_renderizar_estado_altura` | `modelo` ausente | Sim (linha 679) | Sim (linha 679) | Nenhuma — arquivo proibido, não modificado |
| `teste_diagnostico.py::teste_modo_executavel` | `resultado_esperado` ausente | Sim (linha 228) | Sim (linha 228) | Nenhuma — arquivo proibido, não modificado |

---

## 8. Análise individual dos erros de coleta

Cada função coletada com erro pelo pytest tem as mesmas propriedades em baseline e no estado atual:

### 8.1 Funções em `teste_loader.py` (6 erros)

As funções `teste_erros(tmp_base)`, `teste_tipos_validos(tmp_base)`, `teste_grupo_estrutural(tmp_base)`, `teste_arranjo_corpo_h0019(tmp_base)`, `teste_distribuicao_corpo_h0025(tmp_base)`, `teste_hierarquia_grupos_adr0019(tmp_base)`:

1. **Nome começa com `teste_`**: Sim → pytest as coleta como funções de teste.
2. **Possui parâmetro `tmp_base`**: Sim → pytest tenta injetar como fixture, mas não existe.
3. **Parâmetro fornecido por executor interno**: Sim. A função `main()` do arquivo cria `tmp_base = Path(tempfile.mkdtemp(...))` e passa como argumento posicional. O parâmetro não é um fixture pytest.
4. **Chamada por rotina `main`**: Sim. `main()` chama `teste_erros(tmp_base)`, `teste_tipos_validos(tmp_base)`, etc.
5. **Fixture pytest declarada**: Não. Não existe `@pytest.fixture` nem `conftest.py`.
6. **Passa na execução direta**: Sim. Cada uma faz parte do total 129/129 → 0 falhas no baseline direto.
7. **Existia em `f00b0bb`**: Sim. Linhas idênticas, mesmo comportamento.
8. **H-0028 modificou**: Não. O H-0028 adicionou `TestValidacaoMatrizH0028` APÓS essas funções (linhas 1450+). As funções permanecem na mesma linha e com a mesma assinatura.

**Classificação**: `PREEXISTENTE_COLETA_PYTEST`

### 8.2 Funções em `teste_demo.py` (3 erros)

As funções `teste_navegacao_minima(modelo)`, `teste_renderizar_estado(modelo)`, `teste_renderizar_estado_altura(modelo)`:

1. **Nome começa com `teste_`**: Sim.
2. **Possui parâmetro `modelo`**: Sim → pytest tenta injetar como fixture, mas não existe.
3. **Parâmetro fornecido por executor interno**: Sim. `main()` cria `modelo = _carregar_modelo()` e passa como argumento.
4. **Chamada por rotina `main`**: Sim.
5. **Fixture pytest declarada**: Não.
6. **Passa na execução direta**: Sim. Parte do total 303/303.
7. **Existia em `f00b0bb`**: Sim.
8. **H-0028 modificou**: Não. `teste_demo.py` é arquivo proibido no H-0028 e não foi alterado (confirmado por `git diff --name-only`).

**Classificação**: `PREEXISTENTE_COLETA_PYTEST`

### 8.3 Função em `teste_diagnostico.py` (1 erro)

A função `teste_modo_executavel(resultado_esperado)`:

1. **Nome começa com `teste_`**: Sim.
2. **Possui parâmetro `resultado_esperado`**: Sim → pytest tenta injetar como fixture.
3. **Parâmetro fornecido por executor interno**: Sim. `main()` obtém `resultado` de uma função anterior e passa como argumento.
4. **Chamada por rotina `main`**: Sim.
5. **Fixture pytest declarada**: Não.
6. **Passa na execução direta**: Sim. Parte do total 28/28.
7. **Existia em `f00b0bb`**: Sim.
8. **H-0028 modificou**: Não. `teste_diagnostico.py` é arquivo proibido no H-0028 e não foi alterado.

**Classificação**: `PREEXISTENTE_COLETA_PYTEST`

### 8.4 Resumo de classificação

| Erro | Classificação |
|------|---------------|
| `teste_loader.py::teste_erros` | `PREEXISTENTE_COLETA_PYTEST` |
| `teste_loader.py::teste_tipos_validos` | `PREEXISTENTE_COLETA_PYTEST` |
| `teste_loader.py::teste_grupo_estrutural` | `PREEXISTENTE_COLETA_PYTEST` |
| `teste_loader.py::teste_arranjo_corpo_h0019` | `PREEXISTENTE_COLETA_PYTEST` |
| `teste_loader.py::teste_distribuicao_corpo_h0025` | `PREEXISTENTE_COLETA_PYTEST` |
| `teste_loader.py::teste_hierarquia_grupos_adr0019` | `PREEXISTENTE_COLETA_PYTEST` |
| `teste_demo.py::teste_navegacao_minima` | `PREEXISTENTE_COLETA_PYTEST` |
| `teste_demo.py::teste_renderizar_estado` | `PREEXISTENTE_COLETA_PYTEST` |
| `teste_demo.py::teste_renderizar_estado_altura` | `PREEXISTENTE_COLETA_PYTEST` |
| `teste_diagnostico.py::teste_modo_executavel` | `PREEXISTENTE_COLETA_PYTEST` |

Nenhum erro é `INTRODUZIDO_H0028`.

---

## 9. Execuções diretas

### 9.1 Baseline (`f00b0bb`)

```text
baseline_direto:
  loader:       total=129  aprovados=129  falhos=0  codigo_saida=0
  modelo:       total=81   aprovados=81   falhos=0  codigo_saida=0
  renderizador: total=491  aprovados=491  falhos=0  codigo_saida=0
  demo:         total=303  aprovados=303  falhos=0  codigo_saida=0
  diagnostico:  total=28   aprovados=28   falhos=0  codigo_saida=0
  barra:        total=38   aprovados=38   falhos=0  codigo_saida=0
  TOTAL:        total=1070 aprovados=1070 falhos=0
```

**Nota**: O total de 1070 verificações em 6 arquivos é o valor medido diretamente na cópia do commit `f00b0bb`. O valor "1004" referenciado pelo handoff corresponde à contagem dos 4 arquivos principais (loader + modelo + renderizador + demo = 129 + 81 + 491 + 303 = 1004), excluindo `teste_diagnostico.py` (28) e `teste_explorar_barra_de_menus.py` (38), conforme a contagem histórica do ciclo H-0027.

### 9.2 Implementação atual

```text
atual_direto:
  loader:       total=172  aprovados=172  falhos=0  codigo_saida=0
  modelo:       total=88   aprovados=88   falhos=0  codigo_saida=0
  renderizador: total=504  aprovados=504  falhos=0  codigo_saida=0
  demo:         total=303  aprovados=303  falhos=0  codigo_saida=0
  diagnostico:  total=28   aprovados=28   falhos=0  codigo_saida=0
  barra:        total=38   aprovados=38   falhos=0  codigo_saida=0
  TOTAL:        total=1133 aprovados=1133 falhos=0
```

Confirmado: `1133/1133`, código de saída 0 em todos os 6 arquivos. Zero falhas.

---

## 10. Testes novos do H-0028

### 10.1 Novas classes adicionadas

| Classe | Arquivo | Linha inicial |
|--------|---------|---------------|
| `TestValidacaoMatrizH0028` | `teste_loader.py` | 1450 |
| `TestModeloMatrizH0028` | `teste_modelo.py` | 717 |
| `TestRenderizadorMatrizH0028` | `teste_renderizador.py` | 4987 |

As classes não existiam no baseline `f00b0bb`.

### 10.2 Métodos pytest-coletáveis (prefixo `test_`)

| Arquivo | Métodos `test_` no baseline | Métodos `test_` no atual | Novos |
|---------|----------------------------|--------------------------|-------|
| `teste_loader.py` | 0 | 6 | +6 |
| `teste_modelo.py` | 0 | 3 | +3 |
| `teste_renderizador.py` | 158 | 166 | +8 |
| **Total** | **158** | **175** | **+17** |

Confirmado: 17 novos métodos `test_` coletados e aprovados pelo pytest (224 - 207 = 17).

### 10.3 Verificações adicionais na execução direta

| Arquivo | Verificações no baseline | Verificações no atual | Novas |
|---------|-------------------------|----------------------|-------|
| `teste_loader.py` | 129 | 172 | +43 |
| `teste_modelo.py` | 81 | 88 | +7 |
| `teste_renderizador.py` | 491 | 504 | +13 |
| `teste_demo.py` | 303 | 303 | 0 |
| `teste_diagnostico.py` | 28 | 28 | 0 |
| `teste_explorar_barra_de_menus.py` | 38 | 38 | 0 |
| **Total** | **1070** | **1133** | **+63** |

### 10.4 Coberturas verificadas (execução direta)

Com base nas classes adicionadas pelo H-0028 e nos resultados das execuções diretas:

- **Loader** (TestValidacaoMatrizH0028): compatibilidade livre/ausente, dimensões válidas, modos igual/percentual/fracao, modos mistos, pesos assimétricos, células fora de ordem, tipos console/lancador/dashboard/grupo, rejeições de schema, dimensão, distribuição, coordenada, duplicidade, referência, cobertura e profundidade. Aprovado: 43 verificações diretas.
- **Modelo** (TestModeloMatrizH0028): transporte de `estrutura` e `matriz` em `_campos_inertes`, preservação sem inferência. Aprovado: 7 verificações diretas.
- **Renderizador** (TestRenderizadorMatrizH0028): alinhamento de cortes compartilhados, restos por eixo, redimensionamento, terminal estreito propagando `RenderizadorErro`. Aprovado: 13 verificações diretas.
- **Regressão de `livre`**: sem falhas nos 303 testes diretos de `teste_demo.py` (que exercita o caminho livre via JSON de produção).

---

## 11. Natureza do comando pytest

O handoff apresenta o comando pytest como **critério obrigatório de aprovação** (seção 26, critério 12): "Suite completa aprovada: todos os testes (anteriores + novos) passam com resultado N/N."

O critério não admite erros de coleta nem exceções documentais. O resultado esperado é explicitamente `N/N` (zero erros, zero falhas).

**Este critério não pode ser satisfeito sem modificar arquivos proibidos** (`teste_demo.py`, `teste_diagnostico.py`) ou sem adicionar configuração pytest (`conftest.py`) fora da lista de arquivos permitidos pelo handoff. As funções `teste_erros`, `teste_tipos_validos` etc. em `teste_loader.py` também precisariam ser renomeadas ou convertidas para usar fixtures reais.

---

## 12. Impacto sobre a implementação

Os 10 erros são **inteiramente pré-existentes** ao H-0028. A implementação:

- Não introduziu nenhum dos 10 erros de coleta.
- Não alterou nenhuma das funções afetadas.
- Adicionou 17 novos métodos `test_` que o pytest coleta e executa sem erros.
- Adicionou 63 verificações diretas que passam com código de saída 0.
- Preservou os 1070 testes do baseline (1133 - 63 = 1070).
- Não introduziu nenhuma falha em nenhum arquivo.

O critério 12 da seção 26 do handoff especifica `N/N`, mas o baseline já não satisfazia esse critério com o mesmo comando pytest. A falha no critério 12 é uma propriedade estrutural do harness legado, não um defeito da implementação H-0028.

---

## 13. Atualização do IMP-0029

O arquivo `IMP-0029-matriz-de-grupos-coordenadas-explicitas.md` foi atualizado com a seção "Evidência complementar de testes", adicionando os fatos comprovados nesta etapa.

Status do IMP-0029 atualizado de `IMPLEMENTATION_INCOMPLETE` para `IMPLEMENTATION_COMPLETED` (com ressalva explícita de que `QA_IMPLEMENTACAO` ainda está pendente).

---

## 14. Resíduos mecânicos

O diretório `scripts/.pytest_cache/` existia e foi criado/atualizado pelas execuções de pytest deste ciclo de investigação (e do ciclo de implementação anterior). Confirmado como resíduo mecânico e removido:

```bash
rm -rf -- scripts/.pytest_cache
```

O diretório `scripts/tela/__pycache__/` foi preservado (já existia como não rastreado antes deste ciclo e não é de responsabilidade desta etapa).

---

## 15. Estado Git final

```text
git status --short:
 M scripts/docs/NOMENCLATURA.md
 M scripts/docs/adr/INDICE_ADR.md
 M scripts/docs/contratos/contrato_composicao_corpo.md
 M scripts/docs/contratos/contrato_json_tela_minima.md
 M scripts/docs/contratos/contrato_tela_json.md
 M scripts/tela/loader.py
 M scripts/tela/renderizador.py
 M scripts/tela/teste_loader.py
 M scripts/tela/teste_modelo.py
 M scripts/tela/teste_renderizador.py
?? scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md
?? scripts/docs/handoff/H-0028-matriz-de-grupos-coordenadas-explicitas.md
?? scripts/docs/relatorios/IMP-0029-matriz-de-grupos-coordenadas-explicitas.md
?? scripts/docs/relatorios/RELATORIO_APLICACAO_ADR-0020.md
?? scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md
?? scripts/docs/relatorios/RELATORIO_QA_ADR-0020.md
?? scripts/docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0020.md
?? scripts/docs/relatorios/RELATORIO_QA_H-0028_HANDOFF.md
?? scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0020.md
?? scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md
?? scripts/docs/relatorios/RELATORIO_RESOLUCAO_EVIDENCIA_TESTES_H-0028.md
?? scripts/tela/__pycache__/

Stage: vazio
Nenhum commit criado.
git diff --check: sem saída.
git diff --cached --check: sem saída.
scripts/.pytest_cache: ausente.
scripts/tela/__pycache__/: preservado.
```

Nenhum código foi alterado nesta etapa. Apenas o IMP-0029 foi atualizado (arquivo já existente) e o relatório de resolução foi criado (arquivo novo). Ambos são documentos, não código.

---

## 16. Status final

```text
HANDOFF_TEST_COMMAND_PATCH_REQUIRED
```

**Justificativa**: Os 10 erros existem identicamente no baseline `f00b0bb` e no estado atual. Nenhum foi introduzido pelo H-0028. A causa é estrutural: funções nomeadas com prefixo `teste_` que recebem argumentos posicionais (fornecidos pelo executor interno `main()`) são coletadas indevidamente pelo pytest como funções de teste com fixtures ausentes. O handoff apresenta o resultado `N/N` do comando pytest como critério obrigatório de aprovação (critério 12, seção 26), que não pode ser satisfeito sem modificar arquivos proibidos neste ciclo.

---

## 17. Próxima categoria processual

```text
PATCH_HANDOFF
```

O patch deverá corrigir somente a definição da evidência de testes no handoff H-0028, sem alterar código nem testes. As opções prováveis são:

1. Excluir `teste_demo.py` e `teste_diagnostico.py` do comando pytest (esses arquivos contêm funções com parâmetros não-fixture);
2. Substituir o critério "N/N" por "N passed, 10 errors" documentados como pré-existentes;
3. Reformular o critério 12 para referenciar as execuções diretas como evidência canônica, e o pytest como verificação complementar sem exigência de zero erros.

O patch não deve alterar código, testes, ADRs nem contratos.
