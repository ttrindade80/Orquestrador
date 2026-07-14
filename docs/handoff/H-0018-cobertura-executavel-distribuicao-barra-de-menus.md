# H-0018 — Cobertura executável completa da seção `distribuicao` da `barra_de_menus`

```
status:        HANDOFF_READY
ciclo:         H-0018
título:        Cobertura executável completa da barra_de_menus.distribuicao
depende-de:    H-0017 (implementado, IMP-0017, QA aprovado — commit c8a20fa)
commit-base:   c8a20fa  test: adiciona explorador da barra de menus
data:          2026-07-09
autor-handoff: Claude Code
executor:      OpenCode / GLM
```

---

## Rastreabilidade

| Item | Referência |
|------|-----------|
| ADR normativo | `scripts/docs/adr/ADR-0014-barra-horizontal-termos-especificos.md` |
| Contrato de processo | `scripts/docs/contratos/contrato_processo_desenvolvimento.md` |
| Contrato tela JSON | `scripts/docs/contratos/contrato_tela_json.md` |
| Contrato barra de menus | `scripts/docs/contratos/contrato_barra_de_menus.md` |
| Contrato JSON barra de menus | `scripts/docs/contratos/contrato_json_barra_de_menus.md` |
| Contrato chip | `scripts/docs/contratos/contrato_chip.md` |
| H-0016 (base) | `scripts/docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md` |
| IMP-0016 | `scripts/docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md` |
| QA H-0016 | `scripts/docs/relatorios/RELATORIO_QA_H-0016_MIGRACAO_JSON_BARRA_DE_MENUS_HORIZONTAL_RESPONSIVA.md` |
| H-0017 (base) | `scripts/docs/handoff/H-0017-script-exploracao-combinacoes-barra-de-menus.md` |
| IMP-0017 | `scripts/docs/relatorios/IMP-0017-script-exploracao-combinacoes-barra-de-menus.md` |
| QA H-0017 | `scripts/docs/relatorios/RELATORIO_QA_H-0017_SCRIPT_EXPLORACAO_COMBINACOES_BARRA_DE_MENUS.md` |
| Relatório auditoria a gerar | `scripts/docs/relatorios/RELATORIO_AUDITORIA_H-0018_HANDOFF.md` |
| Relatório de implementação a gerar | `scripts/docs/relatorios/IMP-0018-cobertura-executavel-distribuicao-barra-de-menus.md` |
| Relatório de QA a gerar | `scripts/docs/relatorios/RELATORIO_QA_H-0018_COBERTURA_EXECUTAVEL_DISTRIBUICAO_BARRA_DE_MENUS.md` |

---

## Status

```
HANDOFF_READY
```

---

## Contexto operacional

O fluxo vigente neste ciclo é:

```
1. Claude Code      → gera handoff (este arquivo)
2. Claude Code      → auditoria do handoff (RELATORIO_AUDITORIA_H-0018_HANDOFF.md)
3. Claude Code      → implementação do código (em contexto limpo)
4. Claude Code      → QA final (RELATORIO_QA_H-0018_...)
5. Usuário          → commit
```

O executor **não decide arquitetura**. Toda decisão de design está registrada no
ADR-0014 e nos contratos. Se qualquer item normativo estiver ausente ou conflitante,
bloquear com `ARCHITECTURE_REVIEW_REQUIRED` antes de implementar.

---

## Contexto técnico — estado pós H-0017

O ciclo H-0016 implementou a renderização horizontal responsiva da `barra_de_menus`
(ADR-0014). O ciclo H-0017 criou o script de exploração
`explorar_barra_de_menus.py` e seu teste automatizado. Estado atual do código
relevante para este ciclo:

**`renderizador.py`** — função `_linhas_barra(barra_de_menus, content_w)`:

- Lê e aplica:
  - `vao_entre_chips.minimo` (usado como separador em linha única)
  - `vao_entre_colunas.minimo` (usado como separador em coluna_a_coluna)
  - `preenchimento_multilinha` (coluna_a_coluna / linha_a_linha)
  - `linhas.maximo` (iteração de 2 até maximo)
  - `overflow.quando_nao_couber = "erro_layout"` (erro determinístico)
  - flags de overflow (validadas deterministicamente, booleanas)
  - `ordem.politica = "declaracao"` (validada)
  - âncoras primeiro/último (validadas)

- **NÃO lê / ignora silenciosamente:**
  - `vao_chip_texto` — formato `[{tecla}] {texto}` é construído com 1 espaço
    fixo em `_texto_chip_barra`; o valor declarado em `vao_chip_texto.minimo`
    nunca é aplicado
  - `margem_horizontal` — o conteúdo começa imediatamente na primeira posição
    do `content_w`; nenhum padding lateral é inserido
  - `vao_vertical_entre_linhas` — sempre 0; valor declarado nunca lido
  - `alinhamento_linhas` — sempre esquerda (`ljust`/natural); valor declarado
    nunca lido
  - `linhas.minimo` — nunca validado contra o resultado; o renderer ignora
    silenciosamente quando o resultado tem mais linhas que `minimo`... na
    prática não ocorre porque só itera de 2 para cima, mas `minimo > 1` não
    é tratado deterministicamente
  - `preferir_menor_numero` — não lido; a iteração de 2 a `maximo` é
    implicitamente preferir-menor, mas o campo em si não é lido nem validado
  - `colunas.largura` — valor `"por_maior_item_da_coluna"` está hardcoded no
    comportamento de `_montar_coluna_a_coluna`; o campo não é lido nem
    validado
  - `subcolunas.chip.alinhamento` e `subcolunas.texto.alinhamento` — não
    lidos; o alinhamento é sempre à esquerda por comportamento implícito

**`explorar_barra_de_menus.py`** — parametriza via CLI:
- `--larguras`, `--chips`, `--linhas-max`, `--preenchimentos`
- `--vao-entre-chips`, `--vao-entre-colunas` (via perfis de espaçamento)

- **NÃO parametriza explicitamente:**
  - `--margens-horizontais`
  - `--vaos-chip-texto`
  - `--vaos-verticais`
  - `--alinhamentos-linhas`

**Achados manuais do usuário confirmados pelo código:**
1. `vao_entre_chips` mostrou efeito → CONFIRMADO (campo lido)
2. `vao_chip_texto` não mostrou efeito observável → CONFIRMADO (campo ignorado)
3. `margem_horizontal` não mostrou efeito observável → CONFIRMADO (campo ignorado)

**Contagem de testes pós H-0017:** 476/476 em 6 suítes:
- `teste_loader.py`: 79/79
- `teste_modelo.py`: 56/56
- `teste_renderizador.py`: 171/171
- `teste_demo.py`: 117/117
- `teste_diagnostico.py`: 28/28
- `teste_explorar_barra_de_menus.py`: 25/25

---

## Motivação

Após os ciclos H-0016 e H-0017, detectou-se manualmente que vários campos da
seção `barra_de_menus.distribuicao` do JSON canônico são ignorados silenciosamente
pelo renderer. O IMP-0017 e o QA do H-0017 registraram achados (QA-01, QA-02,
QA-N-01, QA-N-02) que devem ser corrigidos.

A omissão silenciosa de campos normativos viola o princípio do ADR-0014: o renderer
deve respeitar a distribuição declarada. Campos declarados que não têm efeito são
dívida técnica ativa — ou são implementados com semântica verificável, ou são
rejeitados deterministicamente, mas nunca podem ser ignorados em silêncio.

---

## Evidências dos achados (H-0017)

### Achados do QA H-0017 a tratar neste ciclo

**QA-01 (baixa)**: INV-4 do explorador verifica ordem apenas por pares
consecutivos. Em `coluna_a_coluna` com K≥2 linhas, chips não consecutivos que
compartilham uma linha (ex.: chip[0] e chip[2] na linha 0 com K=2) não têm
sua ordem relativa verificada. Recomendação: verificar todos os pares (i, j)
com i < j presentes em cada linha.

**QA-02 (baixa)**: `linhas.maximo=1` ausente na matriz padrão do explorador.
O IMP-0017 afirma incorretamente que `linhas.maximo=1` é exercitado na
"matriz padrão"; na realidade, só é coberto via CLI `--linhas-max 1`.
Recomendação: adicionar ao menos 1 cenário com `linhas.maximo=1` à matriz padrão.

**QA-N-01 (nota)**: `explorar_barra_de_menus.py:906` contém `or True`
tornando a condicional sempre verdadeira. Comportamento resultante é correto
(resumo sempre impresso), mas o código é confuso. Recomendação: substituir
por `print(resumo)` diretamente.

**QA-N-02 (nota)**: INV-2 (chip inventado) verificada implicitamente.
Não há varredura explícita da saída em busca de textos não declarados.
Recomendação: complementar com verificação explícita de tokens no formato
`[tecla] texto` contra a lista de chips declarados.

---

## Alerta: JSON duplicado

O usuário testou manualmente colando um exemplo com dois blocos `barra_de_menus`
idênticos em sequência. Este handoff registra explicitamente:

- O JSON real de tela deve conter **um único bloco `barra_de_menus`**.
- O ciclo H-0018 **não deve duplicar `barra_de_menus`** em nenhum arquivo JSON.
- Se qualquer arquivo real tiver a chave `barra_de_menus` duplicada, isso deve
  ser tratado como erro/bloqueio — parsers JSON descartam silenciosamente chaves
  duplicadas ou retornam o último valor, comportamento indefinido e proibido.
- A implementação não deve depender de comportamento ambíguo de parser para
  chaves duplicadas.
- Testes devem usar objetos sintéticos em memória ou fixtures controladas, nunca
  alterar JSONs ativos de produção.

---

## Leitura obrigatória

O executor deve ler na íntegra antes de tocar qualquer arquivo:

1. `scripts/docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md`
2. `scripts/docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md`
3. `scripts/docs/relatorios/RELATORIO_QA_H-0016_MIGRACAO_JSON_BARRA_DE_MENUS_HORIZONTAL_RESPONSIVA.md`
4. `scripts/docs/handoff/H-0017-script-exploracao-combinacoes-barra-de-menus.md`
5. `scripts/docs/relatorios/IMP-0017-script-exploracao-combinacoes-barra-de-menus.md`
6. `scripts/docs/relatorios/RELATORIO_QA_H-0017_SCRIPT_EXPLORACAO_COMBINACOES_BARRA_DE_MENUS.md`
7. `scripts/docs/adr/ADR-0014-barra-horizontal-termos-especificos.md`
8. `scripts/docs/contratos/contrato_barra_de_menus.md`
9. `scripts/docs/contratos/contrato_json_barra_de_menus.md`
10. `scripts/docs/contratos/contrato_chip.md`
11. `scripts/docs/contratos/contrato_tela_json.md`
12. `scripts/docs/contratos/contrato_processo_desenvolvimento.md`
13. `scripts/docs/NOMENCLATURA.md`
14. `scripts/tela/renderizador.py` (integralmente)
15. `scripts/tela/explorar_barra_de_menus.py` (integralmente)
16. `scripts/tela/teste_explorar_barra_de_menus.py` (integralmente)
17. `scripts/tela/teste_renderizador.py` (integralmente)
18. `scripts/config/telas/orquestrador.json`
19. Este handoff até o final.

---

## Seção JSON alvo

O handoff trata como superfície executável toda a seção:

```json
"barra_de_menus": {
  "distribuicao": {
    "modo": "horizontal_responsiva",
    "ordem": {
      "politica": "declaracao",
      "ancoras": {
        "primeiro": ["chip_esc"],
        "ultimo": ["chip_ajuda"]
      }
    },
    "tentativa_inicial": "linha_unica",
    "quebra": "multilinha_quando_nao_couber",
    "preenchimento_multilinha": "coluna_a_coluna",
    "preenchimentos_multilinha_suportados": [
      "coluna_a_coluna",
      "linha_a_linha"
    ],
    "linhas": {
      "minimo": 1,
      "maximo": 2,
      "preferir_menor_numero": true
    },
    "alinhamento_linhas": "esquerda",
    "espacamentos": {
      "margem_horizontal": {
        "minimo": 1,
        "maximo": null
      },
      "vao_chip_texto": {
        "minimo": 1,
        "maximo": 3
      },
      "vao_entre_chips": {
        "minimo": 2,
        "maximo": 6
      },
      "vao_entre_colunas": {
        "minimo": 2,
        "maximo": 8
      },
      "vao_vertical_entre_linhas": {
        "minimo": 0,
        "maximo": 0
      }
    },
    "colunas": {
      "largura": "por_maior_item_da_coluna",
      "subcolunas": {
        "chip": {
          "alinhamento": "esquerda"
        },
        "texto": {
          "alinhamento": "esquerda"
        }
      }
    },
    "overflow": {
      "quando_nao_couber": "erro_layout",
      "nao_omitir_chips": true,
      "nao_truncar_texto": true,
      "nao_reordenar": true
    }
  },
  "chips": [...]
}
```

---

## Lista completa de campos cobertos

O executor deve garantir cobertura explícita de **todos** os 30 campos listados
abaixo. Nenhum campo pode terminar com status "ignorado".

| # | Campo | Status exigido |
|---|-------|---------------|
| 1 | `distribuicao.modo` | implementado ou validado |
| 2 | `distribuicao.ordem.politica` | implementado ou validado |
| 3 | `distribuicao.ordem.ancoras.primeiro` | implementado ou validado |
| 4 | `distribuicao.ordem.ancoras.ultimo` | implementado ou validado |
| 5 | `distribuicao.tentativa_inicial` | implementado ou validado |
| 6 | `distribuicao.quebra` | implementado ou validado |
| 7 | `distribuicao.preenchimento_multilinha` | implementado |
| 8 | `distribuicao.preenchimentos_multilinha_suportados` | implementado |
| 9 | `distribuicao.linhas.minimo` | implementado ou rejeitado_deterministicamente |
| 10 | `distribuicao.linhas.maximo` | implementado |
| 11 | `distribuicao.linhas.preferir_menor_numero` | implementado ou rejeitado_deterministicamente |
| 12 | `distribuicao.alinhamento_linhas` | implementado (esquerda) ou rejeitado_deterministicamente (outros) |
| 13 | `distribuicao.espacamentos.margem_horizontal.minimo` | implementado |
| 14 | `distribuicao.espacamentos.margem_horizontal.maximo` | implementado ou validado |
| 15 | `distribuicao.espacamentos.vao_chip_texto.minimo` | implementado |
| 16 | `distribuicao.espacamentos.vao_chip_texto.maximo` | implementado ou validado |
| 17 | `distribuicao.espacamentos.vao_entre_chips.minimo` | implementado (já existe) |
| 18 | `distribuicao.espacamentos.vao_entre_chips.maximo` | implementado ou validado |
| 19 | `distribuicao.espacamentos.vao_entre_colunas.minimo` | implementado (já existe) |
| 20 | `distribuicao.espacamentos.vao_entre_colunas.maximo` | implementado ou validado |
| 21 | `distribuicao.espacamentos.vao_vertical_entre_linhas.minimo` | implementado ou rejeitado_deterministicamente |
| 22 | `distribuicao.espacamentos.vao_vertical_entre_linhas.maximo` | implementado ou rejeitado_deterministicamente |
| 23 | `distribuicao.colunas.largura` | implementado ou validado |
| 24 | `distribuicao.colunas.subcolunas.chip.alinhamento` | implementado ou rejeitado_deterministicamente |
| 25 | `distribuicao.colunas.subcolunas.texto.alinhamento` | implementado ou rejeitado_deterministicamente |
| 26 | `distribuicao.overflow.quando_nao_couber` | implementado (já existe) |
| 27 | `distribuicao.overflow.nao_omitir_chips` | implementado (já existe) |
| 28 | `distribuicao.overflow.nao_truncar_texto` | implementado (já existe) |
| 29 | `distribuicao.overflow.nao_reordenar` | implementado (já existe) |
| 30 | `barra_de_menus.chips[]` | implementado (já existe) |

---

## Semântica operacional por campo

### 1. `vao_chip_texto`

**Bug atual**: `_texto_chip_barra` sempre gera `"[{tecla}] {texto}"` com 1 espaço
fixo entre `]` e o texto, ignorando `vao_chip_texto.minimo`.

**Semântica exigida**:

```
vao_chip_texto.minimo = 1:
  "[Esc] Sair"           (1 espaço entre ] e Sair)

vao_chip_texto.minimo = 3:
  "[Esc]   Sair"         (3 espaços entre ] e Sair)

vao_chip_texto.minimo = 10:
  "[Esc]          Sair"  (10 espaços entre ] e Sair)
```

O formato de chip deve tornar-se: `"[{tecla}]{padding}{texto}"` onde
`padding = " " * vao_chip_texto.minimo`.

**Atenção ao cálculo de comprimento da linha única**: após esta correção, o
comprimento de um chip no modo linha única passa de `len("[{tecla}] {texto}")` para
`len("[{tecla}]") + vao_chip_texto.minimo + len("{texto}")`. O cálculo de encaixe
em `content_w` e nos modos multilinha deve usar o comprimento real do chip com o
`vao_chip_texto.minimo` correto.

**Regra de validação**: `vao_chip_texto.minimo` deve ser `int >= 1`. Se ausente,
usar o default do objeto canônico (1). Se inválido (não-int, `< 1`), levantar
`RenderizadorErro` determinístico.

**`vao_chip_texto.maximo`**: não usado no cálculo de layout neste ciclo (o layout
usa o mínimo para maximizar o encaixe); mas deve ser validado se presente
(deve ser `int >= vao_chip_texto.minimo` ou `null`). Se inválido, `RenderizadorErro`.

### 2. `margem_horizontal`

**Bug atual**: nenhum padding lateral é aplicado; o conteúdo começa imediatamente
no primeiro caractere de `content_w`.

**Semântica exigida**:

```
margem_horizontal.minimo = 1:
 [Esc] Sair  [?] Ajuda        (1 espaço antes do primeiro item)

margem_horizontal.minimo = 4:
    [Esc] Sair  [?] Ajuda     (4 espaços antes do primeiro item)
```

A margem esquerda mínima deve aparecer antes do primeiro item em cada linha da
barra. A largura disponível para chips deve ser reduzida por `2 * margem_horizontal.minimo`
(esquerda + direita) no cálculo de encaixe:

```
largura_util = content_w - 2 * margem_horizontal.minimo
```

Se `largura_util <= 0`, levantar `RenderizadorErro` determinístico antes de
tentar qualquer layout.

A margem é aplicada prefixando cada linha de conteúdo da barra com
`" " * margem_horizontal.minimo`. Quando `alinhamento_linhas = "esquerda"`, a
sobra adicional (após margem e chips) fica à direita naturalmente.

**Regra de validação**: `margem_horizontal.minimo` deve ser `int >= 0`. Se ausente,
usar o default (1). Se inválido (não-int, `< 0`), `RenderizadorErro`. Se
`margem_horizontal.maximo` for `null`, sem limite superior; se for int, deve ser
`>= minimo`.

**Overflow com margem alta**: se `margem_horizontal.minimo` for tão alto que
`largura_util` não comporte os chips, o renderer deve tentar multilinha com
`largura_util` como largura disponível; se ainda não couber dentro de
`linhas.maximo`, gerar `RenderizadorErro` com `"erro_layout"`.

### 3. `vao_entre_chips`

**Semântica já implementada** (campo lido). Verificação: a separação mínima entre
chips em linha única deve ser exatamente `vao_entre_chips.minimo` espaços.

```
vao_entre_chips = 2:
[Esc] Sair  [?] Ajuda

vao_entre_chips = 6:
[Esc] Sair      [?] Ajuda
```

O teste isolado deve confirmar que alterar `vao_entre_chips.minimo` altera a saída.

### 4. `vao_entre_colunas`

**Semântica já implementada** (campo lido) para modo `coluna_a_coluna`. O teste
isolado deve confirmar efeito em cenário multilinha.

### 5. `vao_vertical_entre_linhas`

**Bug atual**: o campo nunca é lido. O renderer sempre gera linhas da barra sem
espaçamento vertical entre elas.

**Decisão obrigatória**: o executor deve escolher **uma** das opções abaixo e
implementar a escolha com teste determinístico:

**Opção A — Implementar efeito visual quando valor > 0**:
- Para cada linha da barra, inserir `vao_vertical_entre_linhas.minimo` linhas
  vazias entre elas (strings `""`).
- O valor atual nos JSONs ativos é 0, portanto o comportamento padrão não muda.
- Deve haver teste confirmando efeito com `minimo > 0`.

**Opção B — Rejeitar valores > 0 deterministicamente**:
- Se `vao_vertical_entre_linhas.minimo > 0` ou `maximo > 0`, levantar
  `RenderizadorErro` com mensagem descritiva:
  `"vao_vertical_entre_linhas com valor > 0 nao suportado neste ciclo"`.
- O valor `0` (nos JSONs ativos) continua sendo aceito silenciosamente.
- Deve haver teste confirmando o erro para `minimo = 1`.

A decisão entre A e B deve ser documentada no IMP-0018. O executor pode escolher
qualquer uma. A Opção A é preferida se a implementação for simples. Se houver
qualquer dúvida arquitetural sobre inserção de linhas vazias dentro da caixa da
barra, usar a Opção B.

**Independentemente da opção escolhida**: o campo deve ser lido e a decisão deve
ser determinística. Não pode ficar silenciosamente ignorado.

### 6. `alinhamento_linhas`

**Bug atual**: o campo nunca é lido. O alinhamento é sempre à esquerda por comportamento
implícito (`ljust`/natural).

**Valores normativos** (ADR-0014):
- `"esquerda"`: chips alinhados à esquerda, sobra à direita.
- `"centro"`: sobra dividida entre margem esquerda e direita.
- `"direita"`: sobra à esquerda, preservando margem direita mínima.
- `"justificado"`: sobra distribuída entre vãos até máximos; sobra adicional
  vai para margens.

**Decisão obrigatória para H-0018**:

- `"esquerda"` deve continuar funcionando (comportamento já é esquerda).
- `"centro"`, `"direita"` e `"justificado"` **não podem ser ignorados silenciosamente**.

O executor deve escolher uma das opções para cada valor não-esquerda:
- **Implementar**: se a implementação for local e não exigir nova norma.
- **Rejeitar deterministicamente**: levantar `RenderizadorErro` com mensagem
  `"alinhamento_linhas '{valor}' nao suportado neste ciclo"`.

Se `"centro"`, `"direita"` e `"justificado"` exigirem decisão arquitetural nova
não coberta pelo ADR-0014, bloquear com `ARCHITECTURE_REVIEW_REQUIRED`.

Deve haver teste para `"esquerda"` (passa) e para cada valor não-suportado
(rejeição determinística ou implementação verificável).

### 7. `linhas.minimo` e `preferir_menor_numero`

**Bug atual**: `linhas.minimo` é validado como `int >= 1` (H-0016 PR-M-03), mas não
é usado no algoritmo de layout. `preferir_menor_numero` nunca é lido.

**Semântica exigida para `linhas.minimo`**:

O renderer já itera de `2` a `linhas.maximo` tentando o menor número de linhas
(1 antes da iteração). Quando `linhas.minimo > 1`, o renderer não deve retornar
resultado com menos linhas que `minimo`. Se `minimo = 2` e `maximo = 2`, o renderer
deve pular a tentativa de linha única e ir direto para 2 linhas.

**Implementação**: antes da tentativa de linha única, verificar se `minimo <= 1`.
Se `minimo >= 2`, pular a tentativa de linha única e iniciar a iteração multilinha
em `minimo`. A iteração multilinha fica de `max(2, minimo)` até `maximo`.

**Regra**: `linhas.minimo` já está validado como int ≥ 1. Se `minimo > maximo`,
já é erro (PR-M-03). O executor não precisa re-validar, mas deve usar o valor
no algoritmo.

**Semântica exigida para `preferir_menor_numero`**:

O executor deve escolher uma das opções:
- **Implementar**: `preferir_menor_numero = true` (comportamento atual implícito:
  itera de menor para maior); `preferir_menor_numero = false` (itera de `maximo`
  para `minimo`, i.e., preferir mais linhas).
- **Rejeitar `false` deterministicamente**: aceitar `true` (comportamento atual);
  levantar `RenderizadorErro` com mensagem
  `"preferir_menor_numero=false nao suportado neste ciclo"` quando `false`.

Deve haver validação de que o campo é bool (`isinstance(valor, bool)`). Se não-bool,
`RenderizadorErro`.

Deve haver testes para:
- `linhas.maximo = 1` (linha única obrigatória → erro_layout se não couber)
- `linhas.maximo = 2` (padrão)
- `linhas.maximo = 3` em cenário sintético
- `linhas.minimo > 1` (pula tentativa de linha única)
- `linhas.maximo < linhas.minimo` (erro, já coberto em H-0016)
- `preferir_menor_numero = true`
- `preferir_menor_numero = false` (implementado ou rejeitado deterministicamente)

### 8. `preenchimento_multilinha` e `preenchimentos_multilinha_suportados`

**Semântica já implementada** para `coluna_a_coluna` e `linha_a_linha`.

**Exigências adicionais**:
- Testes de padrão de distribuição, não apenas "passou": confirmar que
  `coluna_a_coluna` distribui coluna-a-coluna (verificável pela posição dos chips
  nas linhas) e que `linha_a_linha` distribui linha-a-linha.
- `preenchimentos_multilinha_suportados` deve ser validado conforme H-0016: o
  valor ativo de `preenchimento_multilinha` deve estar na lista; se não estiver,
  `RenderizadorErro`.
- Valor inválido em `preenchimento_multilinha` deve gerar `RenderizadorErro`
  (já implementado em H-0016).
- Deve haver teste de `linha_a_linha` com cenário que forçadamente produz 2 linhas.

### 9. `colunas.largura`

**Bug atual**: o valor `"por_maior_item_da_coluna"` está hardcoded no comportamento
de `_montar_coluna_a_coluna`; o campo não é lido.

**Decisão exigida**:
- O executor deve ler o campo `colunas.largura`.
- Se o valor for `"por_maior_item_da_coluna"`, continuar o comportamento atual.
- Se o valor for qualquer outro string ou inválido, levantar `RenderizadorErro`
  com mensagem:
  `"colunas.largura '{valor}' nao suportado neste ciclo; valor aceito: 'por_maior_item_da_coluna'"`.
- Se o campo estiver ausente, usar `"por_maior_item_da_coluna"` como default
  (sem erro).

Deve haver teste para valor inválido em `colunas.largura`.

### 10. `subcolunas.chip.alinhamento` e `subcolunas.texto.alinhamento`

**Bug atual**: os campos nunca são lidos. O alinhamento é sempre à esquerda.

**Decisão exigida**:
- O executor deve ler os campos.
- Se o valor for `"esquerda"`, continuar o comportamento atual.
- Se o valor for qualquer outro string ou inválido (incluindo `"centro"` e
  `"direita"`), levantar `RenderizadorErro` com mensagem:
  `"subcolunas.{chip|texto}.alinhamento '{valor}' nao suportado neste ciclo; valor aceito: 'esquerda'"`.
- Se o campo estiver ausente, usar `"esquerda"` como default (sem erro).

Deve haver testes para valor inválido em cada subcampo.

### 11. `overflow` (flags)

**Semântica já implementada**. Validação defensiva para:
- `quando_nao_couber` diferente de `"erro_layout"` → `RenderizadorErro`.
- `nao_omitir_chips`, `nao_truncar_texto`, `nao_reordenar` não-bool → `RenderizadorErro`.

**Exigências adicionais neste ciclo**:
- Não há novos valores a implementar para overflow.
- Mas deve haver testes explícitos de que `nao_omitir_chips = false`,
  `nao_truncar_texto = false`, `nao_reordenar = false` geram `RenderizadorErro`
  (valores booleanos mas contrários ao esperado). O H-0016 validava apenas que
  os campos fossem `bool`; este ciclo exige que os valores `true` sejam obrigatórios.

**Decisão**: o executor deve adicionar validação de que os três flags de overflow
sejam exatamente `true`. Valor `false` deve gerar `RenderizadorErro`:
`"overflow.{flag} deve ser true; recebido: false"`.

### 12. Valores exagerados (casos extremos)

Cenários com valores exagerados devem produzir resultado determinístico, nunca
silêncio:

```json
"margem_horizontal": {"minimo": 50, "maximo": null}
```
→ `largura_util = content_w - 100 <= 0` → `RenderizadorErro` imediato.

```json
"vao_chip_texto": {"minimo": 10, "maximo": 30}
```
→ texto de chip com 10 espaços extras → linha mais longa → pode forçar multilinha
ou `erro_layout`.

```json
"vao_entre_chips": {"minimo": 20, "maximo": 46}
```
→ linha única muito longa → multilinha ou `erro_layout`.

Todos devem ser testados e cobertos em teste isolado do renderer e no explorador.

---

## Objetivo técnico do H-0018

1. **Auditar no código**: verificar quais campos de `distribuicao` o renderer lê,
   aplica, ignora ou apenas valida. O executor deve fazer isso lendo
   `renderizador.py` integralmente antes de implementar.
2. **Corrigir o renderer**: aplicar os campos que estão sendo ignorados,
   conforme a semântica operacional descrita acima.
3. **Criar testes isolados**: um teste por campo ou grupo de campos, detectando
   efeito observável ou validação determinística.
4. **Atualizar o explorador**: adicionar parâmetros CLI para todos os campos de
   espaçamento relevantes.
5. **Atualizar testes do explorador**: cobrir os novos parâmetros e os achados
   do QA H-0017 (QA-01, QA-02, QA-N-01, QA-N-02).
6. **Criar relatório IMP-0018**.

---

## Correções exigidas dos achados H-0017

**QA-01 → Novo comportamento obrigatório**:
Substituir a verificação INV-4 de pares consecutivos por verificação de todos os
pares (i, j) com i < j que estão presentes em cada linha:

```python
# Para cada linha, extrair os índices de chips presentes
# Para todo par (i, j) com i < j:
#   se chips[i] e chips[j] estão na linha, verificar pos(chips[i]) < pos(chips[j])
```

**QA-02 → Novo cenário obrigatório na matriz padrão**:
Adicionar ao menos 1 cenário com `linhas.maximo = 1` à `_matriz_padrao()` do
explorador. Exemplo:

```
C15: 4 chips médios, content_w = 20, linhas.maximo = 1.
     Esperado: RenderizadorErro com "erro_layout" (overflow forçado com max=1).
     Classificado como erro esperado.
```

**QA-N-01 → Limpeza obrigatória**:
Remover `or True` da condição de impressão do resumo. Substituir pela impressão
direta: `print(resumo)`.

**QA-N-02 → Nova verificação obrigatória (INV-2 explícita)**:
Adicionar verificação explícita de tokens não declarados na saída renderizada.
Para cada linha da barra renderizada, verificar que todos os tokens no formato
`[tecla] texto` (ou `[tecla]texto` com qualquer espaçamento) correspondem a
algum chip declarado.

Implementação sugerida:

```python
# Para cada linha da saída:
#   varrer por tokens que começam com "[" e terminam com "]"
#   confirmar que cada tecla extraída pertence a algum chip declarado
#   se encontrar tecla não declarada → violação de INV-2
```

**Novo QA-03 (exigido neste ciclo)**:
Adicionar variação e teste explícito de `vao_chip_texto` no explorador.

**Novo QA-04 (exigido neste ciclo)**:
Adicionar variação e teste explícito de `margem_horizontal` no explorador.

---

## Atualização do explorador

O explorador `scripts/tela/explorar_barra_de_menus.py` deve ser atualizado para
aceitar/variar os novos campos:

### Novos parâmetros CLI obrigatórios

```
--margens-horizontais
    Lista de valores de margem_horizontal.minimo a testar, separadas por vírgula.
    Exemplo: --margens-horizontais 0,1,4,50
    Default: [1] (valor padrão do canônico)

--vaos-chip-texto
    Lista de valores de vao_chip_texto.minimo a testar, separadas por vírgula.
    Exemplo: --vaos-chip-texto 1,3,10
    Default: [1]

--vaos-entre-chips
    Lista de valores de vao_entre_chips.minimo a testar, separadas por vírgula.
    Exemplo: --vaos-entre-chips 2,6,20
    Default: [2]

--vaos-entre-colunas
    Lista de valores de vao_entre_colunas.minimo a testar, separadas por vírgula.
    Exemplo: --vaos-entre-colunas 2,8
    Default: [2]
```

Os parâmetros `--vaos-verticais` (vao_vertical_entre_linhas) e
`--alinhamentos-linhas` são opcionais neste ciclo: se a implementação do renderer
para esses campos for determinística, o explorador deve incluí-los; se o renderer
os rejeitar deterministicamente, o explorador deve documentá-los como cenário de
erro esperado.

### Atualização de `_fabricar_distribuicao`

A função deve receber e usar `vao_chip_texto` e `margem_horizontal`:

```python
def _fabricar_distribuicao(
    preenchimento="coluna_a_coluna",
    linhas_maximo=2,
    vao_entre_chips=2,
    vao_entre_colunas=2,
    vao_chip_texto=1,
    margem_horizontal=1,
    ancoras=None,
):
    ...
    "espacamentos": {
        "margem_horizontal": {"minimo": margem_horizontal, "maximo": None},
        "vao_chip_texto":    {"minimo": vao_chip_texto, "maximo": 3},
        ...
    }
```

### Atualização da `_verificar_invariantes`

Substituir INV-4 pela verificação de todos os pares presentes em cada linha
(ver QA-01 acima).

Adicionar INV-2 explícita (ver QA-N-02 acima).

### Correção do `or True`

Substituir:
```python
if modo_saida == "resumo" or True:
    print(resumo)
```
por:
```python
print(resumo)
```

### Cenário C15 obrigatório na matriz padrão

Adicionar cenário com `linhas.maximo = 1` à `_matriz_padrao()`.

---

## Atualização dos testes do renderer

O arquivo `scripts/tela/teste_renderizador.py` deve receber novos testes para
todos os campos cobertos neste ciclo. Os testes existentes devem continuar passando.

### Testes obrigatórios (novos ou a reforçar)

Todos os testes abaixo devem ser adicionados. O executor pode criar uma nova classe
`TestDistribuicaoH0018` ou integrar nos blocos existentes, seguindo o padrão
procedural da suíte (`_registrar`).

```
1. test_vao_chip_texto_altera_distancia:
   Alterar apenas vao_chip_texto.minimo de 1 para 3.
   Confirmar que o chip renderizado contém 3 espaços entre "]" e o texto.
   Ex.: chip com tecla="Esc", texto="Sair", vao=3 → "[Esc]   Sair"

2. test_vao_chip_texto_10_espaco_extra:
   vao_chip_texto.minimo = 10.
   Confirmar 10 espaços entre "]" e o texto.

3. test_vao_chip_texto_altera_comprimento_linha:
   Confirmar que vao_chip_texto maior resulta em linha mais longa ou em
   quebra multilinha quando a linha única não couber.

4. test_margem_horizontal_altera_padding:
   Alterar apenas margem_horizontal.minimo de 1 para 4.
   Confirmar que cada linha da barra começa com pelo menos 4 espaços.

5. test_margem_horizontal_participa_do_overflow:
   margem_horizontal.minimo = 50 em content_w = 39.
   Confirmar RenderizadorErro (largura_util <= 0 → erro antes do layout).

6. test_margem_horizontal_0_permitido:
   margem_horizontal.minimo = 0.
   Confirmar que não gera erro e que a linha não começa com espaço extra.

7. test_vao_entre_chips_altera_distancia:
   Confirmar que aumentar vao_entre_chips.minimo de 2 para 6 produz saída
   mais longa em linha única.

8. test_vao_entre_colunas_altera_distancia_multilinha:
   Em cenário que força multilinha (coluna_a_coluna).
   Confirmar que aumentar vao_entre_colunas.minimo altera o layout.

9. test_vao_vertical_entre_linhas_implementado_ou_rejeitado:
   vao_vertical_entre_linhas.minimo = 1.
   Confirmar: (Opção A) saída com linha vazia entre linhas da barra; ou
   (Opção B) RenderizadorErro com mensagem descritiva.
   O teste deve ser determinístico.

10. test_alinhamento_linhas_esquerda_funciona:
    alinhamento_linhas = "esquerda".
    Confirmar que a saída é produzida normalmente (esquerda é o padrão).

11. test_alinhamento_linhas_nao_suportado_erro:
    alinhamento_linhas = "centro".
    Confirmar RenderizadorErro com "'centro' nao suportado" (se rejeitado).
    Ou confirmar saída correta com chips centrados (se implementado).

12. test_linhas_minimo_maior_que_1_pula_linha_unica:
    linhas.minimo = 2, linhas.maximo = 2, chips que caberiam em linha única.
    Confirmar que o resultado tem 2 linhas (não 1), pois minimo = 2.

13. test_linhas_maximo_1_overflow_se_nao_couber:
    linhas.maximo = 1.
    Chips que não cabem em linha única.
    Confirmar RenderizadorErro com "erro_layout".

14. test_linhas_maximo_1_ok_se_couber:
    linhas.maximo = 1.
    Chips que cabem em linha única.
    Confirmar resultado com 1 linha.

15. test_linhas_maximo_3_tres_linhas:
    linhas.maximo = 3, chips e largura que forçam 3 linhas.
    Confirmar que o renderer usa 3 linhas sem erro.

16. test_preferir_menor_numero_false_implementado_ou_rejeitado:
    preferir_menor_numero = false.
    Confirmar: (opção A) ordem de iteração invertida ou
    (opção B) RenderizadorErro com mensagem descritiva.

17. test_preferir_menor_numero_nao_bool_erro:
    preferir_menor_numero = "sim" (string não-bool).
    Confirmar RenderizadorErro.

18. test_colunas_largura_invalido_erro:
    colunas.largura = "outro_valor".
    Confirmar RenderizadorErro com mensagem descritiva.

19. test_colunas_largura_ausente_usa_default:
    colunas ausente ou largura ausente.
    Confirmar comportamento normal (usa por_maior_item_da_coluna).

20. test_subcoluna_chip_alinhamento_invalido_erro:
    subcolunas.chip.alinhamento = "centro".
    Confirmar RenderizadorErro.

21. test_subcoluna_texto_alinhamento_invalido_erro:
    subcolunas.texto.alinhamento = "direita".
    Confirmar RenderizadorErro.

22. test_overflow_nao_omitir_chips_false_erro:
    overflow.nao_omitir_chips = false.
    Confirmar RenderizadorErro.

23. test_overflow_nao_truncar_texto_false_erro:
    overflow.nao_truncar_texto = false.
    Confirmar RenderizadorErro.

24. test_overflow_nao_reordenar_false_erro:
    overflow.nao_reordenar = false.
    Confirmar RenderizadorErro.

25. test_preenchimentos_multilinha_suportados_valida_preenchimento:
    preenchimento_multilinha = "coluna_a_coluna" e
    preenchimentos_multilinha_suportados = ["linha_a_linha"].
    Confirmar RenderizadorErro (ativo não está na lista suportada).

26. test_valores_exagerados_margem_50:
    margem_horizontal.minimo = 50, content_w = 39.
    Confirmar RenderizadorErro determinístico.

27. test_valores_exagerados_vao_chip_texto_10:
    vao_chip_texto.minimo = 10, chips suficientes para forçar multilinha
    ou erro_layout.
    Confirmar que o resultado é determinístico (não silêncio).

28. test_valores_exagerados_vao_entre_chips_20:
    vao_entre_chips.minimo = 20, content_w pequeno.
    Confirmar multilinha ou erro_layout (não silêncio).
```

---

## Testes obrigatórios do explorador

O arquivo `scripts/tela/teste_explorar_barra_de_menus.py` deve ser atualizado
com os seguintes casos novos:

```
11. test_vao_chip_texto_3_altera_saida:
    _linhas_barra com vao_chip_texto.minimo=3.
    Confirmar que a saída contém chips com 3 espaços entre "]" e texto.

12. test_margem_horizontal_4_altera_saida:
    _linhas_barra com margem_horizontal.minimo=4.
    Confirmar que cada linha começa com 4 espaços.

13. test_margem_horizontal_overflow:
    _linhas_barra com margem_horizontal.minimo=50, content_w=39.
    Confirmar RenderizadorErro.

14. test_matriz_padrao_inclui_linhas_max_1:
    Executar explorar_barra_de_menus.py sem argumentos (subprocess).
    Verificar que o resumo contém "1:" na seção "Por linhas.maximo".

15. test_inv4_verifica_pares_nao_consecutivos:
    Cenário coluna_a_coluna com 4 chips e K=2.
    Confirmar que INV-4 verificaria chip[0] antes de chip[2] na linha 0
    (verificação via chamada direta a _verificar_invariantes ou verificação
    do código-fonte da função).

16. test_inv2_detecta_token_nao_declarado:
    Cenário sintético onde a saída contém texto de chip não declarado.
    Confirmar que _verificar_invariantes detecta a violação de INV-2
    (pode ser verificado por inspeção de código ou cenário controlado).

17. test_or_true_removido:
    Verificar que o código-fonte de explorar_barra_de_menus.py não contém
    "or True" (inspeção direta do arquivo).

18. test_cli_margens_horizontais:
    subprocess.run com --margens-horizontais 1,4.
    Confirmar exit code 0.

19. test_cli_vaos_chip_texto:
    subprocess.run com --vaos-chip-texto 1,3.
    Confirmar exit code 0.
```

Os 10 casos anteriores do teste (1-10) devem continuar passando.

---

## Escopo positivo

O H-0018 pode e deve implementar:

```
- Corrigir _texto_chip_barra em renderizador.py para usar vao_chip_texto.minimo.
- Adicionar cálculo de margem_horizontal em _linhas_barra.
- Implementar ou rejeitar deterministicamente: vao_vertical_entre_linhas,
  alinhamento_linhas, preferir_menor_numero.
- Implementar leitura e validação de colunas.largura,
  subcolunas.chip.alinhamento, subcolunas.texto.alinhamento.
- Implementar uso de linhas.minimo no algoritmo de layout.
- Adicionar validação de overflow flags false.
- Adicionar novos testes em teste_renderizador.py.
- Atualizar explorar_barra_de_menus.py com novos parâmetros CLI e correções
  dos achados H-0017 (QA-01, QA-02, QA-N-01, QA-N-02).
- Atualizar teste_explorar_barra_de_menus.py com novos casos.
- Criar IMP-0018.
```

---

## Escopo negativo

O H-0018 **NÃO deve** implementar:

```
- Alteração de ADR (nenhuma).
- Alteração de contrato (nenhuma).
- Alteração de NOMENCLATURA.md.
- Alteração dos JSONs ativos de produção (orquestrador.json, grupo_minimo.json,
  destino_minimo.json, stub_b.json) como caminho principal.
- Duplicação de barra_de_menus nos JSONs.
- Nova semântica não documentada no ADR-0014 ou contratos existentes.
- Composição horizontal do corpo.
- Distribuição de altura entre elementos do corpo.
- Correção do preenchimento vertical do H-0015.
- Console real.
- Paginação.
- Filtros.
- Seleção.
- Registry novo de ações.
- Registry novo de telas.
- Mudança no lancador.
```

Alterar JSONs ativos para testes manuais temporários é proibido. Testes devem usar
objetos sintéticos em memória ou fixtures controladas dentro dos testes.

---

## Arquivos permitidos

O executor pode criar ou editar **somente** os seguintes arquivos:

```
scripts/tela/renderizador.py
scripts/tela/teste_renderizador.py
scripts/tela/explorar_barra_de_menus.py
scripts/tela/teste_explorar_barra_de_menus.py
scripts/docs/relatorios/IMP-0018-cobertura-executavel-distribuicao-barra-de-menus.md
```

Os dois relatórios abaixo são criados em etapas futuras (auditoria e QA), não
pelo implementador:

```
scripts/docs/relatorios/RELATORIO_AUDITORIA_H-0018_HANDOFF.md  (auditoria)
scripts/docs/relatorios/RELATORIO_QA_H-0018_COBERTURA_EXECUTAVEL_DISTRIBUICAO_BARRA_DE_MENUS.md  (QA final)
```

---

## Arquivos proibidos

O executor **não deve tocar** em nenhum dos seguintes arquivos:

```
scripts/docs/adr/                      ← todos os ADRs
scripts/docs/contratos/                ← todos os contratos
scripts/docs/NOMENCLATURA.md
scripts/docs/INDICE.md

scripts/config/telas/                  ← todos os JSONs de tela ativos
scripts/config/estilo.json
scripts/config/lancador.json
scripts/config/layout_console.json

scripts/tela/loader.py
scripts/tela/modelo.py
scripts/tela/demo.py
scripts/tela/diagnostico.py

scripts/tela/teste_loader.py
scripts/tela/teste_modelo.py
scripts/tela/teste_demo.py
scripts/tela/teste_diagnostico.py
```

Se qualquer arquivo desta lista precisar ser alterado para concluir a implementação,
o executor deve parar com:

```
ARCHITECTURE_REVIEW_REQUIRED
```

---

## Critérios de aceite

O ciclo H-0018 é considerado **concluído** quando todos os critérios abaixo forem
atendidos:

```
 1. vao_chip_texto.minimo altera visualmente a distância entre "[tecla]" e "texto"
    do chip na saída renderizada.
 2. margem_horizontal.minimo altera visualmente a margem esquerda de cada linha
    da barra renderizada.
 3. margem_horizontal.minimo participa do cálculo de overflow (margem alta →
    largura_util menor → multilinha ou erro_layout).
 4. vao_entre_chips.minimo continua funcionando (campo já existia).
 5. vao_entre_colunas.minimo continua funcionando em modo multilinha.
 6. vao_vertical_entre_linhas não é ignorado silenciosamente: é implementado
    (linhas vazias entre linhas da barra) ou rejeitado deterministicamente.
 7. alinhamento_linhas = "esquerda" continua funcionando.
 8. alinhamento_linhas com valores não-suportados gera RenderizadorErro (ou é
    implementado deterministicamente).
 9. linhas.minimo > 1 pula a tentativa de linha única e começa em minimo linhas.
10. linhas.maximo = 1 com chips que não cabem em linha única gera erro_layout.
11. linhas.maximo = 1 com chips que cabem em linha única produz 1 linha.
12. preferir_menor_numero não é ignorado silenciosamente: é implementado ou
    rejeitado deterministicamente para valor false.
13. preenchimento_multilinha = "coluna_a_coluna" distribui corretamente
    (padrão coluna-a-coluna verificável).
14. preenchimento_multilinha = "linha_a_linha" distribui corretamente
    (padrão linha-a-linha verificável).
15. preenchimentos_multilinha_suportados valida que o preenchimento ativo está
    na lista.
16. colunas.largura é lido e validado; valor inválido gera RenderizadorErro.
17. subcolunas.chip.alinhamento é lido; valor inválido gera RenderizadorErro.
18. subcolunas.texto.alinhamento é lido; valor inválido gera RenderizadorErro.
19. overflow.quando_nao_couber continua gerando erro_layout (já existia).
20. overflow.nao_omitir_chips = false gera RenderizadorErro.
21. overflow.nao_truncar_texto = false gera RenderizadorErro.
22. overflow.nao_reordenar = false gera RenderizadorErro.
23. Valores exagerados (margem=50, vao_chip_texto=10, vao_entre_chips=20) geram
    efeito visual, multilinha ou erro_layout — nunca silêncio.
24. Explorador varia margem_horizontal.minimo via --margens-horizontais.
25. Explorador varia vao_chip_texto.minimo via --vaos-chip-texto.
26. Explorador varia vao_entre_chips.minimo via --vaos-entre-chips.
27. Explorador varia vao_entre_colunas.minimo via --vaos-entre-colunas.
28. INV-4 do explorador verifica todos os pares (i, j) com i < j presentes em
    cada linha.
29. INV-2 do explorador detecta tokens renderizados não declarados.
30. Matriz padrão do explorador inclui cenário com linhas.maximo = 1.
31. `or True` removido do explorador.
32. Testes existentes (476 verificações em 6 suítes) continuam passando.
33. Nenhum JSON ativo é alterado.
34. Nenhum contrato/ADR/NOMENCLATURA é alterado.
35. Nenhum __pycache__ ou .pyc fica no workspace.
36. Nenhuma chave barra_de_menus duplicada em nenhum JSON real.
```

---

## Testes obrigatórios

### Suítes existentes (devem continuar passando)

```bash
cd scripts
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
python tela/teste_diagnostico.py
python tela/teste_explorar_barra_de_menus.py
```

### Execuções manuais obrigatórias do explorador

```bash
cd scripts

# Execução padrão (deve incluir linhas.maximo=1 no resumo)
python tela/explorar_barra_de_menus.py

# Cobertura dos novos campos de espaçamento
python tela/explorar_barra_de_menus.py \
  --modo-saida resumo \
  --larguras 40,80,120 \
  --chips 2,4,8 \
  --linhas-max 1,2,3 \
  --preenchimentos coluna_a_coluna,linha_a_linha \
  --margens-horizontais 0,1,4,50 \
  --vaos-chip-texto 1,3,10 \
  --vaos-entre-chips 2,6,20 \
  --vaos-entre-colunas 2,8

# Modo detalhado com erros — deve mostrar erros de margem e vao exagerados
python tela/explorar_barra_de_menus.py \
  --modo-saida detalhado \
  --mostrar-erros \
  --limite-casos 50
```

Se a CLI final usar nomes de parâmetros diferentes dos acima, o executor deve
documentar os nomes reais no IMP-0018.

---

## Relatório de implementação

O executor deve criar:

```
scripts/docs/relatorios/IMP-0018-cobertura-executavel-distribuicao-barra-de-menus.md
```

Com a seguinte estrutura:

```markdown
# IMP-0018 — Cobertura executável da distribuição da barra_de_menus

## Status

## Resumo

## Arquivos alterados/criados

## Campos da distribuição cobertos

(Tabela com todos os 30 campos e status:
 implementado | validado | rejeitado_deterministicamente | fora_de_escopo_com_bloqueio)

## Correções no renderer

## Decisões locais

(Registrar: qual opção foi escolhida para vao_vertical_entre_linhas,
 alinhamento_linhas, preferir_menor_numero)

## Testes do renderer adicionados

## Atualizações no explorador

## Testes do explorador adicionados

## Tratamento dos achados H-0017

(QA-01, QA-02, QA-N-01, QA-N-02)

## Execuções manuais

(Saída completa das execuções obrigatórias)

## Resultados

## Limitações conhecidas

## Confirmação de fora de escopo
```

A seção "Campos da distribuição cobertos" deve ter **todos os 30 campos** listados
na seção "Lista completa de campos cobertos" deste handoff, com o status de cada
um. Nenhum campo pode ter status "ignorado".

---

## Critérios de bloqueio — ARCHITECTURE_REVIEW_REQUIRED

O executor deve bloquear com `ARCHITECTURE_REVIEW_REQUIRED` se:

```
1. For necessário alterar ADR, contrato ou NOMENCLATURA.
2. Algum campo da distribuição exigir semântica nova não coberta pelo
   ADR-0014, contratos ou este handoff.
3. For necessário alterar os JSONs ativos de produção.
4. For necessário alterar loader.py, modelo.py, demo.py ou diagnostico.py
   (fonte).
5. For necessário alterar teste_loader.py, teste_modelo.py, teste_demo.py ou
   teste_diagnostico.py.
6. For necessário introduzir composição horizontal do corpo.
7. Não for possível definir efeito visual ou rejeição determinística para
   algum campo sem nova norma.
8. Houver ambiguidade sobre duplicidade de barra_de_menus em JSON real.
9. A implementação de alinhamento_linhas ≠ "esquerda" exigir nova norma não
   coberta pelo ADR-0014.
10. A implementação de preferir_menor_numero = false exigir nova norma.
```

Ao bloquear:
- Registrar `ARCHITECTURE_REVIEW_REQUIRED` no topo do IMP-0018.
- Descrever precisamente qual decisão arquitetural está faltando.
- **Não implementar código** além do que está especificado sem bloqueio.

---

## Instrução explícita ao executor

Você é Claude Code atuando como **executor de implementação** em contexto limpo.

Hierarquia de autoridade (não negociável):

```
contrato_processo_desenvolvimento.md
  > ADRs aceitos (especialmente ADR-0014)
    > contratos de módulo
      > este handoff
        > decisões de implementação locais
```

**Regras operacionais**:

- Ler toda a seção "Leitura obrigatória" antes de tocar qualquer arquivo.
- Implementar **exatamente** o que este handoff especifica — sem funcionalidades
  extras, sem refatorações não solicitadas, sem abstrações adicionais.
- Não alterar nenhum arquivo da lista "Arquivos proibidos".
- Não decidir arquitetura — qualquer dúvida arquitetural → `ARCHITECTURE_REVIEW_REQUIRED`.
- Não fazer commit — o commit é responsabilidade do usuário.
- Para cada campo sem cobertura, escolher explicitamente entre implementar,
  validar ou rejeitar deterministicamente, conforme as opções deste handoff.
- Registrar todas as decisões locais no IMP-0018.

**Ordem de implementação recomendada**:

1. Ler toda a leitura obrigatória (especialmente `renderizador.py` integralmente).
2. Auditar campo a campo o que o renderer já lê vs. o que ignora.
3. Corrigir `_texto_chip_barra` para usar `vao_chip_texto.minimo`.
4. Corrigir `_linhas_barra` para aplicar `margem_horizontal.minimo`.
5. Implementar `linhas.minimo` no algoritmo de layout.
6. Adicionar leitura e validação de `colunas.largura`, `subcolunas.*.alinhamento`.
7. Implementar ou rejeitar `vao_vertical_entre_linhas`, `alinhamento_linhas`,
   `preferir_menor_numero`.
8. Adicionar validação de overflow flags false.
9. Rodar todas as 6 suítes existentes — confirmar que continuam passando.
10. Adicionar novos testes em `teste_renderizador.py`.
11. Atualizar `explorar_barra_de_menus.py` com correções dos achados H-0017 e
    novos parâmetros CLI.
12. Atualizar `teste_explorar_barra_de_menus.py` com novos casos.
13. Executar as 3 execuções manuais obrigatórias do explorador.
14. Criar IMP-0018.

---

## Saída final esperada

Ao concluir, o executor deve reportar:

```
IMPLEMENTATION_COMPLETED

arquivos-alterados:
  scripts/tela/renderizador.py
  scripts/tela/teste_renderizador.py
  scripts/tela/explorar_barra_de_menus.py
  scripts/tela/teste_explorar_barra_de_menus.py
  scripts/docs/relatorios/IMP-0018-cobertura-executavel-distribuicao-barra-de-menus.md

testes:
  teste_loader.py:                      <N>/<N>
  teste_modelo.py:                      <N>/<N>
  teste_renderizador.py:                <N>/<N>
  teste_demo.py:                        <N>/<N>
  teste_diagnostico.py:                 <N>/<N>
  teste_explorar_barra_de_menus.py:     <N>/<N>

verificacoes:
  <git status --short>
  <git diff --stat>
  <git diff --name-only>
```
