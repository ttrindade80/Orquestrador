---
name: H-0051-paginacao-universal-pageup-pagedown
description: "Migra universalmente a paginação interativa do Orquestrador para as teclas físicas PageUp/PageDown e para a representação [PgUp][PgDn] Páginas, extinguindo qualquer função de paginação de '<', '>', ',' e '.', sem alterar a semântica restante da paginação limitada já fixada pela ADR-0038"
metadata:
  type: handoff_implementacao
  status: CONCLUIDO
  id: H-0051
  data_criacao: "2026-08-07"
rastreabilidade:
  contrato_alvo:
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_chip.md
  adr_relacionadas:
    - docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md
    - docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md
  issues_relacionadas:
    - ITEM-0003
  handoffs_anteriores:
    - docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
---

# H-0051 — Implementar paginação universal por PageUp/PageDown

## 1. Etapa única

Este handoff autoriza exclusivamente:

`IMPLEMENTAR`

Ele não autoriza QA, aprovação, aplicação documental adicional, commit nem
início de outro ciclo (inclusive `ITEM-0007`).

## 2. Ordem de autoridade

1. decisões explícitas D-PGU-01 a D-PGU-08 (ADR-0041);
2. ADR-0041 aceita e aplicada documentalmente; ADR-0038 (D-PAG-01 a D-PAG-13,
   integralmente preservadas — apenas D-PAG-14 é especializada);
3. `contrato_console.md` §12, §22.8, §24; `contrato_barra_de_menus.md` §7,
   §8.3, §24; `contrato_chip.md` §7, §9;
4. este handoff.

Se houver falta, divergência ou decisão nova necessária, bloquear com
`LEITURA_ADICIONAL_NECESSARIA`.

## 3. Estado transportado

```yaml
adr:
  id: ADR-0041
  status: aceita_e_aplicada
  qa_adr: ADR_APPROVED
  qa_aplicacao: ADR_APPLICATION_APPROVED
adr_0038:
  decisoes_preservadas: D-PAG-01 a D-PAG-13   # integralmente vigentes
  decisao_especializada: D-PAG-14              # tecla e notação, por D-PGU-01 a D-PGU-04
item_0003_no_backlog:
  capacidade_ja_implementada_por: H-0045
  estado_da_paginacao_no_codigo: implementada_e_validada_para_virgula_ponto_menor_maior
```

## 4. Objetivo e capacidade coesa

Migrar universalmente a paginação interativa do Orquestrador para
`PageUp`/`PageDown` e para a representação `[PgUp][PgDn] Páginas`, removendo
`<`, `>`, `,` e `.` como entradas de paginação, sem alterar a semântica
restante da paginação limitada já fixada pela ADR-0038 e implementada pelo
H-0045.

### 4.1 Comportamento a entregar

- tecla física `PageUp` muda para a página anterior;
- tecla física `PageDown` muda para a próxima página;
- `<`, `>`, `,` e `.` não executam paginação sob nenhuma condição;
- não permanecem aliases, atalhos ou fallbacks funcionais desses caracteres;
- chips de paginação usam a notação canônica `[PgUp][PgDn] Páginas`;
- estado ativo/inativo dos controles continua seguindo a paginação limitada
  já vigente (D-PAG-01, D-PAG-11 a D-PAG-13);
- `página X/Y`, inclusive `página 1/1`, permanece;
- nenhuma outra semântica de paginação muda.

### 4.2 Preservações obrigatórias

Não alterar:

- cálculo das páginas;
- topologia sem wrap;
- repaginação;
- reconciliação;
- cursor;
- seleção;
- foco;
- navegação interna por setas;
- distribuição ou layout além do texto/tamanho estritamente decorrente dos
  novos chips;
- navegação multinível (`ITEM-0007` — fora de escopo integral).

## 5. Manifesto fechado de leitura

```yaml
leitura_integral:
  - docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_chip.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/handoff/H-0051-paginacao-universal-pageup-pagedown.md

buscas_autorizadas:
  - comando: >-
      rg -n --glob '*.py' --glob '*.json' 'PageUp|PageDown|PgUp|PgDn'
      tela demo config
    finalidade: localizar suporte já existente ou referências às novas teclas.
    resultado_desta_execucao: NENHUMA_OCORRENCIA — capacidade ainda não implementada.
  - comando: >-
      rg -n --glob '*.py' --glob '*.json'
      "KEY_PPAGE|KEY_NPAGE|KEY_LEFT|KEY_RIGHT|ord\(['\"][,.<>]['\"]\)|['\"][,.<>]['\"]"
      tela demo config
    finalidade: localizar bindings e tratamento vigente potencialmente relacionado à paginação.
  - comando: >-
      rg -n --glob '*.py' --glob '*.json'
      '\[<\]|\[>\]|\[<\]\[>\]|Páginas|Paginas|pagina_anterior|proxima_pagina|página anterior|próxima página'
      tela demo config
    finalidade: localizar renderização, chips, configuração, fixtures e testes da paginação existente.

nao_ler:
  - docs/relatorios/**
  - outras_ADRs
  - outros_contratos
  - docs/nomenclatura/**
  - docs/backlog.md
  - branch_descartada_da_tentativa_multinivel
  - documentos_do_sistema_de_prompts
```

Nota de caminhos: os diretórios `tests/` e o arquivo `orquestrador.py` citados
no enunciado original não existem neste repositório; os comandos acima já
refletem os caminhos reais (`tela`, `demo`, `config`). Ler somente as saídas
das buscas. Se faltar arquivo indispensável, parar antes de alterar com
`LEITURA_ADICIONAL_NECESSARIA`, informando caminho e alvo exatos.

## 6. Escopo da implementação

### 6.1 Arquivos de implementação (podem ser alterados)

| Caminho | Achado pela busca | Finalidade da alteração |
|---|---|---|
| `demo/demo.py` | busca 2 (linhas ~696-742, ~1138-1140) | Único ponto encontrado que reconhece os caracteres `,`/`<`/`.`/`>` como comando de teclado e os despacha para `paginacao.pagina_anterior`/`paginacao.pagina_proxima` (bloco do laço de comandos e comentário correlato sobre foco inicial). Deve passar a reconhecer as sequências físicas de `PageUp`/`PageDown` no lugar desses caracteres. |
| `tela/renderizacao/barra_menus.py` | patch pós-QA (achado H-0051-B) — leitura focal dos trechos proprietários da montagem individual dos chips e da junção/separação entre chips | Autorização estritamente focal: introduzir somente o tratamento necessário para que `chip_pagina_anterior` e `chip_pagina_proxima` — que permanecem dois chips lógicos independentes, com `regra_existencia`, `regra_ativo`, cor e estado próprios — sejam apresentados, quando ambos renderizados, como a sequência contígua `[PgUp][PgDn] Páginas`, sem espaço, separador ou texto intermediário entre `[PgUp]` e `[PgDn]`. Limites em §6.1.1. |

Nenhum outro arquivo `.py` de implementação foi localizado pelas buscas
autorizadas como proprietário de tecla ou notação de paginação:

- `tela/paginacao.py` (`pagina_anterior`, `pagina_proxima`, linhas ~324-338) —
  lógica pura de transição de página, sem referência a tecla ou caractere;
  **preservar integralmente**, nenhuma alteração é necessária aqui.
- `tela/renderizacao/contexto_execucao.py` — calcula `regra_ativo`/
  `regra_existencia` dos chips `chip_pagina_anterior`/`chip_pagina_proxima`
  por nome de regra declarativa (`pagina_nao_e_primeira`, `pagina_nao_e_ultima`,
  `console_com_paginacao`), não por tecla nem símbolo literal;
  **preservar integralmente**.

`tela/renderizacao/barra_menus.py` deixa de constar como arquivo
integralmente preservado (ver tabela acima e §6.1.1); toda a lógica nele não
relacionada ao agrupamento focal da paginação permanece preservada.

Se a leitura focal revelar outro proprietário real não listado acima, parar
com `LEITURA_ADICIONAL_NECESSARIA` antes de alterar.

#### 6.1.1 Limite da alteração em `tela/renderizacao/barra_menus.py`

A autorização de `tela/renderizacao/barra_menus.py` acima é estritamente
focal. Ela pode introduzir somente o tratamento necessário para que os dois
chips lógicos de paginação sejam apresentados como o agrupamento canônico.
Ela não pode:

- criar mecanismo genérico novo de agrupamento de chips além do necessário
  para esta capacidade;
- alterar distribuição global da barra;
- alterar outros chips;
- alterar regras de existência;
- alterar regras de ativo/inativo;
- alterar cores;
- alterar foco;
- alterar paginação;
- alterar navegação.

### 6.2 Arquivos de configuração/fixture realmente afetados

Todas as 11 fixtures de demonstração H-0045 que declaram os chips
`chip_pagina_anterior`/`chip_pagina_proxima` com `"tecla": "<"` e
`"tecla": ">"` (busca 2 e busca 3 — conjunto idêntico e completo de
`config/telas/demo/h0045_*.json`):

```text
config/telas/demo/h0045_paginacao_console_unico.json
config/telas/demo/h0045_validacao_vazio.json
config/telas/demo/h0045_dois_consoles_paginas_independentes.json
config/telas/demo/h0045_validacao_manter_junto.json
config/telas/demo/h0045_paginacao_modo_verboso_multilinha.json
config/telas/demo/h0045_paginacao_conjunto_vazio.json
config/telas/demo/h0045_fluxo_execucao_paginado.json
config/telas/demo/h0045_paginacao_politicas_quebra.json
config/telas/demo/h0045_validacao_continuacao.json
config/telas/demo/h0045_validacao_nova_pagina.json
config/telas/demo/h0045_validacao_fluxo_continuo.json
```

Cada uma declara dois chips separados. `regra_existencia:
console_com_paginacao` e `regra_ativo` em `pagina_nao_e_primeira`/
`pagina_nao_e_ultima` **não mudam de nome nem de semântica** — são a mesma
paginação limitada já vigente. Os valores de `tecla` e `texto` passam a ser
os seguintes, sem escolha material remanescente para o implementador:

- `chip_pagina_anterior`: `"tecla": "PgUp"`, `"texto": ""`;
- `chip_pagina_proxima`: `"tecla": "PgDn"`, `"texto": "Páginas"`.

Essa combinação, somada ao tratamento focal de junção autorizado em §6.1.1,
produz a sequência contígua `[PgUp][PgDn] Páginas` exigida por D-PGU-01 a
D-PGU-03: `[PgUp]` sem rótulo próprio, seguido imediatamente por `[PgDn]`,
com o rótulo `Páginas` aparecendo uma única vez, após `[PgDn]`. A
materialização visual agrupada pertence ao tratamento focal do renderer
(§6.1.1), não a uma fusão dos dois controles no JSON: as 11 fixtures
continuam declarando `chip_pagina_anterior` e `chip_pagina_proxima` como
dois controles lógicos separados, com teclas correspondentes a `PageUp` e
`PageDown`.

**Fora de escopo, não tocar**: `config/elementos/barra_de_menus.json`
contém `"simbolo": "[<][>]"` e `"rotulo": "Páginas"` (busca 3, linhas 41-42),
mas é um artefato transicional — confirmado, por busca adicional dirigida ao
nome do arquivo, que nenhum módulo `.py` do repositório o carrega ou
referencia. `contrato_barra_de_menus.md` §5 já o classifica como "não é mais
a fonte universal definitiva dos valores concretos da instância". Alterá-lo
não é necessário para o comportamento exigido por esta capacidade e fica fora
deste handoff.

### 6.3 Arquivos de teste realmente afetados

| Caminho | Achado pela busca | Natureza do impacto |
|---|---|---|
| `demo/teste_demo_paginacao.py` | busca 2 e 3 (uso extensivo em todo o arquivo) | Suíte primária de regressão da paginação H-0045: dezenas de asserts usam `,`/`<`/`.`/`>` como comando de teclado enviado a `processar_comando`/TTY, e `"[<]"`/`"[>]"` como texto renderizado esperado. Precisa passar a exercitar `PageUp`/`PageDown` e `"[PgUp]"`/`"[PgDn]"`, preservando a estrutura de cada cenário (P01 a P23 e correlatos). |
| `demo/teste_demo_navegacao.py` | busca 2 (linha ~851) | Laço de comandos testados sob geometria inválida inclui `".", ">", ",", "<"` junto às setas; deve deixar de exercitar esses caracteres como paginação (ou trocá-los por `PageUp`/`PageDown`) mantendo a asserção de ausência de movimento em geometria inválida. |
| `tela/testes_renderizador/integracao.py` | busca 3 (linhas ~764, 791-797, 913-916) | Asserts de existência/rótulo `"[<]"`/`"[>]"` e do estado `chip_pagina_anterior` em cenários de integração de corpo. |
| `tela/testes_renderizador/barra_menus.py` | busca 3 (linhas ~1266-1543) | Asserts de existência, ordem, estado ativo/inativo e cor (`cor_inativo`) de `"[<]"`/`"[>]"` na barra renderizada. |
| `tela/testes_renderizador/fundamentos.py` | busca 3 (linhas ~176-177, ~649-650) | Asserts **negativos** de ausência de `"[<>] Páginas"` (tela sem console paginado) e de que o código-fonte do renderer não contém o literal `"Páginas"` hardcoded. Os literais verificados devem ser atualizados para a nova notação canônica; a intenção do teste (ausência do chip / proibição de hardcoding) não muda. |

Se qualquer teste ou execução revelar dependência material em arquivo não
enumerado no escopo nominal deste handoff, o implementador deve parar antes
de ler ou alterar esse arquivo e retornar `LEITURA_ADICIONAL_NECESSARIA`,
informando caminho, alvo, motivo e impacto sem a expansão.

Nenhum arquivo não enumerado pode ser alterado automaticamente por ser
considerado "regressão direta" desta capacidade.

### 6.4 Arquivos preservados (não tocar)

- `tela/paginacao.py` — cálculo de páginas e transição (`pagina_anterior`,
  `pagina_proxima`, `total_paginas`, `pagina_do_item_logico` etc.);
- `tela/navegacao.py` — navegação por setas, foco, Tab/Shift+Tab;
- `tela/renderizacao/barra_menus.py` — preservada toda a lógica não
  relacionada ao agrupamento focal da paginação (distribuição global,
  `regra_ativo`/`regra_existencia`, outros chips, cores, foco); a alteração
  autorizada é estritamente a de §6.1.1;
- `tela/renderizacao/contexto_execucao.py` — íntegro, quanto à lógica de
  `regra_ativo`/`regra_existencia` (ver §6.1);
- `config/elementos/barra_de_menus.json` (ver §6.2);
- toda navegação multinível, código ou fixture do `ITEM-0007`;
- qualquer código ou fixture de branch descartada de tentativa multinível
  anterior — não reaproveitar;
- ADR-0041, ADR-0038, os três contratos, a nomenclatura, o backlog e o
  índice de ADRs.

## 7. Testes obrigatórios

| # | Caso | Expectativa |
|---|---|---|
| 1 | `PageUp` em console focado paginado, página > 1 | Muda para a página anterior |
| 2 | `PageDown` em console focado paginado, página < total | Muda para a próxima página |
| 3 | `PageUp` na primeira página | Não recua (no-op), controle inativo |
| 4 | `PageDown` na última página | Não avança (no-op), controle inativo |
| 5 | Console com uma única página (`página 1/1`) | Ambos os controles inativos, inclusive com conjunto vazio |
| 6 | `<`, `>`, `,`, `.` em qualquer estado de paginação | Nenhum efeito de paginação — sem alias, atalho ou fallback |
| 7 | Barra de menus com console paginado em foco | Ver critérios 7.1 a 7.6 abaixo |
| 8 | Setas de navegação interna (`[✥]`) dentro da página atual | Não mudam de página (topologia toroidal só dentro da página, sem wrap entre páginas) |
| 9 | Regressão da paginação vigente (H-0045) | Cálculo de páginas, cursor no primeiro item navegável do destino, repaginação por redimensionamento/modo, filtro, seleção múltipla e fluxo focal (ADR-0037) permanecem sem alteração de comportamento |

Critérios 7.1 a 7.6 (achado H-0051-B do QA), todos exigidos:

7.1. `chip_pagina_anterior` e `chip_pagina_proxima` continuam existindo como
     dois controles lógicos independentes (mesma `regra_existencia`,
     avaliada independentemente para cada um).
7.2. o estado ativo/inativo de cada um permanece independente (`regra_ativo`
     avaliada por chip, conforme §6.1.1).
7.3. a representação visual, quando ambos renderizados, é literal e
     contígua: `[PgUp][PgDn] Páginas`.
7.4. não há separador (espaço ou outro caractere) entre `[PgUp]` e `[PgDn]`.
7.5. `Páginas` aparece uma única vez no agrupamento, após `[PgDn]`.
7.6. nenhum efeito colateral na apresentação dos demais chips da barra.

Suíte canônica aplicável, a executar a partir da raiz do Orquestrador:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_paginacao.py demo/teste_demo_navegacao.py tela/testes_renderizador/integracao.py tela/testes_renderizador/barra_menus.py tela/testes_renderizador/fundamentos.py
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

## 8. Demonstração manual

A validação visual/interativa é exclusiva do usuário, em TTY real.

```yaml
cwd: "."
comando: python demo/demo.py h0045_paginacao_console_unico
configuracao: config/telas/demo/h0045_paginacao_console_unico.json
roteiro:
  - abrir a tela e confirmar o chip de paginação lendo [PgUp][PgDn] Páginas
    na barra de menus, com o controle de página anterior inativo (primeira
    página);
  - pressionar PageDown e confirmar avanço de página (indicador "página X/Y"
    incrementa; o controle de página anterior passa a ficar ativo);
  - pressionar PageUp e confirmar retorno à página anterior;
  - pressionar sucessivamente ',', '<', '.', '>' e confirmar que nenhum
    deles altera a página nem o indicador "página X/Y";
  - avançar até a última página e confirmar que o controle de próxima
    página fica inativo; recuar até a primeira e confirmar o controle de
    página anterior inativo.
gabarito:
  resultado_observado:
    - CONFORME
    - 'DIVERGENTE: <etapa e comportamento observado>'
```

`config/telas/demo/h0045_dois_consoles_paginas_independentes.json` pode ser
usado como roteiro complementar opcional para confirmar que `PageUp`/
`PageDown` continuam dirigidos exclusivamente ao console focado (D-PAG-13,
preservado).

## 9. Relatório da execução

Criar exclusivamente:

```text
docs/relatorios/IMP-0051-paginacao-universal-pageup-pagedown.md
```

Máximo normal: 900 palavras. Usar o template canônico de relatório de
implementação vigente no repositório, registrando fatos verificáveis:
arquivos efetivamente alterados (implementação, fixtures, testes), resultado
da suíte canônica, resultado da demonstração manual (ou pendência factual se
não houver TTY real disponível), e qualquer bloqueio por
`LEITURA_ADICIONAL_NECESSARIA` decorrente de dependência material em arquivo
não enumerado no escopo nominal (§6.3). Não reproduzir este handoff nem
aprovar a própria entrega.

## 10. Proibições

O futuro implementador não pode:

- tocar na navegação multinível (`ITEM-0007`);
- aproveitar código da branch descartada da tentativa multinível;
- criar novo mecanismo de paginação paralelo ao já existente em
  `tela/paginacao.py`;
- manter aliases, atalhos ou fallbacks funcionais para `,`/`<`/`.`/`>`;
- alterar contratos ou ADR (`ADR-0041`, `ADR-0038` e os três contratos
  permanecem como autoridade, não como alvo de edição);
- fazer commit, stage, QA ou aprovação da própria entrega.

## 11. Condições de bloqueio

```yaml
BLOCKED_DOCUMENTATION:
  quando: autoridades aplicadas (ADR-0041, contratos §6.1) forem contraditórias
LEITURA_ADICIONAL_NECESSARIA:
  quando: saida_das_buscas_autorizadas_nao_bastar_para_identificar_um_proprietario_real
  resposta: caminho_e_alvo_exatos
```

Não contornar bloqueio por inferência, leitura ampla fora do manifesto,
alteração de autoridade documental ou ampliação silenciosa do escopo de
arquivos autorizados.

## 12. Limite de encerramento

Este handoff autoriza somente `IMPLEMENTAR` conforme §1. Não implementar,
testar, validar TTY, fazer QA, aprovar a própria entrega, preparar stage ou
commit a partir deste documento — essas ações pertencem à etapa de
implementação que este handoff autoriza para execução futura, não à criação
deste handoff.
