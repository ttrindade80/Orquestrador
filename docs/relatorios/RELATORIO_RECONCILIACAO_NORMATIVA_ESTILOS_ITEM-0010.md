# Relatório de Reconciliação Normativa — Estilos/Chips/Menu Bar (ITEM-0010)

```yaml
rastreabilidade:
  etapa: RECONCILIACAO_NORMATIVA_DOCUMENTAL
  item: ITEM-0010
  adr: ADR-0046
  handoffs_analisados: [H-0069, H-0070]
  papel: levantamento_e_reconciliacao_documental
  decide_proximo_estagio: false
  cria_ou_altera_ADR: false
  cria_H0071: false
  altera_H0070: false
  implementa_codigo: false
  executa_QA: false
```

## 1. Escopo e manifesto efetivamente lido

Leitura controlada, restrita exatamente aos artefatos abaixo (manifesto fechado):

- `docs/handoff/H-0070-refinamentos-finais-apresentacao-estilo-chips-barra-menus.md` (completo)
- `docs/handoff/H-0069-demonstracao-integrada-override-local-estilo.md` (completo)
- `docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md` (completo)
- `docs/contratos/contrato_estilo.md` (completo)
- `docs/contratos/contrato_barra_de_menus.md` (completo)
- `docs/contratos/contrato_console.md` (completo, incluindo a seção 22 — políticas multinível/`dois_niveis_por_foco` — e a seção 24 — paginação)
- `docs/nomenclatura/10_ESTILO.md` (completo)
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` (completo)
- `docs/nomenclatura/32_CONSOLE.md` (completo)
- `docs/relatorios/RELATORIO_VALIDACAO_MANUAL_FINAL_ITEM-0010.md` (completo)

Nenhum outro handoff, relatório, contrato ou módulo de nomenclatura foi lido. Não foi feita busca ampla no repositório. A rastreabilidade handoff→ADR (todos citam `item: ITEM-0010` / `adr: ADR-0046`) não foi reverificada — foi tratada como fato já estabelecido, conforme instrução recebida.

As regras externas R1–R9 fornecidas pelo usuário foram tratadas como **entrada não normativa** durante toda a análise — nenhuma foi presumida já aprovada pelo projeto.

---

## 2. Matriz de prescrições H-0070 → autoridade

Convenção: "autoridade estrita" = ADR-0046 + contratos + nomenclatura do manifesto (exclui H-0069/H-0070, que são handoffs, não autoridade normativa primária). Onde H-0070 coincide ou diverge do que H-0069 registra, isso é anotado como informação operacional, não como base da classificação.

| ID | Resumo da regra | Seção H-0070 | Autoridade alegada pelo handoff | Evidência normativa real encontrada | Autoridade e seção | Classificação |
|---|---|---|---|---|---|---|
| H70-R01 | Remover ordinais alfabéticos (`A)`,`B)`,`C)`) dos filhos da tela Estilo | §5 | ADR-0046 (genérico) | ADR-0046 delega explicitamente "geometria exata da tela" e detalhes de apresentação aos handoffs, desde que não contrariem decisões normativas/contratos | ADR-0046, seção "Detalhes deliberadamente não fechados" | COMPATIVEL_MAS_NAO_EXPLICITADA |
| H70-R02 | Cursor ocupa a região liberada pelo ordinal; largura de prefixo idêntica entre focalizado/não focalizado | §5 | ADR-0046 (genérico) | "Tem largura reservada estável — a coluna não se desloca ao mudar o cursor de item" (indicador do item corrente) | `contrato_console.md` §22.6 | EXPLICITAMENTE_AUTORIZADA |
| H70-R03 | Indicador de preset vigente/não vigente (`●`/`○`) preservado exatamente como hoje | §5 | ADR-0046 §4/§7 (camadas de estado) | Schema de `indicadores.incluido` (par on/off) é campo obrigatório do estilo; mecanismo de "seleção exclusiva obrigatória de filho por pai" em `dois_niveis_por_foco` exige indicador de escolha do filho | `contrato_estilo.md` §3.3; `contrato_console.md` §22.16 | EXPLICITAMENTE_AUTORIZADA |
| H70-R04 | Amostras de uma mesma categoria começam na mesma coluna visual (`_largura_sem_ansi`/`_ljust_sem_ansi`) | §6 | ADR-0046 §2.4 (amostras derivadas do preset) | ADR-0046 exige que cada filho apresente nome+amostra, mas não fixa alinhamento colunar entre irmãos; detalhe delegado | ADR-0046 §2; "Detalhes deliberadamente não fechados" | COMPATIVEL_MAS_NAO_EXPLICITADA |
| H70-R05 | Chips de uma tecla permanecem idênticos ao comportamento vigente, em todos os presets/telas | §7 | Implícito (não regressão) | O schema de chip resolve exatamente 5 campos por preset (determinístico); nada no schema prevê exceção para caso de tecla única — o comportamento de tecla única é o único caso já descrito pelo schema | `contrato_estilo.md` §3.2, R-3, R-10 | EXPLICITAMENTE_AUTORIZADA |
| H70-R06 | Presets delimitados (Colchete/Curva/Ornamental/Traço) preservam concatenação individual por tecla, sem `"/"` introduzido | §8 | ADR-0046 (não introduzir segundo mecanismo) | `[PgUp][PgDn] Páginas` é a representação canônica documental fixada para a paginação; porém `contrato_barra_de_menus.md` §5 qualifica que essa notação é "documental, não normativa" quanto aos caracteres concretos, que vêm do preset resolvido | `contrato_barra_de_menus.md` §5, §24.4 | COMPATIVEL_MAS_NAO_EXPLICITADA |
| H70-R07 | Preset `Ponto` multitecla: unidade única, teclas separadas por `"/"`, um ponto final (`" PgUp/PgDn."`) | §9 | Discriminação estrutural §4.3 (não citação de autoridade externa) | Nenhuma autoridade do manifesto define convenção de separador `"/"` para composição multitecla; o campo não existe no schema de 5 campos do chip | `contrato_estilo.md` §3.2 (schema não prevê separador) | COMPATIVEL_MAS_NAO_EXPLICITADA — ver nota de tensão com R-2 (hardcoding) na seção 9 deste relatório |
| H70-R08 | Preset `Destaque Texto` multitecla: unidade única, `"/"`, espaços laterais sem cor obrigatória | §10 | Discriminação estrutural §4.3 | Idem H70-R07; `cor_texto` é campo do schema, mas a regra de "unidade com `/`" não é | `contrato_estilo.md` §3.2 | COMPATIVEL_MAS_NAO_EXPLICITADA |
| H70-R09 | Preset `Destaque Fundo` multitecla: unidade única, `"/"`, fundo cobre os dois espaços laterais | §11 | Discriminação estrutural §4.3 | Idem H70-R07/08; `cor_fundo` é campo do schema, mas o envelope de composição multitecla não | `contrato_estilo.md` §3.2 | COMPATIVEL_MAS_NAO_EXPLICITADA |
| H70-R10 | Comportamentos de §9-§11 devem valer nos chips **reais** da Barra de Menus, não só na amostra da tela Estilo; `_texto_chip_barra` deve parar de descartar `cor_texto`/`cor_fundo` | §12 | ADR-0046 (estilo global único consumido por todos os renderers) | "Todas as classes de tela e todos os renderers... leem desse objeto" (R-1); proibição de hardcoding (R-2); "O renderer da `barra_de_menus` não define nem hardcoda cores de estado dinâmico — lê exclusivamente do schema de estilo ativo" | `contrato_estilo.md` §2, R-1, R-2; `contrato_barra_de_menus.md` §18, R-7 | EXPLICITAMENTE_AUTORIZADA |
| H70-R11 | Cálculo de largura/alinhamento da Barra deve considerar sequências ANSI corretamente | §13 | Mecanismo já existente (`_largura_sem_ansi`) | Renderização final em terminal (caracteres, cores, escape codes) é expressamente colocada fora do escopo do contrato, o que não contradiz a exigência, apenas não a fixa textualmente | `contrato_console.md` §18 ("Renderização final em terminal... não pertencem a este contrato") | COMPATIVEL_MAS_NAO_EXPLICITADA |

Nenhuma leitura adicional foi necessária para completar esta matriz dentro do manifesto fechado.

---

## 3. Matriz R1–R9 (entrada externa do usuário) → classificação normativa

Comparação restrita a ADR-0046 + contratos + nomenclatura (autoridade estrita). Alinhamento/conflito com H-0069/H-0070 é registrado como nota informativa, não como base da classificação.

| Regra | Classificação | Evidência favorável | Evidência conflitante | Autoridade/seção | Justificativa |
|---|---|---|---|---|---|
| R1 — chip de uma tecla permanece como está | **JA_EXIGIDA** | Schema de chip resolve exatamente 5 campos determinísticos por preset; não há exceção para tecla única | nenhuma | `contrato_estilo.md` §3.2, R-3, R-10 | O comportamento de tecla única já é o único caso descrito pelo schema; qualquer alteração dele exigiria mudar o preset resolvido, não a composição multitecla |
| R2 — 2+ teclas formam unidade única `"tecla1/tecla2"`, delimitadores só nas extremidades, **para qualquer preset** | **ALTERACAO_NORMATIVA** | Nenhuma | Contradiz H-0070 §8, que preserva explicitamente a concatenação individual sem `"/"` para os presets delimitados (Colchete, Curva, Ornamental, Traço); nenhum campo do schema de 5 campos do chip representa um separador `"/"` | `contrato_estilo.md` §3.2 (schema não define separador); H-0070 §8 (nota informativa, não autoridade) | Introduz convenção de composição não prevista em nenhuma autoridade e, ao aplicar-se universalmente, entra em rota de colisão com uma decisão já fechada (H-0070 §8) para a família de presets delimitados — decisão que precisaria ser incorporada normativamente antes de implementação |
| R3 — preset `Ponto`: delimitador assimétrico (espaço à esquerda, ponto à direita), `" PgUp/PgDn."` | **COMPATIVEL_NAO_EXPLICITADA** | Não contradiz nenhuma autoridade estrita; não é preset delimitado, logo não colide com H-0070 §8 | nenhuma na autoridade estrita | `contrato_estilo.md` §3.2 | Coincide integralmente com a decisão já fechada em H-0070 §9 (nota informativa: **já exigida por H-0070**, ainda que não pela ADR/contratos diretamente) |
| R4 — presets de cor/destaque multitecla também usam unidade única `"/"` com espaçamento lateral coerente | **COMPATIVEL_NAO_EXPLICITADA** | Não contradiz autoridade estrita; refere-se apenas a `Destaque Texto`/`Destaque Fundo`, não aos presets delimitados | nenhuma na autoridade estrita | `contrato_estilo.md` §3.2 | Coincide com H-0070 §10-§11 (nota informativa: já exigida por H-0070 para essa família de presets) |
| R5 — estilos globais devem ser aplicados à Menu Bar **real**, não só a demonstrações/telas de estilo | **JA_EXIGIDA** | "Todas as classes de tela e todos os renderers... leem desse objeto"; proibição de hardcoding; "o renderer da barra_de_menus... lê exclusivamente do schema de estilo ativo" | nenhuma | `contrato_estilo.md` §2, R-1, R-2; `contrato_barra_de_menus.md` §18, R-7 | Já é regra vigente e explícita, independentemente de H-0070; o defeito documentado em H-0070 §4.2 (`_texto_chip_barra` descarta `cor_texto`/`cor_fundo`) é justamente violação dessa regra já existente |
| R6 — destaque de fundo forma unidade única, não vaza para o texto descritivo nem para o chip seguinte | **COMPATIVEL_NAO_EXPLICITADA** | Consistente com o padrão de envelope (`código + conteúdo + reset`) já usado para `cor_inativo`/`cor_alerta`, citado em H-0070 §4.2 como mecanismo existente | nenhuma na autoridade estrita | `contrato_estilo.md` R-7 (tradução de cor exclusiva do renderer, implica fechamento correto do envelope) | Não há regra textual sobre "vazamento" de envelope de cor entre chips, mas é corolário razoável da responsabilidade de tradução de cor do renderer |
| R7 — "Destaque Texto": espaço esquerdo na cor do terminal, espaço direito na cor de destaque do fundo | **ALTERACAO_NORMATIVA** | Nenhuma | Contradiz o desenho simétrico de H-0070 §10 (`Destaque Texto`: cor aplica-se só ao conteúdo, espaços não recebem cor, sem assimetria) e de H-0070 §11 (`Destaque Fundo`: fundo cobre os dois espaços simetricamente); o schema de chip só tem um `cor_texto` OU um `cor_fundo` por preset — nenhum campo permite duas cores distintas por lado dentro do mesmo preset | `contrato_estilo.md` §3.2 (schema não comporta coloração assimétrica de dois lados); H-0070 §10/§11 (nota informativa) | A formulação mistura terminologia de "Destaque Texto" (título) com comportamento de "cor de destaque do fundo" (conteúdo), descrevendo um comportamento que nenhum preset atual do schema é capaz de representar sozinho — decisão que exige fechamento normativo explícito antes de qualquer implementação, não apenas reinterpretação de código |
| R8 — cálculo de largura/alinhamento da Barra deve considerar ANSI corretamente | **COMPATIVEL_NAO_EXPLICITADA** | Não contradiz autoridade; "renderização final em terminal... escape codes... não pertencem a este contrato" — deferido, não proibido | nenhuma | `contrato_console.md` §18 | Mecânica de renderização é expressamente delegada à implementação; não há conflito, apenas ausência de fixação textual |
| R9 — motivação: uniformizar lógica visual entre presets de dois lados como unidade visual da ação | **COMPATIVEL_NAO_EXPLICITADA** | Não contradiz nenhuma autoridade | nenhuma | — | É enunciado de motivação/princípio de design, não uma regra verificável isoladamente; não colide com nada no manifesto |

### Nota de tensão normativa (R2, R4, R7, H70-R07/R08/R09)

`contrato_estilo.md` §2/R-2 proíbe hardcoding de "símbolo, cor ou caractere pertencente a esta especificação... sem exceção para valores óbvios ou padrões universais". O caractere `"/"` usado como separador entre teclas (R2–R4, H70-R07/R08/R09) não é um dos 5 campos do schema de chip (`caractere_esquerdo`, `caractere_direito`, `cor_texto`, `caixa_alta`, `cor_fundo`) — é um caractere fixo introduzido pela composição multitecla, não derivado de `config/estilo.json`. Este relatório não resolve se esse caractere de junção deve ser tratado como "aparência hardcoded" (proibida por R-2) ou como "glue estrutural de layout" (categoria já aceita pelo contrato para itens como `vao_chip_texto`, análogo aos vãos declarados em `contrato_barra_de_menus.md` §17). Essa é uma tensão interpretativa real, não decidida por nenhuma autoridade do manifesto, e é registrada aqui para julgamento do Gerente Web — sem que este relatório proponha a resposta.

---

## 4. Mapeamento MF-ITEM0010-001..003

| Achado | Regra afetada em H-0070 | Autoridade vigente correspondente | Regras externas relacionadas | Natureza |
|---|---|---|---|---|
| **MF-ITEM0010-001** — composição multitecla incorreta (`"╭PgUp][PgDn╮"`) | §8 (presets delimitados preservam concatenação individual) e §12 (agrupamento deve depender da família estrutural do preset) | `contrato_estilo.md` §3.2/R-3/R-10 — um preset resolvido (`Curva`) deve produzir renderização coerente com seus próprios campos; misturar delimitadores de `Colchete` (`][`) dentro de bordas de `Curva` (`╭…╮`) viola a determinação do preset resolvido | R1 (não implicada diretamente); **R2** (decisão do usuário de estender `"/"` a **todos** os modelos multitecla, inclusive presets delimitados, o que supera o que H-0070 §8 havia fechado); R6 (não vazamento de unidade visual) | **Misto**: o defeito observado em si é `IMPLEMENTACAO_NAO_CONFORME_COM_AUTORIDADE_EXISTENTE` (viola H-0070 §8 e a coerência de preset resolvido exigida por `contrato_estilo.md`); a "decisão fechada pelo usuário para continuidade" (uniformizar `"/"` mesmo em presets delimitados) é `REGRA_NOVA_DO_USUARIO_AINDA_NAO_NORMATIVA`, pois contradiz e substituiria uma decisão já fechada em H-0070 §8 |
| **MF-ITEM0010-002** — cor/fundo não aplicados corretamente na Barra de Menus real | §4.2 (documenta o defeito: `_texto_chip_barra` descarta `cor_texto`/`cor_fundo`) e §12 (correção exigida) | `contrato_estilo.md` §2/R-1/R-2; `contrato_barra_de_menus.md` §18/R-7 — todo renderer deve consumir e aplicar o schema de estilo ativo, sem descartar campos resolvidos | **R5** (já `JA_EXIGIDA` — núcleo do achado); R4 (composição multitecla de cor); **R7** (formulação assimétrica específica de espaço-cor, que vai além do que qualquer autoridade define) | **Misto**: o núcleo do defeito (cor/fundo simplesmente não chegam à Barra real) é `IMPLEMENTACAO_NAO_CONFORME_COM_AUTORIDADE_EXISTENTE`, apoiado diretamente em regra já vigente (R-1/R-2 de `contrato_estilo.md`); a formulação assimétrica específica trazida pelo usuário (R7) é uma exigência adicional sem base normativa localizada, pendente de fechamento (`ALTERACAO_NORMATIVA`) |
| **MF-ITEM0010-003** — ordem/indentação de cursor, toggle e texto incorretas | §5 (cursor deve ocupar a região do ordinal; indentação/alinhamento preservados; largura idêntica entre focado/não focado) | `docs/nomenclatura/32_CONSOLE.md` §4.4 — estrutura do item do console é "sempre na ordem `ec`, `tg`, `tx`" (cursor, toggle, texto); `contrato_console.md` §22.6 — indicador do item corrente tem largura reservada estável | **Nenhuma de R1–R9** trata de geometria hierárquica cursor/toggle/texto; este achado é tematicamente independente do conjunto R1–R9 | `IMPLEMENTACAO_NAO_CONFORME_COM_AUTORIDADE_EXISTENTE` — a "decisão fechada pelo usuário" (ordem cursor → toggle → texto, indentação aplicada ao prefixo completo) **não é regra nova**: coincide exatamente com a ordem `ec, tg, tx` já fixada por `docs/nomenclatura/32_CONSOLE.md` §4.4, vigente independentemente desta manifestação do usuário |

---

## 5. Respostas às sete questões de síntese

**1. H-0070 contém alguma prescrição visual sem base normativa localizada nas autoridades vigentes? Quais IDs?**
Nenhuma prescrição de H-0070 foi classificada como `SEM_BASE_NORMATIVA_LOCALIZADA` neste levantamento. Várias (H70-R01, H70-R04, H70-R06, H70-R07, H70-R08, H70-R09, H70-R11) foram classificadas como `COMPATIVEL_MAS_NAO_EXPLICITADA`: amparadas pela cláusula de delegação de "detalhes deliberadamente não fechados" da ADR-0046 (ou, no caso de H70-R11, pela exclusão explícita de mecânica de renderização terminal do escopo do `contrato_console.md` §18), mas sem determinação textual explícita em ADR/contrato/nomenclatura.

**2. H-0070 contém alguma prescrição que contrarie autoridade vigente? Quais IDs?**
Não. Nenhum item da matriz H70-R01 a H70-R11 foi classificado como `CONTRARIA_A_AUTORIDADE` em relação a ADR-0046/contratos/nomenclatura. As únicas tensões de contrariedade identificadas neste relatório ocorrem entre **regras externas do usuário** (R2, R7) e **decisões já fechadas em H-0070** (§8, §10/§11) — não entre H-0070 e a autoridade normativa primária.

**3. As falhas manuais finais são defeitos de implementação de regra já existente, lacunas de especificação/handoff, ou dependem das novas regras do usuário?**
As três são de natureza mista, mas com núcleos distintos:
- MF-ITEM0010-001: núcleo é defeito de implementação (viola H-0070 §8 e a coerência de preset resolvido); a extensão do `"/"` a presets delimitados é regra nova do usuário, ainda não normativa.
- MF-ITEM0010-002: núcleo é defeito de implementação de regra já vigente (`contrato_estilo.md` R-1/R-2); a formulação assimétrica de cor (R7) é exigência adicional sem base normativa, pendente de fechamento.
- MF-ITEM0010-003: é integralmente defeito de implementação de regra **já existente e alheia às regras R1–R9** — a ordem `ec, tg, tx` já estava fixada por `docs/nomenclatura/32_CONSOLE.md` §4.4 antes de qualquer manifestação do usuário nesta rodada.

**4. Quais R1..R9 já eram exigidas antes da manifestação externa do usuário?**
R1 e R5.

**5. Quais R1..R9 são apenas compatíveis, mas ainda não explicitadas?**
R3, R4, R6, R8 e R9.

**6. Quais R1..R9 exigem alteração normativa?**
R2 e R7.

**7. Existe algum ponto que não pode ser resolvido com o manifesto fechado? Se sim, indique somente o artefato exato necessário e por quê.**
Sim, um ponto pontual: `docs/contratos/contrato_chip.md`. Tanto `contrato_estilo.md` quanto `contrato_barra_de_menus.md` referenciam esse contrato (pendência DOC-B006, "modelagem conceitual... deve ser formalizada em contrato próprio") como a futura autoridade completa da entidade `chip`, incluindo potencialmente regras de composição. Este relatório não teve autorização para lê-lo. Sem essa leitura, não é possível confirmar com certeza total se `contrato_chip.md` já contém (ainda que como rascunho/pendência) alguma regra sobre composição multitecla ou separador `"/"` que mudaria a classificação `ALTERACAO_NORMATIVA` atribuída a R2 e R7 — ou que resolveria a tensão de hardcoding registrada na seção 3. Nenhum outro artefato fora do manifesto foi identificado como estritamente necessário.

---

## 6. Leituras adicionais estritamente necessárias

- `docs/contratos/contrato_chip.md` — necessário exclusivamente para confirmar ou refutar, com certeza documental completa, a classificação `ALTERACAO_NORMATIVA` de R2 e R7 e a tensão de hardcoding do separador `"/"` (seção 3 deste relatório). Não lido nesta etapa por não constar no manifesto fechado.

Nenhuma outra leitura adicional foi identificada como necessária dentro do escopo desta tarefa.

---

## 7. Nota factual — status YAML da ADR-0046

O bloco YAML de `docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md` (linha 6) registra `status: proposta`. Este relatório apenas constata o fato, conforme instruído — não investiga o ciclo de vida de promoção da ADR, não lê outros relatórios para explicá-lo e não usa essa constatação para alterar nenhuma das classificações das seções 2–4, uma vez que o texto normativo da própria ADR-0046 não condiciona nenhuma de suas seções a esse campo de status.

---

## 8. Conclusão factual

A leitura controlada do manifesto fechado permite afirmar, sem prescrever o próximo estágio do ciclo:

- Nenhuma prescrição de H-0070 contraria a autoridade vigente (ADR-0046/contratos/nomenclatura); parte delas é explicitamente autorizada (H70-R02, H70-R03, H70-R05, H70-R06, H70-R10) e parte é compatível mas não explicitada, amparada pela cláusula de delegação de detalhes da ADR-0046 ou pela exclusão de mecânica de renderização do `contrato_console.md`.
- Das regras externas R1–R9, duas (R1, R5) já eram normativamente exigidas antes desta manifestação do usuário; cinco (R3, R4, R6, R8, R9) são compatíveis mas ainda não explicitadas; duas (R2, R7) mudam ou contradizem decisão já fechada (H-0070 §8 e §10/§11, respectivamente) e introduzem convenção de composição sem base no schema de estilo — exigindo fechamento normativo antes de qualquer implementação.
- Dos três achados de validação manual final, MF-ITEM0010-002 e MF-ITEM0010-003 têm núcleo claramente identificável em regra já vigente e violada pela implementação atual (`contrato_estilo.md` R-1/R-2 para o primeiro; `docs/nomenclatura/32_CONSOLE.md` §4.4 para o segundo); MF-ITEM0010-001 combina defeito de implementação com uma extensão normativa nova ainda não fechada (aplicação universal de `"/"` a presets delimitados).
- Existe uma tensão interpretativa real e não resolvida — se o caractere separador `"/"` da composição multitecla constitui "aparência hardcoded" proibida por `contrato_estilo.md` R-2 ou "glue estrutural de layout" já aceito pelo contrato — que este relatório não tem mandato para decidir.
- Um único artefato fora do manifesto (`docs/contratos/contrato_chip.md`) permaneceria útil para eliminar a incerteza residual sobre R2/R7 e sobre essa tensão de hardcoding.

Este relatório não determina PATCH_ADR, nova ADR, PATCH_HANDOFF, PATCH_IMPLEMENTACAO ou qualquer outra ação subsequente. Essas decisões pertencem ao Gerente Web.
