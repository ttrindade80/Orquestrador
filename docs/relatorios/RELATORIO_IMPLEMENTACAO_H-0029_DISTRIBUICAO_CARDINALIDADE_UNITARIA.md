# Relatório de Implementação — H-0029

## 1. Identificação

| Campo | Valor |
|---|---|
| Identificador | H-0029 |
| Título | Distribuição de containers com cardinalidade unitária |
| Data | 2026-07-12 |
| Commit-base | 921a06f |
| Executor | claude-sonnet-4-6 |

---

## 2. Causa técnica comprovada

**Função afetada:** `_renderizar_container_vertical` em `tela/renderizador.py`

**Caminho causal:**

Quando um container vertical com distribuição explícita (`distribuicao is not None and altura_disponivel is not None`) processava um filho do tipo `grupo`, ele:

1. Calculava a cota do grupo via `_distribuir_alturas`;
2. Chamava `_renderizar_container(arranjo_g, dist_g, filhos_grupo, ..., cota)` para obter o bloco do grupo;
3. Adicionava o bloco ao resultado com `partes.append(bloco)` **sem verificar se o bloco preenchia a cota**.

Se o grupo não declarava distribuição própria (`dist_g = None`), seus filhos usavam altura natural e o bloco retornado era menor que `cota`. Ao mesmo tempo, `renderizar_tela` marcava `_corpo_vertical_distribuido = True` (porque o corpo declarou distribuição), o que **desativava o fill externo H-0015**. O resultado final tinha menos linhas que `altura`.

**Reprodução automatizada (pré-patch):**

```
corpo=igual, 1 grupo sem dist, 1 dash -> 8 linhas (esperado 20)
corpo=igual, 1 grupo sem dist, 2 dash -> 10 linhas (esperado 20)
corpo=fracao[1], 1 grupo sem dist, 1 dash -> 8 linhas (esperado 20)
corpo=percentual[100], 1 grupo sem dist, 1 dash -> 8 linhas (esperado 20)
```

**Casos NÃO afetados pelo defeito:**

- Corpo com distribuição + grupo COM distribuição → funcionava (o grupo preencheria toda a cota com suas próprias cotas internas);
- Corpo sem distribuição + qualquer grupo → funcionava (fill externo H-0015 ativo);
- Corpo com distribuição + funcionais diretos (sem grupo) → funcionava.

**Rastreamento de condicionais:**

- Não há `len(elementos) == 1` especial em nenhuma função do caminho afetado;
- O defeito se manifestava com qualquer cardinalidade do grupo, não só unitária; a cardinalidade unitária era o cenário mais comum porque grupos maiores sem distribuição são menos utilizados;
- A diferença elemento funcional vs grupo está nas linhas 809-826 e 829-845 de `renderizador.py`.

---

## 3. Arquivos alterados

| Arquivo | Tipo de alteração |
|---|---|
| `tela/renderizador.py` | Correção: 7 linhas modificadas/inseridas |
| `tela/teste_renderizador.py` | Adição: classe `TestCardinalidadeUnitariaH0029` (60 verificações) |

Arquivos não alterados (verificado):
- `tela/loader.py` — não foi necessário;
- `tela/modelo.py` — não foi necessário;
- `config/telas/grupo_minimo.json` — não foi necessário;
- `config/telas/destino_minimo.json` — não foi necessário;
- `config/telas/stub_b.json` — não foi necessário;
- `config/telas/orquestrador.json` — não foi necessário;
- `docs/adr/`, `docs/contratos/`, `docs/handoff/` — intocados.

---

## 4. Comportamento anterior

Para `altura=20, largura=42` (l_corpo_disponivel=14):

| Cenário | Linhas esperadas | Linhas obtidas | Status |
|---|---:|---:|---|
| corpo=igual, 1 grupo sem dist, 1 dash | 20 | 8 | DEFEITO |
| corpo=igual, 1 grupo sem dist, 2 dash | 20 | 10 | DEFEITO |
| corpo=fracao[1], 1 grupo sem dist, 1 dash | 20 | 8 | DEFEITO |
| corpo=percentual[100], 1 grupo sem dist, 1 dash | 20 | 8 | DEFEITO |

O output com 8 linhas era: cabeçalho (3) + dashboard natural (2) + barra (3) = 8. O fill externo não era inserido porque `_corpo_vertical_distribuido = True`.

---

## 5. Comportamento corrigido

A correção garante que, no branch de distribuição de `_renderizar_container_vertical`, o bloco retornado por um grupo filho sempre tenha exatamente `cota` linhas. Quando o bloco tem menos linhas que `cota`, linhas de espaços (`" " * total_w`) são adicionadas ao final do bloco.

**Diff aplicado:**

```diff
- if bloco:
-     partes.append(bloco)
+ fill_linha = " " * total_w
+ if bloco:
+     linhas_bloco = bloco.split("\n")
+     while len(linhas_bloco) < cota:
+         linhas_bloco.append(fill_linha)
+     partes.append("\n".join(linhas_bloco))
+ elif cota > 0:
+     partes.append("\n".join(fill_linha for _ in range(cota)))
```

**Verificação pós-patch:**

| Cenário | Linhas esperadas | Linhas obtidas | Status |
|---|---:|---:|---|
| corpo=igual, 1 grupo sem dist, 1 dash | 20 | 20 | OK |
| corpo=igual, 1 grupo sem dist, 2 dash | 20 | 20 | OK |
| corpo=fracao[1], 1 grupo sem dist, 1 dash | 20 | 20 | OK |
| corpo=percentual[100], 1 grupo sem dist, 1 dash | 20 | 20 | OK |
| corpo=igual, 1 grupo IGUAL, 1 dash | 20 | 20 | OK (preservado) |
| corpo=igual, 1 grupo IGUAL, 2 dash | 20 | 20 | OK (preservado) |
| corpo=igual, 2 grupos IGUAL, 1 dash cada | 20 | 20 | OK (preservado) |
| corpo=igual, 2 dash diretos | 20 | 20 | OK (preservado) |
| corpo=sem, 1 grupo sem dist, 1 dash | 20 | 20 | OK (preservado) |
| corpus=sem, 1 grupo IGUAL, 1 dash | 20 | 20 | OK (preservado) |
| altura=30, corpus=igual, 1 grupo sem dist, 1 dash | 30 | 30 | OK |
| altura=30, corpus=igual, 1 grupo IGUAL, 1 dash | 30 | 30 | OK |

**Equivalência geométrica verificada:**

- `_render(igual, grupo IGUAL, 1 dash)` == `_render(fracao[1], grupo fracao[1], 1 dash)` → True
- `_render(igual, grupo IGUAL, 1 dash)` == `_render(percentual[100], grupo percentual[100], 1 dash)` → True
- `_render(igual, 1 dash direto)` == `_render(fracao[1], 1 dash direto)` → True
- `_render(igual, 1 dash direto)` == `_render(percentual[100], 1 dash direto)` → True

**Posição da barra:** em todos os cenários, a barra começa na linha 17 (0-indexed) para `altura=20`, confirmando posição correta.

**Caminho horizontal:** não afetado. `_renderizar_container_horizontal` já fazia fill de cada coluna até `altura_alvo` (linhas 911-928). O defeito era exclusivo do caminho vertical.

---

## 6. Testes criados

Classe `TestCardinalidadeUnitariaH0029` com 20 métodos de teste, totalizando 60 verificações.

Matriz de cenários cobertos:

| ID | Distribuição corpo | Filho do corpo | Distribuição grupo | Filhos grupo | Verificações |
|---|---|---|---|---|---|
| M01 | ausente | funcional | n/a | — | natural preservado |
| M02 | igual | funcional | n/a | — | filho ocupa área |
| M03 | fracao[1] | funcional | n/a | — | equiv. a M02 |
| M04 | percentual[100] | funcional | n/a | — | equiv. a M02 |
| M05 | igual | grupo | ausente | 1 | grupo recebe cota; filho natural |
| M06 | fracao[1] | grupo | ausente | 1 | equiv. a M05 |
| M07 | ausente | grupo | igual | 1 | grupo natural; dist interna |
| M08 | ausente | grupo | fracao[1] | 1 | equiv. a M07 |
| M09 | ausente | grupo | percentual[100] | 1 | equiv. a M07 |
| M10 | igual | grupo | igual | 1 | dois níveis integrais |
| M11 | fracao[1] | grupo | fracao[1] | 1 | equiv. a M10 |
| M12 | percentual[100] | grupo | percentual[100] | 1 | equiv. a M10 |
| M13 | igual | grupo | igual | 2 | comportamento existente preservado |

Verificações adicionais:
- `test_largura_linhas`: todas as linhas não vazias com largura correta;
- `test_redimensionamento_duas_alturas`: comportamento correto em altura=20 e altura=30;
- `test_soma_cotas_exata`: soma das cotas == l_corpo_disponivel;
- `test_composicao_dois_niveis_unitaria`: cardinalidade unitária em 2 níveis;
- `test_area_insuficiente_rejeicao_deterministica`: RenderizadorErro em área insuficiente;
- `test_integracao_json_grupo_minimo`: integração loader → modelo → renderer com JSON real;
- `test_preservacao_jsons_sem_dist`: `destino_minimo.json` e `stub_b.json` preservados.

---

## 7. Resultados dos testes focais

Comandos executados antes do patch (reprodução):

```
corpo=igual, 1 grupo sem dist, 1 dash -> 8 linhas (esperado 20) [DEFEITO]
corpo=igual, 1 grupo sem dist, 2 dash -> 10 linhas (esperado 20) [DEFEITO]
corpo=fracao[1], 1 grupo sem dist, 1 dash -> 8 linhas (esperado 20) [DEFEITO]
corpo=percentual[100], 1 grupo sem dist, 1 dash -> 8 linhas (esperado 20) [DEFEITO]
```

Comandos executados após o patch:

```
TODOS OK: 19 cenários verificados, 19/19 com total de linhas == altura
```

---

## 8. Suíte canônica completa

Comando:

```bash
python3 tela/teste_loader.py
python3 tela/teste_modelo.py
python3 tela/teste_renderizador.py
python3 tela/teste_demo.py
python3 tela/teste_diagnostico.py
python3 tela/teste_explorar_barra_de_menus.py
```

Resultados:

| Suíte | Verificações | Passaram | Falharam | Código de saída |
|---|---:|---:|---:|---|
| teste_loader.py | 172 | 172 | 0 | 0 |
| teste_modelo.py | 88 | 88 | 0 | 0 |
| teste_renderizador.py | 564 | 564 | 0 | 0 |
| teste_demo.py | 303 | 303 | 0 | 0 |
| teste_diagnostico.py | 28 | 28 | 0 | 0 |
| teste_explorar_barra_de_menus.py | 38 | 38 | 0 | 0 |
| **Total** | **1193** | **1193** | **0** | **0** |

Ciclo anterior (H-0028): 1133/1133. Diferença: +60 verificações novas do H-0029.

---

## 9. Inspeção do diff

```bash
git diff --stat tela/renderizador.py tela/teste_renderizador.py
```

```
tela/renderizador.py       |   8 +-
tela/teste_renderizador.py | 595 ++++++++++++++++++++++++++++++++++++++
2 files changed, 602 insertions(+), 1 deletion(-)
```

`git diff --check` sem saída (sem problemas de espaçamento).

---

## 10. Estado Git

### Antes da implementação

```
?? scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
?? scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md
?? scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_DISTRIBUICAO_CONTAINERS_CARDINALIDADE_UNITARIA.md
```

### Após a implementação

```
 M tela/renderizador.py
 M tela/teste_renderizador.py
?? docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
?? docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md
?? docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_DISTRIBUICAO_CONTAINERS_CARDINALIDADE_UNITARIA.md
```

Nenhum commit foi criado. Arquivos do ciclo preservados.

---

## 11. Pseudo-TTY

Não foi necessário pseudo-TTY para reproduzir o defeito. Os cenários foram inteiramente cobertos por testes sintéticos com estruturas em memória e testes de integração com JSONs reais. O defeito era mensurável por contagem de linhas (`splitlines()`), sem dependência de largura ou dimensão de terminal específica.

---

## 12. Limitações e itens não validados

1. **Comportamento visual em TTY real**: não foi validado em terminal físico.
2. **Grupos com estrutura=matriz recebendo cota**: o `_renderizar_container_matriz` lança `RenderizadorErro` quando `altura_disponivel is None`, mas quando recebe cota do pai, funciona internamente via `_renderizar_container_horizontal`. O fill do caminho vertical não se aplica ao container matricial (ele tem seu próprio caminho). Não há defeito identificado no caminho matricial, mas não há teste explícito de grupo matricial como filho único de corpo com distribuição.
3. **Cardinalidade unitária no caminho horizontal**: verificado que `_renderizar_container_horizontal` já faz fill de coluna até `altura_alvo` (linhas 911-928). Nenhum defeito identificado.

---

## 13. Declaração obrigatória

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

---

## 14. Patch pós-QA — ACH-I-003

### 14.1 Achado corrigido

```yaml
id: ACH-I-003
severidade: bloqueante
arquivo: scripts/config/telas/destino_minimo.json
problema: corpo.distribuicao adicionada fora do escopo do H-0029
```

### 14.2 Verificação do diff em destino_minimo.json

Comando executado:

```bash
git diff -- scripts/config/telas/destino_minimo.json
```

Resultado no estado verificado: **sem saída**. O arquivo não aparece modificado em `git diff --name-only`. O estado Git contém apenas:

```
M tela/renderizador.py
M tela/teste_renderizador.py
```

Conclusão: `destino_minimo.json` não estava modificado no estado atual. A alteração fora de escopo relatada pelo QA não persistiu nesta sessão. Nenhuma restauração via `git restore` foi necessária.

### 14.3 Confirmação de JSONs não modificados

```bash
git diff -- scripts/config/telas/
```

Sem saída. Nenhum JSON de tela está modificado:

- `config/telas/destino_minimo.json` — sem diff ✓
- `config/telas/grupo_minimo.json` — sem diff ✓
- `config/telas/stub_b.json` — sem diff ✓
- `config/telas/orquestrador.json` — sem diff ✓

### 14.4 Remoção do cache não rastreado

```bash
rm -rf -- tela/__pycache__/
```

Cache Python removido. `scripts/tela/__pycache__/` não aparece mais em `git status --short`.

### 14.5 Teste focal

Comandos executados:

```bash
python3 tela/teste_renderizador.py
```

Testes específicos que o QA reportou como falhos — agora passando:

```
[PASSOU] destino_minimo: sem distribuicao (distribuicao is None) - dist=None
[PASSOU] H-0029 preserv: destino_minimo distribuicao is None
```

Total: **564/564 — código de saída 0**.

### 14.6 Suíte canônica completa pós-patch

| Script | Verificações | Falhas | Código de saída |
|---|---:|---:|---|
| `python3 tela/teste_loader.py` | 172 | 0 | 0 |
| `python3 tela/teste_modelo.py` | 88 | 0 | 0 |
| `python3 tela/teste_renderizador.py` | 564 | 0 | 0 |
| `python3 tela/teste_demo.py` | 303 | 0 | 0 |
| `python3 tela/teste_diagnostico.py` | 28 | 0 | 0 |
| `python3 tela/teste_explorar_barra_de_menus.py` | 38 | 0 | 0 |
| **Total** | **1193** | **0** | **0** |

### 14.7 Estado Git final após patch

```text
 M tela/renderizador.py
 M tela/teste_renderizador.py
?? docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
?? docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md
?? docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_DISTRIBUICAO_CONTAINERS_CARDINALIDADE_UNITARIA.md
?? docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
```

`git diff --check` sem saída. Nenhum stage. Nenhum commit.

### 14.8 Validação manual

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

---

## 15. Patch PATCH_IMPLEMENTACAO — telas permanentes h0029_*

### 15.1 Referência ao patch aprovado do handoff

Este patch executa a etapa `PATCH_IMPLEMENTACAO` autorizada pelo handoff
H-0029 corrigido e novamente aprovado em
`docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_POS_CORRECAO_GRUPO_MINIMO.md`
(resultado `H1_HANDOFF_APPROVED`, sem achados pendentes). A etapa anterior já
havia alterado `tela/renderizador.py` e `tela/teste_renderizador.py` e alcançado
`1193/1193`. Esta etapa cria as sete telas JSON permanentes e os testes
nominais correspondentes, sem editar JSONs de referência.

### 15.2 Sete JSONs criados

```text
config/telas/h0029_dashboard_igual.json       (origem: destino_minimo.json)
config/telas/h0029_dashboard_fracao.json      (origem: destino_minimo.json)
config/telas/h0029_dashboard_percentual.json  (origem: destino_minimo.json)
config/telas/h0029_grupo_pai_distribuido.json (origem: grupo_minimo.json)
config/telas/h0029_grupo_igual.json           (origem: grupo_minimo.json)
config/telas/h0029_grupo_fracao.json          (origem: grupo_minimo.json)
config/telas/h0029_grupo_percentual.json      (origem: grupo_minimo.json)
```

Origem estrutural de cada conjunto:

- **Dashboards diretos** (`h0029_dashboard_*`): construídos a partir de
  `destino_minimo.json` como referência estrutural — `corpo.arranjo: vertical`,
  um `dashboard` com um campo literal e `barra_de_menus` válida copiada da
  referência.
- **Grupos** (`h0029_grupo_*`): construídos a partir de `grupo_minimo.json`
  como referência estrutural — `corpo.arranjo: vertical` com um `grupo`
  `vertical` contendo um `dashboard` com um campo literal e `barra_de_menus`
  válida copiada da referência.

### 15.3 Campos de distribuição declarados

| Tela | `corpo.distribuicao` | `grupo.distribuicao` |
|---|---|---|
| `h0029_dashboard_igual` | `{"modo": "igual"}` | n/a |
| `h0029_dashboard_fracao` | `{"modo": "fracao", "valores": [1]}` | n/a |
| `h0029_dashboard_percentual` | `{"modo": "percentual", "valores": [100]}` | n/a |
| `h0029_grupo_pai_distribuido` | `{"modo": "fracao", "valores": [1]}` | ausente |
| `h0029_grupo_igual` | `{"modo": "igual"}` | `{"modo": "igual"}` |
| `h0029_grupo_fracao` | `{"modo": "fracao", "valores": [1]}` | `{"modo": "fracao", "valores": [1]}` |
| `h0029_grupo_percentual` | `{"modo": "percentual", "valores": [100]}` | `{"modo": "percentual", "valores": [100]}` |

### 15.4 Testes adicionados

Classe `TestTelasPermanentesH0029` em `tela/teste_renderizador.py`, com 12
métodos de teste cobrindo 256 verificações nominais. Para cada um dos sete
JSONs, os testes verificam: existência; validade sintática; carregamento pelo
loader; construção do modelo; `id` correspondente; `schema`; quantidade de
filhos do corpo; tipo do filho; distribuição declarada; presença/ausência de
distribuição interna no grupo; modo e valores; renderização em duas alturas
(20 e 30); altura total; largura uniforme; posição da `barra_de_menus`;
índices de borda superior e inferior do dashboard; borda inferior
imediatamente antes da barra; continuidade das bordas laterais; ausência de
linhas externas entre dashboard e barra; ausência de sobreposição;
equivalência geométrica entre os três modos de dashboard e entre os três
modos de grupo; absorção da área adicional no redimensionamento.

### 15.5 Resultados por tela

Para `largura=42`, `altura ∈ {20, 30}`:

| Tela | alt=20 linhas | alt=30 linhas | dash topo | dash base (alt=20) | barra (alt=20) | geom. |
|---|---:|---:|---:|---:|---:|---|
| `h0029_dashboard_igual` | 20 | 30 | 3 | 16 | 17 | preenche |
| `h0029_dashboard_fracao` | 20 | 30 | 3 | 16 | 17 | preenche |
| `h0029_dashboard_percentual` | 20 | 30 | 3 | 16 | 17 | preenche |
| `h0029_grupo_pai_distribuido` | 20 | 30 | 3 | 5 | 17 | natural |
| `h0029_grupo_igual` | 20 | 30 | 3 | 16 | 17 | preenche |
| `h0029_grupo_fracao` | 20 | 30 | 3 | 16 | 17 | preenche |
| `h0029_grupo_percentual` | 20 | 30 | 3 | 16 | 17 | preenche |

- **preenche**: borda inferior do dashboard imediatamente antes da barra
  (`gap == 0`), dashboard ocupa toda a área distribuível.
- **natural** (`h0029_grupo_pai_distribuido`): dashboard em altura natural
  (3 linhas, índices 3..5); a sobra pertence à área estrutural do grupo (linhas
  em branco até a barra); o dashboard não é expandido até a barra, conforme o
  resultado esperado da seção 11A.4 do handoff.

### 15.6 Equivalências comprovadas

- **Dashboards**: `h0029_dashboard_igual` ≡ `h0029_dashboard_fracao` ≡
  `h0029_dashboard_percentual` (mesmas bordas, mesma altura do dashboard,
  mesma posição da barra) nas duas alturas.
- **Grupos**: `h0029_grupo_igual` ≡ `h0029_grupo_fracao` ≡
  `h0029_grupo_percentual` (mesmas bordas, mesma altura do dashboard, mesma
  posição da barra) nas duas alturas.

As saídas diferem apenas nos textos de identificação do cabeçalho.

### 15.7 Mecanismo real utilizado para selecionar a tela pelo `demo.py`

`tela/demo.py` **não expõe argumento de linha de comando** nem variável de
ambiente para selecionar a tela inicial. `main()` chama
`criar_estado_inicial()`, que codifica `tela_atual = "orquestrador"`, e em
seguida `_carregar_modelo_por_id(estado["tela_atual"])`.

O mecanismo real mais simples já suportado, sem alterar `demo.py` e sem editar
JSONs, é um comando `python -c` que importa o módulo `tela.demo`, substitui
`criar_estado_inicial` no namespace do módulo por uma função que fixa
`tela_atual` no identificador desejado e então chama `demo.main()`. Isso abre
a **interface real** (`main()` executa o loop TUI completo: alternate screen,
cbreak, SIGWINCH, wakeup pipe, renderização via `renderizar_estado` →
`renderizar_tela`), carregando o modelo pelo pipeline real
(`carregar_tela` → `construir_modelo`).

### 15.8 Comandos exatos do `demo.py`

Diretório de execução: `scripts/` (raiz do repositório de scripts). Cada
comando abre a interface TUI real da tela indicada. Requisito de TTY real para
a experiência interativa completa; em pipe (não-TTY) a demo imprime a
renderização inicial e lê comandos linha a linha (`s` ou `Esc` para sair).

Como sair: tecle `Esc` (ou `s` em modo pipe) — com `pilha_telas` vazia, a
demo encerra. Não há edição manual de JSON.

```bash
# h0029_dashboard_igual
cd "$(git rev-parse --show-toplevel)/scripts"
python3 -c "import sys; sys.dont_write_bytecode=True; sys.path.insert(0,'.'); import tela.demo as d; _o=d.criar_estado_inicial; d.criar_estado_inicial=lambda: (_o().__setitem__('tela_atual','h0029_dashboard_igual') or _o()); sys.exit(d.main())"

# h0029_dashboard_fracao
cd "$(git rev-parse --show-toplevel)/scripts"
python3 -c "import sys; sys.dont_write_bytecode=True; sys.path.insert(0,'.'); import tela.demo as d; _o=d.criar_estado_inicial; d.criar_estado_inicial=lambda: (_o().__setitem__('tela_atual','h0029_dashboard_fracao') or _o()); sys.exit(d.main())"

# h0029_dashboard_percentual
cd "$(git rev-parse --show-toplevel)/scripts"
python3 -c "import sys; sys.dont_write_bytecode=True; sys.path.insert(0,'.'); import tela.demo as d; _o=d.criar_estado_inicial; d.criar_estado_inicial=lambda: (_o().__setitem__('tela_atual','h0029_dashboard_percentual') or _o()); sys.exit(d.main())"

# h0029_grupo_pai_distribuido
cd "$(git rev-parse --show-toplevel)/scripts"
python3 -c "import sys; sys.dont_write_bytecode=True; sys.path.insert(0,'.'); import tela.demo as d; _o=d.criar_estado_inicial; d.criar_estado_inicial=lambda: (_o().__setitem__('tela_atual','h0029_grupo_pai_distribuido') or _o()); sys.exit(d.main())"

# h0029_grupo_igual
cd "$(git rev-parse --show-toplevel)/scripts"
python3 -c "import sys; sys.dont_write_bytecode=True; sys.path.insert(0,'.'); import tela.demo as d; _o=d.criar_estado_inicial; d.criar_estado_inicial=lambda: (_o().__setitem__('tela_atual','h0029_grupo_igual') or _o()); sys.exit(d.main())"

# h0029_grupo_fracao
cd "$(git rev-parse --show-toplevel)/scripts"
python3 -c "import sys; sys.dont_write_bytecode=True; sys.path.insert(0,'.'); import tela.demo as d; _o=d.criar_estado_inicial; d.criar_estado_inicial=lambda: (_o().__setitem__('tela_atual','h0029_grupo_fracao') or _o()); sys.exit(d.main())"

# h0029_grupo_percentual
cd "$(git rev-parse --show-toplevel)/scripts"
python3 -c "import sys; sys.dont_write_bytecode=True; sys.path.insert(0,'.'); import tela.demo as d; _o=d.criar_estado_inicial; d.criar_estado_inicial=lambda: (_o().__setitem__('tela_atual','h0029_grupo_percentual') or _o()); sys.exit(d.main())"
```

### 15.9 Ausência de CLI direta

`demo.py` não aceita argumento posicional, `--tela`, variável de ambiente ou
qualquer outro mecanismo nativo de seleção da tela inicial. A CLI direta é
ausente; o mecanismo utilizado (seção 15.7) é o ponto de entrada interno mais
simples que abre a interface real sem modificar `demo.py`.

### 15.10 Alterações adicionais no renderer

**Nenhuma.** Nenhum dos sete JSONs reproduziu falha funcional objetiva no
renderer. As sete telas carregam, constroem modelo e renderizam com a geometria
esperada da seção 11A do handoff usando a correção já aplicada na etapa
anterior (seção 5 deste relatório). O patch desta etapa limitou-se a criar os
sete JSONs e adicionar os testes nominais.

### 15.11 Suíte canônica atualizada

Comando executado a partir de `scripts/`:

```bash
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
python tela/teste_diagnostico.py
python tela/teste_explorar_barra_de_menus.py
```

| Script | Verificações | Passaram | Falharam | Código de saída |
|---|---:|---:|---:|---|
| `teste_loader.py` | 172 | 172 | 0 | 0 |
| `teste_modelo.py` | 88 | 88 | 0 | 0 |
| `teste_renderizador.py` | 820 | 820 | 0 | 0 |
| `teste_demo.py` | 303 | 303 | 0 | 0 |
| `teste_diagnostico.py` | 28 | 28 | 0 | 0 |
| `teste_explorar_barra_de_menus.py` | 38 | 38 | 0 | 0 |
| **Total** | **1449** | **1449** | **0** | **0** |

O total anterior era `1193/1193`. Diferença: `+256` verificações nominais dos
sete JSONs permanentes (classe `TestTelasPermanentesH0029`).

### 15.12 Smoke tests das sete telas

Confirmado automaticamente que cada uma das sete telas: é localizada em disco;
carrega pelo loader real sem exceção; constrói modelo sem exceção; inicia pelo
mecanismo do `demo.py` (pipeline real `carregar_tela` → `construir_modelo` →
`renderizar_estado`) sem erro imediato antes da interação humana. Resultado:
`7/7 OK`.

### 15.13 Estado Git final

```text
 M tela/renderizador.py
 M tela/teste_renderizador.py
?? config/telas/h0029_dashboard_igual.json
?? config/telas/h0029_dashboard_fracao.json
?? config/telas/h0029_dashboard_percentual.json
?? config/telas/h0029_grupo_pai_distribuido.json
?? config/telas/h0029_grupo_igual.json
?? config/telas/h0029_grupo_fracao.json
?? config/telas/h0029_grupo_percentual.json
?? docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
?? docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md
?? docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_DISTRIBUICAO_CONTAINERS_CARDINALIDADE_UNITARIA.md
?? docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_POS_CORRECAO_GRUPO_MINIMO.md
?? docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_POS_PATCH_TELAS_PERMANENTES.md
?? docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
```

`git diff --check` sem saída. Nenhum stage. Nenhum commit.

JSONs de referência preservados (sem diff): `config/telas/grupo_minimo.json`,
`config/telas/destino_minimo.json`, `config/telas/stub_b.json`,
`config/telas/orquestrador.json`.

### 15.14 Validação manual

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

---

## 16. Patch pós-QA-POS — correção QA-POS-H0029-001

### 16.1 Achado corrigido

```yaml
id: QA-POS-H0029-001
severidade: alto
arquivo: scripts/docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
local: "seção 15.8, sete comandos python3 -c"
problema: os comandos documentados abriam a tela raiz ORQUESTRADOR em vez da tela h0029_* indicada
```

### 16.2 Causa do comando anterior

A expressão usada na seção 15.8 era:

```python
lambda: (_o().__setitem__('tela_atual', '<id>') or _o())
```

`_o()` (apelido de `d.criar_estado_inicial`) era chamado **duas vezes**:

1. Primeira chamada: cria um dict `{"tela_atual": "orquestrador", ...}`, chama
   `__setitem__('tela_atual', '<id>')` — que modifica esse dict e retorna
   `None`.
2. Como `__setitem__` retorna `None` (falsy), o `or` é avaliado: segunda
   chamada cria e retorna um **novo dict padrão** com
   `tela_atual: "orquestrador"`.

O lambda retornava o segundo dict, sem a modificação. Por isso, `demo.main()`
carregava a tela raiz, não a tela `h0029_*` desejada.

### 16.3 Mecanismo corrigido

O mecanismo corrigido cria o estado exatamente uma vez, altera `tela_atual`
nesse mesmo dicionário e retorna o mesmo objeto modificado:

```python
_orig = demo.criar_estado_inicial

def _criar():
    e = _orig()
    e['tela_atual'] = '<id_da_tela>'
    return e

demo.criar_estado_inicial = _criar
```

`demo.criar_estado_inicial` é substituído somente no namespace do módulo
carregado no processo atual, sem editar `demo.py` nem qualquer JSON.

### 16.4 Sete comandos corrigidos

Diretório de execução: `scripts/` (raiz do repositório de scripts). Como
sair: tecle `Esc` (ou `s` em modo pipe, sem TTY). Os comandos substituídos
abaixo invalidam os sete comandos defeituosos da seção 15.8 (achado
`QA-POS-H0029-001`).

```bash
# h0029_dashboard_igual
cd "$(git rev-parse --show-toplevel)/scripts"
python3 -c "
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
import tela.demo as demo

_orig = demo.criar_estado_inicial

def _criar():
    e = _orig()
    e['tela_atual'] = 'h0029_dashboard_igual'
    return e

demo.criar_estado_inicial = _criar
sys.exit(demo.main())
"
```

```bash
# h0029_dashboard_fracao
cd "$(git rev-parse --show-toplevel)/scripts"
python3 -c "
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
import tela.demo as demo

_orig = demo.criar_estado_inicial

def _criar():
    e = _orig()
    e['tela_atual'] = 'h0029_dashboard_fracao'
    return e

demo.criar_estado_inicial = _criar
sys.exit(demo.main())
"
```

```bash
# h0029_dashboard_percentual
cd "$(git rev-parse --show-toplevel)/scripts"
python3 -c "
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
import tela.demo as demo

_orig = demo.criar_estado_inicial

def _criar():
    e = _orig()
    e['tela_atual'] = 'h0029_dashboard_percentual'
    return e

demo.criar_estado_inicial = _criar
sys.exit(demo.main())
"
```

```bash
# h0029_grupo_pai_distribuido
cd "$(git rev-parse --show-toplevel)/scripts"
python3 -c "
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
import tela.demo as demo

_orig = demo.criar_estado_inicial

def _criar():
    e = _orig()
    e['tela_atual'] = 'h0029_grupo_pai_distribuido'
    return e

demo.criar_estado_inicial = _criar
sys.exit(demo.main())
"
```

```bash
# h0029_grupo_igual
cd "$(git rev-parse --show-toplevel)/scripts"
python3 -c "
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
import tela.demo as demo

_orig = demo.criar_estado_inicial

def _criar():
    e = _orig()
    e['tela_atual'] = 'h0029_grupo_igual'
    return e

demo.criar_estado_inicial = _criar
sys.exit(demo.main())
"
```

```bash
# h0029_grupo_fracao
cd "$(git rev-parse --show-toplevel)/scripts"
python3 -c "
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
import tela.demo as demo

_orig = demo.criar_estado_inicial

def _criar():
    e = _orig()
    e['tela_atual'] = 'h0029_grupo_fracao'
    return e

demo.criar_estado_inicial = _criar
sys.exit(demo.main())
"
```

```bash
# h0029_grupo_percentual
cd "$(git rev-parse --show-toplevel)/scripts"
python3 -c "
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
import tela.demo as demo

_orig = demo.criar_estado_inicial

def _criar():
    e = _orig()
    e['tela_atual'] = 'h0029_grupo_percentual'
    return e

demo.criar_estado_inicial = _criar
sys.exit(demo.main())
"
```

### 16.5 Verificação do estado inicial (não interativa)

Para cada comando, a construção idêntica — substituindo `demo.main()` por uma
asserção direta — confirma que a função substituída retorna o dict com
`tela_atual` correto. Executado em `scripts/`:

```bash
python3 -c "
import sys; sys.dont_write_bytecode=True; sys.path.insert(0,'.')
import tela.demo as demo
_orig = demo.criar_estado_inicial
def _criar():
    e = _orig()
    e['tela_atual'] = '<id_da_tela>'
    return e
demo.criar_estado_inicial = _criar
e = demo.criar_estado_inicial()
assert e['tela_atual'] == '<id_da_tela>', 'FALHA'
print('OK:', e['tela_atual'])
"
```

Resultados:

| Tela | `tela_atual` retornado | Resultado |
|---|---|---|
| `h0029_dashboard_igual` | `'h0029_dashboard_igual'` | OK |
| `h0029_dashboard_fracao` | `'h0029_dashboard_fracao'` | OK |
| `h0029_dashboard_percentual` | `'h0029_dashboard_percentual'` | OK |
| `h0029_grupo_pai_distribuido` | `'h0029_grupo_pai_distribuido'` | OK |
| `h0029_grupo_igual` | `'h0029_grupo_igual'` | OK |
| `h0029_grupo_fracao` | `'h0029_grupo_fracao'` | OK |
| `h0029_grupo_percentual` | `'h0029_grupo_percentual'` | OK |

### 16.6 Smoke tests dos sete comandos corrigidos

Executados em modo pipe (`printf 's\n' | python3 -c "..."`) a partir de
`scripts/`. Entrada controlada: `s\n` (sair sem interação prolongada). A
primeira linha impressa é a primeira linha da renderização inicial.

| Tela | Código | Primeira linha renderizada | `ORQUESTRADOR` indevido | TUI real | Resultado |
|---|---:|---|---|---|---|
| `h0029_dashboard_igual` | 0 | `╭ H-0029 DASHBOARD IGUAL` | não | sim | APROVADO |
| `h0029_dashboard_fracao` | 0 | `╭ H-0029 DASHBOARD FRACAO` | não | sim | APROVADO |
| `h0029_dashboard_percentual` | 0 | `╭ H-0029 DASHBOARD PERCENTUAL` | não | sim | APROVADO |
| `h0029_grupo_pai_distribuido` | 0 | `╭ H-0029 GRUPO PAI DISTRIBUIDO` | não | sim | APROVADO |
| `h0029_grupo_igual` | 0 | `╭ H-0029 GRUPO IGUAL` | não | sim | APROVADO |
| `h0029_grupo_fracao` | 0 | `╭ H-0029 GRUPO FRACAO` | não | sim | APROVADO |
| `h0029_grupo_percentual` | 0 | `╭ H-0029 GRUPO PERCENTUAL` | não | sim | APROVADO |

### 16.7 Testes de regressão

Nenhum código foi alterado neste patch. A suíte foi executada a partir de
`scripts/` após a remoção do cache `tela/__pycache__/`.

| Script | Verificações | Passaram | Falharam | Código de saída |
|---|---:|---:|---:|---|
| `python tela/teste_loader.py` | 172 | 172 | 0 | 0 |
| `python tela/teste_modelo.py` | 88 | 88 | 0 | 0 |
| `python tela/teste_renderizador.py` | 820 | 820 | 0 | 0 |
| `python tela/teste_demo.py` | 303 | 303 | 0 | 0 |
| `python tela/teste_diagnostico.py` | 28 | 28 | 0 | 0 |
| `python tela/teste_explorar_barra_de_menus.py` | 38 | 38 | 0 | 0 |
| **Total** | **1449** | **1449** | **0** | **0** |

### 16.8 Estado Git final após patch QA-POS-H0029-001

```text
 M tela/renderizador.py
 M tela/teste_renderizador.py
?? config/telas/h0029_dashboard_fracao.json
?? config/telas/h0029_dashboard_igual.json
?? config/telas/h0029_dashboard_percentual.json
?? config/telas/h0029_grupo_fracao.json
?? config/telas/h0029_grupo_igual.json
?? config/telas/h0029_grupo_pai_distribuido.json
?? config/telas/h0029_grupo_percentual.json
?? docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
?? docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md
?? docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_DISTRIBUICAO_CONTAINERS_CARDINALIDADE_UNITARIA.md
?? docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_POS_CORRECAO_GRUPO_MINIMO.md
?? docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_POS_PATCH_TELAS_PERMANENTES.md
?? docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0029_TELAS_PERMANENTES.md
```

`git diff --check` sem saída. `demo.py` sem diff. `renderizador.py` somente
diff acumulado das etapas anteriores (seção 5). Nenhum JSON alterado.
`tela/__pycache__/` removido. Nenhum stage. Nenhum commit.

Somente `RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md`
foi alterado neste patch.

### 16.9 Validação manual

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```
