# RELATORIO_LEVANTAMENTO_POS_H0018_PROXIMO_CORPO

> **Nota**: Este é um relatório auxiliar de levantamento pós-H-0018. Não consome número de handoff. O próximo handoff real reservado é H-0019.

```text
levantamento_por:  Claude Code (papel levantamento pós-ciclo)
data:              2026-07-09
ciclo_referencia:  H-0018
titulo:            Levantamento pós-H-0018; identificação do próximo ciclo de composição/layout do corpo
commit_base:       46e0cb9  feat: cobre distribuicao da barra de menus
diretorio_base:    /home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts
```

---

## Status

```text
LEVANTAMENTO_CONCLUIDO
```

Nenhum bloqueio identificado. Workspace limpo. HEAD confirmado. Testes em baseline perfeito.
Artefatos H-0015 a H-0018 todos presentes. Próximo ciclo identificado.

---

## Base verificada

### HEAD observado

```text
46e0cb9  feat: cobre distribuicao da barra de menus  ← CONFIRMADO
```

Corresponde exatamente ao commit esperado pela especificação do levantamento.

### Sequência recente de commits

```text
46e0cb9 feat: cobre distribuicao da barra de menus
c8a20fa test: adiciona explorador da barra de menus
ab5ad68 feat: renderiza barra de menus horizontal responsiva
b2eb458 feat: ocupa altura do terminal pelo corpo
4762583 docs: registra ocupacao vertical e barra responsiva
8a6403a feat: migra arranjo vertical e barra declarativa
ceaf0be docs: registra ADRs de arranjo e barra declarativa
ab48702 feat: adiciona acesso demonstravel ao grupo minimo
```

Sequência coerente com os ciclos H-0015 (b2eb458), H-0016 (ab5ad68), H-0017 (c8a20fa),
H-0018 (46e0cb9). Sem commit fora de ordem identificado.

### Estado do workspace

```text
git status --short : (sem saída — workspace limpo)
git diff --stat    : (sem saída — sem alterações staged ou unstaged)
git diff --name-only : (sem saída)
```

**Workspace: LIMPO**. Nenhum arquivo modificado, staged ou não rastreado.

### Diretório operacional detectado

```text
/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts
```

Estou **dentro de `scripts/`**. Todos os caminhos relativos neste relatório partem
desta raiz (ex.: `docs/contratos/`, `tela/`, `config/`).

---

## Artefatos H-0015 a H-0018 encontrados

Resultado do comando:

```bash
find docs -type f \( -name '*H-0015*' -o -name '*H-0016*' -o -name '*H-0017*' -o -name '*H-0018*' \) | sort
```

```text
docs/handoff/H-0015-ocupacao-vertical-janela-terminal-corpo.md
docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
docs/handoff/H-0017-script-exploracao-combinacoes-barra-de-menus.md
docs/handoff/H-0018-cobertura-executavel-distribuicao-barra-de-menus.md
docs/relatorios/RELATORIO_AUDITORIA_H-0015_HANDOFF.md
docs/relatorios/RELATORIO_AUDITORIA_H-0016_HANDOFF.md
docs/relatorios/RELATORIO_AUDITORIA_H-0016_HANDOFF_POS_REVISAO.md
docs/relatorios/RELATORIO_AUDITORIA_H-0017_HANDOFF.md
docs/relatorios/RELATORIO_AUDITORIA_H-0018_HANDOFF.md
docs/relatorios/RELATORIO_QA_H-0015_OCUPACAO_VERTICAL_JANELA_TERMINAL_CORPO.md
docs/relatorios/RELATORIO_QA_H-0016_MIGRACAO_JSON_BARRA_DE_MENUS_HORIZONTAL_RESPONSIVA.md
docs/relatorios/RELATORIO_QA_H-0017_SCRIPT_EXPLORACAO_COMBINACOES_BARRA_DE_MENUS.md
docs/relatorios/RELATORIO_QA_H-0018_COBERTURA_EXECUTAVEL_DISTRIBUICAO_BARRA_DE_MENUS.md
docs/relatorios/RELATORIO_QA_H-0018_POS_CORRECOES.md
```

Adicionalmente, os relatórios de implementação (IMP) estão em `docs/relatorios/`:

```text
docs/relatorios/IMP-0015-ocupacao-vertical-janela-terminal-corpo.md
docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
docs/relatorios/IMP-0017-script-exploracao-combinacoes-barra-de-menus.md
docs/relatorios/IMP-0018-cobertura-executavel-distribuicao-barra-de-menus.md
```

### Tabela de artefatos por ciclo

| Ciclo | Handoff encontrado? | IMP encontrado? | QA encontrado? | Status identificado | Observações |
|-------|---------------------|-----------------|----------------|---------------------|-------------|
| H-0015 | Sim — `H-0015-ocupacao-vertical-janela-terminal-corpo.md` | Sim — `IMP-0015-...` | Sim — `RELATORIO_QA_H-0015_...` | FECHADO | Auditoria presente; QA aprovado |
| H-0016 | Sim — `H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md` | Sim — `IMP-0016-...` | Sim — `RELATORIO_QA_H-0016_...` | FECHADO | Auditoria pós-revisão presente (2 versões) |
| H-0017 | Sim — `H-0017-script-exploracao-combinacoes-barra-de-menus.md` | Sim — `IMP-0017-...` | Sim — `RELATORIO_QA_H-0017_...` | FECHADO | Auditoria presente |
| H-0018 | Sim — `H-0018-cobertura-executavel-distribuicao-barra-de-menus.md` | Sim — `IMP-0018-...` | Sim — 2 versões (QA + pós-correções) | FECHADO / QA_POST_CORRECTIONS_APPROVED | Status final: QA pós-correções aprovado; 544/544 verificações |

**Conclusão**: todos os artefatos esperados estão presentes. H-0018 encerrado com
`QA_POST_CORRECTIONS_APPROVED` conforme relatório `RELATORIO_QA_H-0018_POS_CORRECOES.md`.

---

## Resultado dos testes de baseline

Comandos executados com `PYTHONDONTWRITEBYTECODE=1` para evitar geração de `.pyc`.

### Tabela de resultados

| Comando | Exit code | Verificações | Resultado |
|---------|-----------|--------------|-----------|
| `python tela/teste_loader.py` | 0 | 79/79 | PASSOU |
| `python tela/teste_modelo.py` | 0 | 56/56 | PASSOU |
| `python tela/teste_renderizador.py` | 0 | 226/226 | PASSOU |
| `python tela/teste_demo.py` | 0 | 117/117 | PASSOU |
| `python tela/teste_diagnostico.py` | 0 | 28/28 | PASSOU |
| `python tela/teste_explorar_barra_de_menus.py` | 0 | 38/38 | PASSOU |

**Total: 544/544 verificações passando.** Nenhuma falha. Baseline perfeito.

### Verificação de caches Python

```bash
find . -name '__pycache__' -type d -print   → (sem saída)
find . -name '*.pyc' -print                 → (sem saída)
```

Nenhum cache criado durante esta execução. `PYTHONDONTWRITEBYTECODE=1` foi efetivo.
Nenhum arquivo removido.

---

## Estado da barra_de_menus

### Campos de `barra_de_menus.distribuicao` já cobertos

Conforme `IMP-0018-cobertura-executavel-distribuicao-barra-de-menus.md`, todos os
30 campos de `barra_de_menus.distribuicao` estão cobertos:

| Categoria | Campos | Quantidade |
|-----------|--------|------------|
| USADO (efeito observável no layout) | `modo`, `ordem.ancoras.{primeiro,ultimo}`, `preenchimento_multilinha`, `linhas.{minimo,maximo}`, `espacamentos.margem_horizontal.minimo`, `espacamentos.vao_chip_texto.minimo`, `espacamentos.vao_entre_{chips,colunas}.minimo`, `chips[]` | 13 |
| VALIDADO (lido, erro se inválido) | `ordem.politica`, `preenchimentos_multilinha_suportados`, `espacamentos.margem_horizontal.maximo`, `espacamentos.vao_chip_texto.maximo`, `espacamentos.vao_entre_{chips,colunas}.maximo`, `overflow.{quando_nao_couber,nao_omitir_chips,nao_truncar_texto,nao_reordenar}` | 10 |
| REJEITADO (valor fora do subconjunto suportado → `RenderizadorErro`) | `tentativa_inicial`, `quebra`, `linhas.preferir_menor_numero`, `alinhamento_linhas`, `espacamentos.vao_vertical_entre_linhas.{minimo,maximo}`, `colunas.largura`, `colunas.subcolunas.{chip,texto}.alinhamento` | 10 |

Nenhum campo com status "ignorado". Cobertura: 30/30.

### Invariantes que devem ser preservados

- `_normaliza_distribuicao`: normalização canônica de `distribuicao = "horizontal"` ou ausente para objeto padrão.
- `_validar_distribuicao`: 10 validações de rejeição explícita para campos "Option B" não suportados.
- `_linhas_barra`: aplica `margem_horizontal.minimo` (prefixo de espaços) e `vao_chip_texto.minimo`; respeita `linhas.minimo > 1` para pular tentativa de linha única.
- `explorar_barra_de_menus.py`: matriz C15 padrão; INV-2, INV-4 corretos; sem bug `or True`.

### Riscos de regressão para o próximo ciclo

1. **Qualquer alteração em `_linhas_barra`, `_normaliza_distribuicao` ou `_validar_distribuicao`**
   sem necessidade explícita pode reverter coberturas de H-0018.
2. **Alteração de snapshots em `teste_demo.py` ou `teste_diagnostico.py`** sem justificativa
   formal pode mascarar regressão de margem.
3. **Nova import, refatoração de módulo ou reordenação de funções** em `renderizador.py`
   pode quebrar os 226 testes de `teste_renderizador.py` de forma silenciosa se os
   testes não forem executados.

### Arquivos que o próximo ciclo deve evitar alterar salvo necessidade explícita

```text
tela/renderizador.py          → apenas as funções _normaliza_distribuicao,
                                 _validar_distribuicao e _linhas_barra
tela/explorar_barra_de_menus.py
tela/teste_explorar_barra_de_menus.py
tela/teste_renderizador.py    → apenas a classe TestDistribuicaoH0018
tela/teste_demo.py            → apenas snapshots com margem_horizontal
tela/teste_diagnostico.py     → apenas snapshots com margem_horizontal
```

---

## Estado da composição do corpo

### Estado atual de `console`, `lancador`, `dashboard` e `grupo`

| Tipo | Suportado pelo loader? | Suportado pelo modelo? | Suportado pelo renderer? | Observação |
|------|------------------------|------------------------|--------------------------|------------|
| `console` | Sim (validado por tipo) | Sim (Elemento) | Sim (caixa via `_caixa_de_elemento`) | Limitado: não renderiza itens internos com conteúdo real |
| `lancador` | Sim | Sim | Sim (caixa com itens `chip + texto`) | Modo fila/matriz calculado; `texto ≤ 15 chars` validado |
| `dashboard` | Sim | Sim | Sim (caixa) | Conteúdo interno placeholder; campos do Orquestrador não renderizados |
| `grupo` | Sim (H-0012) | Sim (container plano) | Sim (percorre elementos internos) | Apenas `arranjo = "vertical"` ou alias `"sobreposto"`; horizontal explicitamente rejeitado pelo loader |

### O que já existe no loader/modelo/renderizador

- **Loader** (`loader.py`): valida tipos de elemento (`console`, `lancador`, `dashboard`, `grupo`);
  lê `corpo.arranjo` mas **não valida o valor** no nível da tela (qualquer string ou `None` é aceito);
  rejeita `grupo` com `arranjo = "horizontal"` ou `"lado_a_lado"` (H-0014).
- **Modelo** (`modelo.py`): armazena `corpo.arranjo` como string ou `None` sem normalização.
  Estrutura: `Corpo(arranjo, elementos=[...])`.
- **Renderer** (`renderizador.py`, função `tela()`): percorre `modelo.corpo.elementos` em
  **laço sequencial** (linhas 779–795) e empilha caixas verticalmente. O campo
  `modelo.corpo.arranjo` **não é lido em nenhum momento** pelo renderer — o arranjo
  horizontal está especificado no contrato mas não implementado.

### Limitações atuais observadas

1. **`corpo.arranjo = "horizontal"` não implementado**: qualquer tela com este arranjo
   seria renderizada verticalmente sem erro e sem aviso. O renderer não diferencia
   vertical de horizontal.
2. **Aliases transicionais não normalizados**: `destino_minimo.json` e `stub_b.json`
   declaram `"arranjo": "sobreposto"` (alias de "vertical" por ADR-0011). O loader
   passa o valor sem normalizar; o modelo armazena "sobreposto". O renderer ignora,
   mas quando implementar horizontal precisará distinguir "sobreposto" → vertical de
   "lado_a_lado" → horizontal.
3. **Loader não valida `arranjo` no nível da tela**: valor inválido como `"diagonal"`
   seria aceito silenciosamente.
4. **Conteúdo interno de `console` e `dashboard`** não é renderizado com campos reais —
   apenas placeholder/estrutura mínima. Não é bloqueio para o próximo ciclo de layout.

### O que ainda não existe ou não está comprovado

- Renderer que leia e aplique `modelo.corpo.arranjo` para decidir layout.
- Suporte a `arranjo = "horizontal"` com 3 vãos iguais (especificado no contrato,
  seção 5.6, mas sem implementação).
- JSON ativo com `arranjo = "horizontal"` (nenhum JSON de produção usa horizontal).
- Validação de `arranjo` no loader para o nível da tela (só rejeita horizontal em grupos).

---

## Pendências reais

| # | Descrição | Evidência | Impacto | Sugestão de tratamento |
|---|-----------|-----------|---------|----------------------|
| P-1 | Renderer ignora `corpo.arranjo` — não diferencia vertical de horizontal | `tela()` linhas 779-795: laço sequencial sem branch por `arranjo` | Tela com `arranjo = "horizontal"` renderizada incorretamente sem erro | H-0019: implementar suporte a horizontal no renderer |
| P-2 | `destino_minimo.json` e `stub_b.json` usam alias transitional `"sobreposto"` | `grep config/telas/*.json` | Baixo impacto atual; risco quando renderer começar a distinguir arranjos | Bundlar com H-0019 ou ciclo de migração dedicado |
| P-3 | Loader não valida `arranjo` no nível da tela | `loader.py` linha 347: `arranjo = corpo.get("arranjo")` sem verificação | Valor inválido aceito silenciosamente | Validar em H-0019 junto com implementação horizontal |
| P-4 | Nenhum JSON ativo de teste usa `arranjo = "horizontal"` | `grep config/telas/*.json` | Horizontal nunca testado em integração | H-0019 deve criar ou adaptar JSON de teste |

---

## Itens adiados de propósito

Os itens abaixo foram explicitamente adiados em ciclos anteriores e **não devem
bloquear nem entrar no próximo ciclo**:

| Item | Origem do adiamento | Motivo do adiamento |
|------|---------------------|---------------------|
| Combinação `arranjo = horizontal` + `dashboard` presente (indicador de paginação) | `contrato_composicao_corpo.md` seção 9 | Comportamento indefinido; aguarda handoff futuro após implementação básica horizontal |
| Migração do campo `posicao_dashboard` (ADR-0010) | `contrato_composicao_corpo.md` seção 9 | JSONs existentes com o campo mantidos por compatibilidade; migração em handoff específico |
| Schema de grupos hierárquicos no `corpo.elementos[]` | `contrato_composicao_corpo.md` seção 9 | Especificado incrementalmente; não criar schema antecipado |
| Revisão formal de `contrato_lancador.md` (DOC-0020) | `contrato_composicao_corpo.md` seção 5.2 | Tarefa documental pendente; não bloqueia implementação de layout |
| Revisão de `console` como container genérico (DOC-0024) | `contrato_composicao_corpo.md` seção 5.4 | Pendência documental; contrato e tipos internos de item são DOC-B008 |
| Relação entre `filtro_de_grupo` e `formacao_de_selecao` | `contrato_composicao_corpo.md` seção 9 | Coexistência/exclusividade não definida; não afeta layout básico |
| Distribuição percentual/fração de espaço | — | Capacidade futura; não confundir com layout horizontal plano |
| Aninhamento real de grupos com arranjo hierárquico | — | Capacidade futura além do grupo plano (H-0012) |

---

## Riscos para o próximo handoff

### R-1 — Misturar layout horizontal com percentual/fração ou aninhamento

**Descrição**: implementar horizontal flat (3 vãos iguais) e ao mesmo tempo introduzir
lógica de distribuição percentual de largura ou suporte a grupos aninhados com arranjos
próprios.

**Por que é risco**: o contrato especifica 3 vãos iguais para horizontal (seção 5.6) —
não percentual. Misturar os dois no mesmo ciclo torna a verificação de requisitos
ambígua e dificulta reversão parcial.

**Mitigação**: escopo do próximo ciclo limitado a `arranjo = "horizontal"` com 3 vãos
iguais. Percentual/fração e aninhamento são ciclos futuros separados.

### R-2 — Reabrir H-0011 ou H-0011A

**Descrição**: handoff H-0011 (renderização lado a lado com barra mínima) foi CANCELADO
antes de qualquer implementação. H-0011A foi REMOVIDO por granularidade excessiva.

**Por que é risco**: ao implementar layout horizontal, pode surgir tentação de reabrir
H-0011 como "base histórica" ou de criar H-0011A como etapa intermediária.

**Evidência de histórico**: documentação em `docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md`
e `H-0013-...` contém as diretrizes:
```text
NÃO reabrir H-0011.
NÃO recriar H-0011A.
NÃO usar H-0011 nem H-0011A como base implementável.
```

**Mitigação**: o próximo handoff (H-0019) NÃO menciona H-0011 ou H-0011A como referência.
H-0011 permanece como referência histórica arquivada.

### R-3 — Alterar barra_de_menus sem necessidade

**Descrição**: ao modificar a função `tela()` para suportar arranjo horizontal,
pode haver tentação de refatorar também as funções de `barra_de_menus` na mesma passagem.

**Por que é risco**: `barra_de_menus.distribuicao` foi coberta com precisão em H-0018.
Alteração sem necessidade pode desfazer validações de rejeição ou comportamentos
de `_linhas_barra`.

**Mitigação**: H-0019 deve tocar `renderizador.py` apenas na função `tela()` (e possivelmente
`_caixa_de_elemento`), não em `_normaliza_distribuicao`, `_validar_distribuicao` nem
`_linhas_barra`.

### R-4 — Decisão arquitetural implícita no renderer

**Descrição**: implementar horizontal no renderer pode requerer decisão sobre como
representar "2 caixas lado a lado" em texto — como strings com zip por linhas?
Como matriz 2D? A escolha tem consequências para paginação, indicador, grupos aninhados.

**Por que é risco**: a escolha pode criar acoplamento implícito com funcionalidades
futuras (combinação horizontal + dashboard, aninhamento).

**Mitigação**: o handoff H-0019 deve estabelecer explicitamente o mecanismo de
renderização lado a lado (provavelmente zip de linhas das caixas) e documentar
que o escopo é exclusivamente 2+ elementos no topo da lista plana — sem aninhamento.

### R-5 — Alteração por filtro parcial nos termos "horizontal" ou "vertical"

**Descrição**: o projeto usa "horizontal" em dois contextos distintos:
(a) `barra_de_menus.distribuicao.modo = "horizontal_responsiva"` e
(b) `corpo.arranjo = "horizontal"`.

Um grep ou substituição com o termo "horizontal" pode atingir ambos os contextos.

**Por que é risco**: a barra e o corpo são módulos completamente distintos (seções 2 e 6
do `contrato_composicao_corpo.md`). Confundi-los em uma busca pode gerar alterações
indevidas na barra ao trabalhar no corpo, ou vice-versa.

**Mitigação**: o handoff H-0019 deve especificar explicitamente que "horizontal" nos
critérios de busca se refere a `corpo.arranjo`, não a `barra_de_menus.distribuicao.modo`.
Buscas devem usar padrões específicos: `modelo.corpo.arranjo` ou `"arranjo":`.

---

## Recomendação do próximo ciclo

```text
Próximo ciclo recomendado: H-0019 — Layout horizontal plano do corpo
Tipo: handoff de implementação

Justificativa:
  A barra_de_menus está estabilizada (H-0015 a H-0018). O contrato de
  composição do corpo (contrato_composicao_corpo.md seção 5.6) especifica
  que o arranjo horizontal distribui o espaço disponível em 3 vãos iguais,
  mas essa especificação não está implementada no renderer. O renderer atual
  ignora corpus.arranjo inteiramente, empilhando todos os elementos
  verticalmente. O próximo passo natural — e mais seguro — é implementar
  o suporte a corpo.arranjo = "horizontal" com exatamente o comportamento
  especificado: 3 vãos iguais entre os elementos lado a lado. É o menor
  ciclo funcional verificável que abre o eixo de composição/layout do corpo.

Escopo mínimo:
  - Ler modelo.corpo.arranjo na função tela() do renderizador.
  - Para arranjo = "horizontal" (e alias "lado_a_lado"): distribuir os
    elementos do corpo lado a lado com 3 vãos iguais de espaço horizontal.
  - Para arranjo = "vertical", "sobreposto" ou None: manter comportamento
    atual (empilhamento sequencial).
  - Validar arranjo no loader no nível da tela (rejeitar valores fora do
    conjunto {"vertical", "horizontal", "sobreposto", "lado_a_lado", None}).
  - Criar ou adaptar ao menos um JSON de teste com arranjo = "horizontal".
  - Adicionar testes isolados verificando o layout horizontal.
  - Migrar destino_minimo.json e stub_b.json de "sobreposto" para "vertical"
    (alias transitional — ADR-0011 — pode ser bundled neste ciclo ou em
    ciclo de migração separado; decisão do handoff).

Fora de escopo:
  - Distribuição percentual/fração de largura entre elementos.
  - Aninhamento de grupos com arranjos próprios.
  - Combinação horizontal + dashboard + indicador de paginação.
  - Migração de posicao_dashboard.
  - Alteração de _normaliza_distribuicao, _validar_distribuicao ou
    _linhas_barra.
  - Qualquer alteração em contrato_barra_de_menus.md.

Arquivos provavelmente envolvidos:
  - tela/renderizador.py        (função tela(); possivelmente _caixa_de_elemento)
  - tela/loader.py              (validação de arranjo no nível da tela)
  - tela/teste_renderizador.py  (novos casos de teste horizontal)
  - config/telas/               (novo JSON de teste ou adaptação de existente)
  - config/telas/destino_minimo.json  (se migração bundled: "sobreposto" → "vertical")
  - config/telas/stub_b.json          (se migração bundled: "sobreposto" → "vertical")

Testes provavelmente necessários:
  - test_arranjo_horizontal_dois_elementos_lado_a_lado
  - test_arranjo_horizontal_tres_vaos_iguais
  - test_arranjo_vertical_preservado_apos_horizontal
  - test_alias_sobreposto_equivale_vertical
  - test_alias_lado_a_lado_equivale_horizontal
  - test_loader_rejeita_arranjo_invalido_nivel_tela
```

---

## Conclusão

O projeto está em estado limpo e estável após H-0018:

- HEAD confirmado em `46e0cb9`.
- Workspace sem modificações.
- 544/544 verificações passando em 6 suítes.
- Todos os artefatos H-0015 a H-0018 presentes e fechados.
- `barra_de_menus` estabilizada e protegida.
- Nenhum risco imediato de regressão.

**Podemos avançar para a criação do próximo handoff.**

O próximo handoff recomendado é **H-0019 — Layout horizontal plano do corpo**,
que implementa o suporte a `corpo.arranjo = "horizontal"` no renderer (3 vãos
iguais), complementa com validação de arranjo no loader, e abre o eixo de
composição/layout do corpo de forma incremental e verificável.

Não há bloqueio documental, técnico ou arquitetural que impeça a criação imediata
do H-0019.
