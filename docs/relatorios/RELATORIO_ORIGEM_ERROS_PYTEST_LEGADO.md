# RELATORIO_ORIGEM_ERROS_PYTEST_LEGADO

## 1. Identificação

- etapa: `INVESTIGAR_ORIGEM_ERROS_PYTEST_LEGADO`
- papel: Investigador histórico de Git e testes
- raiz Git: `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`
- branch: `master`
- HEAD: `f00b0bb` (Baseline)
- intervalo histórico investigado: de `0c98fa1` (INICIO) até `f00b0bb` (Baseline)

## 2. Problema

A execução complementar do comando de suíte completa exigido originalmente pelo handoff H-0028 (`python3 -m pytest ...` executado a partir do diretório `scripts/`) terminou com 10 erros de coleta automática. O objetivo desta investigação histórica é determinar:
1. Quando as funções coletadas com erro foram introduzidas no repositório;
2. Se essas funções nasceram incompatíveis com a coleta automática do `pytest`;
3. Se existiam fixtures ou configurações que davam suporte a elas e foram removidas posteriormente;
4. Qual o primeiro commit em que os erros apareceram no pytest;
5. Se houve perda histórica de compatibilidade no código ou se o comando `pytest` nunca foi uma suíte válida para esses arquivos de teste baseados em execução direta.

## 3. Estado já comprovado

O levantamento e a investigação anteriores do ciclo H-0028 comprovaram o seguinte estado:
- **Baseline (`f00b0bb`)**: `207 passed, 10 errors`, código de saída 1.
- **Implementação atual (IMP-0029)**: `224 passed, 10 errors`, código de saída 1.
- **Diferença de erros**: 0 erros adicionais introduzidos pelo H-0028/IMP-0029. Os mesmos 10 node IDs de erros de coleta, nas mesmas linhas e mesmos arquivos.
- **Execução direta (Suíte canônica)**:
  - Baseline completo: `1070/1070` testes passando (código de saída 0 em todos os 6 arquivos).
  - Atual completo: `1133/1133` testes passando (código de saída 0 em todos os 6 arquivos).
- **Fixtures ausentes identificadas**: `tmp_base` (6 erros no loader), `modelo` (3 erros no demo) e `resultado_esperado` (1 erro no diagnóstico).

## 4. Dez erros investigados

Abaixo está o mapeamento detalhado dos dez erros de coleta identificados e analisados:

| Nº | Node ID | Arquivo | Função | Parâmetro interpretado como fixture | Fixture ausente | Ocorrências |
| -: | :--- | :--- | :--- | :--- | :--- | :---: |
| 1 | `tela/teste_loader.py::teste_erros` | `scripts/tela/teste_loader.py` | `teste_erros` | `tmp_base` | `tmp_base` | 1 |
| 2 | `tela/teste_loader.py::teste_tipos_validos` | `scripts/tela/teste_loader.py` | `teste_tipos_validos` | `tmp_base` | `tmp_base` | 1 |
| 3 | `tela/teste_loader.py::teste_grupo_estrutural` | `scripts/tela/teste_loader.py` | `teste_grupo_estrutural` | `tmp_base` | `tmp_base` | 1 |
| 4 | `tela/teste_loader.py::teste_arranjo_corpo_h0019` | `scripts/tela/teste_loader.py` | `teste_arranjo_corpo_h0019` | `tmp_base` | `tmp_base` | 1 |
| 5 | `tela/teste_loader.py::teste_distribuicao_corpo_h0025` | `scripts/tela/teste_loader.py` | `teste_distribuicao_corpo_h0025` | `tmp_base` | `tmp_base` | 1 |
| 6 | `tela/teste_loader.py::teste_hierarquia_grupos_adr0019` | `scripts/tela/teste_loader.py` | `teste_hierarquia_grupos_adr0019` | `tmp_base` | `tmp_base` | 1 |
| 7 | `tela/teste_demo.py::teste_navegacao_minima` | `scripts/tela/teste_demo.py` | `teste_navegacao_minima` | `modelo` | `modelo` | 1 |
| 8 | `tela/teste_demo.py::teste_renderizar_estado` | `scripts/tela/teste_demo.py` | `teste_renderizar_estado` | `modelo` | `modelo` | 1 |
| 9 | `tela/teste_demo.py::teste_renderizar_estado_altura` | `scripts/tela/teste_demo.py` | `teste_renderizar_estado_altura` | `modelo` | `modelo` | 1 |
| 10 | `tela/teste_diagnostico.py::teste_modo_executavel` | `scripts/tela/teste_diagnostico.py` | `teste_modo_executavel` | `resultado_esperado` | `resultado_esperado` | 1 |

## 5. Estrutura atual dos testes

A análise estrutural detalhada de cada uma das funções e arquivos de testes afetados revela:
1. **Prefixo**: Todas as funções afetadas começam com o prefixo `teste_` (e não `test_`).
2. **Coleta automática**: O `pytest` em seu comportamento padrão de coleta localiza funções que começam com `test_` ou `teste_` (caso não seja sobrescrito por configurações como `python_functions`). Logo, o pytest tenta coletar todas as dez funções.
3. **Parâmetros posicionais**: Cada uma dessas dez funções recebe exatamente um parâmetro posicional obrigatório (`tmp_base`, `modelo` ou `resultado_esperado`).
4. **Provedor na execução direta**: Na execução direta do script pelo interpretador Python, esses argumentos são gerados dinamicamente e passados de forma posicional manual dentro do ponto de entrada `main()` ou de outra função de teste.
5. **Rotina main/Executor interno**: Cada um dos arquivos possui uma função `main()` que atua como executor próprio e manual, registrando resultados detalhados de aprovação e falha em uma lista global chamada `_RESULTADOS`.
6. **Fixture real existente**: Não há nenhuma fixture pytest com esses nomes definida em nenhum lugar do repositório.
7. **Helper projetado**: Essas funções foram estruturadas originalmente como helpers de teste parametrizados específicos de cada arquivo, projetados para receber dados de infraestrutura local gerados e limpos pelo próprio script. Elas nunca foram projetadas como casos de teste unitários pytest tradicionais.
8. **Import de pytest**: Nenhum dos arquivos de teste afetados importa o pacote `pytest`.
9. **Decoradores pytest**: Nenhum dos arquivos afetados utiliza decoradores do `pytest` (como `@pytest.mark` ou `@pytest.fixture`).
10. **Dependência de __main__**: Todos dependem da condicional de execução direta:
    ```python
    if __name__ == "__main__":
        sys.exit(main())
    ```

## 6. Histórico das funções afetadas

A busca no histórico do Git confirmou a origem e as alterações de cada assinatura de função afetada:

### 6.1 `teste_erros` e `teste_tipos_validos` (no arquivo `teste_loader.py`)
- **Introduzido no commit**: `0e2bf0a2acca3917604ccc09a11ecb2479c8da73` (`0e2bf0a`)
- **Data**: Tue Jul 7 18:41:50 2026 -0300
- **Mensagem**: `feat: implementa loader mínimo de tela JSON`
- **Assinatura original**:
  - `def teste_erros(tmp_base):`
  - `def teste_tipos_validos(tmp_base):`
- **Forma de chamada original**: Chamados posicionalmente de dentro da função `main()`, passando a variável `tmp_base` do tipo `Path` gerada por um diretório temporário (`tempfile.mkdtemp`).
- **Análise**: Os parâmetros problemáticos de infraestrutura `tmp_base` já existiam desde o primeiro commit de criação do arquivo. Nenhuma renomeação de arquivo ocorreu (ele nasceu como `scripts/tela/teste_loader.py`).

### 6.2 `teste_grupo_estrutural` (no arquivo `teste_loader.py`)
- **Introduzido no commit**: `0bcb47796d11b3ef9a7ec0ea862ef2a9fb9e1d84` (`0bcb477`)
- **Data**: Wed Jul 8 18:19:04 2026 -0300
- **Mensagem**: `feat: implementa grupo estrutural minimo em tela isolada`
- **Assinatura original**: `def teste_grupo_estrutural(tmp_base):`
- **Chamada**: Chamado em `main()` passando a mesma variável local `tmp_base`. Nasceu com a assinatura idêntica e sem suporte a pytest.

### 6.3 `teste_arranjo_corpo_h0019` (no arquivo `teste_loader.py`)
- **Introduzido no commit**: `29a8a7985fc8488e072fec1ba99d21469e35b719` (`29a8a79`)
- **Data**: Fri Jul 10 10:23:59 2026 -0300
- **Mensagem**: `feat: implementa layout horizontal plano do corpo`
- **Assinatura original**: `def teste_arranjo_corpo_h0019(tmp_base):`
- **Análise**: Introduzido no H-0019 com parâmetro posicional para diretório temporário.

### 6.4 `teste_distribuicao_corpo_h0025` (no arquivo `teste_loader.py`)
- **Introduzido no commit**: `1cc0dffe8f6d6349312b9d0b64beea207b539fa7` (`1cc0dff`)
- **Data**: Sat Jul 11 20:37:25 2026 -0300
- **Mensagem**: `feat: implementa distribuicao vertical explicita do corpo`
- **Assinatura original**: `def teste_distribuicao_corpo_h0025(tmp_base):`

### 6.5 `teste_hierarquia_grupos_adr0019` (no arquivo `teste_loader.py`)
- **Introduzido no commit**: `c003f3e18cfbf69e7bf2e1329bf367098e946a48` (`c003f3e`)
- **Data**: Sun Jul 12 13:42:31 2026 -0300
- **Mensagem**: `feat: implementa composicao hierarquica do corpo com tres niveis de grupos`
- **Assinatura original**: `def teste_hierarquia_grupos_adr0019(tmp_base):`

### 6.6 `teste_modo_executavel` (no arquivo `teste_diagnostico.py`)
- **Introduzido no commit**: `54e85093557e4e1144f8007a8fe8f77d33b5c391` (`54e8509`)
- **Data**: Tue Jul 7 20:29:10 2026 -0300
- **Mensagem**: `feat: implementa diagnostico executavel da tela raiz`
- **Assinatura original**: `def teste_modo_executavel(resultado_esperado):`
- **Análise**: O arquivo `teste_diagnostico.py` nasceu com essa assinatura que espera a string de resultado gerada no teste anterior do mesmo arquivo e passada manualmente no `main()`.

### 6.7 `teste_renderizar_estado` e `teste_renderizar_estado_altura` (no arquivo `teste_demo.py`)
- **`teste_renderizar_estado` introduzido no commit**: `2c6efe6be0a4f5c9281a8b941566440db7f7b3df` (`2c6efe6`)
  - **Data**: Tue Jul 7 23:36:11 2026 -0300
  - **Mensagem**: `feat: adiciona demo minima de borda e sair`
  - **Assinatura original**: `def teste_renderizar_estado(modelo):`
- **`teste_renderizar_estado_altura` introduzido no commit**: `b2eb45831634fa6be594d2325ec2be6c97a7801a` (`b2eb458`)
  - **Data**: Thu Jul 9 12:34:18 2026 -0300
  - **Mensagem**: `feat: ocupa altura do terminal pelo corpo`
  - **Assinatura original**: `def teste_renderizar_estado_altura(modelo):`

### 6.8 `teste_navegacao_minima` (no arquivo `teste_demo.py`)
- **Introduzido no commit**: `36c55d233f2cf19760773b06bc9170fc84333b2a` (`36c55d2`)
- **Data**: Wed Jul 8 13:44:35 2026 -0300
- **Mensagem**: `feat: implementa fluxo minimo do lancador com tela destino`
- **Assinatura original**: `def teste_navegacao_minima(modelo):`

---

**Fato Histórico Fundamental**: Todas as dez funções afetadas por erros de coleta do `pytest` nasceram com suas assinaturas parametrizadas incompatíveis com o `pytest` desde o primeiro dia de sua respectiva criação. Não houve alterações posteriores que tenham quebrado o comportamento; elas foram criadas especificamente dessa forma estrutural.

## 7. Histórico das fixtures

A pesquisa completa realizada no histórico histórico de todo o repositório Git provou:
- **`tmp_base` como fixture**: Nunca foi definida como fixture `@pytest.fixture` na história do projeto.
- **`modelo` como fixture**: Nunca foi definida como fixture `@pytest.fixture` na história do projeto.
- **`resultado_esperado` como fixture**: Nunca foi definida como fixture `@pytest.fixture` na história do projeto.
- **Uso do decorador `@pytest.fixture`**: O comando `git log -G'@pytest.fixture'` retornou absolutamente zero correspondências. Ou seja, **nunca existiu nenhuma fixture declarada em todo o repositório em nenhuma versão de sua história**.

## 8. Histórico da configuração pytest

A pesquisa exaustiva de arquivos de configuração histórica do `pytest` revelou:
- **`conftest.py`**: Nunca existiu no repositório.
- **`pytest.ini`**: Nunca existiu no repositório.
- **`pyproject.toml`**: Nunca existiu no repositório.
- **`setup.cfg`**: Nunca existiu no repositório.
- **`tox.ini`**: Nunca existiu no repositório.

O projeto nunca adotou configurações de coleta do `pytest` e sempre se baseou na execução de scripts simples e isolados via biblioteca padrão do Python.

## 9. Histórico do comando pytest

Ao analisar a história de documentos sob `scripts/docs/`:
- **Proibição expressa**: Em todos os handoffs iniciais (como H-0003, H-0004, H-0005, H-0006, H-0007, H-0008), o documento continha uma proibição literal estrita:
  > *"Não usar `unittest`, `pytest` nem nenhum framework externo."*
- **Primeiro aparecimento**: O primeiro documento a mencionar e introduzir formalmente o comando de coleta `pytest` como um gate de suíte obrigatório foi o handoff original `H-0028-matriz-de-grupos-coordenadas-explicitas.md`.
- **Causa da inclusão**: O gate foi adicionado ao handoff sem que os arquivos de testes legados fossem primeiro convertidos ou que uma configuração de exclusão de coleta fosse criada. O comando assumia incorretamente que o prefixo `teste_` seria coletado sem problemas funcionais pelo pytest, ignorando o fato de que as funções históricas recebiam parâmetros.

Diferenciação clara:
- **Origem do código de teste**: Iniciada no commit `0e2bf0a` (Loader), `54e8509` (Diagnóstico) e `2c6efe6` (Demo) como scripts simples baseados puramente em biblioteca padrão.
- **Origem do comando de processo**: Introduzida recentemente como gate obrigatório documental em `H-0028` para verificar cobertura automatizada agregada.

## 10. Commits selecionados

Para reproduzir e comprovar a evolução histórica dos erros de coleta do `pytest`, selecionou-se os seguintes pontos de verificação na linha do tempo do Git:

1. `b7532d5` — Estado anterior à criação do primeiro arquivo de teste (`teste_loader.py`).
2. `0e2bf0a` — Introdução de `teste_loader.py` com as funções `teste_erros` e `teste_tipos_validos`.
3. `54e8509` — Introdução de `teste_diagnostico.py` com `teste_modo_executavel`.
4. `2c6efe6` — Introdução de `teste_demo.py` com `teste_renderizar_estado`.
5. `36c55d2` — Adição de `teste_navegacao_minima` no `teste_demo.py`.
6. `0bcb477` — Adição de `teste_grupo_estrutural` no `teste_loader.py`.
7. `b2eb458` — Adição de `teste_renderizar_estado_altura` no `teste_demo.py`.
8. `29a8a79` — Adição de `teste_arranjo_corpo_h0019` no `teste_loader.py`.
9. `1cc0dff` — Adição de `teste_distribuicao_corpo_h0025` no `teste_loader.py`.
10. `c003f3e` — Adição de `teste_hierarquia_grupos_adr0019` no `teste_loader.py` (fechando as 10 funções afetadas).
11. `f00b0bb` — Commit de referência Baseline (anterior ao H-0028).

## 11. Reproduções históricas

A reprodução foi realizada extraindo os snapshots de cada commit em cópias de diretórios isolados sob `/tmp` e executando o ambiente Python global:
- **Python**: `3.14.6`
- **pytest**: `9.0.3`

Resultados das reproduções:

| Commit | Data | Execução direta (Passed/Total) | Pytest (Passed/Failed) | Erros de Coleta | Observação / Causa |
| :---: | :---: | :---: | :---: | :---: | :--- |
| `b7532d5` | 2026-07-07 | 0 / 0 | 0 / 0 | 0 | Sem nenhum arquivo de teste no repositório. |
| `0e2bf0a` | 2026-07-07 | 37 / 37 | 2 / 0 | 2 | **Surgem os 2 primeiros erros**: `tmp_base` ausente nas novas funções `teste_erros` e `teste_tipos_validos`. |
| `54e8509` | 2026-07-07 | 133 / 133 | 12 / 0 | 3 | **Surgem 3 erros**: `resultado_esperado` ausente em `teste_modo_executavel`. |
| `2c6efe6` | 2026-07-07 | 200 / 200 | 19 / 0 | 4 | **Surgem 4 erros**: `modelo` ausente em `teste_renderizar_estado`. |
| `36c55d2` | 2026-07-08 | 301 / 301 | 24 / 0 | 5 | **Surgem 5 erros**: `modelo` ausente em `teste_navegacao_minima`. |
| `0bcb477` | 2026-07-08 | 345 / 345 | 26 / 0 | 6 | **Surgem 6 erros**: `tmp_base` ausente em `teste_grupo_estrutural`. |
| `b2eb458` | 2026-07-09 | 398 / 398 | 27 / 0 | 7 | **Surgem 7 erros**: `modelo` ausente em `teste_renderizar_estado_altura`. |
| `29a8a79` | 2026-07-10 | 589 / 589 | 121 / 0 | 8 | **Surgem 8 erros**: `tmp_base` ausente em `teste_arranjo_corpo_h0019`. |
| `1cc0dff` | 2026-07-11 | 917 / 917 | 171 / 0 | 9 | **Surgem 9 erros**: `tmp_base` ausente em `teste_distribuicao_corpo_h0025`. |
| `c003f3e` | 2026-07-12 | 1070 / 1070 | 207 / 0 | 10 | **Surgem os 10 erros**: `tmp_base` ausente em `teste_hierarquia_grupos_adr0019`. |
| `f00b0bb` | 2026-07-12 | 1070 / 1070 | 207 / 0 | 10 | Baseline estabilizado com exatamente os 10 erros históricos. |

## 12. Primeiro commit afetado

Para cada grupo de erros, o primeiro commit afetado e o surgimento do comportamento ocorrem exatamente na introdução das funções nos scripts locais:

- **Grupo `tmp_base`**:
  - `teste_erros` e `teste_tipos_validos`: Primeiro commit afetado é `0e2bf0a`.
  - `teste_grupo_estrutural`: Primeiro commit afetado é `0bcb477`.
  - `teste_arranjo_corpo_h0019`: Primeiro commit afetado é `29a8a79`.
  - `teste_distribuicao_corpo_h0025`: Primeiro commit afetado é `1cc0dff`.
  - `teste_hierarquia_grupos_adr0019`: Primeiro commit afetado é `c003f3e`.
- **Grupo `modelo`**:
  - `teste_renderizar_estado`: Primeiro commit afetado é `2c6efe6`.
  - `teste_navegacao_minima`: Primeiro commit afetado é `36c55d2`.
  - `teste_renderizar_estado_altura`: Primeiro commit afetado é `b2eb458`.
- **Grupo `resultado_esperado`**:
  - `teste_modo_executavel`: Primeiro commit afetado é `54e8509`.

Cada um desses commits é marcado por: `INCOMPATIVEL_COM_PYTEST_DESDE_A_ORIGEM`.

## 13. Último commit não afetado

- Para os erros de `tmp_base` (loader): o commit anterior imediato é `b7532d5`.
- Para os erros de `resultado_esperado` (diagnóstico): o commit anterior imediato é `0e2bf0a`.
- Para os erros de `modelo` (demo): o commit anterior imediato é `54e8509`.

## 14. Classificação por grupo de erro

A classificação de cada grupo de erro de coleta do `pytest` é determinada de forma inequívoca como:

- **Grupo `tmp_base`** (6 erros em `teste_loader.py`):
  `A — INCOMPATIVEL_COM_PYTEST_DESDE_A_ORIGEM`
- **Grupo `modelo`** (3 erros em `teste_demo.py`):
  `A — INCOMPATIVEL_COM_PYTEST_DESDE_A_ORIGEM`
- **Grupo `resultado_esperado`** (1 erro em `teste_diagnostico.py`):
  `A — INCOMPATIVEL_COM_PYTEST_DESDE_A_ORIGEM`

O comando `pytest` introduzido no H-0028 se enquadra na categoria:
- `E — COMANDO_PYTEST_INTRODUZIDO_SEM_SUPORTE_PREVIO`

## 15. Compatibilidade histórica

Os fatos comprovados historicamente atestam:
1. **Suíte direta**: Todas as funções de teste sempre operaram com 100% de sucesso e retorno limpo (código de saída 0) de forma ininterrupta nas execuções diretas de seus respectivos arquivos desde o dia em que nasceram.
2. **Coleta automática**: O `pytest` nunca foi compatível com a totalidade do harness legado. Não houve uma alteração de código ou de configuração que removeu compatibilidade anterior. O código em si nunca regrediu; foi a imposição documental do comando global do `pytest` como gate que introduziu uma falha de design procedimental.

## 16. Influência possível de versões

O projeto nunca conteve versões fixadas do interpretador Python, do pacote `pytest` ou de plugins em arquivos como `requirements.txt` ou equivalentes.
- **Python nativo**: O harness usa apenas pacotes nativos (shutil, sys, tempfile, os, json, subprocess).
- **Sem fixtures externas**: A falha de coleta de fixtures é inerente ao interpretador do pytest ao coletar funções parametrizadas (independente se em versões antigas ou modernas como a `9.0.3` atual). Nenhuma mudança de versão resolveria o problema por si só sem alterar a assinatura do código ou desativar a coleta do prefixo `teste_`.

## 17. Causa técnica

A causa técnica dos erros é o mecanismo de coleta padrão do `pytest`:
- O `pytest` coleta recursivamente arquivos correspondentes aos caminhos indicados. Quando encontra funções com o prefixo `teste_`, ele as trata como casos de teste unitários automáticos.
- Se uma função candidata a teste declara parâmetros de entrada na sua assinatura, o `pytest` assume que esses parâmetros são fixtures que devem ser injetadas.
- Como `tmp_base`, `modelo` e `resultado_esperado` não são fixtures, mas sim argumentos posicionais fornecidos manualmente pelos scripts diretos dentro do ponto de entrada `main()`, a fase de coleta falha em tempo de compilação/montagem da árvore de testes.

## 18. Causa processual

- **Harness centrado em scripts simples**: Desde o início, o projeto priorizou scripts de testes diretos e portáveis, dependendo apenas da biblioteca padrão e executáveis diretamente por `python3 scripts/tela/teste_*.py`.
- **Falta de validação documental anterior**: O comando de suíte completa `pytest` foi introduzido no documento de handoff H-0028 como critério obrigatório de aceite automatizado ("resultado N/N") pelo gestor do projeto, sem ter sido validado em uma execução limpa de baseline anterior. O comando assumia incorretamente que o pytest faria uma coleta limpa, criando uma restrição insolúvel no pipeline.

## 19. Impacto sobre o H-0028

O H-0028 e sua correspondente implementação IMP-0029 são **totalmente isentos de responsabilidade** sobre esses erros:
- Nenhum dos 10 erros foi introduzido, modificado ou agravado pelas alterações realizadas na implementação da matriz declarativa de grupos (H-0028).
- A implementação cumpriu integralmente todos os requisitos funcionais, adicionando inclusive 17 testes coletáveis pelo pytest que passam sem erros (elevando passed de 207 para 224) e 63 novas verificações diretas (elevando total direto de 1070 para 1133).
- O impedimento que o pytest causava na homologação da entrega era puramente documental e de design do harness, o qual foi adequadamente resolvido pós-patch com a alteração do critério de aceite principal para os scripts diretos (suíte canônica).

## 20. Alternativas futuras de correção

Para que o comando complementar do `pytest` possa rodar no futuro sem exibir os dez erros de coleta preexistentes, as seguintes alternativas técnicas são listadas como possíveis soluções (a serem decididas em ciclo futuro):

1. **Correção de Nomenclatura (Mais simples e limpa)**:
   - Renomear as dez funções auxiliares e parametrizadas de `teste_` para outro prefixo (ex: `_teste_`, `helper_teste_` ou `verificar_`), evitando que sejam elegíveis para coleta automática pelo pytest, mantendo o prefixo `test_` apenas para métodos de teste pytest reais.
2. **Definição de Fixtures Reais**:
   - Reescrever o harness de testes para adotar o framework `pytest` de forma definitiva, criando fixtures formais para as dependências de ambiente e eliminando os loops `main` customizados.
3. **Uso de Wrappers Customizados**:
   - Manter as assinaturas e criar wrappers específicos decorados com `@pytest.mark.skip` ou desativar temporariamente sua coleta via marcadores.
4. **Configuração pytest de exclusão de prefixo**:
   - Criar um arquivo `pytest.ini` ou `pyproject.toml` definindo `python_functions = test_*`, o que faria o pytest ignorar todas as funções iniciadas com `teste_` (em português) e coletar apenas os novos testes escritos como `test_` (em inglês), resolvendo instantaneamente os 10 erros históricos sem alterar uma única linha de código.
5. **Configuração de exclusão de arquivos**:
   - Configurar o pytest para ignorar os arquivos inteiros que causam erros de coleta de dependências manuais (`teste_demo.py` e `teste_diagnostico.py`), limitando a coleta aos testes unitários puros.

## 21. Limitações da investigação

- Esta investigação foi conduzida retrospectivamente reconstruindo snapshots históricos através do comando `git archive` e testando sob o ambiente interpretador Python local.
- Não foram testadas versões legadas históricas do pytest anteriores à `9.0.3` (versão do ambiente atual de trabalho), visto que a falha de dependência de fixtures decorre de regras fixas de coleta do pytest que permanecem inalteradas há diversas versões.

## 22. Escopo Git

Conforme diretrizes regulatórias e restrições estabelecidas pelo prompt:
- **Nenhum arquivo de código foi alterado**.
- **Nenhum teste existente ou novo foi alterado**.
- **Nenhum relatório existente foi modificado**.
- **O stage do Git permanece inteiramente limpo e vazio**.
- **Nenhuma operação Git em andamento**.
- **O único arquivo novo criado é o presente relatório**.

## 23. Status final

```text
ORIGIN_CONFIRMED_NEVER_PYTEST_COMPATIBLE
```

## 24. Próxima categoria processual

```text
VALIDACAO_MANUAL
```
