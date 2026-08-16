# H-0073 — Aplicação da formatação de `dois_niveis_por_foco` às telas reais

## 1. Metadata e rastreabilidade

```yaml
projeto: Orquestrador
adr: ADR-0047
handoff: H-0073
data_criacao: 2026-08-15
status: CONCLUIDO
patch_handoff: P03
predecessor_funcional: H-0072
prontidao_documental_apos_p03: HANDOFF_APPROVED
estado_executivo:
  H-0055: CONCLUIDO
  H-0063: CONCLUIDO
  bloqueios: nenhum
qa_final_implementacao: I1_IMPLEMENTATION_APPROVED
validacao_manual_final: MANUAL_REVALIDATION_APPROVED
VM-H0073-001: RESOLVIDO
VM-H0073-002: RESOLVIDO
H0055_TABULACAO_DINAMICA: APROVADO
H0063_TABULACAO_DINAMICA: APROVADO
H0063_ESPACAMENTO_COLUNAS_3_8: PRESERVADO
H0070: FALHA_HISTORICA_NAO_CAUSAL
estado_documental_transportado:
  ADR-0047:
    status_qa: ADR_APPROVED
    patch: P03
    status_aplicacao: aceita_e_aplicada
  aplicacao_documental_ADR-0047:
    patch: P02
    status_qa: ADR_APPLICATION_APPROVED
  H-0072:
    patch_handoff: P01
    status_qa_handoff: HANDOFF_APPROVED
    patch_implementacao: P01
    status_qa_implementacao: I1_IMPLEMENTATION_APPROVED
    achado_material_pendente: nenhum
  ACH-001:
    estado: RESOLVIDO
    origem_historica: H-0055 exigia A) e a capacidade então aceitava só designador.tipo
    comprovacao_p02: BLOCKED_DOCUMENTATION sem alterar este handoff
    resolucao: H-0072 P01 (prefixo/sufixo estruturais) + este P03
dimensionamento_da_atividade:
  H-0072: capacidade_generica_de_formatacao_dos_filhos (concluído e corrigido)
  H-0073: aplicacao_da_capacidade_as_telas_reais_existentes (este handoff)
escopo_efetivamente_fechado:
  h0055_dois_niveis_por_foco: CONCLUIDO
  h0063_estilo_estrutura_navegacao_dois_niveis: CONCLUIDO
escopo_bloqueado: nenhum
bloqueio_documental_h0063:
  estado: BLOQUEIO_DOCUMENTAL_RESOLVIDO
  origem_historica: campos semânticos separados ausentes na criação deste handoff
  resolucao:
    ADR-0047_P02: colunas literais preset / amostra
    QA_pos_P02: ADR_APPROVED
    aplicacao_documental_P01: contratos reconciliados
    QA_pos_aplicacao: ADR_APPLICATION_APPROVED
  colunas:
    1: preset
    2: amostra
bloqueio_ach001_h0055:
  estado: RESOLVIDO
  origem_historica: sufixo ")" não cabia no schema estrutural só-tipo
  resolucao:
    ADR-0047_P03: designador.prefixo e designador.sufixo opcionais
    aplicacao_documental_P02: contratos reconciliados
    H-0072_P01: capacidade genérica corrigida e aprovada
    este_P03: H-0055 declara sufixo ")" na configuração estrutural
```

Este handoff autoriza exclusivamente a **aplicação declarativa** da capacidade
genérica já implementada e corrigida por H-0072 às telas reais existentes que
usam `politica_navegacao.tipo = "dois_niveis_por_foco"`. Não cria capacidade
nova, não redesenha conteúdo, não altera navegação, seleção ou schema. Não
altera código, fixture, conteúdo externo nem testes de H-0072 — apenas
consome a capacidade agora aprovada.

O patch P01 removeu o bloqueio documental de H-0063 (`preset`/`amostra`) e
não reabre essa decisão. O patch P02 comprovou ACH-001
(`BLOCKED_DOCUMENTATION`) sem alterar este handoff: a capacidade então
aceitava só `designador.tipo` e não representava `A)`. Depois disso,
ADR-0047 P03, a aplicação documental P02 e H-0072 P01 fecharam
`prefixo`/`sufixo` estruturais. Este P03 remove definitivamente ACH-001 e
fecha H-0055 com `sufixo: ")"`. H-0055 e H-0063 foram concluídos e aprovados
na revalidação manual final. Nenhum bloqueio permanece ativo. Nenhuma decisão
já fechada é reaberta por este fechamento.

---

## 2. Capacidade herdada (não redefinida aqui)

A capacidade `formato.dois_niveis_por_foco.filho` (tabulação, designador
com `tipo` obrigatório e `prefixo`/`sufixo` opcionais, apresentação
`texto`/`tabela`, colunas e espaçamento) já está implementada, corrigida
e aprovada por H-0072 P01 (`I1_IMPLEMENTATION_APPROVED`; achados materiais:
nenhum). Para tipos visuais:

```text
designador_visual = prefixo + designador_base + sufixo
```

Ausência de `prefixo` ou `sufixo` equivale a string vazia. O sufixo de
H-0055 vem da **configuração estrutural** da tela; não depende de herança
do conteúdo. Este handoff não altera `tela/modelo.py`,
`tela/carregamento/tela_json.py`,
`tela/carregamento/formato_dois_niveis_por_foco.py`,
`tela/renderizacao/console.py`, `tela/renderizacao/conteudo_externo.py`,
`tela/renderizacao/designadores.py`, `tela/renderizacao/matriz_participantes.py`
nem `tela/navegacao.py`/`tela/selecao.py` — todos preservados integralmente
(§7.3 / §7.4). Não altera fixture estrutural, conteúdo externo nem testes
de H-0072.

A única edição de código autorizada é a extensão compatível da projeção
dinâmica de H-0063 em `tela/estilo.py` (§8.4). `tela/renderizacao/estilo.py`
não é editado (§8.4.1).

---

## 3. Autoridades

Autoridade normativa integral, sem reabertura:

- `docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md` — D-DNF-01 a
  D-DNF-11; schema literal em §4.13 (`prefixo`/`sufixo` opcionais, P03);
  especialização de Estilo em §4.11 e fechamento literal `preset`/`amostra`
  em §4.11.1 (P02); especialização H-0055 em §4.11.2 (P03); aplicação
  futura em §4.12. Nenhuma dessas decisões é reaberta.
- `docs/handoff/H-0072-formatacao-generica-filhos-dois-niveis-por-foco.md` —
  capacidade genérica corrigida e aprovada (P01), consumida sem alteração.
- `docs/contratos/contrato_console.md` §22.16 (política, ADR-0042) e §25
  (comportamento de formatação, ADR-0047), inclusive
  `designador_visual = prefixo + designador_base + sufixo`.
- `docs/contratos/contrato_tela_json.md` §36 (schema literal do bloco
  `formato.dois_niveis_por_foco.filho`), §36.4 (`prefixo`/`sufixo`),
  §36.8 (especialização H-0063: `preset` / `amostra`) e §36.9
  (especialização H-0055: `alfabetico_maiusculo` com `sufixo: ")"`).
- `docs/contratos/contrato_json_console.md` §7.1 (`politica_navegacao.tipo`)
  e §15 (fronteira: documento externo de conteúdo não declara apresentação;
  §15.1 extensão compatível da projeção de H-0063).
- `docs/nomenclatura/32_CONSOLE.md` §4.10 (vocabulário `dois_niveis_por_foco`,
  ADR-0042) e §4.11 (unidade inteira do filho deslocada, ADR-0047).
- `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` §4.6
  (apresentação dos filhos) e §8B (fronteira com navegação simples).

---

## 4. Levantamento focal — telas reais com `dois_niveis_por_foco`

Busca executada na criação, restrita a `config/telas/demo`:

```
rg -l 'dois_niveis_por_foco' config/telas/demo
rg -n 'politica_navegacao' config/telas/demo -A2
```

Resultado — quatro arquivos estruturais declaram
`politica_navegacao.tipo = "dois_niveis_por_foco"`:

| Arquivo | Classificação | Tratamento neste handoff |
|---|---|---|
| `config/telas/demo/h0055_dois_niveis_por_foco.json` | Tela real legada, com conteúdo estático navegável | **Alvo — reconciliação fechada (§8.1); ACH-001 resolvido (§9.3)** |
| `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json` | Tela real, conteúdo dinâmico (Estilo) | **Alvo — reconciliação fechada (§8.3); bloqueio documental resolvido (§9)** |
| `config/telas/demo/h0062_estilo.json` | Tela estrutural órfã/histórica, sem produtor de conteúdo ativo | **Excluída — justificativa em §5.1** |
| `config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco.json` (+ `..._conteudo.json`) | Fixture de referência da própria capacidade genérica (H-0072) | **Excluída — não é tela legada, é a fixture que já materializa a capacidade (§5.2)** |

Nenhuma outra tela em `config/telas/demo` declara
`politica_navegacao.tipo = "dois_niveis_por_foco"`.

---

## 5. Telas explicitamente preservadas (fora do escopo de implementação)

### 5.1 `config/telas/demo/h0062_estilo.json` — precedente histórico órfão

Achado além dos alvos conhecidos (H-0055/H-0063), tratado focalmente conforme
exigido:

- Declara `politica_navegacao.tipo = "dois_niveis_por_foco"` e `itens: []`
  (`origem_dados.tipo = "declarados"`), sem nenhum documento de conteúdo
  externo associado e sem catálogo de associação em `demo/demo.py`
  (`_CATALOGO_CONTEUDO_EXTERNO`, `demo/demo.py:247-269`, não contém
  `h0062_estilo`).
- Busca por `console_h0062_estilo` em todo o repositório (fora `.git`) só
  retorna o próprio JSON e documentação histórica — nenhum controlador ou
  produtor de conteúdo Python o referencia.
- `docs/handoff/H-0066-acao-aplicar-candidato-estilo.md:147` já o classifica
  explicitamente como *"precedente declarativo histórico"*, superado pela
  tela `h0063_estilo_estrutura_navegacao_dois_niveis`.
- H-0072 já o listou como preservado (`RELATORIO_CRIACAO_HANDOFF_H-0072.md:62`,
  `RELATORIO_QA_IMPLEMENTACAO_H-0072.md:19`), sem alteração.

Sem produtor de conteúdo ativo, o console de `h0062_estilo` nunca apresenta
filhos navegáveis reais — não há o que tabular, recuar ou designar. Reconciliar
sua configuração estrutural não teria efeito observável e extrapolaria o
objetivo exclusivo deste handoff (aplicar a telas reais em uso). Preservado
integralmente; nenhuma alteração autorizada. Não será reconciliado neste
handoff.

### 5.2 Fixture `h0072_formatacao_generica_dois_niveis_por_foco{,_conteudo}.json`

Materializa a própria capacidade genérica (H-0072 §4.4, §22) — não é tela
legada a migrar, é a referência de capacidade. Preservada integralmente;
nenhuma alteração autorizada. A aplicação concreta de H-0073 não pode
alterar essas fixtures para fazer regressão passar.

---

## 6. Objetivo exclusivo do H-0073

Aplicar `formato.dois_niveis_por_foco.filho` — já implementado — às telas
reais listadas em §4, reconciliando configuração declarativa sem alterar
conteúdo visível, navegação, seleção ou schema. Nenhuma capacidade genérica
nova é criada. Nenhum redesenho de conteúdo é autorizado. Nenhuma política
nova é criada: os filhos de H-0055 e de H-0063 continuam pertencendo a
`dois_niveis_por_foco`.

Pacote fechado por este handoff (P01 + P03):

- H-0055 reconciliada (`apresentacao = texto`; `designador.tipo =
  alfabetico_maiusculo` com `sufixo: ")"`; resultado visual `A)`, `B)`,
  `C)`, `D)`; `A` sem `)` não é equivalente);
- H-0055 continua mostrando `A)`; conteúdo externo intacto;
- H-0063 reconciliada (`apresentacao = tabela`, colunas `preset` e
  `amostra`) — estado fechado no P01, preservado integralmente;
- `titulo` de H-0063 preservado;
- H-0062 preservada;
- H-0072 preservada (capacidade genérica corrigida, sem alteração aqui);
- conteúdo externo de H-0055 preservado byte-a-byte;
- campos existentes de H-0063 preservados, com `amostra` como extensão
  compatível da projeção;
- navegação e seleção preservadas;
- testes focais, demonstrações, regressão H-0070, regressão H-0072 e
  suíte canônica.

---

## 7. Escopo nominal fechado — arquivos

Nenhuma descoberta de arquivo é transferida para IMPLEMENTAR. Todo arquivo
futuro possui caminho literal. A lista nominal fechada pelo P01 permanece;
este P03 altera somente o que ACH-001 tornou necessário (expectativa `A)`
e `sufixo: ")"` estrutural de H-0055), sem reabrir H-0063 nem acrescentar
arquivo fora das quatro classes abaixo.

### 7.1 ARQUIVOS AUTORIZADOS PARA EDIÇÃO

| Arquivo | Alteração autorizada |
|---|---|
| `config/telas/demo/h0055_dois_niveis_por_foco.json` | Adicionar `corpo.elementos[0].formato.dois_niveis_por_foco.filho` exatamente como §8.1 (`tabulacao` 5..10, `designador.tipo: alfabetico_maiusculo` com `sufixo: ")"`, `apresentacao: texto`), preservando `formato.excesso` já existente |
| `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json` | Adicionar `formato.dois_niveis_por_foco.filho` exatamente como §8.3 |
| `tela/estilo.py` | Em `ControladorTelaEstilo._construir_conteudo`, expor `campos["amostra"]` preservando integralmente os campos existentes (§8.4) |
| `tela/teste_navegacao.py` (seção "H-0055 -- dois_niveis_por_foco", a partir de `~L2032`) | Adicionar casos que exercitem `formato_filho_dois_niveis` populado sobre a árvore de H-0055, preservando os testes existentes de toroide/seleção/Tab (`teste_h0055_*`). Se assertirem o designador visível, exigir `A)`/`B)`/`C)`/`D)`, nunca `A` sem `)` |
| `demo/teste_demo_console.py` (cenário `h0055_dois_niveis_por_foco`, `~L157-566`) | Estender as asserções de linhas físicas para cobrir tabulação efetiva (5..10), recuo unitário de `ec`/`tg`/designador/conteúdo e designador `A)`, `B)`, `C)`, `D)` produzido por `tipo: alfabetico_maiusculo` com `sufixo: ")"` na configuração estrutural (§8.1). É proibido aceitar `A`/`B`/`C`/`D` sem `)` como resultado correto |

### 7.2 ARQUIVOS NOVOS AUTORIZADOS

| Arquivo | Papel |
|---|---|
| `demo/teste_demo_h0073_h0055_reconciliado.py` | Demonstração de H-0055 pelo ponto de entrada real (`demo/demo.py`); fluxo real, não somente helper isolado; prova `A)` com `sufixo: ")"` estrutural, tabulação 5..10 e unidade `ec`/`tg`/designador/conteúdo (§10.2) |
| `tela/teste_estilo_h0073_h0063.py` | Prova automatizada dos 18 critérios obrigatórios de H-0063 (§11.2), inclusive projeção `preset`/`titulo`/`amostra`, configuração estrutural e apresentação tabular |
| `demo/teste_demo_h0073_h0063_reconciliado.py` | Demonstração de H-0063 reconciliada pelo ponto de entrada real (`demo/demo.py`); fluxo real, não somente helper isolado; análoga em forma a `demo/teste_demo_h0072_formatacao_generica.py` |

Nenhuma fixture nova é necessária. H-0055 reutiliza suas próprias fixtures
existentes (§8.2). H-0063 continua com projeção dinâmica — não recebe
documento externo de conteúdo.

### 7.3 ARQUIVOS SOMENTE PARA LEITURA/TESTE

Executar sem alterar (exceto a extensão já autorizada em §7.1 para os dois
arquivos de H-0055). Caminhos literais:

| Arquivo | Papel |
|---|---|
| `tela/renderizacao/estilo.py` | Leitura da proveniência de `amostra` (`amostra_de_preset`, `compor_titulo_com_amostra`). Sem edição (§8.4.1) |
| `demo/demo.py` | Ponto de entrada real das demonstrações H-0055 e H-0063. Sem edição |
| `tela/teste_estilo_h0063.py` | Regressão da estrutura/projeção/navegação de H-0063 |
| `demo/teste_demo_estilo_h0063.py` | Regressão da demonstração F4/non-TTY/resize/navegação de H-0063 |
| `tela/teste_estilo_h0064.py` | Regressão da composição de `titulo` e da amostra semântica já existente |
| `tela/teste_estilo_h0065.py` | Regressão de seleção e candidato |
| `tela/teste_estilo_h0066.py` | Regressão de aplicação |
| `tela/teste_estilo_h0067.py` | Regressão da confirmação de aplicação |
| `tela/teste_estilo_h0068.py` | Regressão de persistência e publicação |
| `tela/teste_estilo_h0070.py` | Regressão H-0070, inclusive `test_filhos_sem_ordinais_cursor_e_indicadores_preservados` (§12). Assertiva não alterada |
| `tela/teste_formato_filho_dois_niveis_por_foco.py` | Regressão da capacidade genérica corrigida H-0072; sem alteração para obter verde |
| `demo/teste_demo_h0072_formatacao_generica.py` | Regressão da demonstração H-0072; o caso `sufixo ")"` já foi provado e aprovado; sem alteração |

### 7.4 ARQUIVOS PRESERVADOS

Nenhuma alteração autorizada:

| Arquivo | Motivo |
|---|---|
| `config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json` | Conteúdo externo de H-0055; permanece byte-a-byte inalterado, inclusive a declaração histórica de designador (§8.2) |
| `config/telas/demo/h0062_estilo.json` | Precedente declarativo histórico sem produtor ativo; não reconciliar (§5.1) |
| `config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco.json` | Fixture da capacidade genérica corrigida; nenhuma alteração (§5.2) |
| `config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco_conteudo.json` | Fixture da capacidade genérica corrigida; nenhuma alteração (§5.2) |
| `tela/modelo.py` | Capacidade genérica corrigida; nenhuma alteração neste handoff |
| `tela/carregamento/tela_json.py` | Capacidade genérica corrigida; nenhuma alteração neste handoff |
| `tela/carregamento/formato_dois_niveis_por_foco.py` | Capacidade genérica corrigida; nenhuma alteração neste handoff |
| `tela/renderizacao/console.py` | Capacidade genérica corrigida; nenhuma alteração neste handoff |
| `tela/renderizacao/conteudo_externo.py` | Capacidade genérica corrigida; nenhuma alteração neste handoff |
| `tela/renderizacao/designadores.py` | Capacidade genérica corrigida; nenhuma alteração neste handoff |
| `tela/renderizacao/matriz_participantes.py` | Capacidade genérica já fechada |
| `tela/navegacao.py` | Navegação preservada |
| `tela/selecao.py` | Seleção preservada |
| `tela/renderizacao/estilo.py` | Sem necessidade causal de edição (§8.4.1); listado também em §7.3 como leitura |

---

## 8. Configuração exata por tela

### 8.1 H-0055 — `config/telas/demo/h0055_dois_niveis_por_foco.json`

Adição ao elemento `console_h0055`, preservando `formato.excesso` já
existente:

```json
"formato": {
  "excesso": {
    "politica_modo": "somente_nao_verboso"
  },
  "dois_niveis_por_foco": {
    "filho": {
      "tabulacao": { "minimo": 5, "maximo": 10 },
      "designador": {
        "tipo": "alfabetico_maiusculo",
        "sufixo": ")"
      },
      "apresentacao": "texto"
    }
  }
}
```

Declaração estrutural autorizada, equivalente:

```yaml
formato.dois_niveis_por_foco.filho:
  tabulacao:
    minimo: 5
    maximo: 10
  designador:
    tipo: alfabetico_maiusculo
    sufixo: ")"
  apresentacao: texto
```

Justificativa de cada campo:

- `tabulacao.minimo/maximo = 5/10` — valor fechado pela ADR-0047 §4.2 para as
  telas desta atividade; não hardcoded no renderer (H-0072 já implementado).
- `designador.tipo = "alfabetico_maiusculo"` com `sufixo: ")"` — configuração
  estrutural obrigatória deste P03. Produz o resultado visual
  `A)`, `B)`, `C)`, `D)`, … via
  `designador_visual = prefixo + designador_base + sufixo`. O `)` vem da
  **configuração estrutural** da tela, não de herança do conteúdo. É
  **proibido** aceitar `A`, `B`, `C`, `D` (sem `)`) como equivalente.
  Contexto histórico (não mais vigente): ACH-001 existiu porque a capacidade
  então aceitava só `designador.tipo`; P02 comprovou a impossibilidade e
  terminou `BLOCKED_DOCUMENTATION` sem alterar este handoff. H-0072 P01
  passou a aceitar `prefixo`/`sufixo` opcionais; este P03 aplica essa
  capacidade já aprovada. Nenhuma alteração de H-0072 é autorizada aqui.
  Nenhuma herança automática do `niveis[1].designador` do conteúdo é
  requerida nem usada.
- `apresentacao = "texto"` — os filhos de H-0055 são conteúdo textual normal
  (`titulo`), sem dados tabulares; nenhuma tabela é inventada só porque a
  capacidade existe. O bloco `tabela` não é declarado (proibido quando
  `apresentacao = "texto"`, V-DNF-05). H-0055 não é transformada em tabela.

Comportamento preservado de H-0055: navegação de pais, navegação dos filhos,
toroides, seleção, conteúdo, ordem, identidade lógica e apresentação
`texto`. A única mudança material é a nova disposição física contratada:

```text
tabulação → ec → tg, quando existir → designador → conteúdo
```

com tabulação efetiva no intervalo 5..10. Designador e navegação permanecem
conforme já fechado nesta seção; estas decisões não são reabertas.

### 8.2 Conteúdo de H-0055 — preservado integralmente

`config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json` **não é
alterado**. Preservar integralmente e byte-a-byte. Não remover sua
declaração histórica de designador
(`niveis[1].designador = {"tipo": "alfabetico_maiusculo", "sufixo": ")"}`)
apenas porque a configuração estrutural agora declara explicitamente o
designador utilizado pela nova apresentação. A nova capacidade **não
depende** de herança automática desse documento.

Verificação mecânica: com `apresentacao_filho == "texto"`, o renderer usa
`_texto_no_conteudo(filho, nivel_filho)`
(`tela/renderizacao/conteudo_externo.py:463-464`), que lê o campo nomeado por
`niveis[1].conteudo` do documento de conteúdo (`"titulo"`, já existente e
inalterado) — nenhum campo novo é consumido, nenhuma necessidade estrutural
mecânica de tocar o arquivo de conteúdo foi identificada. A preferência de
preservação integral é satisfeita sem ressalva.

### 8.3 H-0063 — configuração estrutural fechada

`config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json` não
declara hoje o bloco `formato`. A implementação adiciona, no elemento
`console_h0063_estilo`, exatamente:

```json
"formato": {
  "dois_niveis_por_foco": {
    "filho": {
      "tabulacao": { "minimo": 5, "maximo": 10 },
      "designador": { "tipo": "nenhum" },
      "apresentacao": "tabela",
      "tabela": {
        "colunas": [
          { "campo": "preset" },
          { "campo": "amostra" }
        ],
        "espacamento": { "minimo": 3, "maximo": 8 }
      }
    }
  }
}
```

Coluna 1 = `preset`. Coluna 2 = `amostra`. Não existe campo pendente.

Os filhos continuam na política `dois_niveis_por_foco`. Não se cria política
nova. A apresentação local tem exatamente 2 colunas, sem cabeçalho, sem
separador, sem borda própria e sem título próprio. A tabulação ocorre antes
de `ec`:

```text
tabulação → ec → tg, quando existir → designador, quando existir → conteúdo
```

Como o designador é `nenhum`, nenhuma identificação visual adicional do
filho é criada.

Nenhum conteúdo visível é autorizado a mudar: nomes de categorias, nomes de
presets, textos, amostras, símbolos, cores, valores de estilo, ordem,
seleção, candidato, baseline, aplicar, persistir e publicar permanecem
semanticamente idênticos. `titulo` continua sendo produzido com o mesmo
valor atual para consumidores preexistentes. A apresentação tabular usa
`preset` e `amostra`; isso não autoriza remover, simplificar ou redefinir
`titulo`.

O arquivo estrutural contém a configuração. A projeção dinâmica contém os
dados. Conteúdo dinâmico continua sendo dados, sem configuração visual
embutida.

### 8.4 H-0063 — extensão compatível da projeção

Produtor real da projeção (levantamento focal P01):

`tela/estilo.py::ControladorTelaEstilo._construir_conteudo`

Forma atual dos campos de cada filho:

```python
campos={
    "navegavel": True,
    "selecionavel": True,
    "titulo": compor_titulo_com_amostra(
        nome, categoria, preset.dados, largura_nome=largura_nome,
    ),
    "categoria": categoria,
    "preset": nome,
}
```

A implementação adiciona `campos["amostra"]` nesse dicionário, sem remover,
renomear ou redefinir campo existente.

Regras fechadas:

- `campos["preset"]` permanece inalterado;
- `campos["titulo"]` permanece integralmente inalterado (mesmo valor, mesmo
  significado, mesmos consumidores);
- `campos["amostra"]` é novo somente como campo da projeção semântica;
- o valor de `amostra` é exatamente a mesma amostra já produzida pelo fluxo
  existente;
- é proibido obter `amostra` por parsing de `titulo`;
- nenhum conteúdo visível muda.

A proveniência semântica de `amostra` é o mesmo componente que já produz a
amostra antes da composição final de `titulo`:
`tela/renderizacao/estilo.py::amostra_de_preset`, invocado hoje dentro de
`compor_titulo_com_amostra`. A implementação obtém o valor chamando
`amostra_de_preset` (já exportada por aquele módulo) a partir dos mesmos
argumentos já disponíveis em `_construir_conteudo` (`categoria`,
`preset.dados`). Não altera `amostra_de_preset` nem `compor_titulo_com_amostra`.

O restante de `tela/estilo.py` — inclusive `_NIVEIS_FORMATO`, escolhas,
candidato, baseline, aplicar, persistir e publicar — permanece intacto.

### 8.4.1 `tela/renderizacao/estilo.py` — leitura, sem edição

Levantamento focal P01: `amostra_de_preset` (linha 151) e
`compor_titulo_com_amostra` (linhas 164-175) já produzem o valor semântico
necessário. `_construir_conteudo` já importa `compor_titulo_com_amostra`;
pode importar também `amostra_de_preset` sem modificar o módulo de origem.
Nenhuma necessidade causal concreta de editar
`tela/renderizacao/estilo.py` foi demonstrada. Edição desse arquivo **não**
está autorizada.

---

## 9. Bloqueio documental de H-0063 — RESOLVIDO (não está mais ativo)

### 9.1 Contexto histórico (criação deste handoff)

Na criação, H-0063 ficou `BLOCKED_DOCUMENTATION` porque
`_construir_conteudo` populava `navegavel`, `selecionavel`, `titulo`,
`categoria` e `preset`, mas não possuía campo separado para o exemplo
visual. `compor_titulo_com_amostra` concatenava nome e amostra em
`campos["titulo"]`. Sem nomes literais fechados para as duas colunas, este
handoff recusou inventar `campo` e recusou editar o produtor sem decisão
documental prévia. Esse registro permanece como contexto factual. **O
bloqueio não está mais ativo.**

### 9.2 Decisão documental agora fechada

Transportada de ADR-0047 §4.11.1 (P02), contratos §36.8 / §15.1, e QA
`ADR_APPROVED` + `ADR_APPLICATION_APPROVED`:

- coluna 1 = `preset` (já existente, inalterado);
- coluna 2 = `amostra` (novo somente na projeção, mesmo valor semântico já
  produzido por `amostra_de_preset` antes de compor `titulo`);
- `titulo` permanece integralmente inalterado;
- parsing de `titulo` é proibido;
- nenhum campo existente é removido, renomeado ou redefinido;
- nenhum conteúdo visível muda.

Nenhuma decisão documental material permanece aberta. H-0063 está fechada
para implementação neste handoff.

### 9.3 ACH-001 (H-0055 / sufixo) — RESOLVIDO (não está mais ativo)

Contexto histórico: o QA pós-P01 registrou ACH-001 — H-0055 deve continuar
exibindo `A)`, `B)`, `C)`, `D)`, mas a capacidade H-0072 então aceitava
apenas `designador.tipo` e não representava `sufixo: ")"`. O PATCH_HANDOFF
H-0073 P02 comprovou essa impossibilidade e terminou `BLOCKED_DOCUMENTATION`
sem alterar este handoff. `A` não foi aceito como equivalente de `A)`.

Esse registro permanece como contexto factual. **O bloqueio não está mais
ativo.** A capacidade genérica corrigida (H-0072 P01,
`I1_IMPLEMENTATION_APPROVED`) aceita:

```yaml
designador:
  tipo: <tipo_canônico>
  prefixo: <string opcional>
  sufixo: <string opcional>
```

Este P03 fecha H-0055 com `tipo: alfabetico_maiusculo` e `sufixo: ")"` na
configuração estrutural (§8.1). Não é necessária nova decisão documental.
Não é necessário alterar H-0072. H-0055 está `FECHADO_PARA_IMPLEMENTACAO`.

---

## 10. Testes e demonstrações

Todo arquivo futuro possui caminho literal. Não há curingas.

### 10.1 Testes existentes a atualizar (somente H-0055)

| Arquivo | Ação |
|---|---|
| `tela/teste_navegacao.py` (seção H-0055, `~L2032-2200`) | Estender com casos que constroem o console com `formato_filho_dois_niveis` preenchido; testes existentes (`teste_h0055_politica_explicita_e_terceiro_nivel_invalido`, `teste_h0055_toroides_independentes_wrap_entrada_e_retorno`, `teste_h0055_rotulo_esc_recalcula_nos_dois_niveis`, `teste_h0055_escolha_inicial_transferencia_idempotencia_e_isolamento`, `teste_h0055_tab_reseta_cursor_sem_alterar_escolhas_e_preserva_resize`) não são reescritos — continuam válidos porque testam navegação/seleção, não formatação física |
| `demo/teste_demo_console.py` (cenário `h0055_dois_niveis_por_foco`, `~L157-566`) | Estender asserções de linhas físicas para tabulação 5..10, designador `A)`/`B)`/`C)`/`D)` (nunca `A`/`B`/`C`/`D` sem `)` como resultado correto) e recuo unitário de `ec`/`tg`/designador/conteúdo |

Nenhum teste existente de H-0063 precisa ser alterado: `preset`, `titulo`,
navegação, seleção, candidato, baseline, aplicação, persistência e
publicação permanecem semanticamente idênticos, e as assertivas atuais
continuam válidas. É proibido maquiar teste existente para obter verde.

### 10.2 Teste novo (H-0055)

`demo/teste_demo_h0073_h0055_reconciliado.py` — prova, pelo ponto de entrada
real (`demo/demo.py`), que a tela reconciliada é carregada e renderizada com
a nova configuração (não apenas por chamada direta ao renderer), na mesma
forma de `demo/teste_demo_h0072_formatacao_generica.py`. Exercita fluxo
real, não somente helper isolado. Deve provar:

1. a configuração estrutural contém `sufixo: ")"`;
2. o renderer produz `A)`;
3. o `)` vem da configuração estrutural;
4. o conteúdo externo permanece byte-a-byte inalterado;
5. a tabulação respeita 5..10;
6. `ec`/`tg`/designador/conteúdo se deslocam como unidade;
7. a apresentação continua `texto`;
8. navegação e seleção permanecem.

### 10.3 Testes novos (H-0063)

`tela/teste_estilo_h0073_h0063.py` — prova os 18 critérios de §11.2.
Obtém `amostra` por comparação com `amostra_de_preset`, nunca por parsing
de `titulo`. Não altera `tela/teste_estilo_h0070.py`.

`demo/teste_demo_h0073_h0063_reconciliado.py` — demonstração adequada de
H-0063 pelo ponto de entrada real (`demo/demo.py` /
`h0063_estilo_estrutura_navegacao_dois_niveis`), na mesma forma de
`demo/teste_demo_h0072_formatacao_generica.py`. Exercita fluxo real, não
somente helper isolado.

### 10.4 Testes existentes a executar (sem alteração)

H-0063 / Estilo:

- `tela/teste_estilo_h0063.py`
- `demo/teste_demo_estilo_h0063.py`
- `tela/teste_estilo_h0064.py`
- `tela/teste_estilo_h0065.py`
- `tela/teste_estilo_h0066.py`
- `tela/teste_estilo_h0067.py`
- `tela/teste_estilo_h0068.py`
- `tela/teste_estilo_h0070.py` (§12)

H-0072 (a aplicação concreta não pode quebrar o mecanismo genérico
corrigido; nenhum artefato H-0072 é alterado para obter verde; o caso de
`sufixo ")"` já foi provado e aprovado em H-0072):

- `tela/teste_formato_filho_dois_niveis_por_foco.py`
- `demo/teste_demo_h0072_formatacao_generica.py`

### 10.5 Suíte focal (não ampliar genericamente)

Execução mínima obrigatória:

1. `tela/teste_navegacao.py` (seção H-0055)
2. `demo/teste_demo_console.py` (cenário `h0055_dois_niveis_por_foco`)
3. `demo/teste_demo_h0073_h0055_reconciliado.py` (novo)
4. `tela/teste_estilo_h0073_h0063.py` (novo)
5. `demo/teste_demo_h0073_h0063_reconciliado.py` (novo)
6. `tela/teste_estilo_h0063.py`
7. `demo/teste_demo_estilo_h0063.py`
8. `tela/teste_estilo_h0064.py`
9. `tela/teste_estilo_h0065.py`
10. `tela/teste_estilo_h0066.py`
11. `tela/teste_estilo_h0067.py`
12. `tela/teste_estilo_h0068.py`
13. `tela/teste_estilo_h0070.py` (inclui a falha histórica §12)
14. `tela/teste_formato_filho_dois_niveis_por_foco.py`
15. `demo/teste_demo_h0072_formatacao_generica.py`

Nenhuma alteração genérica em toda a suíte é autorizada.

---

## 11. Critérios de aceite

### 11.1 H-0055 (obrigatórios)

- [ ] `h0055_dois_niveis_por_foco.json` declara
  `console.formato.dois_niveis_por_foco.filho` exatamente como §8.1
  (incluindo `sufixo: ")"` literal), preservando `formato.excesso` existente.
- [ ] `h0055_dois_niveis_por_foco_conteudo.json` permanece byte-a-byte
  inalterado, inclusive a declaração histórica de designador no envelope.
- [ ] Nenhum filho de H-0055 mantém `ec`/`tg` alinhado ao pai — a unidade
  inteira (`ec`, `tg` quando existir, designador, conteúdo) desloca-se junto
  a partir da tabulação.
- [ ] Tabulação efetiva de H-0055 respeita o intervalo 5..10.
- [ ] Designador de filho de H-0055 usa `alfabetico_maiusculo` com
  `sufixo: ")"` na configuração estrutural, produzindo `A)`, `B)`, `C)`,
  `D)`, …; `A`/`B`/`C`/`D` sem `)` **não** é resultado correto; o `)` vem
  da configuração estrutural, não de herança do conteúdo; nenhuma
  identidade lógica nova é criada.
- [ ] Apresentação de H-0055 continua `texto`; H-0055 não é transformada em
  tabela.
- [ ] Conteúdo textual dos filhos de H-0055 (`titulo`) permanece idêntico ao
  atual.
- [ ] Navegação de H-0055 (toroide de pais, toroide de filhos por pai,
  seleção exclusiva obrigatória de filho por pai, paginação) permanece
  integralmente preservada.
- [ ] Resize de H-0055 recalcula tabulação sem perder o item lógico
  corrente.

### 11.2 H-0063 (obrigatórios)

- [ ] `campos["preset"]` continua igual ao valor anterior.
- [ ] `campos["titulo"]` continua exatamente igual ao valor anterior.
- [ ] `campos["amostra"]` existe.
- [ ] `amostra` corresponde ao mesmo valor produzido semanticamente pelo
  fluxo atual (`amostra_de_preset`).
- [ ] `amostra` não é obtida por parsing de `titulo`.
- [ ] H-0063 declara tabulação 5..10.
- [ ] H-0063 usa designador `nenhum`.
- [ ] H-0063 usa `apresentacao = tabela`.
- [ ] H-0063 declara exatamente as colunas `campo: preset` e
  `campo: amostra`.
- [ ] Espaçamento é 3..8.
- [ ] Filhos de pais diferentes compartilham alinhamento de colunas.
- [ ] Cursor/toggle do filho são deslocados com a unidade inteira.
- [ ] Não aparece designador visual do filho.
- [ ] Conteúdo visível de preset e amostra permanece semanticamente
  idêntico.
- [ ] Seleção e navegação continuam iguais.
- [ ] Candidato, baseline, aplicação, persistência e publicação permanecem
  inalterados.
- [ ] Resize recalcula a disposição.
- [ ] Conteúdo dinâmico continua sendo dados, sem configuração visual
  embutida.

### 11.3 Pacote e preservação

- [ ] `h0062_estilo.json` permanece intocado (§5.1).
- [ ] As fixtures `h0072_formatacao_generica_dois_niveis_por_foco{,_conteudo}.json`
  permanecem intocadas e a suíte de H-0072 continua passando sem alteração
  dessas fixtures, do código H-0072 ou dos testes H-0072.
- [ ] Nenhuma configuração de apresentação foi transferida para nenhum
  documento externo de conteúdo nem para a projeção dinâmica além do campo
  semântico `amostra`.
- [ ] `tela/teste_formato_filho_dois_niveis_por_foco.py` e
  `demo/teste_demo_h0072_formatacao_generica.py` continuam passando sem
  alteração.
- [ ] `tela/teste_estilo_h0070.py::test_filhos_sem_ordinais_cursor_e_indicadores_preservados`
  foi executado na regressão; sua assertiva não foi alterada (§12).
- [ ] Demonstrações reais pelo ponto de entrada: `demo/teste_demo_h0073_h0055_reconciliado.py`
  e `demo/teste_demo_h0073_h0063_reconciliado.py`.
- [ ] Relatório de implementação em
  `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0073.md`.

---

## 12. Regressão H-0070

`tela/teste_estilo_h0070.py::test_filhos_sem_ordinais_cursor_e_indicadores_preservados`
é falha histórica: encontrava o cursor do filho na posição 2 quando
esperava posição `>= 4`. H-0072 demonstrou que essa falha era não causal à
capacidade genérica.

H-0073 altera a apresentação concreta de H-0063. Este teste **entra na
REGRESSÃO a executar** (§10.5 item 13). A assertiva **não é alterada**
antecipadamente. É proibido maquiar o teste para obter verde.

Resultado esperado na implementação / QA:

- se a nova configuração correta de H-0063 fizer o teste passar, registrar
  a resolução causal pelo H-0073;
- se ele continuar falhando, o QA determina causalidade.

---

## 13. Relatório de implementação

A implementação deste handoff deve criar nominalmente:

```
docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0073.md
```

registrando: arquivos efetivamente alterados/criados frente às listas de
§7.1 e §7.2; resultado de cada critério de §11; confirmação de que os
arquivos de §7.4 permaneceram intocados; resultado da suíte focal de
§10.5; status do teste de regressão H-0070 (§12); confirmação de que
`campos["titulo"]` e `campos["preset"]` permaneceram inalterados e de que
`amostra` não foi obtida por parsing de `titulo`. Máximo normal: 700
palavras.

---

## 14. Exceção operacional focal

A busca da criação foi restrita a `config/telas/demo` via `rg` (nunca
`find .`, `tree`, inventário genérico ou busca em `docs/relatorios`). A
cadeia do produtor de H-0063 usou identificadores da própria configuração
e dos arquivos diretamente na cadeia (`tela/estilo.py`,
`tela/renderizacao/estilo.py`, `tela/renderizacao/conteudo_externo.py`,
`tela/teste_estilo_h0070.py`). A verificação de `h0062_estilo.json` (§5.1)
usou apenas o próprio identificador da tela e documentação já existente.

O levantamento P01, para fechar arquivos nominais de H-0063, restringiu-se
a: `h0063_estilo_estrutura_navegacao_dois_niveis`, `ControladorTelaEstilo`,
`_construir_conteudo`, `campos["preset"]`, `campos["titulo"]`,
`amostra_de_preset`, testes que mencionam `h0063`, testes que exercitam a
projeção de conteúdo de Estilo, e o teste histórico H-0070. Não houve
inventário genérico nem busca em `docs/relatorios/**` além do predecessor
autorizado
(`docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0047_POS_P01.md`).

---

## 15. Bloqueios

Nenhum.

Estado executivo final, inequívoco:

```yaml
H-0055: CONCLUIDO
H-0063: CONCLUIDO
bloqueios: nenhum
```

O bloqueio documental de H-0063 registrado na criação (**não está mais
ativo**) foi resolvido por ADR-0047 P02, QA `ADR_APPROVED`, patch P01 da
aplicação documental e QA `ADR_APPLICATION_APPROVED`. Coluna 1 = `preset`.
Coluna 2 = `amostra`. Estado fechado no P01, preservado neste P03.

ACH-001 (**não está mais ativo**) foi comprovado no P02
(`BLOCKED_DOCUMENTATION`, handoff intocado) e resolvido após H-0072 P01
(`I1_IMPLEMENTATION_APPROVED`) por este P03: H-0055 declara
`sufixo: ")"` na configuração estrutural e continua mostrando `A)`. Não
há pendência de H-0055, não há incapacidade de representar `A)`, não há
necessidade de alterar H-0072 e não há necessidade de nova decisão
documental. O QA final foi `I1_IMPLEMENTATION_APPROVED`; a revalidação manual
final foi `MANUAL_REVALIDATION_APPROVED`, com VM-H0073-001 e VM-H0073-002
resolvidos, tabulação dinâmica de H-0055/H-0063 aprovada e espaçamento 3..8
preservado. H-0070 permanece `FALHA_HISTORICA_NAO_CAUSAL`, fora deste ciclo.
\n