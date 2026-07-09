# H-0016 — Migração de JSON e renderização horizontal responsiva da barra de menus

```
status:        HANDOFF_READY
revisao:       AUDIT_REJECTED → REVISED (B-001, B-002, B-003, A-001)
ciclo:         H-0016
título:        Migração JSON barra_de_menus + renderização horizontal responsiva
ADR:           ADR-0014 (barra-horizontal-termos-especificos)
depende-de:    H-0015 (implementado, IMP-0015, QA aprovado)
commit-base:   b2eb458  feat: ocupa altura do terminal pelo corpo
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
| Contrato tela JSON | `scripts/docs/contratos/contrato_tela_json.md` (seção 18) |
| Contrato barra de menus | `scripts/docs/contratos/contrato_barra_de_menus.md` (seção 17) |
| Contrato JSON barra de menus | `scripts/docs/contratos/contrato_json_barra_de_menus.md` |
| Contrato chip | `scripts/docs/contratos/contrato_chip.md` |
| H-0015 (base implementado) | `scripts/docs/handoff/H-0015-ocupacao-vertical-janela-terminal-corpo.md` |
| IMP-0015 (base) | `scripts/docs/relatorios/IMP-0015-ocupacao-vertical-janela-terminal-corpo.md` |
| QA H-0015 (aprovado) | `scripts/docs/relatorios/RELATORIO_QA_H-0015_OCUPACAO_VERTICAL_JANELA_TERMINAL_CORPO.md` |
| Relatório a gerar | `scripts/docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md` |

---

## Status

```
HANDOFF_READY
```

---

## Contexto operacional temporário

O Codex está indisponível. O fluxo vigente neste ciclo é:

```
Claude Code      → gera handoff (este arquivo)
OpenCode / GLM   → auditoria/QA do handoff + implementação do código
Claude Code      → QA final da implementação
```

O executor **não decide arquitetura**. Toda decisão de design está registrada no ADR-0014 e nos contratos. Se qualquer item normativo estiver ausente ou conflitante, bloquear com `ARCHITECTURE_REVIEW_REQUIRED` antes de implementar.

---

## Contexto técnico — estado pós H-0015

O ciclo H-0015 implementou a ocupação vertical da janela do terminal pelo corpo (ADR-0013). Estado atual do código:

- **`renderizador.py`**: `renderizar_tela` aceita `altura: int | None = None`. Quando fornecida, preenche o corpo verticalmente com linhas em branco para atingir exatamente `altura` linhas na saída.
- **`_linhas_barra(barra_de_menus)`**: retorna uma lista com um chip por linha (`"[{tecla}] {texto}"`), empilhando verticalmente — **incompatível com ADR-0014**.
- **`l_barra = len(linhas_barra) + 2`**: cálculo de altura da barra (2 para bordas superior e inferior), usado em H-0015 para `altura`. Este cálculo permanece válido após H-0016 porque `linhas_barra` continuará retornando as linhas de conteúdo da caixa — mas o número de linhas retornadas mudará com a renderização horizontal.
- **JSONs ativos**: todos os 4 arquivos de tela têm `"distribuicao": "horizontal"` como string simples (alias transitório, não estrutura canônica).
- **Testes**: 398/398 passando em 5 suítes após H-0015. Alguns desses testes contêm asserções literais de layout que **serão afetados pela mudança de renderização** — ver seção "Atualização de testes e snapshots".

O ADR-0014 foi **explicitamente proibido** no H-0015 e adiado para este ciclo. Não há overlap.

---

## Relação com ADR-0014

O ADR-0014 tem duas partes:

**Parte A** — Semântica de `barra_de_menus.distribuicao = "horizontal"`:
- `"horizontal"` significa distribuição **horizontal responsiva** (não linha única fixa).
- O alias de string `"horizontal"` é transitório; a estrutura canônica é um objeto com `modo = "horizontal_responsiva"`.
- Algoritmo normativo mínimo: (1) tenta linha única → (2) se não couber, tenta multilinha (até `linhas.maximo`) → (3) se ainda não couber, erro determinístico (`erro_layout`).
- Âncoras são **restrições de validação declarativa**, não instruções de reordenação.
- `overflow.quando_nao_couber = "erro_layout"`: nunca omitir, truncar ou reordenar chips.

**Parte B** — Alteração por termo específico completo:
- Mudanças normativas devem visar o **termo específico completo** (ex.: `distribuicao`), nunca substrings parciais.
- Relevante para o executor ao escrever testes e ao nomear constantes.

---

## Decisão gerencial do ciclo

H-0016 resolve a **dívida técnica deixada explícita pelo H-0015**: implementar o ADR-0014 integralmente.

Duas entregas obrigatórias:

1. **Migração de JSON**: todos os JSONs ativos com `distribuicao: "horizontal"` (string) devem ser migrados para a estrutura canônica de objeto.
2. **Renderização horizontal responsiva**: `_linhas_barra` deve ser substituída por lógica que respeite `distribuicao` declarativo, implementando o algoritmo normativo do ADR-0014.

---

## Objetivo

Implementar:

1. Migrar os 4 JSONs ativos de `barra_de_menus.distribuicao` de `"horizontal"` (string) para objeto canônico `{"modo": "horizontal_responsiva", ...}`.
2. Substituir `_linhas_barra` em `renderizador.py` por função que lê a estrutura `distribuicao` do JSON e gera linhas horizontais responsivas dos chips.
3. Atualizar a assinatura de `_linhas_barra` para receber `content_w: int` (necessário para calcular se os chips cabem na largura disponível).
4. Manter a compatibilidade transitória: string `"horizontal"` deve continuar sendo aceita como alias para `{"modo": "horizontal_responsiva"}` com defaults normativos.
5. Preservar integralmente o `altura` de H-0015 e o cálculo `l_barra = len(linhas_barra) + 2`.
6. Atualizar testes existentes afetados pela mudança de layout — preservando a intenção dos testes, não o texto antigo das asserções; adicionar testes para o caminho canônico horizontal.

---

## Leitura obrigatória antes de implementar

O executor deve ler na íntegra antes de tocar qualquer arquivo:

1. `scripts/docs/adr/ADR-0014-barra-horizontal-termos-especificos.md`
2. `scripts/docs/contratos/contrato_barra_de_menus.md` — seção 17 (distribuição, âncoras, overflow)
3. `scripts/docs/contratos/contrato_tela_json.md` — seção 18 (`barra_de_menus`)
4. `scripts/docs/contratos/contrato_json_barra_de_menus.md`
5. `scripts/docs/contratos/contrato_chip.md`
6. `scripts/docs/contratos/contrato_processo_desenvolvimento.md` — seção 10 (alteração por termo completo)
7. `scripts/docs/handoff/H-0015-ocupacao-vertical-janela-terminal-corpo.md`
8. `scripts/docs/relatorios/IMP-0015-ocupacao-vertical-janela-terminal-corpo.md`
9. Este handoff até o final.

---

## JSONs a migrar

### Inventário atual (pré-migração)

Todos os 4 JSONs ativos têm `"distribuicao": "horizontal"` como string:

| Arquivo | chips declarados |
|---------|-----------------|
| `scripts/config/telas/orquestrador.json` | `chip_esc` ("Esc"/"Sair"), `chip_ajuda` ("?"/"Ajuda") |
| `scripts/config/telas/grupo_minimo.json` | `chip_esc` ("Esc"/"Voltar"), `chip_ajuda` ("?"/"Ajuda") |
| `scripts/config/telas/destino_minimo.json` | `chip_esc` ("Esc"/"Voltar"), `chip_ajuda` ("?"/"Ajuda") |
| `scripts/config/telas/stub_b.json` | `chip_esc` ("Esc"/"Voltar"), `chip_ajuda` ("?"/"Ajuda") |

### Estrutura canônica de `distribuicao` (alvo da migração)

Cada JSON deve ter `barra_de_menus.distribuicao` substituído pelo objeto abaixo **exatamente**:

```json
{
  "modo": "horizontal_responsiva",
  "ordem": {
    "politica": "declaracao",
    "ancoras": {
      "primeiro": ["chip_esc"],
      "ultimo":   ["chip_ajuda"]
    }
  },
  "tentativa_inicial": "linha_unica",
  "quebra": "multilinha_quando_nao_couber",
  "preenchimento_multilinha": "coluna_a_coluna",
  "preenchimentos_multilinha_suportados": ["coluna_a_coluna", "linha_a_linha"],
  "linhas": {
    "minimo": 1,
    "maximo": 2,
    "preferir_menor_numero": true
  },
  "alinhamento_linhas": "esquerda",
  "espacamentos": {
    "margem_horizontal":       {"minimo": 1, "maximo": null},
    "vao_chip_texto":          {"minimo": 1, "maximo": 3},
    "vao_entre_chips":         {"minimo": 2, "maximo": 6},
    "vao_entre_colunas":       {"minimo": 2, "maximo": 8},
    "vao_vertical_entre_linhas": {"minimo": 0, "maximo": 0}
  },
  "colunas": {
    "largura": "por_maior_item_da_coluna",
    "subcolunas": {
      "chip":  {"alinhamento": "esquerda"},
      "texto": {"alinhamento": "esquerda"}
    }
  },
  "overflow": {
    "quando_nao_couber": "erro_layout",
    "nao_omitir_chips":  true,
    "nao_truncar_texto": true,
    "nao_reordenar":     true
  }
}
```

**Observação sobre âncoras**: os valores de `ancoras.primeiro` e `ancoras.ultimo` são os IDs reais dos chips declarados nos JSONs. Os IDs reais encontrados em todos os JSONs ativos são `chip_esc` (primeiro) e `chip_ajuda` (último). O implementador deve usar os IDs reais dos chips encontrados nos JSONs — não renomear IDs apenas para combinar com o exemplo acima.

---

## Estrutura canônica de distribuição — semântica de campos

| Campo | Semântica |
|-------|-----------|
| `modo` | `"horizontal_responsiva"`: chips distribuídos horizontalmente na linha, com fallback multilinha |
| `ordem.politica` | `"declaracao"`: a ordem base é `chips[]` no JSON; o renderer preserva a ordem declarada; âncoras são validações dessa declaração, não instruções de reordenação |
| `ordem.ancoras` | Restrições de validação declarativa (ver seção âncoras abaixo) |
| `tentativa_inicial` | `"linha_unica"`: tenta encaixar todos os chips em uma única linha primeiro |
| `quebra` | `"multilinha_quando_nao_couber"`: se não couber em linha única, tenta multilinha |
| `preenchimento_multilinha` | `"coluna_a_coluna"`: modo padrão de preenchimento em múltiplas linhas |
| `preenchimentos_multilinha_suportados` | Lista dos modos suportados pela implementação H-0016 |
| `linhas.minimo` | Número mínimo de linhas físicas (1) |
| `linhas.maximo` | Número máximo de linhas físicas (2) |
| `linhas.preferir_menor_numero` | `true`: usar o menor número de linhas que comporte todos os chips |
| `alinhamento_linhas` | `"esquerda"`: chips alinhados à esquerda em cada linha |
| `espacamentos.*` | Restrições de espaçamento (ver seção espaçamentos abaixo) |
| `colunas.largura` | `"por_maior_item_da_coluna"`: largura de cada coluna determinada pelo maior chip da coluna |
| `overflow.quando_nao_couber` | `"erro_layout"`: erro determinístico quando chips não cabem |
| `overflow.nao_omitir_chips` | Proibição de omissão |
| `overflow.nao_truncar_texto` | Proibição de truncamento |
| `overflow.nao_reordenar` | Proibição de reordenação |

---

## Regras de ordem e âncoras

**`ordem.politica = "declaracao"`** (valor normativo definido pela ADR-0014):
1. A ordem dos chips na saída visual é **exatamente** a ordem de declaração em `chips[]` no JSON.
2. O renderer **não reordena** chips automaticamente.
3. Âncoras, se declaradas, são **restrições de validação** da declaração.
4. Âncoras não autorizam reordenação automática.
5. O renderer não usa ordem canônica global.
6. O renderer não reordena por heurística.

**Âncoras — comportamento normativo**:
- `ancoras.primeiro: ["chip_esc"]`: valida que o chip com `id = "chip_esc"` é o primeiro na lista `chips[]` do JSON. Se violado, levantar `RenderizadorErro` com mensagem descritiva.
- `ancoras.ultimo: ["chip_ajuda"]`: valida que o chip com `id = "chip_ajuda"` é o último na lista `chips[]` do JSON. Se violado, levantar `RenderizadorErro` com mensagem descritiva.
- O renderer **NÃO** move automaticamente um chip para satisfazer a âncora. A violação é erro, não correção silenciosa.
- Quando `ancoras` está ausente ou vazio, nenhuma validação de âncora é executada.

---

## Algoritmo de renderização horizontal responsiva

### Assinatura da função

```python
def _linhas_barra(barra_de_menus: dict, content_w: int) -> list[str]:
```

`content_w` é a largura disponível para conteúdo dentro da caixa (`total_w - 3`), recebido do contexto de `renderizar_tela`.

### Fluxo principal

```
1. Ler chips[] de barra_de_menus (lista ordenada; ordem declarada = ordem final)
2. Ler distribuicao de barra_de_menus
3. Normalizar distribuicao:
   - se string "horizontal" → tratar como objeto canônico com defaults normativos
   - se objeto com modo "horizontal_responsiva" → usar campos declarados
   - outros valores → RenderizadorErro
4. Validar âncoras (se declaradas)
5. Tentar linha única (tentativa_inicial = "linha_unica")
   - se couber → retornar [linha_unica]
6. Tentar multilinha (quebra = "multilinha_quando_nao_couber")
   - iterar de linhas.minimo+1 até linhas.maximo (preferir_menor_numero)
   - para cada tentativa de N linhas, aplicar preenchimento_multilinha
   - se couber com N linhas → retornar linhas_multilinha
7. Se nenhuma configuração couber → RenderizadorErro (erro_layout)
```

### Formato de cada chip na linha

```
"[{tecla}] {texto}"
```

Chips em uma linha são separados por espaços respeitando `espacamentos.vao_entre_chips.minimo`.

### Espaçamentos na renderização (valores mínimos normativos)

| Espaçamento | Mínimo | Aplicação |
|-------------|--------|-----------|
| `vao_chip_texto` | 1 | espaço entre `[tecla]` e `texto` (já incluso no formato `"[t] texto"`) |
| `vao_entre_chips` | 2 | espaços entre o final de um chip e o início do próximo na mesma linha |
| `vao_entre_colunas` | 2 | espaços entre colunas no modo `coluna_a_coluna` |
| `vao_vertical_entre_linhas` | 0 | linhas físicas entre linhas de chips (= zero: sem linha em branco entre elas) |
| `margem_horizontal` | 1 | margem à esquerda (já garantida pela borda da caixa) |

**Para verificar se um conjunto de chips cabe em `content_w`**: calcular o comprimento total da linha como soma dos comprimentos de cada chip (`len("[{tecla}] {texto}")`) mais `vao_entre_chips.minimo * (N_chips - 1)`. Se ≤ `content_w`, cabe.

### Modo `coluna_a_coluna` (preenchimento multilinha)

Para N chips distribuídos em K linhas:
- Número de colunas = `ceil(N / K)`
- Preenche coluna por coluna de cima para baixo
- Largura de cada coluna = largura do maior chip da coluna (`colunas.largura = "por_maior_item_da_coluna"`)
- Chips alinhados à esquerda dentro da coluna (`subcolunas.chip.alinhamento = "esquerda"`, `subcolunas.texto.alinhamento = "esquerda"`)
- Colunas separadas por `vao_entre_colunas.minimo` espaços

**Exemplo** com chips `[A, B, C, D, E]` e `K=2` linhas:
- `ceil(5/2) = 3` colunas
- Col 1: A, B → linha 1: A, linha 2: B
- Col 2: C, D → linha 1: C, linha 2: D
- Col 3: E, _  → linha 1: E (sem chip na posição 2)
- Resultado: `linha1 = "A  C  E"`, `linha2 = "B  D"`

### Modo `linha_a_linha` (suportado; somente como fallback de coluna_a_coluna)

Para N chips em K linhas:
- `chips_por_linha = ceil(N / K)`
- Linha i recebe chips `[i*chips_por_linha : (i+1)*chips_por_linha]`
- Chips separados por `vao_entre_chips.minimo` espaços

**Exemplo** com `[A, B, C, D, E]` e `K=2` linhas:
- `ceil(5/2) = 3` chips por linha
- Linha 1: A B C; Linha 2: D E

**Implementação**: o executor **pode** implementar `linha_a_linha` como fallback alternativo dentro da lógica multilinha, mas o modo padrão declarado em `preenchimento_multilinha` é `coluna_a_coluna`. Ambos devem ser implementados se `preenchimentos_multilinha_suportados` os lista. Se o executor optar por não implementar `linha_a_linha`, deve rejeitá-lo com `RenderizadorErro` determinístico quando solicitado.

### Verificação de encaixe no modo multilinha

Para verificar se N chips cabem em K linhas com modo `coluna_a_coluna`:
- Calcular layout de colunas
- Para cada linha gerada: comprimento = soma das larguras das colunas ocupadas na linha + `vao_entre_colunas.minimo * (colunas_na_linha - 1)`
- Se o comprimento máximo entre todas as linhas ≤ `content_w` → cabe

---

## Compatibilidade transitória

A string `"horizontal"` em `distribuicao` deve continuar sendo aceita como alias **permanente durante este ciclo** (a migração dos JSONs é parte deste ciclo, mas testes legados podem usar a string).

**Normalização interna** (não exposta ao JSON):
```python
# dentro de _linhas_barra ou função auxiliar de normalização
if isinstance(distribuicao, str) and distribuicao == "horizontal":
    distribuicao = _DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT
```

Onde `_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT` é um dict Python com os mesmos valores do objeto canônico JSON (defaults normativos do ADR-0014).

**Após a migração dos JSONs**, todos os arquivos ativos terão o objeto canônico. O alias de string permanece apenas para compatibilidade com testes antigos que ainda usem `"horizontal"` diretamente, e pode ser usado em testes de compatibilidade transitória.

---

## Atualização de testes e snapshots

A migração da `barra_de_menus` de empilhamento vertical para renderização horizontal responsiva **altera a forma física da barra** e, portanto, pode alterar snapshots e expectativas literais de renderização.

### Nova contabilidade de L_barra

**Antes** (comportamento pré-H-0016):
```
L_barra = 2 + N_chips
```
porque cada chip ocupava uma linha separada.

**Depois** (comportamento pós-H-0016):
```
L_barra = 2 + N_linhas_barra
```
onde `N_linhas_barra` é o número de linhas físicas produzidas pela distribuição horizontal responsiva.

**Exemplo concreto**: com 2 chips (`chip_esc`, `chip_ajuda`) em `largura=42` (`content_w=39`):
- `[Esc] Sair` (10 chars) + 2 espaços + `[?] Ajuda` (9 chars) = 21 ≤ 39 → cabe em linha única
- `N_linhas_barra = 1` → `L_barra = 3` (antes era 4)

O H-0015 continua funcionando, mas com o novo `L_barra`:
```
altura_total = L_cab + L_corpo + L_barra
```
e `L_barra` agora depende da distribuição horizontal responsiva, não de `N_chips`.

### Testes que devem ser atualizados

Os testes existentes que comparam saída literal devem ser atualizados quando a mudança for efeito esperado do H-0016. Isso inclui, se aplicável:

- `_EXPECTED_ORQUESTRADOR` e `_EXPECTED_ORQUESTRADOR_RETA` — asserções literais da barra empilhada verticalmente quebram com a barra horizontal.
- Expectativas de `teste_altura_explicita` que assumem `l_barra = 4` e `n_minimo = 16` — após H-0016, `l_barra = 3` e `n_minimo = 15` no caso de 2 chips em largura 42.
- Expectativas de diagnóstico que comparam saída literal da barra.
- Expectativas de demo/subprocess que renderizam a tela completa.

**Regra**: o implementador deve atualizar as expectativas para refletir a saída horizontal correta, preservando a **intenção** dos testes (validar que a renderização é correta), não o **texto antigo** das asserções (que descrevia a renderização vertical, agora obsoleta).

---

## Escopo positivo — o que H-0016 deve fazer

1. Migrar `barra_de_menus.distribuicao` em `orquestrador.json` de string para objeto canônico.
2. Migrar `barra_de_menus.distribuicao` em `grupo_minimo.json` de string para objeto canônico.
3. Migrar `barra_de_menus.distribuicao` em `destino_minimo.json` de string para objeto canônico.
4. Migrar `barra_de_menus.distribuicao` em `stub_b.json` de string para objeto canônico.
5. Substituir `_linhas_barra(barra_de_menus)` por `_linhas_barra(barra_de_menus, content_w)` em `renderizador.py`.
6. Implementar normalização de `distribuicao`: string `"horizontal"` → objeto canônico com defaults.
7. Implementar validação de âncoras: `primeiro`/`ultimo` verificados contra `chips[0].id` e `chips[-1].id`; violação levanta `RenderizadorErro`.
8. Implementar tentativa de linha única: calcular comprimento total dos chips + separadores; se ≤ `content_w`, retornar linha única.
9. Implementar tentativa multilinha com `coluna_a_coluna`: iterar de 2 até `linhas.maximo`, retornar na primeira configuração que encaixa.
10. Implementar `linha_a_linha` como modo alternativo suportado (quando `preenchimento_multilinha = "linha_a_linha"`), ou rejeitá-lo deterministicamente se o executor optar por não implementá-lo neste ciclo.
11. Implementar `overflow.quando_nao_couber = "erro_layout"`: quando nenhuma configuração cabe, levantar `RenderizadorErro` com mensagem descritiva.
12. Atualizar a chamada `_linhas_barra(modelo.barra_de_menus)` em `renderizar_tela` para `_linhas_barra(modelo.barra_de_menus, content_w)`.
13. Garantir que `l_barra = len(linhas_barra) + 2` continue correto (invariante: `linhas_barra` retorna lista de strings, cada string é uma linha de conteúdo da caixa).
14. Adicionar testes para o caminho canônico com objeto `distribuicao`.
15. Adicionar testes para âncoras violadas (levanta `RenderizadorErro`).
16. Adicionar testes para `erro_layout` (nenhuma configuração cabe, levanta `RenderizadorErro`).
17. Atualizar snapshots e expectativas literais de renderização afetados pela mudança de layout horizontal.

---

## Escopo negativo — o que H-0016 NÃO deve fazer

- Não implementar composição horizontal do corpo.
- Não implementar `corpo.arranjo = "horizontal"`.
- Não implementar distribuição de altura entre elementos do corpo.
- Não corrigir o preenchimento vertical do H-0015.
- Não implementar grupo com 2 elementos.
- Não implementar aninhamento.
- Não implementar percentual/fração.
- Não implementar console real.
- Não implementar foco entre elementos.
- Não implementar navegação por `[✥]`.
- Não implementar paginação de console.
- Não implementar filtros.
- Não implementar modo verboso.
- Não implementar seleção.
- Não criar registry novo de ações.
- Não criar registry novo de telas.
- Não alterar semântica de Esc, g, d, b ou Enter.
- Não alterar a navegação do lancador.
- Não alterar `contrato_barra_de_menus.md`, `contrato_tela_json.md` ou qualquer outro contrato.
- Não alterar `ADR-0014` nem qualquer outro ADR.
- Não alterar `NOMENCLATURA.md` nem `INDICE.md`.
- Não alterar `estilo.json`, `lancador.json` ou `layout_console.json`.
- Não hardcodar lista canônica global de chips.
- Não truncar texto de chip para caber.
- Não omitir chip quando não couber (use `erro_layout`).
- Não reordenar chips heuristicamente.
- Não usar "um chip por linha" como fallback vertical.
- Não usar regras do lancador como se fossem regras da barra_de_menus.
- Não incluir chips do lancador na barra_de_menus.
- Não alterar `loader.py` nem `modelo.py` para validar ou transformar `distribuicao` (loader e modelo passam `barra_de_menus` como dict sem modificação; a validação é responsabilidade do renderer).
- Não implementar `modo` diferente de `"horizontal_responsiva"` (não existe outro modo neste ciclo).
- Não remover o fallback `TOTAL_WIDTH = 42` (herança técnica, sem caráter normativo).
- Não implementar `alinhamento = "direita"` ou `"centro"` para chips (apenas `"esquerda"` é suportado neste ciclo).
- Não implementar `linhas.maximo > 2` como caso testado adicional.

---

## Preservações obrigatórias

As seguintes características do código atual devem ser preservadas **integralmente**:

1. **Assinatura de `renderizar_tela`**: `renderizar_tela(modelo, tipo_borda="curva", largura=None, altura=None)` — nenhum parâmetro removido ou renomeado.
2. **Parâmetro `altura` (H-0015)**: todo o bloco de ocupação vertical (`if altura is not None:`) deve ser preservado sem alteração de lógica.
3. **`l_barra = len(linhas_barra) + 2`**: cálculo de altura da barra permanece correto porque `_linhas_barra` continua retornando lista de strings (linhas de conteúdo). O valor numérico de `l_barra` mudará com a barra horizontal — mas a fórmula permanece.
4. **`RenderizadorErro`**: classe de exceção existente, usada para todos os erros de renderização.
5. **`_LABEL_BARRA = "Menus"`**: label fixo da caixa da barra (apenas rótulo visual).
6. **`_caixa`, `_linha_topo`, `_linha_base`, `_linha_conteudo`**: funções de construção de caixa, sem alteração.
7. **`_linhas_console`, `_linhas_dashboard`, `_linhas_lancador`**: funções de conteúdo de outros elementos, sem alteração.
8. **`_caixa_de_elemento`**: função de despacho de elementos, sem alteração.
9. **Grupo estrutural** (H-0012): lógica de `elemento.tipo == "grupo"` em `renderizar_tela`, sem alteração.
10. **`_TEXTO_ITEM_MAX = 15`**: limite de texto de item de lancador, sem alteração.
11. **`_BORDAS`**: dicionário de conjuntos de caracteres de borda (`curva`, `reta`), sem alteração.
12. **Testes existentes**: os testes existentes devem continuar passando **com as expectativas atualizadas** quando a mudança de layout for efeito esperado do H-0016. Testes que validam comportamento não afetado pela barra horizontal não devem ser alterados.

---

## Arquivos permitidos

O executor pode criar ou editar **somente** os seguintes arquivos:

```
scripts/config/telas/orquestrador.json
scripts/config/telas/grupo_minimo.json
scripts/config/telas/destino_minimo.json
scripts/config/telas/stub_b.json

scripts/tela/loader.py
scripts/tela/modelo.py
scripts/tela/renderizador.py
scripts/tela/demo.py
scripts/tela/diagnostico.py

scripts/tela/teste_loader.py
scripts/tela/teste_modelo.py
scripts/tela/teste_renderizador.py
scripts/tela/teste_demo.py
scripts/tela/teste_diagnostico.py

scripts/docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
```

**Justificativa para inclusão dos arquivos de teste**: a migração do JSON e a alteração física da barra_de_menus podem alterar validação/carga, modelo exposto, snapshots de renderer, snapshots de demo e snapshots de diagnóstico. Todos os arquivos de teste devem estar autorizados para que o implementador possa atualizar expectativas afetadas.

---

## Arquivos proibidos

O executor **não deve tocar** em nenhum dos seguintes arquivos:

```
scripts/docs/contratos/            ← todos os arquivos de contrato
scripts/docs/adr/                  ← todos os ADRs
scripts/docs/NOMENCLATURA.md
scripts/docs/INDICE.md
scripts/config/estilo.json
scripts/config/lancador.json
scripts/config/layout_console.json
```

Se qualquer item acima precisar ser alterado para concluir a implementação, bloquear com `ARCHITECTURE_REVIEW_REQUIRED` e **não alterar o arquivo**.

---

## Especificação funcional por módulo

### `scripts/config/telas/*.json` (4 arquivos)

**Alteração**: substituir o valor do campo `barra_de_menus.distribuicao` de:
```json
"distribuicao": "horizontal"
```
para o objeto canônico (conforme seção "Estrutura canônica de `distribuicao`" acima).

Os demais campos de `barra_de_menus` (especialmente `chips[]`) não devem ser alterados:
- não adicionar chips;
- não remover chips;
- não reordenar chips;
- não alterar `id`, `tecla`, `texto`, `acao`, `regra_existencia`, `regra_ativo`, `forma_exibicao`.

### `scripts/tela/renderizador.py`

**Alteração 1 — Assinatura de `_linhas_barra`**:

```python
# ANTES
def _linhas_barra(barra_de_menus):

# DEPOIS
def _linhas_barra(barra_de_menus: dict, content_w: int) -> list[str]:
```

**Alteração 2 — Implementação de `_linhas_barra`**:

Substituir o corpo atual (que empilha um chip por linha) pela lógica horizontal responsiva descrita na seção "Algoritmo de renderização horizontal responsiva".

Estrutura interna esperada (pseudocódigo normativo):

```
_linhas_barra(barra_de_menus, content_w):
  chips = barra_de_menus["chips"] ou []
  distribuicao = _normalizar_distribuicao(barra_de_menus.get("distribuicao"))
  _validar_ancoras(chips, distribuicao)
  texto_chips = ["[{tecla}] {texto}".format(...) for chip in chips]
  # Tentativa linha única
  linha_unica = _montar_linha_unica(texto_chips, distribuicao)
  if len(linha_unica) <= content_w:
      return [linha_unica]
  # Tentativa multilinha
  for n_linhas in range(2, distribuicao["linhas"]["maximo"] + 1):
      linhas = _montar_multilinha(texto_chips, n_linhas, distribuicao, content_w)
      if linhas is not None:
          return linhas
  # Overflow → erro determinístico
  raise RenderizadorErro("erro_layout: chips da barra_de_menus não cabem em {0} "
                         "caracteres com no máximo {1} linhas".format(
                             content_w, distribuicao["linhas"]["maximo"]))
```

**Alteração 3 — Chamada de `_linhas_barra` em `renderizar_tela`**:

```python
# ANTES (linha ~361)
linhas_barra = _linhas_barra(modelo.barra_de_menus)

# DEPOIS
linhas_barra = _linhas_barra(modelo.barra_de_menus, content_w)
```

**Constante auxiliar — defaults do alias transitório**:

```python
_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT = {
    "modo": "horizontal_responsiva",
    "ordem": {
        "politica": "declaracao",
        "ancoras": {}
    },
    "tentativa_inicial": "linha_unica",
    "quebra": "multilinha_quando_nao_couber",
    "preenchimento_multilinha": "coluna_a_coluna",
    "preenchimentos_multilinha_suportados": ["coluna_a_coluna", "linha_a_linha"],
    "linhas": {"minimo": 1, "maximo": 2, "preferir_menor_numero": True},
    "alinhamento_linhas": "esquerda",
    "espacamentos": {
        "margem_horizontal":           {"minimo": 1,  "maximo": None},
        "vao_chip_texto":              {"minimo": 1,  "maximo": 3},
        "vao_entre_chips":             {"minimo": 2,  "maximo": 6},
        "vao_entre_colunas":           {"minimo": 2,  "maximo": 8},
        "vao_vertical_entre_linhas":   {"minimo": 0,  "maximo": 0},
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
```

**Nota sobre `ancoras` no default**: quando o alias de string `"horizontal"` é normalizado, `ancoras` fica vazio (sem âncoras declaradas, nenhuma validação de âncora é executada). Apenas o objeto canônico pode declarar âncoras.

### `scripts/tela/teste_renderizador.py`

Adicionar casos de teste para H-0016 (ver seção "Testes obrigatórios").

Atualizar asserções literais existentes que comparam saída de renderização da barra_de_menus (ex.: `_EXPECTED_ORQUESTRADOR`, `_EXPECTED_ORQUESTRADOR_RETA`, `l_barra = 4`, `n_minimo = 16`) para refletir a nova renderização horizontal. A intenção de cada teste deve ser preservada; apenas o valor esperado muda para espelhar a saída horizontal correta.

### `scripts/tela/teste_demo.py` e `scripts/tela/teste_diagnostico.py`

Verificar se há asserções literais afetadas pela mudança de layout da barra. Se houver, atualizar as expectativas para refletir a saída horizontal. Se não houver impacto, não alterar.

---

## Regras técnicas

1. **Apenas biblioteca padrão do Python** — não importar módulos externos.
2. **Sem hardcoding de texto** de chip, tecla ou rótulo — tudo vem do JSON/modelo.
3. **Sem reordenação silenciosa** — a ordem de saída é sempre a ordem de `chips[]`.
4. **Sem omissão silenciosa** — todos os chips declarados aparecem na saída ou o renderer lança `RenderizadorErro`.
5. **Sem truncamento silencioso** — nenhum texto de chip é cortado para caber.
6. **`RenderizadorErro` com mensagem descritiva** em todos os casos de erro: qual chip, qual âncora, qual tamanho esperado vs. disponível.
7. **Invariante de altura**: `l_barra = len(linhas_barra) + 2` deve continuar correto. `_linhas_barra` retorna lista de strings onde cada string é uma linha de conteúdo da caixa.
8. **`content_w`** passado para `_linhas_barra` é `total_w - 3` (calculado em `renderizar_tela`, conforme código atual).
9. **`vao_entre_chips.minimo = 2`**: separador mínimo entre chips na mesma linha.
10. **`vao_entre_colunas.minimo = 2`**: separador mínimo entre colunas no modo `coluna_a_coluna`.
11. **Preferência por menor número de linhas** (`preferir_menor_numero = true`): ao iterar tentativas multilinha, tentar 2 linhas antes de 3, etc. Com `maximo = 2`, só há uma tentativa multilinha.
12. **Âncoras validadas antes da renderização**: se a validação falha, o erro é levantado antes de qualquer cálculo de layout.
13. **`distribuicao` ausente ou `None`**: tratar como `"horizontal"` (alias com defaults normativos). Não levantar erro por `distribuicao` ausente.
14. **`chips` vazia ou ausente**: retornar lista vazia `[]` (caixa sem linhas de conteúdo), sem erro.

---

## Critérios de aceite

O ciclo H-0016 é considerado **concluído** quando todos os critérios abaixo forem atendidos:

### JSON

1. `orquestrador.json` tem `barra_de_menus.distribuicao` como objeto com `modo = "horizontal_responsiva"`.
2. `grupo_minimo.json` tem `barra_de_menus.distribuicao` como objeto com `modo = "horizontal_responsiva"`.
3. `destino_minimo.json` tem `barra_de_menus.distribuicao` como objeto com `modo = "horizontal_responsiva"`.
4. `stub_b.json` tem `barra_de_menus.distribuicao` como objeto com `modo = "horizontal_responsiva"`.
5. Nenhum dos 4 JSONs alterou `barra_de_menus.chips[]` (ids, teclas, textos, ações, regras preservados exatamente).
6. Todos os 4 JSONs são válidos (parseable por `json.loads`).
7. `ordem.politica` nos 4 JSONs migrados usa o valor `"declaracao"` (não `"declaracao_validada"` nem outro valor fora da ADR-0014).

### Renderizador — caminho canônico

8. `_linhas_barra` aceita dois parâmetros: `barra_de_menus` e `content_w`.
9. Com `distribuicao` objeto canônico e chips que cabem em linha única, retorna lista com uma string.
10. Com `distribuicao` objeto canônico e chips que não cabem em linha única mas cabem em 2 linhas, retorna lista com duas strings.
11. Com `distribuicao` objeto canônico e chips que não cabem em 2 linhas, levanta `RenderizadorErro`.
12. A mensagem do critério 11 contém a palavra `"erro_layout"`.
13. `coluna_a_coluna` distribui chips de forma determinística conforme a especificação.
14. `linha_a_linha` é implementado deterministicamente ou rejeitado com `RenderizadorErro` determinístico quando solicitado.

### Renderizador — âncoras

15. Com âncora `primeiro: ["chip_esc"]` e `chips[0].id != "chip_esc"`, levanta `RenderizadorErro`.
16. Com âncora `ultimo: ["chip_ajuda"]` e `chips[-1].id != "chip_ajuda"`, levanta `RenderizadorErro`.
17. Com âncora para id inexistente em `chips[]`, levanta `RenderizadorErro`.
18. Com âncoras respeitadas, não levanta `RenderizadorErro` por âncora.

### Renderizador — compatibilidade transitória

19. Com `distribuicao = "horizontal"` (string), o renderer não levanta erro e produz saída horizontal.
20. Com `distribuicao` ausente/`None`, o renderer não levanta erro e produz saída horizontal.

### Preservações e proibições

21. Cada chip declarado aparece exatamente uma vez na saída.
22. Nenhum chip ausente é inventado.
23. Nenhum texto de chip é truncado.
24. Nenhum chip é omitido para caber (overflow → erro).
25. Chips de lancador não aparecem na barra_de_menus.
26. `corpo.arranjo` não influencia a barra.

### Testes e snapshots

27. Snapshots e expectativas literais afetados pela mudança de layout são atualizados para refletir a saída horizontal correta.
28. H-0015 continua funcionando com altura explícita, considerando o novo `l_barra` (calculado com `N_linhas_barra` da distribuição horizontal responsiva).
29. `g/d/b/Esc` continuam funcionando.
30. Diagnóstico continua determinístico, com expectativa atualizada se necessário.
31. Todos os testes automatizados passam após as atualizações de expectativa.
32. Nenhum arquivo fora do escopo permitido é alterado.
33. Nenhum `__pycache__` ou `.pyc` fica no workspace.

---

## Testes obrigatórios

### Comandos a executar

```bash
cd scripts
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
python tela/teste_diagnostico.py
```

### Casos obrigatórios em `scripts/tela/teste_renderizador.py`

Adicionar ao menos os seguintes casos (classe `TestLinhasBarra`):

```python
class TestLinhasBarra:
    def test_linha_unica_cabe(self):
        # chips que cabem em linha única com content_w suficiente
        # resultado: lista com 1 string contendo ambos os chips

    def test_linha_unica_nao_cabe_vai_para_multilinha(self):
        # content_w pequeno → chips não cabem em linha única
        # mas cabem em 2 linhas → resultado: lista com 2 strings

    def test_multilinha_nao_cabe_erro_layout(self):
        # content_w muito pequeno → chips não cabem em nenhuma configuração
        # resultado: RenderizadorErro com "erro_layout" na mensagem

    def test_alias_string_horizontal_aceito(self):
        # distribuicao = "horizontal" (string) → não lança erro, produz saída horizontal

    def test_distribuicao_ausente_aceito(self):
        # barra_de_menus sem campo "distribuicao" → não lança erro

    def test_chips_vazia_retorna_lista_vazia(self):
        # chips = [] → retorna []

    def test_ancora_primeiro_valida(self):
        # chips[0].id == âncora declarada → sem erro

    def test_ancora_primeiro_violada(self):
        # chips[0].id != âncora declarada → RenderizadorErro

    def test_ancora_ultimo_valida(self):
        # chips[-1].id == âncora declarada → sem erro

    def test_ancora_ultimo_violada(self):
        # chips[-1].id != âncora declarada → RenderizadorErro

    def test_ancora_id_inexistente(self):
        # id declarado em âncora não existe em chips[] → RenderizadorErro

    def test_ordem_preservada(self):
        # ordem na saída = ordem declarada nos chips

    def test_chips_do_lancador_nao_entram_na_barra(self):
        # chips de lancador (ex.: g, d) não pertencem à barra_de_menus

    def test_coluna_a_coluna_layout(self):
        # verificar que coluna_a_coluna distribui chips corretamente

    def test_linha_a_linha_implementado_ou_rejeitado(self):
        # se implementado: distribui chips linha a linha corretamente
        # se não implementado: RenderizadorErro determinístico

    def test_renderizar_tela_com_distribuicao_canonica(self):
        # renderizar_tela com modelo de JSON migrado → saída com chips em linha horizontal
        # snapshot atualizado para barra horizontal

    def test_renderizar_tela_preserva_altura_h0015(self):
        # renderizar_tela com altura → invariante l_barra correto com novo valor
        # l_barra = len(linhas_barra) + 2 com barra horizontal

    def test_altura_minima_com_barra_horizontal(self):
        # n_minimo correto após H-0016 (ex.: 15 em vez de 16 para 2 chips em largura 42)

    def test_fluxo_g_d_b_esc_preservado(self):
        # renderização preserva navegação g/d/b/Esc sem alteração semântica
```

### Cobertura obrigatória por suíte

- **`teste_loader.py`**: JSONs migrados carregam corretamente; distribuição é exposta como objeto.
- **`teste_modelo.py`**: modelo expõe distribuição como objeto ao renderer.
- **`teste_renderizador.py`**: todos os casos acima + snapshots de renderer atualizados para barra horizontal.
- **`teste_demo.py`**: snapshots de demo atualizados quando necessário.
- **`teste_diagnostico.py`**: diagnóstico determinístico; snapshots atualizados se necessário.

---

## Relatório de implementação

O executor deve criar o arquivo:

```
scripts/docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
```

Com a seguinte estrutura mínima:

```markdown
# IMP-0016 — Migração JSON da barra_de_menus e renderização horizontal responsiva

## Status

## Resumo

## Arquivos alterados/criados

## JSONs migrados

## Implementação realizada

## Validações implementadas

## Testes/snapshots atualizados

## Decisões locais

## Testes executados

## Resultados

## Limitações conhecidas

## Confirmação de fora de escopo
```

---

## Critérios de bloqueio — ARCHITECTURE_REVIEW_REQUIRED

O executor deve bloquear a implementação e registrar `ARCHITECTURE_REVIEW_REQUIRED` nos seguintes casos:

1. O algoritmo de encaixe horizontal exigir lógica de quebra não coberta pelo ADR-0014 (ex.: quebra em mais de 2 linhas por default, quebra por palavra).
2. A implementação de `coluna_a_coluna` exigir decisão sobre chips com larguras muito diferentes não coberta pelas regras de `colunas.largura = "por_maior_item_da_coluna"`.
3. A implementação de âncoras exigir semântica diferente de "validação de posição no array `chips[]`" (ex.: âncoras por tipo, âncoras dinâmicas).
4. Qualquer arquivo na lista de "Arquivos proibidos" precisar ser alterado para concluir a implementação.
5. O cálculo `l_barra = len(linhas_barra) + 2` se tornar inválido pela lógica implementada (ex.: `_linhas_barra` precisar retornar estrutura diferente de lista de strings).
6. A integração com H-0015 (`altura`) exigir alteração na lógica de preenchimento vertical.
7. `loader.py` ou `modelo.py` precisarem validar ou transformar `distribuicao` para que `renderizador.py` funcione.
8. Qualquer nova regra normativa for necessária e não estiver coberta pelo ADR-0014 ou contratos existentes.

**Ao bloquear**, o executor deve:
- Registrar `ARCHITECTURE_REVIEW_REQUIRED` no topo do relatório `IMP-0016`.
- Descrever precisamente qual decisão arquitetural está faltando.
- **Não implementar código** além do que já está especificado sem bloqueio.

---

## Instrução explícita ao executor

Você é o OpenCode / GLM atuando como **executor de implementação**.

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
- Implementar **exatamente** o que este handoff especifica — sem funcionalidades extras, sem refatorações não solicitadas, sem abstrações adicionais.
- Não alterar nenhum arquivo da lista "Arquivos proibidos".
- Não decidir arquitetura — qualquer dúvida arquitetural → `ARCHITECTURE_REVIEW_REQUIRED`.
- Atualizar snapshots e expectativas literais de testes afetados pela mudança de layout horizontal, preservando a intenção dos testes.
- Criar o relatório `IMP-0016` ao final.
- Não fazer commit — o commit é responsabilidade de outra etapa do fluxo.

**Ordem de implementação recomendada**:
1. Migrar os 4 JSONs (menor risco, verificável imediatamente).
2. Implementar `_linhas_barra` nova (com todos os casos: linha única, multilinha, erro_layout, âncoras, alias).
3. Atualizar a chamada em `renderizar_tela`.
4. Rodar todos os testes existentes — identificar quais quebram por mudança de layout esperada.
5. Atualizar snapshots e expectativas literais afetados — garantir que todos passem.
6. Adicionar novos testes para H-0016.
7. Criar `IMP-0016`.

---

## Saída final esperada

Ao concluir, o executor deve reportar:

```
IMPLEMENTATION_COMPLETED

arquivos-alterados:
  scripts/config/telas/orquestrador.json
  scripts/config/telas/grupo_minimo.json
  scripts/config/telas/destino_minimo.json
  scripts/config/telas/stub_b.json
  scripts/tela/renderizador.py
  scripts/tela/teste_renderizador.py
  [scripts/tela/teste_demo.py — se snapshots alterados]
  [scripts/tela/teste_diagnostico.py — se snapshots alterados]
  scripts/docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md

testes:
  <N>/<N> passando

verificacoes:
  <git status --short>
  <git diff --stat>
```
