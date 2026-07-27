---
name: relatorio-patch-h-0040-implementacao
description: Relatorio do patch de implementacao do H-0040 tratando os achados QAI40-001 a QAI40-004 do QA rejeitado
metadata:
  type: relatorio
  etapa: PATCH_IMPLEMENTACAO
  handoff: H-0040
  adr: ADR-0031
---

# Relatório de Patch de Implementação H-0040

## 1. Identificação

```yaml
resultado:
  etapa: PATCH_IMPLEMENTACAO
  handoff: H-0040
  adr: ADR-0031
  data: 2026-07-26
```

## 2. Objeto

Correção da implementação de H-0040 (navegação simples e seleção única em
console de nível único) rejeitada pelo QA independente em
`docs/relatorios/RELATORIO_QA_H-0040_IMPLEMENTACAO.md` com classificação
`I2_IMPLEMENTATION_PATCH_REQUIRED` e quatro achados maiores (`QAI40-001` a
`QAI40-004`). O QA rejeitado permanece integralmente preservado.

## 3. Autoridades

Lidas integralmente:

- `docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md`
- `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md`
- `docs/relatorios/RELATORIO_QA_H-0040_IMPLEMENTACAO.md`
- `docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0040_HANDOFF.md`
- `docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md`

O relatório de implementação inicial não é autoridade superior à evidência
produzida pelo QA.

## 4. Estado inicial

```yaml
handoff:
  numero: H-0040
  qa_handoff: H1_HANDOFF_APPROVED
implementacao_inicial:
  relatorio: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
  encerramento: IMPLEMENTATION_COMPLETED_AWAITING_QA
qa_implementacao:
  relatorio: docs/relatorios/RELATORIO_QA_H-0040_IMPLEMENTACAO.md
  classificacao: I2_IMPLEMENTATION_PATCH_REQUIRED
  achados_bloqueantes: 0
  achados_maiores: 4
validacao_manual:
  executada: false
  liberada: false
```

## 5. Estado Git inicial

```yaml
estado_git_inicial:
  arquivos_staged: []
  arquivos_unstaged:
    - demo/demo.py
    - docs/adr/INDICE_ADR.md
    - docs/backlog.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_chip.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_tela_json.md
    - docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/nomenclatura/32_CONSOLE.md
    - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
    - tela/renderizador.py
  arquivos_staged_e_unstaged: []
  arquivos_nao_rastreados:
    - config/telas/demo/h0040_nav_console_grade_2x3.json
    - config/telas/demo/h0040_nav_console_nao_focalizavel.json
    - config/telas/demo/h0040_nav_console_unico_linear.json
    - config/telas/demo/h0040_nav_degenere_um_item.json
    - config/telas/demo/h0040_nav_degenere_uma_coluna.json
    - config/telas/demo/h0040_nav_degenere_uma_linha.json
    - config/telas/demo/h0040_nav_dois_consoles.json
    - config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
    - demo/demo_navegacao.py
    - demo/teste_demo_navegacao.py
    - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
    - docs/relatorios/RELATORIO_QA_H-0040_IMPLEMENTACAO.md
    - tela/navegacao.py
    - tela/teste_navegacao.py
    - (arquivos documentais acumulados do ciclo ADR-0031)
    - (arquivos __pycache__ preservados)
```

As modificações em `docs/adr/INDICE_ADR.md`, `docs/backlog.md`, `docs/contratos/*`
e `docs/nomenclatura/*` já estavam presentes no worktree acumulado antes do
início deste patch (são parte do ciclo de aplicação documental da ADR-0031,
preservadas) e não foram tocadas por este patch.

## 6. Limite material

### 6.1 Arquivos autorizados para modificação

Modificados por este patch:

```text
demo/demo.py
tela/renderizador.py
tela/navegacao.py
demo/demo_navegacao.py
demo/teste_demo_navegacao.py
tela/teste_navegacao.py
docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
```

### 6.2 Arquivo autorizado para criação

Criado por este patch:

```text
docs/relatorios/RELATORIO_PATCH_H-0040_IMPLEMENTACAO.md
```

### 6.3 Arquivos preservados

Todos os oito JSONs do H-0040, ADR-0031, contratos, nomenclatura, backlog,
índice, todos os relatórios de QA e todos os demais arquivos de produção e teste
permanecem sem alteração por este patch.

## 7. Análise de `QAI40-001` — indicador matricial

### 7.1 Defeito confirmado

No cenário `config/telas/demo/h0040_nav_console_grade_2x3.json` largura 60, a
implementação inicial tratava células row-major como linhas físicas sequenciais.
Reprodução antes da correção:

```text
cursor 0 → indicador antes de G00 (correto)
cursor 1 → indicador antes da linha G10/G11 (não marca G01)
cursor 2 → indicador em linha vazia
cursor 3 → indicador em linha vazia
cursor 4 → indicador em linha vazia
```

Isso viola D11 e D12: a primeira linha física do item corrente não era marcada
para a maior parte da matriz, e linhas vazias recebiam o indicador.

### 7.2 Causa raiz

`_linhas_fisicas_por_item` (renderer) mapeava cada célula row-major a uma linha
física sequencial, embora três células da mesma linha da grade compartilhassem
uma única linha física no canvas. `_aplicar_indicador_linhas` prefixava a linha
física inteira, sem distinguir células lado a lado.

## 8. Correção de `QAI40-001`

O indicador passou a ser inserido DENTRO da célula de cada item, antes da
composição horizontal das células da linha. Implementação em
`tela/renderizador.py`:

- nova função `_renderizar_participante_com_indicador` escreve o marcador
  (`selecionado_simbolo` para a primeira linha física do item corrente;
  `selecionado_off` para as demais células e linhas de continuação) na primeira
  coluna da célula e desloca o texto do item em `ind_w` (largura da coluna
  indicadora);
- `_linhas_distribuicao_matricial` consulta a geometria real do motor
  (`calcular_distribuicao`) e o item corrente do contexto de navegação para
  decidir qual célula marca; cada item navegável possui sua própria coluna
  indicadora (itens lado a lado têm colunas independentes);
- nenhuma linha vazia recebe o indicador; somente a primeira linha física do
  item corrente no console focado recebe o símbolo.

Resultado pós-correção (cursores 0 a 4, largura 60):

```text
cursor 0 → item g00 célula (0,0) → símbolo na célula de g00
cursor 1 → item g01 célula (0,1) → símbolo na célula de g01
cursor 2 → item g02 célula (0,2) → símbolo na célula de g02
cursor 3 → item g10 célula (1,0) → símbolo na célula de g10
cursor 4 → item g11 célula (1,1) → símbolo na célula de g11
```

Cada cursor produz exatamente uma ocorrência do símbolo, na célula correta.

## 9. Análise de `QAI40-002` — geometria única

### 9.1 Defeito confirmado

Para largura total 60, a navegação usava `area_w = 58` (`largura - 2`) e o
renderer usava `area_w = 55` (`(largura - 3) - 2`). O mesmo motor era chamado
com larguras diferentes, divergindo a geometria da grade de navegação da grade
visual renderizada. Isso viola D7, D10 e D12.

### 9.2 Causa raiz

A navegação recebia a largura total e aplicava `largura - LARGURA_INDICADOR`,
enquanto o renderer aplicava `(largura - 3) - LARGURA_INDICADOR`. O desconto
estrutural do renderer (`3`) era conhecido implicitamente apenas por um lado.

## 10. Correção de `QAI40-002`

Centralização da geometria na autoridade única do renderer, sem cristalizar
`total_w - 3 - 2` na navegação:

- `tela/renderizador.py` expõe `DESCONTO_ESTRUTURAL_CONSOLE` (única autoridade
  do desconto estrutural: borda esquerda + espaço interno + borda direita) e
  `largura_util_itens_console(total_w, elemento)`, que aplica o desconto
  estrutural e a reserva do indicador;
- `tela/navegacao.grade_de_itens` recebe `desconto_estrutural` como parâmetro
  EXPLÍCITO (default `0`), aplicando-o à largura antes da reserva do indicador.
  A navegação NÃO conhece implicitamente o desconto estrutural do renderer;
- o runtime real (`demo/demo.py`) repassa `desconto_estrutural =
  DESCONTO_ESTRUTURAL_CONSOLE` no estado, consumido pelos motores de movimento
  (`_mover_horizontal`, `_mover_vertical`, `posicao_corrente`);
- a reserva do indicador entra no requisito mínimo de largura de cada item
  (`min_w = texto + LARGURA_INDICADOR_COLUNA`), de modo que a formação
  calculada coincide exatamente com a grade renderizada (uma coluna indicadora
  por item, lado a lado).

Resultado pós-correção: navegação e renderer consomem a mesma largura útil e a
mesma formação (verificado em AT-0021, PN-0016 e nas reproduções técnicas).

## 11. Análise de `QAI40-003` — `--verboso`

### 11.1 Defeito confirmado

A opção `--verboso` era aceita por `demo/demo_navegacao.py`, mas o estado era
posteriormente redefinido: o JSON `h0040_nav_console_unico_linear` fornece
`politica_exibicao` mas o modelo do console apresentava `politica_modo=None`, e
`demo/demo.py` redefinia `modo_verboso` pelo modelo. As saídas não-TTY normal e
`--verboso` eram idênticas (2908 bytes cada, conteúdo idêntico).

### 11.2 Causa raiz

O override `--verboso` não tinha um canal estável para alcançar o runtime e o
renderer reais: era sobrescrito por `_modo_verboso_de_modelo` e ignorado por
`_verboso_efetivo` quando `politica_modo` era `None`. Adicionalmente, o caminho
matricial de console com itens não honrava o modo verboso (não quebrava texto).

## 12. Correção de `QAI40-003`

- `demo/demo_navegacao.main` propaga `--verboso` como override real via
  `modo_verboso_forcado=True` injetado no estado inicial repassado ao `main`
  real de `demo/demo.py`;
- `demo/demo.py._verboso_efetivo` honra o override (`modo_verboso_forcado`)
  com precedência sobre a política do modelo, sem requerer `politica_modo` e
  sem ser sobrescrito por `politica_modo=None`;
- `tela/renderizador.py._linhas_distribuicao_matricial` honra `verboso` para
  console com itens (sem `conteudo_externo`): o texto longo de cada item é
  quebrado em múltiplas linhas físicas pela largura útil da célula
  (`_quebrar_texto`), produzindo continuação física real;
- o requisito mínimo de altura (`min_hs`) em modo verboso é calculado pela
  quebra efetiva na largura útil real da célula, evitando fallback indevido.

Resultado pós-correção: a saída verbosa é materialmente diferente da não
verbosa (item longo quebrado em múltiplas linhas físicas); ambos encerram com
código zero e sem STDERR; a tecla `V` não foi tornada disponível onde não era
contratada; nenhuma política nova foi criada no JSON.

## 13. Correção factual de `QAI40-004`

Atualização de `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md`:

- preservado o resultado histórico da implementação inicial (57 focais / 480
  canônicos aprovados brutos; QA `I2_IMPLEMENTATION_PATCH_REQUIRED`);
- adicionada seção 16 registrando o resultado histórico, os motivos do QA, o
  patch aplicado e as contagens factuais pós-correção (57 focais / 352
  regressão / 480 canônicos, todos aprovados);
- a última linha permanece `IMPLEMENTATION_COMPLETED_AWAITING_QA`.

## 14. Arquivos modificados

```yaml
arquivos_modificados_neste_patch:
  - demo/demo.py
  - tela/renderizador.py
  - tela/navegacao.py
  - demo/demo_navegacao.py
  - demo/teste_demo_navegacao.py
  - tela/teste_navegacao.py
  - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
```

## 15. Arquivos preservados

```yaml
arquivos_preservados:
  JSONs:
    - config/telas/demo/h0040_nav_console_unico_linear.json
    - config/telas/demo/h0040_nav_dois_consoles.json
    - config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
    - config/telas/demo/h0040_nav_console_grade_2x3.json
    - config/telas/demo/h0040_nav_console_nao_focalizavel.json
    - config/telas/demo/h0040_nav_degenere_um_item.json
    - config/telas/demo/h0040_nav_degenere_uma_linha.json
    - config/telas/demo/h0040_nav_degenere_uma_coluna.json
  autoridades_normativas:
    - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
    - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
    - contratos, nomenclatura, backlog, índice
  relatorios_de_QA:
    - docs/relatorios/RELATORIO_QA_H-0040_IMPLEMENTACAO.md
    - todos os demais relatórios de QA
  testes_de_regressao:
    - tela/teste_renderizador.py
    - demo/teste_demo.py
    - tela/teste_loader.py
    - tela/teste_distribuicao_matricial.py
```

## 16. Testes reformulados

```yaml
testes_reformulados:
  AT:
    - AT-0021  # equivalência grade navegação/renderer (renderer real)
    - AT-0032  # redimensionamento recalcula vizinhos (grades diferentes)
    - AT-0033  # mudança de modo preserva item (modo muda materialmente)
    - AT-0034  # mudança de modo recalcula grade (saída física diferente)
    - AT-0035  # indicador apenas no focado (cursores 0-4 da matriz 2x3)
    - AT-0036  # indicador do estilo e coluna estável (matriz 1x3)
    - AT-0037  # continuações recebem off (continuação física real)
  PN:
    - PN-0010  # indicador fora da primeira linha (continuação real)
    - PN-0011  # modo não reinicia item (override --verboso efetivo)
    - PN-0016  # grade navegação não diverge da visual (renderer integrado)
```

Cada teste reformulado compara contra o renderer real (não reproduz a fórmula
no próprio teste), observa posições físicas reais e falhava coerentemente com o
defeito antes da correção.

## 17. Prova negativa antes da correção

```yaml
prova_negativa_do_patch:
  testes_fortalecidos_antes_da_correcao: 10
    # AT-0021, AT-0032, AT-0033, AT-0034, AT-0035, AT-0036, AT-0037,
    # PN-0010, PN-0011, PN-0016
  falhas_observadas: 10
  defeitos_detectados:
    - QAI40-001  # AT-0035, AT-0036, AT-0037, PN-0010, PN-0016
    - QAI40-002  # AT-0021, AT-0032, PN-0016
    - QAI40-003  # AT-0033, AT-0034, PN-0011
  testes_apos_correcao: 57
  resultado: 57 aprovados, 0 falhas, 0 erros
```

Antes de aplicar a correção, os 10 testes reformulados falharam de forma
coerente com os defeitos. Não foi derivado o resultado esperado da saída
defeituosa: o esperado veio das autoridades (ADR-0031 D7/D10/D11/D12/D12 e
contrato_console.md §6).

## 18. Testes focais finais

```yaml
testes_focais:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py demo/teste_demo_navegacao.py -q
  coletados: 57
  aprovados: 57
  ignorados: 0
  falhas: 0
  erros: 0
```

## 19. Regressão direta

```yaml
regressao_direta:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_renderizador.py demo/teste_demo.py tela/teste_loader.py tela/teste_distribuicao_matricial.py -q
  coletados: 352
  aprovados: 352
  ignorados: 0
  falhas: 0
  erros: 0
```

Os quatro arquivos de teste de regressão não foram alterados por este patch.

## 20. Suíte canônica

```yaml
suite_canonica:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  coletados: 480
  aprovados: 480
  ignorados: 0
  falhas: 0
  erros: 0
```

A coleta permanece em 480 (40 AT + 17 PN = 57 testes novos, sem lacunas,
duplicatas ou ampliação da contagem).

## 21. Reproduções técnicas

### 21.1 Indicador matricial

Cenário `config/telas/demo/h0040_nav_console_grade_2x3.json`, largura 60:

| Cursor | Item lógico | Linha/coluna grade | Célula com indicador | Outras sem indicador | Resultado |
| --- | --- | --- | --- | --- | --- |
| 0 | g00 | (0,0) | g00 | g01, g02, g10, g11 | CORRIGIDO |
| 1 | g01 | (0,1) | g01 | g00, g02, g10, g11 | CORRIGIDO |
| 2 | g02 | (0,2) | g02 | g00, g01, g10, g11 | CORRIGIDO |
| 3 | g10 | (1,0) | g10 | g00, g01, g02, g11 | CORRIGIDO |
| 4 | g11 | (1,1) | g11 | g00, g01, g02, g10 | CORRIGIDO |

Cada cursor produz exatamente uma ocorrência do símbolo na célula correta.

### 21.2 Geometria

| Largura total | Largura útil renderer | Largura útil navegação | Linhas | Colunas | Correspondência |
| --- | --- | --- | --- | --- | --- |
| 60 | 57 (content_w) | 57 (content_w) | 2 | 3 | true |
| 80 | 77 (content_w) | 77 (content_w) | 2 | 3 | true |

A largura útil da navegação e do renderer é idêntica; as formações coincidem.

### 21.3 Verboso

```yaml
normal:
  exit: 0
  stderr_bytes: 0
verboso:
  exit: 0
  stderr_bytes: 0
saidas_materialmente_diferentes: true
modo_verboso_efetivo: true
```

A saída verbosa contém o item multilinha (`Gamma...Theta` + `Iota...Mu`) quebrado
em duas linhas físicas; a saída normal mantém o item em uma linha.

## 22. Smoke checks

```yaml
smoke_checks:
  dois_consoles:
    comando: "printf 's\\n' | PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_dois_consoles.json"
    exit: 0
    stderr_bytes: 0
    stdout_linhas: 24
    resultado: CARREGA_RENDERIZA_SAI_LIMPO
  grade_2x3:
    comando: "printf 's\\n' | PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_grade_2x3.json"
    exit: 0
    stderr_bytes: 0
    stdout_linhas: 24
    resultado: CARREGA_RENDERIZA_SAI_LIMPO
  console_unico_verboso:
    comando: "printf 's\\n' | PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_unico_linear.json --verboso"
    exit: 0
    stderr_bytes: 0
    stdout_linhas: 24
    resultado: CARREGA_RENDERIZA_SAI_LIMPO
```

Isso não substitui validação manual.

## 23. Validação manual não executada

```yaml
validacao_manual:
  executada: false
  motivo: EXCLUSIVA_DO_USUARIO
  roteiro_disponivel: sim (VM-01 a VM-11, seção 23 do H-0040)
```

## 24. Checks mecânicos

```yaml
checks_mecanicos:
  arquivos_modificados_neste_patch:
    - demo/demo.py
    - tela/renderizador.py
    - tela/navegacao.py
    - demo/demo_navegacao.py
    - demo/teste_demo_navegacao.py
    - tela/teste_navegacao.py
    - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
  arquivos_criados_neste_patch:
    - docs/relatorios/RELATORIO_PATCH_H-0040_IMPLEMENTACAO.md
  arquivos_fora_da_lista_alterados: []
  operacoes_git_de_escrita_executadas: []
  commit_executado: nao
  validacao_manual_executada: nao
  newline_final: presente
  cercas_markdown_fechadas: sim
  marcadores_de_conflito: ausentes
  JSONs_alterados: nenhum
  relatorios_de_QA_alterados: nenhum
  documentacao_normativa_alterada: nenhuma
```

## 25. Estado Git final

```yaml
estado_git_final:
  arquivos_staged: []
  arquivos_unstaged:
    - demo/demo.py
    - tela/renderizador.py
    - (demais arquivos documentais do ciclo ADR-0031, preservados)
  arquivos_nao_rastreados:
    - docs/relatorios/RELATORIO_PATCH_H-0040_IMPLEMENTACAO.md
    - (demais arquivos novos do H-0040, preservados)
    - (arquivos __pycache__ preservados)
  operacoes_git_de_escrita_executadas: []
  commit_executado: nao
```

## 26. Bloqueios

```yaml
bloqueios: []
excecoes_solicitadas: []
arquivo_fora_da_lista_necessario: nao
```

## 27. Próximo gate

```yaml
proximo_gate: QA_POS_PATCH_IMPLEMENTACAO
```

O relatório atualizado continua aguardando QA pós-patch. Não foi executado QA
pós-patch, nem validação manual.

## 28. Encerramento

```yaml
resultado:
  etapa: PATCH_IMPLEMENTACAO
  handoff: H-0040
  qa_rejeitado: docs/relatorios/RELATORIO_QA_H-0040_IMPLEMENTACAO.md
  achados_tratados:
    - QAI40-001
    - QAI40-002
    - QAI40-003
    - QAI40-004
  qa_pos_patch_executado: false
  validacao_manual_executada: false
  encerramento: IMPLEMENTATION_PATCH_COMPLETED
```

| Achado    | Tratamento                              | Arquivos                                           | Testes                                       | Estado    |
| --------- | --------------------------------------- | -------------------------------------------------- | -------------------------------------------- | --------- |
| QAI40-001 | Indicador inserido dentro da célula     | tela/renderizador.py                               | AT-0035, AT-0036, AT-0037, PN-0010, PN-0016  | CORRIGIDO |
| QAI40-002 | Autoridade única de largura (renderer)  | tela/renderizador.py, tela/navegacao.py, demo/demo.py | AT-0021, AT-0032, PN-0016                    | CORRIGIDO |
| QAI40-003 | Override `--verboso` + path matricial   | demo/demo.py, demo/demo_navegacao.py, tela/renderizador.py | AT-0033, AT-0034, PN-0011                    | CORRIGIDO |
| QAI40-004 | Relatório factual (histórico + patch)   | docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md  | (relatório)                                  | CORRIGIDO |

IMPLEMENTATION_PATCH_COMPLETED
