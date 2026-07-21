---
name: H-0038-adocao-pytest-padrao-unico-testes
description: Adoção de pytest como padrão único e canônico de execução da suíte de testes — configuração mínima, correção do erro legado e eliminação dos warnings de retorno não-None
metadata:
  type: handoff_implementacao
  status: AGUARDANDO_QA
  id: H-0038
  data_criacao: "2026-07-21"
rastreabilidade:
  decisao_origem: USUARIO
  relatorios_autoridade:
    - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL.md
    - docs/relatorios/RELATORIO_ORIGEM_ERROS_PYTEST_LEGADO.md
  handoffs_anteriores:
    - docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md
---

# H-0038 — Adoção de pytest como padrão único de testes

## 1. Identificação

| Campo | Valor |
|---|---|
| Handoff | H-0038 |
| Título | Adoção de pytest como padrão único e canônico de execução da suíte de testes |
| Arquivo | `docs/handoff/H-0038-adocao-pytest-padrao-unico-testes.md` |
| Data de criação | 2026-07-21 |
| Último ciclo funcional relacionado | H-0037 / commit `c90349c` |
| HEAD de partida | `23f49d0` — `docs: aplica nomenclatura modular e leitura seletiva` |
| Último ciclo concluído | ADR-0029 |

---

## 2. Origem semântica da decisão do usuário

```yaml
decisao:
  origem: USUARIO
  padrao_unico_de_testes: pytest
  comando_canonico: python -m pytest
  forma_recomendada: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  execucao_direta_dos_scripts: deixa_de_ser_padrao_canonico
  objetivo:
    - manter um único modo oficial de executar os testes
    - preservar a cobertura e os comportamentos atualmente verificados
    - permitir descoberta e execução automática da suíte
```

A escolha entre execução direta e `pytest` está encerrada. Este handoff
não reabre essa decisão.

---

## 3. Estado material de partida

> **Nota:** O estado Git descrito nesta seção representa o workspace
> **antes da criação deste handoff** (`ESTADO_HISTORICO_ANTES_DA_CRIACAO_DO_HANDOFF`).
> Não deve ser usado como ponto de partida pela futura implementação.
> A regra para o estado de partida real está na seção 3.1.

```yaml
rotulo: ESTADO_HISTORICO_ANTES_DA_CRIACAO_DO_HANDOFF
branch: master
HEAD: 23f49d0 docs: aplica nomenclatura modular e leitura seletiva
stage: VAZIO
workspace: COM_DOIS_ARQUIVOS_NAO_RASTREADOS
arquivos_nao_rastreados:
  - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_PENDENCIAS_CONSOLE_PROCESSO_E_PROMPTS.md

suite_direta_atual:
  scripts: 10
  verificacoes: 2778
  aprovadas: 2778
  falhas: 0
  erros: 0
  status: VERDE

pytest_padrao_atual:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  itens_coletados: 0
  codigo_de_saida: 5
  causa: ausencia de configuracao — pytest nao localiza teste_*.py por padrao

pytest_explicito_atual:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest <10 arquivos>
  itens_coletados: 422
  aprovados: 421
  erros: 1
  warnings: 7
  codigo_de_saida: 1

erro_atual:
  arquivo: demo/teste_diagnostico.py
  objeto: demo/teste_diagnostico.py::teste_modo_executavel
  tipo: ERROR (setup)
  mensagem: "fixture 'resultado_esperado' not found"
  causa: parametro posicional nao definido como fixture pytest
  origem: LEGADA_COMPROVADA (commit 54e85090, 2026-07-07)

warnings_atuais:
  categoria: PytestReturnNotNoneWarning
  quantidade: 7
  objetos:
    - tela/teste_loader.py::teste_caminho_feliz
    - tela/teste_modelo.py::teste_modelo_orquestrador
    - tela/teste_renderizador.py::teste_renderizador_orquestrador
    - tela/teste_renderizador.py::teste_renderizador_destino_minimo
    - tela/teste_renderizador.py::teste_renderizador_grupo_minimo
    - demo/teste_diagnostico.py::teste_invariantes_anteriores
    - demo/teste_diagnostico.py::teste_gerar_diagnostico

configuracao_pytest:
  pytest_ini: AUSENTE
  pyproject_toml: AUSENTE
  conftest_py: AUSENTE
  setup_cfg: AUSENTE
  tox_ini: AUSENTE
```

### 3.1 Regra para a futura implementação

```yaml
estado_inicial_da_implementacao:
  fonte: observacao_git_real_no_inicio_da_etapa
  nao_presumir:
    - mesma_quantidade_de_arquivos_nao_rastreados_da_criacao_do_handoff
  obrigatorio:
    - preservar handoff
    - preservar levantamentos
    - preservar relatorios_de_QA
    - manter stage vazio
```

O estado real no início da implementação incluirá este handoff, os relatórios de
levantamento e o relatório de QA como arquivos não rastreados. A quantidade exata
de arquivos não rastreados deve ser observada pelo executor, não presumida.

---

## 4. Objetivo desta implementação

Transformar a suíte atual em suíte executável por:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

Esse comando deve:

* localizar automaticamente toda a suíte oficial, sem listagem manual de arquivos;
* executar os testes sem necessidade de listar arquivos manualmente;
* retornar código de saída zero quando todos os testes passarem;
* retornar código diferente de zero diante de falha ou erro;
* substituir a execução direta dos dez scripts como gate canônico;
* preservar a cobertura material existente.

---

## 5. Escopo positivo

A implementação está autorizada a:

1. criar `pytest.ini` com a configuração mínima necessária para descoberta automática;
2. adaptar os arquivos de teste classificados como `modificar` ao padrão único;
3. corrigir o erro legado de `resultado_esperado` em `demo/teste_diagnostico.py`;
4. eliminar retornos de valor não-`None` em funções coletadas como testes pytest;
5. reorganizar a passagem de dados entre funções de teste quando necessário para
   eliminar dependências incompatíveis com pytest (parâmetros posicionais não fixture);
6. preservar as verificações e invariantes atualmente exercitados;
7. manter nomes e estrutura legíveis e rastreáveis;
8. atualizar `docs/contratos/contrato_processo_desenvolvimento.md` para declarar
   formalmente `python -m pytest` como comando canônico;
9. criar o relatório de implementação indicado na seção 11.

---

## 6. Escopo negativo

Este handoff não autoriza:

* alteração de comportamento funcional do Orquestrador;
* redução deliberada da cobertura atual;
* exclusão de testes apenas para obter resultado verde;
* marcação indiscriminada com `skip` ou `xfail`;
* supressão genérica de warnings sem corrigir sua causa;
* manutenção de dois padrões oficiais paralelos após a implementação;
* criação de nova arquitetura de aplicação;
* alteração de contratos funcionais não relacionados aos testes;
* mudança de comportamento visual;
* validação manual de interface;
* stage, commit ou push.

---

## 7. Arquivos autorizados

### 7.1 Arquivos de teste — classificação por inspeção material

Cada arquivo foi inspecionado com base no levantamento de compatibilidade
(`RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL.md`).

#### `demo/teste_diagnostico.py`

```yaml
classificacao: modificar
motivo:
  - teste_modo_executavel(resultado_esperado): parametro posicional sem fixture pytest
    provoca ERROR de setup (fixture 'resultado_esperado' not found); funcao deve ser
    refatorada para calcular resultado_esperado internamente via gerar_diagnostico_tela()
  - teste_invariantes_anteriores(): retorna todos_ok (bool) — PytestReturnNotNoneWarning
  - teste_gerar_diagnostico(): retorna resultado (str) — PytestReturnNotNoneWarning
    e seu retorno e usado por main() para passar a teste_modo_executavel()
alteracoes_autorizadas:
  - remover parametro resultado_esperado de teste_modo_executavel()
  - fazer teste_modo_executavel() computar gerar_diagnostico_tela() internamente
  - remover return todos_ok de teste_invariantes_anteriores()
  - remover return resultado de teste_gerar_diagnostico()
  - atualizar main() para chamar as funcoes sem capturar retorno
restricoes:
  - preservar todas as verificacoes e seus criterios
  - nao alterar comportamento dos testes
  - nao alterar logica de subprocess ou comparacao de stdout
```

#### `tela/teste_loader.py`

```yaml
classificacao: modificar
motivo:
  - teste_caminho_feliz(): retorna tela (dict) — PytestReturnNotNoneWarning
  - o retorno e capturado em main() como tela_real e usado apenas para
    impressao diagnostica (nao para logica de teste subsequente)
alteracoes_autorizadas:
  - remover return tela do final de teste_caminho_feliz()
  - atualizar main() para nao capturar o retorno de teste_caminho_feliz()
    e nao depender de tela_real para a impressao diagnostica (omitir o bloco
    de impressao ou chamar carregar_tela() diretamente em main() se necessario)
restricoes:
  - preservar todas as verificacoes internas de teste_caminho_feliz()
  - nao alterar comportamento das outras funcoes de teste
```

#### `tela/teste_modelo.py`

```yaml
classificacao: modificar
motivo:
  - teste_modelo_orquestrador(): retorna modelo (ModeloTela) — PytestReturnNotNoneWarning
  - o retorno e capturado em main() como modelo mas nao e usado apos a atribuicao
    (as chamadas subsequentes em main() sao independentes)
alteracoes_autorizadas:
  - remover return modelo do final de teste_modelo_orquestrador()
  - alterar main() para chamar teste_modelo_orquestrador() sem capturar retorno
restricoes:
  - preservar todas as verificacoes internas de teste_modelo_orquestrador()
  - nao alterar comportamento das outras funcoes de teste
```

#### `tela/teste_renderizador.py`

```yaml
classificacao: modificar
motivo:
  - teste_renderizador_orquestrador(): retorna modelo (ModeloTela) — PytestReturnNotNoneWarning
  - teste_renderizador_destino_minimo(): retorna modelo (ModeloTela) — PytestReturnNotNoneWarning
  - teste_renderizador_grupo_minimo(): retorna modelo (ModeloTela) — PytestReturnNotNoneWarning
  - em main() nenhum desses retornos e capturado; os valores nao sao usados
alteracoes_autorizadas:
  - remover return modelo do final de teste_renderizador_orquestrador()
  - remover return modelo do final de teste_renderizador_destino_minimo()
  - remover return modelo do final de teste_renderizador_grupo_minimo()
  - nenhuma alteracao necessaria em main()
restricoes:
  - preservar todas as verificacoes internas das tres funcoes
  - nao alterar comportamento das outras funcoes de teste
```

#### `tela/teste_distribuicao_matricial.py`

```yaml
classificacao: preservar_sem_alteracao
motivo: compativel com pytest na coleta explicita (25 itens, 0 erros, 0 warnings de retorno)
```

#### `demo/teste_demo.py`

```yaml
classificacao: preservar_sem_alteracao
motivo: ja define fixture pytest (@pytest.fixture name="modelo") e e compativel
        na coleta explicita (15 itens, 0 erros, 0 warnings de retorno)
```

#### `demo/teste_demo_console.py`

```yaml
classificacao: preservar_sem_alteracao
motivo: compativel com pytest na coleta explicita (6 itens, 0 erros, 0 warnings)
```

#### `demo/teste_demo_console_modos.py`

```yaml
classificacao: preservar_sem_alteracao
motivo: compativel com pytest na coleta explicita (11 itens, 0 erros, 0 warnings)
```

#### `demo/teste_demo_distribuicao.py`

```yaml
classificacao: preservar_sem_alteracao
motivo: compativel com pytest na coleta explicita (14 itens, 0 erros, 0 warnings)
```

#### `demo/teste_explorar_barra_de_menus.py`

```yaml
classificacao: preservar_sem_alteracao
motivo: compativel com pytest na coleta explicita (19 itens, 0 erros, 0 warnings);
        a conversao de falhas internas em falhas pytest e provida por conftest.py
        (secao 7.4), sem necessidade de alteracao individual no arquivo
```

---

### 7.1.2 Inventário de mecanismo de registro por arquivo

Todos os dez arquivos da suíte usam o padrão `_registrar()` → `_RESULTADOS` → `main()`:
verificações internas chamam `_registrar(nome, passou)`, que apenas acumula em
`_RESULTADOS`; `main()` itera `_RESULTADOS`, conta falhas e retorna código 1 se
houver alguma. O pytest coleta e executa as funções diretamente, sem chamar `main()`.
Uma verificação registrada como falsa não produz falha de item pytest sem mecanismo
adicional.

O mecanismo escolhido para converter `_registrar(False)` em falha pytest é um
fixture `autouse` em `conftest.py` (seção 7.4), que limpa `_RESULTADOS` do módulo
antes de cada teste e verifica `_RESULTADOS` após a execução, levantando
`AssertionError` se houver entradas falsas. Os quatro arquivos classificados como
`MODIFICAR` também dependem deste mecanismo, além de suas alterações individuais.

```yaml
tela/teste_loader.py:
  usa_registro_interno_de_resultados: sim
  depende_de_main_para_codigo_de_falha: sim
  falha_interna_ja_reprova_no_pytest: nao
  classificacao: MODIFICAR
  justificativa: warning PytestReturnNotNoneWarning em teste_caminho_feliz(); mecanismo
    de conversao de falhas internas provido por conftest.py

tela/teste_modelo.py:
  usa_registro_interno_de_resultados: sim
  depende_de_main_para_codigo_de_falha: sim
  falha_interna_ja_reprova_no_pytest: nao
  classificacao: MODIFICAR
  justificativa: warning PytestReturnNotNoneWarning em teste_modelo_orquestrador(); mecanismo
    de conversao de falhas internas provido por conftest.py

tela/teste_renderizador.py:
  usa_registro_interno_de_resultados: sim
  depende_de_main_para_codigo_de_falha: sim
  falha_interna_ja_reprova_no_pytest: nao
  classificacao: MODIFICAR
  justificativa: 3 warnings PytestReturnNotNoneWarning; mecanismo de conversao de
    falhas internas provido por conftest.py

tela/teste_distribuicao_matricial.py:
  usa_registro_interno_de_resultados: sim
  depende_de_main_para_codigo_de_falha: sim
  falha_interna_ja_reprova_no_pytest: nao
  classificacao: PRESERVAR_SEM_ALTERACAO
  justificativa: sem erros e sem warnings; mecanismo de conversao de falhas internas
    provido centralmente por conftest.py; nenhuma alteracao individual necessaria

demo/teste_diagnostico.py:
  usa_registro_interno_de_resultados: sim
  depende_de_main_para_codigo_de_falha: sim
  falha_interna_ja_reprova_no_pytest: nao
  classificacao: MODIFICAR
  justificativa: erro legado de fixture resultado_esperado + 2 warnings PytestReturnNotNoneWarning
    + dependencia de main(); requer alteracoes individuais; mecanismo de conversao
    de falhas internas provido por conftest.py

demo/teste_demo.py:
  usa_registro_interno_de_resultados: sim
  depende_de_main_para_codigo_de_falha: sim
  falha_interna_ja_reprova_no_pytest: nao
  classificacao: PRESERVAR_SEM_ALTERACAO
  justificativa: sem erros e sem warnings; fixture pytest para modelo ja existente;
    mecanismo de conversao de falhas internas provido centralmente por conftest.py

demo/teste_demo_console.py:
  usa_registro_interno_de_resultados: sim
  depende_de_main_para_codigo_de_falha: sim
  falha_interna_ja_reprova_no_pytest: nao
  classificacao: PRESERVAR_SEM_ALTERACAO
  justificativa: sem erros e sem warnings; mecanismo de conversao de falhas internas
    provido centralmente por conftest.py; nenhuma alteracao individual necessaria

demo/teste_demo_console_modos.py:
  usa_registro_interno_de_resultados: sim
  depende_de_main_para_codigo_de_falha: sim
  falha_interna_ja_reprova_no_pytest: nao
  classificacao: PRESERVAR_SEM_ALTERACAO
  justificativa: sem erros e sem warnings; mecanismo de conversao de falhas internas
    provido centralmente por conftest.py; nenhuma alteracao individual necessaria

demo/teste_demo_distribuicao.py:
  usa_registro_interno_de_resultados: sim
  depende_de_main_para_codigo_de_falha: sim
  falha_interna_ja_reprova_no_pytest: nao
  classificacao: PRESERVAR_SEM_ALTERACAO
  justificativa: sem erros e sem warnings; mecanismo de conversao de falhas internas
    provido centralmente por conftest.py; nenhuma alteracao individual necessaria

demo/teste_explorar_barra_de_menus.py:
  usa_registro_interno_de_resultados: sim
  depende_de_main_para_codigo_de_falha: sim
  falha_interna_ja_reprova_no_pytest: nao
  classificacao: PRESERVAR_SEM_ALTERACAO
  justificativa: sem erros e sem warnings; mecanismo de conversao de falhas internas
    provido centralmente por conftest.py; nenhuma alteracao individual necessaria
```

**Regra de falha para implementação:**

Toda chamada equivalente a `_registrar(nome, passou)` deve produzir uma falha real
de item pytest quando `passou` for falso. A implementação deve:

1. inventariar, nos dez arquivos, todos os mecanismos de registro ou consolidação de
   resultados;
2. identificar quais dependem de `_RESULTADOS`, `main()` ou código de saída da
   execução direta;
3. implementar o mecanismo conftest.py descrito na seção 7.4, que converte resultados
   falsos em falha do pytest;
4. garantir que a reprovação ocorra durante a execução coletada pelo pytest, sem
   depender do bloco `if __name__ == "__main__"`;
5. não eliminar verificações para obter resultado verde;
6. provar o comportamento com uma falha temporária controlada (seção 10, item 3).

O mecanismo deve preservar a execução das demais verificações do mesmo grupo sempre
que possível, evitando interromper a cobertura no primeiro resultado falso.

O mecanismo escolhido deve ser descrito no relatório de implementação (seção 12).

---

### 7.2 Configuração do pytest — escolha canônica

**Arquivo escolhido:** `pytest.ini`

**Justificativa:**

`pytest.ini` é o arquivo de configuração mais focado e semanticamente restrito ao
pytest. Ele não introduz semântica de build-system, não implica empacotamento Python
e não requer declaração de `[build-system]`. O projeto não possui qualquer uso atual
ou previsto para `pyproject.toml` além do pytest; criar `pyproject.toml` apenas para
configurar o pytest adicionaria semântica de infraestrutura sem necessidade comprovada.

`pytest.ini` é a escolha tecnicamente mínima e semanticamente correta para este escopo.

**Arquivo a criar:** `pytest.ini` (na raiz do repositório)

**Conteúdo mínimo necessário:**

```ini
[pytest]
python_files = teste_*.py
testpaths = tela demo
```

**Justificativa do conteúdo:**

- `python_files = teste_*.py`: o padrão de descoberta padrão do pytest é `test_*.py`
  e `*_test.py`; os dez scripts usam o prefixo `teste_` (português); sem esta diretiva,
  o pytest coleta zero itens.
- `testpaths = tela demo`: limita a descoberta aos dois diretórios onde os dez scripts
  residem; evita varredura desnecessária de toda a árvore do projeto.

Não autorizar simultaneamente `pytest.ini` e `pyproject.toml` com configurações
equivalentes. Um único arquivo de configuração é suficiente e obrigatório.

---

### 7.3 Documentação — classificação e autoridade permanente

#### `docs/contratos/contrato_processo_desenvolvimento.md`

```yaml
classificacao: modificar
motivo: e o documento de maior autoridade para regras de processo; a definicao do
        comando canonico de testes deve residir aqui para superar qualquer handoff
        por hierarquia documental (secao 3 do proprio contrato)
alteracao_autorizada:
  - adicionar nova secao declarando PYTHONDONTWRITEBYTECODE=1 python -m pytest
    como comando canonico de testes
  - declarar que os dez scripts permanecem executaveis diretamente mas nao
    constituem mais o gate canonico
restricoes:
  - nao alterar secoes existentes de processo, ciclo, papeis ou criterios de aceite
  - nao incluir nova semantica de contrato nao relacionada a testes
```

**Autoridade permanente da suíte canônica:**

`docs/contratos/contrato_processo_desenvolvimento.md` é o documento que será a
autoridade permanente para a definição da suíte canônica e do comando canônico de
testes. Contratos têm hierarquia superior a handoffs (seção 3 do contrato de processo).
Uma vez que o contrato declare `python -m pytest` como canônico, essa declaração
prevalece sobre a definição do H-0037 (seções 23.4 e 31), sem necessidade de alterar
o H-0037 diretamente.

#### `docs/INDICE.md`

```yaml
classificacao: preservar_sem_alteracao
motivo: nao referencia comando canonico de testes; ordem de leitura e estrutura
        esperada sao independentes desta mudanca
```

#### `docs/NOMENCLATURA.md`

```yaml
classificacao: preservar_sem_alteracao
motivo: fachada permanente de navegacao terminologica; nao normativa para testes
```

#### `docs/nomenclatura/00_INDICE.md`

```yaml
classificacao: preservar_sem_alteracao
motivo: indice modular de terminologia; nao normativo para politica de testes
```

---

### 7.4 Mecanismo compartilhado de conversão de falhas — `conftest.py`

**Arquivo a criar:** `conftest.py` (na raiz do repositório)

**Justificativa:**

Todos os dez arquivos da suíte usam `_registrar()` → `_RESULTADOS` → `main()` para
consolidar e reportar falhas. O pytest não executa `main()`, portanto verificações
internas registradas como falsas não se convertem automaticamente em falhas de item
pytest. Um fixture `autouse` em `conftest.py` resolve esse problema de forma
centralizada, sem exigir alteração individual em cada arquivo.

**Comportamento exigido do fixture:**

```yaml
nome_do_fixture: verificar_resultados_internos
escopo: function
autouse: true
operacoes:
  antes_do_teste:
    - localizar _RESULTADOS no modulo do teste
    - limpar _RESULTADOS (garantir isolamento entre funcoes de teste)
  apos_o_teste:
    - inspecionar _RESULTADOS do modulo
    - se houver entradas com passou == False:
        levantar AssertionError com lista dos nomes das verificacoes que falharam
    - se _RESULTADOS estiver vazio ou todas as entradas forem True:
        nao levantar excecao
comportamento_de_continuidade:
  - o fixture nao interrompe verificacoes durante a execucao da funcao de teste
  - apenas verifica o acumulado apos o retorno da funcao
  - preserva a semantica de executar todas as verificacoes do grupo antes de reprovar
```

**Restrições:**

```yaml
restricoes:
  - nao alterar a logica interna de _registrar() nos arquivos de teste
  - o conftest.py nao deve exigir alteracoes adicionais nas assinaturas das funcoes de teste, alem da remocao de resultado_esperado ja autorizada em demo/teste_diagnostico.py
  - nao introduzir dependencias de modulos externos alem de pytest
  - conftest.py deve ser o unico arquivo de configuracao compartilhada desta natureza
  - nenhuma outra politica funcional deve ser adicionada ao conftest.py nesta etapa
```

**Autorização formal:**

```yaml
conftest.py:
  classificacao: criar
  local: raiz do repositorio
  motivo: mecanismo compartilhado e unico para conversao de _registrar(False) em
          falha pytest; cobre todos os dez arquivos da suite sem alteracao individual
          nos seis arquivos classificados como preservar_sem_alteracao
  escopo_exato: fixture autouse de escopo function que limpa e verifica _RESULTADOS
  nova_semantica: false
```

---

## 8. Preservação da cobertura

### 8.1 Natureza das grandezas

As grandezas a seguir representam estruturas diferentes e não são equivalentes:

```yaml
verificacoes_diretas: 2778
  significado: afirmacoes internas (_registrar) executadas pelos 10 scripts diretamente
  medida: contagem de chamadas a _registrar() por cada script

itens_pytest_explicito: 422
  significado: funcoes prefixadas com teste_ coletadas pelo pytest explicitamente
  medida: contagem de itens por arquivo na coleta pytest
```

A migração não exige correspondência numérica direta entre 2778 e 422.

### 8.2 Critério obrigatório de preservação

A implementação deve preservar materialmente:

* comportamentos verificados (o quê é verificado);
* casos positivos (caminhos felizes);
* casos negativos (rejeições, erros esperados);
* rejeições e invariantes;
* regressões dos ciclos anteriores;
* cenários cobertos pelos dez scripts da suíte atual.

### 8.3 Matriz de rastreabilidade exigida no relatório

O relatório de implementação deve registrar:

| Script anterior | Verificações ou grupos preservados | Testes pytest correspondentes | Alteração de cobertura |
|---|---|---|---|
| `tela/teste_loader.py` | a preencher | a preencher | a preencher |
| `tela/teste_modelo.py` | a preencher | a preencher | a preencher |
| `tela/teste_renderizador.py` | a preencher | a preencher | a preencher |
| `tela/teste_distribuicao_matricial.py` | a preencher | a preencher | a preencher |
| `demo/teste_diagnostico.py` | a preencher | a preencher | a preencher |
| `demo/teste_demo.py` | a preencher | a preencher | a preencher |
| `demo/teste_demo_console.py` | a preencher | a preencher | a preencher |
| `demo/teste_demo_console_modos.py` | a preencher | a preencher | a preencher |
| `demo/teste_demo_distribuicao.py` | a preencher | a preencher | a preencher |
| `demo/teste_explorar_barra_de_menus.py` | a preencher | a preencher | a preencher |

Qualquer redução deve ser explicitamente registrada. Redução sem autorização posterior
do usuário constitui violação deste handoff.

---

## 9. Critérios de aceite

```yaml
CA-01:
  descricao: comando canonico retorna codigo 0
  verificacao: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  resultado_esperado:
    - codigo de saida 0
    - codigo zero somente e valido quando:
        - nenhum item pytest for marcado como failed ou error
        - nenhuma verificacao interna tiver sido registrada como falsa
          (conftest.py nao levantou AssertionError em nenhum item)
        - a matriz de cobertura demonstrar que os mecanismos anteriores
          de reprovacao foram preservados

CA-02:
  descricao: descoberta automatica sem listagem manual
  verificacao: PYTHONDONTWRITEBYTECODE=1 python -m pytest --collect-only
  resultado_esperado:
    - 10 arquivos coletados automaticamente
    - zero arquivos especificados manualmente na linha de comando

CA-03:
  descricao: nenhuma falha
  verificacao: saida do pytest
  resultado_esperado:
    - 0 failed na saida do pytest
    - 0 AssertionError levantados pelo fixture conftest.py
    - codigo zero somente quando nao houver falhas internas nem falhas pytest

CA-04:
  descricao: nenhum erro
  verificacao: saida do pytest
  resultado_esperado: 0 errors

CA-05:
  descricao: ausencia de PytestReturnNotNoneWarning do projeto
  verificacao: saida do pytest
  resultado_esperado: 0 PytestReturnNotNoneWarning produzidos pelos testes do projeto

CA-06:
  descricao: ausencia do erro resultado_esperado
  verificacao: saida do pytest
  resultado_esperado: fixture 'resultado_esperado' not found ausente

CA-07:
  descricao: padrao unico confirmado
  verificacao: documental
  resultado_esperado:
    - execucao direta nao figura mais como gate canonico
    - contrato_processo_desenvolvimento.md declara python -m pytest como canonico

CA-08:
  descricao: cobertura material sem regressao comprovada
  verificacao: matriz de rastreabilidade no relatorio de implementacao
  resultado_esperado:
    - nenhuma reducao de cobertura material comprovada
    - codigo zero somente quando a matriz demonstrar que os mecanismos de reprovacao
      dos dez arquivos foram preservados sob o novo gate canonico
    - mecanismo conftest.py confirmado como operacional pelo procedimento de prova
      negativa (secao 10, item 3)

CA-09:
  descricao: stage vazio ao encerrar
  verificacao: git diff --cached --name-only
  resultado_esperado: saida vazia

CA-10:
  descricao: inventario de coleta controlado
  verificacao:
    - gerar a lista completa de node IDs com pytest --collect-only
    - consolidar quantidade por arquivo e por classe
    - comparar com o inventario aprovado no relatorio de implementacao
  resultado_esperado:
    - os dez arquivos oficiais sao coletados
    - funcoes teste_* reais permanecem coletadas
    - metodos test_* em classes Test* reais permanecem coletados
    - parametrizacoes e fixtures legitimas permanecem coletadas
    - funcoes auxiliares que nao sao testes nao aparecem como node IDs
    - qualquer mudanca em relacao aos 422 itens iniciais possui justificativa
      e rastreabilidade no relatorio de implementacao

CA-FALHA-INTERNA-01:
  descricao: resultado falso registrado reprova o pytest
  resultado_esperado:
    - pelo menos uma verificacao controlada registrada como falsa
    - item pytest correspondente marcado como failed ou error
    - comando retorna codigo diferente de zero

CA-FALHA-INTERNA-02:
  descricao: resultado verdadeiro registrado permanece aprovado
  resultado_esperado:
    - nenhuma falha pytest produzida pelas verificacoes verdadeiras

CA-FALHA-INTERNA-03:
  descricao: main nao participa do gate canonico
  resultado_esperado:
    - a reprovacao ocorre durante a execucao coletada pelo pytest
    - nenhuma dependencia do bloco if __name__ == "__main__"
```

**Baseline de contagens para CA-10:**

```yaml
baseline_itens_por_arquivo:
  tela/teste_loader.py: 19
  tela/teste_modelo.py: 15
  tela/teste_renderizador.py: 292
  tela/teste_distribuicao_matricial.py: 25
  demo/teste_diagnostico.py: 6
  demo/teste_demo.py: 15
  demo/teste_demo_console.py: 6
  demo/teste_demo_console_modos.py: 11
  demo/teste_demo_distribuicao.py: 14
  demo/teste_explorar_barra_de_menus.py: 19
  total_inicial: 422
nota: a contagem final nao precisa ser exatamente 422, mas qualquer alteracao
      deve ser explicada e rastreada no relatorio de implementacao
```

**Separação obrigatória de warnings:**

Warnings externos de plugins (`anyio`, `typeguard`) ou do ambiente Python devem ser
separados dos warnings produzidos pelos testes do projeto. O CA-05 aplica-se somente
aos warnings produzidos pelos arquivos de teste do projeto.

---

## 10. Testes da futura implementação

A implementação deve executar e registrar:

1. **Execução canônica completa:**
   ```bash
   PYTHONDONTWRITEBYTECODE=1 python -m pytest
   ```
   Confirmar código de saída 0 e ausência de erros e warnings do projeto.

2. **Confirmação de descoberta automática:**
   ```bash
   PYTHONDONTWRITEBYTECODE=1 python -m pytest --collect-only
   ```
   Confirmar que os dez arquivos aparecem sem listagem manual.

3. **Prova negativa — procedimento completo:**

   ```bash
   cd "$(git rev-parse --show-toplevel)"

   arquivo_temporario="tela/teste_h0038_gate_negativo_temporario.py"

   cleanup() {
     rm -f "$arquivo_temporario"
   }
   trap cleanup EXIT

   cat > "$arquivo_temporario" <<'PY'
   _RESULTADOS = []

   def _registrar(nome, passou):
       _RESULTADOS.append((nome, passou))

   def teste_gate_negativo_temporario():
       _registrar("prova negativa controlada do H-0038", False)
   PY

   set +e
   PYTHONDONTWRITEBYTECODE=1 python -m pytest
   codigo=$?
   set -e

   if [ "$codigo" -eq 0 ]; then
     echo "ERRO: o gate retornou zero diante de uma falha proposital" >&2
     exit 1
   fi

   rm -f "$arquivo_temporario"
   trap - EXIT

   test ! -e "$arquivo_temporario"
   git status --short --untracked-files=all
   git diff --cached --name-only
   ```

   O relatório de implementação deve registrar:

   * caminho temporário (`tela/teste_h0038_gate_negativo_temporario.py`);
   * conteúdo exato do arquivo criado;
   * código de saída diferente de zero observado;
   * confirmação de remoção do arquivo temporário;
   * ausência do arquivo no estado Git final (`git status`);
   * stage vazio (`git diff --cached --name-only` sem saída).

   A prova negativa não pode alterar permanentemente nenhum teste, configuração ou
   contrato. O arquivo temporário criado dentro de `tela/` é coletado pelo comando
   canônico (`testpaths = tela demo`), garantindo que a prova teste especificamente a conversão de `_registrar(False)` em falha pelo `conftest.py`.

4. **Testes focais dos arquivos modificados:**
   ```bash
   PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_diagnostico.py
   PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_loader.py
   PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_modelo.py
   PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_renderizador.py
   ```
   Confirmar código 0 e ausência de warnings nos quatro arquivos modificados.

5. **Comparação de cobertura material:**
   Preencher a matriz da seção 8.3.

6. **Confirmação de ausência de coleta acidental:**
   Verificar que funções auxiliares (não testes) não aparecem na listagem de coleta.

7. **Confirmação de ausência de retorno não-None:**
   Confirmar que nenhuma função coletada produz `PytestReturnNotNoneWarning`.

8. **Confirmação de ausência do erro resultado_esperado:**
   Confirmar que `fixture 'resultado_esperado' not found` não aparece na saída.

Não exigir que o usuário faça validação manual de lógica interna.

---

## 11. Compatibilidade e transição

```yaml
antes:
  padrao_canonico: execucao_direta_dos_dez_scripts
  comando: PYTHONDONTWRITEBYTECODE=1 python <script>
  gate: execucao de cada script individualmente
  coleta_pytest_padrao: 0 itens, codigo 5

depois:
  padrao_canonico: python_m_pytest
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  gate: execucao unificada com descoberta automatica

compatibilidade:
  comportamentos_testados: preservados
  scripts_diretamente_executaveis:
    status: nao_canonico_mas_permitido
    obrigacao_de_permanecer_funcional: somente_durante_migracao_se_estritamente_necessario
  dois_padroes_oficiais_paralelos:
    status: proibido_apos_implementacao
```

A implementação pode reorganizar internamente os scripts autorizados quando necessário,
desde que preserve a cobertura e permaneça dentro da lista autorizada na seção 7.

---

## 12. Relatório de implementação

**Nome canônico:**

```text
docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0038_PYTEST_PADRAO_UNICO.md
```

O relatório deve registrar:

* arquivos criados, alterados, preservados e não alterados;
* configuração escolhida e conteúdo do `pytest.ini`;
* comandos executados com saídas completas;
* quantidade de itens coletados antes e depois;
* resultados (passed, failed, errors, warnings);
* warnings separados por origem (projeto vs. ambiente);
* matriz de preservação da cobertura (seção 8.3);
* exceções operacionais autorizadas (seção 13), se houver;
* estado Git inicial observado;
* efeito da implementação sobre o workspace;
* estado Git final observado;
* confirmação de stage vazio;
* encerramento `IMPLEMENTATION_COMPLETED_AWAITING_QA`.

---

## 13. Exceção operacional de arquivo

As restrições desta seção são dirigidas à futura implementação.

Se, durante a implementação, um arquivo fora da lista nominal for estritamente
necessário, o executor deve parar antes de alterá-lo e apresentar ao usuário:

```yaml
arquivo:
necessidade:
risco_de_nao_alterar:
escopo_exato:
nova_semantica: true|false
```

Somente após autorização explícita do usuário a alteração pode ocorrer.

A autorização, o arquivo, a justificativa e o escopo devem ser registrados no
relatório de implementação.

Esta exceção não autoriza:

* nova arquitetura;
* novo schema;
* nova política funcional;
* nova semântica de contrato.

---

## 14. Exequibilidade — verificação do autor

| Item | Verificação | Resultado |
|---|---|---|
| Todos os arquivos necessários autorizados ou classificados | 4 testes modificar + 6 preservar + pytest.ini + conftest.py + contrato | CONFIRMADO |
| Arquivo de configuração pytest.ini autorizado | seção 7.2 | CONFIRMADO |
| conftest.py autorizado como mecanismo compartilhado | seção 7.4 | CONFIRMADO |
| Erro legado (resultado_esperado) corrigível dentro da lista | demo/teste_diagnostico.py na lista de modificar | CONFIRMADO |
| 7 warnings corrigíveis dentro da lista | 4 arquivos com warnings todos na lista de modificar | CONFIRMADO |
| Mecanismo de conversão _registrar(False) → falha pytest prescrito | conftest.py fixture autouse (seção 7.4) | CONFIRMADO |
| Testes de aceitação executáveis | pytest disponível (v9.0.3), scripts executáveis diretamente | CONFIRMADO |
| Relatório criável | caminho autorizado na seção 12 | CONFIRMADO |
| Nenhuma proibição torna a implementação impossível | escopo negativo revisado | CONFIRMADO |

A implementação é exequível dentro dos limites definidos por este handoff.

---

## 15. Estado Git

### 15.1 Estado histórico — anterior à criação do handoff

```yaml
rotulo: ESTADO_HISTORICO_ANTES_DA_CRIACAO_DO_HANDOFF
branch: master
HEAD: 23f49d0 docs: aplica nomenclatura modular e leitura seletiva
stage: VAZIO
workspace: COM_DOIS_ARQUIVOS_NAO_RASTREADOS
arquivos_nao_rastreados:
  - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_PENDENCIAS_CONSOLE_PROCESSO_E_PROMPTS.md
```

### 15.2 Efeito da criação do handoff e do QA

```yaml
efeito_real_das_etapas_documentais:
  arquivos_criados:
    - docs/handoff/H-0038-adocao-pytest-padrao-unico-testes.md
    - docs/relatorios/RELATORIO_QA_H-0038_HANDOFF.md
  arquivos_alterados: []
  arquivos_removidos: []
  arquivos_movidos: []
  stage_alterado: nao
```

### 15.3 Estado do workspace na correção do handoff

```yaml
estado_na_correcao_do_handoff:
  stage: VAZIO
  workspace: COM_QUATRO_ARQUIVOS_NAO_RASTREADOS
  arquivos_nao_rastreados:
    - docs/handoff/H-0038-adocao-pytest-padrao-unico-testes.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_PYTEST_ATUAL.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_PENDENCIAS_CONSOLE_PROCESSO_E_PROMPTS.md
    - docs/relatorios/RELATORIO_QA_H-0038_HANDOFF.md
```

### 15.4 Estado inicial esperado para a futura implementação

```yaml
estado_inicial_da_implementacao:
  fonte: observacao_git_real_no_inicio_da_etapa
  nao_presumir:
    - mesma_quantidade_de_arquivos_nao_rastreados_do_estado_15_3
  obrigatorio:
    - preservar handoff
    - preservar levantamentos
    - preservar relatorios_de_QA
    - manter stage vazio
```

---

## 16. Encerramento

```text
HANDOFF_CORRIGIDO_AGUARDANDO_NOVO_QA
```
