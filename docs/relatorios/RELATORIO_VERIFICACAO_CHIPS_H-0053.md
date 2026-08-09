---
name: RELATORIO_VERIFICACAO_CHIPS_H-0053
description: "Verificação factual das autoridades de chips para H-0053"
metadata:
  type: relatorio_busca_levantamento_verificacao
  tipo_execucao: VERIFICACAO
  status: VERIFICATION_COMPLETE
  data: 2026-08-08
rastreabilidade:
  etapa: VERIFICACAO_FOCAL
  objeto: H-0053 — arvore_colapsavel
  autoridade_principal: docs/contratos/contrato_barra_de_menus.md; docs/contratos/contrato_chip.md
  cadeia_raiz: ADR-0012 → barra_de_menus/chip → ADR-0042
  predecessor_imediato: docs/handoff/H-0053-arvore-colapsavel.md
---

# RELATORIO_VERIFICACAO_CHIPS_H-0053 — Verificação

## 1. Pergunta e status

```yaml
tipo_execucao: VERIFICACAO
pergunta_factual: "Obrigatoriedade de Ajuda e representação documental de Espaço em arvore_colapsavel."
status_literal: VERIFICATION_COMPLETE
```

## 2. Escopo fechado

```yaml
caminhos_consultados:
  - docs/nomenclatura/01_NUCLEO_COMUM.md
  - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  - docs/nomenclatura/32_CONSOLE.md
  - docs/contratos/contrato_chip.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_json_barra_de_menus.md
  - docs/contratos/contrato_console.md
  - docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md
  - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
  - docs/adr/ADR-0042-navegacao-multinivel-do-console.md
  - config/telas/demo/h0053_arvore_colapsavel.json
  - docs/handoff/H-0053-arvore-colapsavel.md
buscas_executadas:
  - comando_ou_padrao: "rg -n 'Ajuda|[?]|Espaço|Espaco|[␣]|chip|barra_de_menus|seleção|selecao|arvore_colapsavel'"
    caminho: "ADRs focais 0012, 0031 e 0042"
    finalidade: "Localizar decisões normativas focais."
  - comando_ou_padrao: "rg -n 'barra_de_menus|chips|Esc|Ajuda|Navegar|Espaço|Espaco|␣|?|acao|regra_existencia|regra_ativo'"
    caminho: "fixture H-0053 e handoff H-0053"
    finalidade: "Verificar declaração concreta e autoridades carregadas."
limites_aplicados:
  - "Nenhum relatório histórico do ciclo foi consultado."
  - "Nenhuma alteração foi feita em fixture, handoff, código, contrato, nomenclatura ou ADR."
```

## 3. Fatos confirmados

```yaml
fatos_confirmados:
  - id: F-01
    fato: "[?] Ajuda é chip canônico, mas a barra é declarativa por tela; canônico fixa semântica e ordem quando presente, não presença universal."
    origem_focal: "ADR-0012 D1-D8; nomenclatura 31 §4.1 e §4.3; contrato_barra_de_menus §§4, 8.2 e 20."
  - id: F-02
    fato: "No contrato_chip, regra_existencia: sempre para [ ? ] vale para a instância concreta declarada; o próprio contrato exige declaração no tela.json."
    origem_focal: "contrato_chip §§2, 6 e 7; contrato_barra_de_menus §8.2 (‘quando declarado’/‘quando presentes’)."
  - id: F-03
    fato: "H-0053 declara somente Esc/Voltar e ✥/Navegar na barra; não declara [ ? ] Ajuda."
    origem_focal: "config/telas/demo/h0053_arvore_colapsavel.json:45-61."
  - id: F-04
    fato: "arvore_colapsavel é navegação hierárquica sem seleção; Espaço abre ou fecha o ramo corrente."
    origem_focal: "ADR-0042 D-MULTI-05 e §4.5; fixture H-0053:34-41."
  - id: F-05
    fato: "[␣] é o chip canônico de Selecionar/toggle de seleção múltipla; sua existência depende de seleção múltipla e item selecionável."
    origem_focal: "nomenclatura 31 §4.3; contrato_barra_de_menus §§12 e 23.1; contrato_chip §§7, 14 e 17; contrato_console §§8, 22.7 e 23.5."
  - id: F-06
    fato: "Não há regra vigente que exija chip visual para toda tecla funcional, nem precedente que feche tipo, rótulo ou ação de chip específico para Espaço em arvore_colapsavel."
    origem_focal: "contratos de barra/chip: chips são declarados no JSON; tipos específicos e ações são declarativos, sem identidade normativa para Espaço."
  - id: F-07
    fato: "O manifesto de leitura do handoff lista ADR-0042, ADR-0041 e contrato_console, mas não contrato_barra_de_menus, contrato_chip ou nomenclatura 31."
    origem_focal: "docs/handoff/H-0053-arvore-colapsavel.md:100-110."
```

## 4. Não confirmados

```yaml
nao_confirmados:
  - id: N-01
    afirmacao: "Que [␣] possa ser reutilizado como ‘Colapsar/Abrir’."
    evidencia_ausente_ou_insuficiente: "A semântica documental de [␣] é seleção; não existe autorização de reutilização."
  - id: N-02
    afirmacao: "Que exista um chip específico obrigatório para Espaço."
    evidencia_ausente_ou_insuficiente: "Nenhum contrato, nomenclatura ou ADR focal fecha essa exigência, tecla, rótulo ou ação."
```

## 5. Achados e bloqueios

```yaml
achados:
  - id: A-01
    fato: "Ajuda é DECLARATIVA, não OBRIGATORIA. A regra ‘sempre’ de contrato_chip é de permanência da instância já declarada; não supera a regra explícita de declaração por tela da ADR-0012 e do contrato da barra. Não há contradição material após essa distinção de escopo: contrato_barra_de_menus rege composição da região, contrato_chip rege a instância de chip e nomenclatura rege termos."
    evidencia_focal: "ADR-0012 D1-D8; contrato_barra_de_menus §4 e §8.2; contrato_chip §2 e §6."
  - id: A-02
    fato: "A ausência de [ ? ] em H-0053 não viola a regra vigente. Se declarado, deve ser último, ativo e não pode ser omitido por paginação ou falta de largura; falta de largura resulta em erro de layout, conforme nao_omitir_chips. Página do console não cria nova instância de barra."
    evidencia_focal: "contrato_barra_de_menus §§7, 17, 19 e 20; contrato_chip §§8-10."
  - id: A-03
    fato: "Espaço em H-0053 não usa [␣]. A representação normativa está aberta: não há chip canônico aplicável nem chip específico exigido; portanto o estado atual classifica a presença de chip como não exigida, sem inventar rótulo ou tipo."
    evidencia_focal: "ADR-0042 D-MULTI-05; ADR-0031 D13-D14; contrato_barra_de_menus §12; contrato_chip §7."
  - id: A-04
    fato: "O handoff omitiu autoridades vigentes de barra_de_menus/chip; deve receber patch documental antes de eventual retomada de validação. Não há patch de implementação decorrente desta verificação."
    evidencia_focal: "Manifesto de leitura do handoff H-0053:100-110, confrontado com os contratos e nomenclatura obrigatórios."
bloqueios: []
```

## 6. Resultado normativo

```yaml
ajuda:
  classificacao: DECLARATIVA
  autoridade: "ADR-0012 D1-D8; contrato_barra_de_menus §§4 e 8.2; contrato_chip §§2 e 6; nomenclatura 31 §4.3."
  consequencia_para_H0053: "A omissão de [ ? ] Ajuda é permitida; se declarado futuramente, fica por último e sempre visível/ativo nesta instância."

espaco:
  classificacao: CHIP_NAO_EXIGIDO
  autoridade: "ADR-0042 D-MULTI-05; nomenclatura 32 §4.10; contrato_barra_de_menus §§12 e 23.1; contrato_chip §§7 e 14."
  representacao_fechada: "Nenhuma. [␣] não pode representar colapso; não há chip específico normativamente exigido ou com rótulo/tipo/ação fechados."
  consequencia_para_H0053: "A ausência de chip visual para Espaço não viola regra vigente; a ação continua sendo a semântica fechada de arvore_colapsavel."

handoff_H0053:
  omissao_de_autoridade_de_chips: SIM
  precisa_patch_handoff: SIM
  precisa_patch_implementacao: NAO

ordem_e_permanencia:
  ajuda: "Último chip quando declarado; não muda com página do console."
  especifico_espaco: "Se algum dia autorizado, faixa entre [⏎] e [V]/[?]; posição, rótulo e ação ainda não estão fechados."
  largura: "Chips declarados não podem ser omitidos; resultado normativo é erro_layout."
  pagina: "Paginação é estado da instância do console, não nova tela/barra."
```

Próxima etapa adequada: `PATCH_HANDOFF`, apenas para registrar a cadeia de
autoridades de barra/chip e este resultado; depois disso, a validação manual
pode ser retomada sem patch de implementação derivado desta verificação.
