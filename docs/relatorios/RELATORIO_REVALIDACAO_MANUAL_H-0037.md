---
status_literal: MANUAL_REVALIDATION_APPROVED
status_normalizado: REVALIDACAO_MANUAL_APROVADA
historia: H-0037
tipo: REVALIDACAO_MANUAL_TTY
data: "2026-07-20"
implementacao_aprovada_manualmente: true
proxima_categoria: PRONTO_PARA_FECHAMENTO_MANUAL
---

# RELATORIO DE REVALIDACAO MANUAL H-0037

## 1. Identificacao

| Campo | Valor |
|---|---|
| Handoff | H-0037 |
| Titulo | Apresentacao multinivel no console com politica de modo por tela (D23) |
| Tipo de relatorio | REVALIDACAO_MANUAL_TTY |
| Data da revalidacao | 2026-07-20 |
| Executado por | Usuario (TTY real) |
| Registrado por | Registrador documental |
| Branch | master |
| HEAD | f6982d08640af1762b8e0e8814b6e90c9421538e |
| Arquivo | `docs/relatorios/RELATORIO_REVALIDACAO_MANUAL_H-0037.md` |
| Relatorio de revalidacao anterior | `docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0037.md` |

---

## 2. Objetivo

Registrar documentalmente o resultado da revalidacao manual executada pelo
usuario em terminal real (TTY real) para o H-0037, apos o oitavo patch de
implementacao e o QA pos-patch 8 com resultado
`IMPLEMENTATION_APPROVED_WITH_NOTES`.

Este relatorio constitui o encerramento do ciclo de validacao manual aberto
pelo `RELATORIO_VALIDACAO_MANUAL_H-0037.md`, que concluiu com status
`MANUAL_VALIDATION_FAILED` e identificou tres achados bloqueantes.

---

## 3. Contexto Da Primeira Validacao

A primeira validacao manual, registrada em
`docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0037.md`, foi executada em
terminal real (TTY) em 2026-07-20 e concluiu com status
`MANUAL_VALIDATION_FAILED`.

Os tres achados bloqueantes identificados foram:

```yaml
H0037-MANUAL-001:
  titulo: Marcador de truncamento ausente
  cenarios: [h0037_console_nao_verboso, h0037_console_tabela_alternavel]
  observado: conteudo_truncado_sem_marcador_...
  estado_na_primeira_validacao: REPROVADO

H0037-MANUAL-002:
  titulo: Chip Esc nao ocupa a primeira posicao na barra de menus
  cenarios: [h0037_console_alternavel_tres_niveis, h0037_console_tabela_alternavel]
  observado: chip_Esc_nao_ocupa_a_primeira_posicao
  estado_na_primeira_validacao: REPROVADO

H0037-MANUAL-003:
  titulo: Tecla v minuscula nao reconhecida como alternancia
  cenarios: [h0037_console_alternavel_tres_niveis, h0037_console_tabela_alternavel]
  observado: somente_V_maiusculo_alternava
  estado_na_primeira_validacao: REPROVADO
```

O relatorio da primeira validacao manual permanece intacto como evidencia
historica de reprovacao. Ele nao foi editado, substituido nem alterado.

---

## 4. Patches E QA Posteriores A Primeira Validacao

Apos a reprovacao manual, foram aplicados patches e realizados ciclos de QA
independente. Os eventos relevantes para esta revalidacao sao:

### Patches 1 a 7 (consolidado no QA pos-patch 7)

O QA pos-patch 7 (`RELATORIO_QA_POS_PATCH_7_H-0037_IMPLEMENTACAO.md`)
concluiu com status `IMPLEMENTATION_PATCH_REQUIRED`. Os tres achados humanos
originais foram parcialmente resolvidos:

- `H0037-MANUAL-002` (Esc primeiro): resolvido.
- `H0037-MANUAL-003` (v minusculo): resolvido.
- `H0037-MANUAL-001` (marcador de truncamento): resolvido no modo nao verboso,
  mas nao conforme no modo verboso reduzido — containers da hierarquia caiam
  no ramo nao verboso e recebiam `_truncar_com_marcador`.

O QA pos-patch 7 registrou dois novos achados tecnicos:

```yaml
H0037-IMPL-QAPP7-001:
  descricao: corte silencioso da hierarquia verbosa em largura reduzida
  causa: containers caiam no ramo else com _truncar_com_marcador mesmo verboso=True
  severidade: MEDIA
  tipo: DEFEITO_IMPLEMENTACAO

H0037-IMPL-QAPP7-002:
  descricao: cobertura automatizada insuficiente para o fluxo verboso estreito
  severidade: MEDIA
  tipo: TESTE_INCORRETO
```

### Oitavo patch e QA pos-patch 8

O QA pos-patch 8 (`RELATORIO_QA_POS_PATCH_8_H-0037_IMPLEMENTACAO.md`)
concluiu com status `IMPLEMENTATION_APPROVED_WITH_NOTES`.

Os dois achados do QA 7 foram integralmente resolvidos:

- `H0037-IMPL-QAPP7-001`: o ramo verboso de `_linhas_apresentacao_hierarquia`
  passou a atender todo no (container e folha) usando `_quebrar_texto` com a
  largura restante real. Corte silencioso e reticencias artificiais ausentes
  no modo verboso.
- `H0037-IMPL-QAPP7-002`: o teste integrado
  `teste_h0037_qapp7_verb_sem_corte_silencioso` (VERB-01 a VERB-13) foi
  adicionado, cobrindo efetivamente os quatro cenarios canonicos, alternancia,
  tabela e conjuntos.

A suite canonica executada pelo QA 8:

```yaml
suite_independente:
  scripts: 10
  verificacoes: 2778
  falhas: 0
  codigo_saida: todos_zero
```

As duas notas do QA 8 (`H0037-IMPL-QAPP8-001` e `H0037-IMPL-QAPP8-002`)
foram classificadas como `OBSERVACAO_NAO_CORRETIVA` — sem exigencia de patch.

A proxima categoria declarada pelo QA 8 foi `REVALIDACAO_MANUAL_USUARIO`.

---

## 5. Ambiente Da Revalidacao

```yaml
ambiente:
  terminal_real: APROVADO
  raiz_correta: APROVADO
  branch: master
  head: f6982d08640af1762b8e0e8814b6e90c9421538e
```

A revalidacao foi executada em terminal real (TTY), na raiz correta do
projeto, apos o oitavo patch e o QA pos-patch 8.

---

## 6. Metodo

O usuario executou o roteiro de revalidacao manual utilizando os quatro
comandos de entrada diretos por cenario:

```bash
python demo/demo.py h0037_console_nao_verboso
python demo/demo.py h0037_console_verboso_dois_niveis
python demo/demo.py h0037_console_alternavel_tres_niveis
python demo/demo.py h0037_console_tabela_alternavel
```

O resultado foi fornecido pelo usuario e registrado abaixo sem
transformacoes, aplicando somente as normalizacoes canonicas:

```yaml
SIM: APROVADO
CORRETO: APROVADO
MOSTRA_TODO_O_TEXTO: APROVADO
SEM: APROVADO
SIM_COM_RECUPERACAO: APROVADO
```

O valor final fornecido pelo usuario foi `APROVADO`, normalizado para o
status literal canonico `MANUAL_REVALIDATION_APPROVED`.

---

## 7. Cenario 1 — Somente Nao Verboso

**Tela:** `h0037_console_nao_verboso`
**Politica:** `somente_nao_verboso`
**Modo inicial:** fixo (nao alternavel)

```yaml
cenario_1_nao_verboso:
  reticencias_quando_truncado: APROVADO
  sem_reticencias_quando_cabe: APROVADO
  linha_unica: APROVADO
  restauracao_ao_ampliar: APROVADO
  V_maiusculo_inerte: APROVADO
  v_minusculo_inerte: APROVADO
  observacao: nenhuma
```

**Resumo do cenario 1:**
- 6 itens aprovados, 0 itens reprovados.
- O marcador `...` foi exibido corretamente ao truncar (achado
  H0037-MANUAL-001 revalidado positivamente neste cenario).
- As teclas `V` maiusculo e `v` minusculo permaneceram inertes na tela de
  politica fixa (correto por contrato).

---

## 8. Cenario 2 — Somente Verboso Em Dois Niveis

**Tela:** `h0037_console_verboso_dois_niveis`
**Politica:** `somente_verboso`
**Modo inicial:** fixo (nao alternavel)

```yaml
cenario_2_verboso_dois_niveis:
  quebra_em_multiplas_linhas: APROVADO
  ausencia_de_corte_silencioso: APROVADO
  palavras_finais_preservadas: APROVADO
  evidencia_do_usuario: mostra_todo_o_texto
  ausencia_de_reticencias: APROVADO
  alinhamento_do_segundo_nivel: APROVADO
  recalculo_ao_ampliar: APROVADO
  V_maiusculo_inerte: APROVADO
  v_minusculo_inerte: APROVADO
  observacao: nenhuma
```

**Resumo do cenario 2:**
- 9 itens aprovados, 0 itens reprovados.
- O usuario confirmou que todo o texto e exibido (evidencia: `mostra_todo_o_texto`),
  normalizado como `APROVADO`.
- Ausencia de corte silencioso e de reticencias artificiais confirmada
  (achado H0037-IMPL-QAPP7-001 revalidado positivamente neste cenario).

---

## 9. Cenario 3 — Alternavel Em Tres Niveis

**Tela:** `h0037_console_alternavel_tres_niveis`
**Politica:** `alternavel`
**Modo inicial:** `nao_verboso`

```yaml
cenario_3_alternavel_tres_niveis:
  Esc_primeiro: APROVADO
  V_depois_de_Esc: APROVADO
  reticencias_no_nao_verboso: APROVADO
  v_minusculo_alterna: APROVADO
  V_maiusculo_alterna: APROVADO
  verboso_sem_corte: APROVADO
  verboso_sem_reticencias: APROVADO
  reversibilidade: APROVADO
  observacao: nenhuma
```

**Resumo do cenario 3:**
- 8 itens aprovados, 0 itens reprovados.
- Chip `[Esc]` na primeira posicao confirmado (achado H0037-MANUAL-002
  revalidado positivamente).
- Tecla `v` minuscula alternando corretamente (achado H0037-MANUAL-003
  revalidado positivamente).
- Modo verboso sem corte silencioso nem reticencias artificiais (achado
  H0037-IMPL-QAPP7-001 revalidado positivamente).

---

## 10. Cenario 4 — Tabela Alternavel

**Tela:** `h0037_console_tabela_alternavel`
**Politica:** `alternavel`
**Modo inicial:** `verboso`

```yaml
cenario_4_tabela_alternavel:
  Esc_primeiro: APROVADO
  V_depois_de_Esc: APROVADO
  verboso_multilinha: APROVADO
  verboso_sem_reticencias: APROVADO
  v_minusculo_alterna: APROVADO
  V_maiusculo_alterna: APROVADO
  nao_verboso_com_reticencias: APROVADO
  cabecalho_e_colunas_preservados: APROVADO
  reversibilidade: APROVADO
  observacao: nenhuma
```

**Resumo do cenario 4:**
- 9 itens aprovados, 0 itens reprovados.
- Chip `[Esc]` na primeira posicao confirmado (achado H0037-MANUAL-002
  revalidado positivamente).
- Tecla `v` minuscula alternando corretamente (achado H0037-MANUAL-003
  revalidado positivamente).
- Modo nao verboso com reticencias (`...`) exibidas ao truncar (achado
  H0037-MANUAL-001 revalidado positivamente neste cenario).

---

## 11. Comportamento Do Terminal

```yaml
terminal:
  teclas_sem_eco: APROVADO
  cursor_oculto: APROVADO
  redesenho: APROVADO
  cintilacao_problematica: ausente
  retorno_ao_terminal: APROVADO
  detalhe: retorno_com_recuperacao_correta
  observacao: nenhuma
```

Todos os 5 itens de comportamento do terminal aprovados sem ressalvas.
O usuario registrou retorno ao terminal com recuperacao correta, valor
`SIM_COM_RECUPERACAO` normalizado para `APROVADO`.

---

## 12. Paginacao Nao Aplicavel

```yaml
paginacao:
  resultado: NAO_APLICAVEL
  motivo: funcionalidade_nao_prevista_para_esta_rodada
  reaberta_na_revalidacao: false
```

A paginacao nao foi reaberta na revalidacao. Nao constitui achado e nao
gera reprovacao.

---

## 13. Correspondencia Com H0037-MANUAL-001

```yaml
H0037_MANUAL_001:
  titulo: Marcador de truncamento ausente
  estado_anterior: REPROVADO
  revalidacao:
    reticencias_na_hierarquia_nao_verbosa: APROVADO
    reticencias_na_tabela_nao_verbosa: APROVADO
    texto_que_cabe_sem_reticencias: APROVADO
  estado_final: RESOLVIDO
```

**Historico:** na primeira validacao, o conteudo era truncado sem exibir o
marcador `...` nos cenarios 1 e 4.

**Revalidacao:** o marcador `...` foi observado corretamente nos dois cenarios
(hierarquia nao verbosa e tabela nao verbosa). Textos que cabem na largura
disponivel nao exibem reticencias (conforme contrato). Achado encerrado como
RESOLVIDO.

---

## 14. Correspondencia Com H0037-MANUAL-002

```yaml
H0037_MANUAL_002:
  titulo: Chip Esc nao ocupa a primeira posicao na barra de menus
  estado_anterior: REPROVADO
  revalidacao:
    Esc_primeiro_no_cenario_3: APROVADO
    Esc_primeiro_no_cenario_4: APROVADO
    V_depois_de_Esc: APROVADO
  estado_final: RESOLVIDO
```

**Historico:** na primeira validacao, o chip `[Esc]` nao ocupava a primeira
posicao nos cenarios 3 e 4.

**Revalidacao:** o chip `[Esc]` foi observado na primeira posicao em ambos
os cenarios alternaveis, precedendo `[V] Verboso`. Achado encerrado como
RESOLVIDO.

---

## 15. Correspondencia Com H0037-MANUAL-003

```yaml
H0037_MANUAL_003:
  titulo: Tecla v minuscula nao reconhecida como alternancia
  estado_anterior: REPROVADO
  revalidacao:
    V_maiusculo: APROVADO
    v_minusculo: APROVADO
    telas_fixas_inertes: APROVADO
    reversibilidade: APROVADO
  estado_final: RESOLVIDO
```

**Historico:** na primeira validacao, somente `V` maiusculo produzia
alternancia; `v` minusculo era ignorado nos cenarios 3 e 4.

**Revalidacao:** tanto `V` maiusculo quanto `v` minusculo alternaram
corretamente nos cenarios 3 e 4. Ambos permaneceram inertes nos cenarios de
politica fixa (1 e 2). Reversibilidade confirmada. Achado encerrado como
RESOLVIDO.

---

## 16. Correspondencia Com H0037-IMPL-QAPP7-001

```yaml
H0037_IMPL_QAPP7_001:
  titulo: Corte silencioso da hierarquia verbosa em largura reduzida
  estado_anterior: DEFEITO_IMPLEMENTACAO (identificado no QA pos-patch 7)
  revalidacao:
    hierarquia_verbosa_quebra_em_linhas: APROVADO
    corte_silencioso: AUSENTE
    palavras_finais_preservadas: APROVADO
    reticencias_no_verboso: AUSENTES
    recalculo_ao_ampliar: APROVADO
  estado_final: RESOLVIDO
```

**Historico:** o QA pos-patch 7 identificou que containers da hierarquia
verbosa caiam no ramo `else` com `_truncar_com_marcador`, exibindo
reticencias artificiais e cortando conteudo silenciosamente em largura
reduzida.

**Revalidacao:** o usuario confirmou que o modo verboso exibe todo o texto,
com quebra em multiplas linhas, sem corte silencioso e sem reticencias. O
cenario 2 (hierarquia verbosa dois niveis) serviu como evidencia direta.
Achado encerrado como RESOLVIDO.

---

## 17. Criterios Aprovados

```yaml
criterios_obrigatorios:
  aprovados: todos
  reprovados: nenhum
  nao_executados: nenhum
  inconclusivos: nenhum
```

Itens aprovados na revalidacao (consolidado dos quatro cenarios e terminal):

**Cenario 1 (nao verboso fixo):**
- Reticencias exibidas quando truncado
- Ausencia de reticencias quando o texto cabe
- Linha unica por item
- Restauracao ao ampliar a janela
- `V` maiusculo inerte (politica fixa)
- `v` minusculo inerte (politica fixa)

**Cenario 2 (verboso fixo, dois niveis):**
- Quebra em multiplas linhas no modo verboso
- Ausencia de corte silencioso
- Palavras finais preservadas (todo o texto visivel)
- Ausencia de reticencias no modo verboso
- Alinhamento correto do segundo nivel
- Recalculo ao ampliar a janela
- `V` maiusculo inerte (politica fixa)
- `v` minusculo inerte (politica fixa)

**Cenario 3 (alternavel, tres niveis):**
- Chip `[Esc]` na primeira posicao
- Chip `[V]` apos `[Esc]`
- Reticencias no modo nao verboso
- `v` minusculo alterna corretamente
- `V` maiusculo alterna corretamente
- Modo verboso sem corte silencioso
- Modo verboso sem reticencias artificiais
- Reversibilidade de modo

**Cenario 4 (tabela alternavel):**
- Chip `[Esc]` na primeira posicao
- Chip `[V]` apos `[Esc]`
- Modo verboso com celulas multilinha
- Modo verboso sem reticencias artificiais
- `v` minusculo alterna corretamente
- `V` maiusculo alterna corretamente
- Modo nao verboso com reticencias quando truncado
- Cabecalho e colunas preservados
- Reversibilidade de modo

**Terminal:**
- Teclas sem eco
- Cursor oculto
- Redesenho apos redimensionamento
- Ausencia de cintilacao problematica
- Retorno correto ao terminal apos sair (com recuperacao correta)

---

## 18. Criterios Reprovados Ou Inconclusivos

```yaml
criterios_reprovados: nenhum
criterios_inconclusivos: nenhum
achados_funcionais_pendentes: nenhum
```

Nenhum criterio foi reprovado ou permaneceu inconclusivo.

---

## 19. Conclusao

A revalidacao manual executada pelo usuario em terminal real apos o oitavo
patch confirma que todos os achados bloqueantes da primeira validacao foram
corrigidos:

- `H0037-MANUAL-001` — marcador de truncamento: RESOLVIDO.
- `H0037-MANUAL-002` — ordem do chip Esc: RESOLVIDO.
- `H0037-MANUAL-003` — tecla v minuscula: RESOLVIDO.
- `H0037-IMPL-QAPP7-001` — corte silencioso no verboso estreito: RESOLVIDO.

Todos os criterios obrigatorios foram aprovados. Nenhum item foi reprovado,
nao executado ou inconclusivo. A revalidacao em TTY real foi concluida. A
implementacao esta aprovada manualmente.

---

## 20. Status Literal

```yaml
status_literal: MANUAL_REVALIDATION_APPROVED
```

---

## 21. Status Normalizado

```yaml
status_normalizado: REVALIDACAO_MANUAL_APROVADA
```

---

## 22. Proxima Categoria

```yaml
proxima_categoria: PRONTO_PARA_FECHAMENTO_MANUAL
implementacao_aprovada_manualmente: true
achados_bloqueantes_pendentes: nenhum
```

---

## 23. Estado Git Observado

```yaml
git:
  raiz: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
  branch: master
  head: f6982d08640af1762b8e0e8814b6e90c9421538e
  head_log: "f6982d0 docs: corrige whitespace do fechamento H-0036"
  stage: vazio
  diff_check: sem_erros
  commit_novo: nao_realizado
  push: nao_executado
```

Arquivos rastreados com modificacoes nao commitadas (worktree acumulada):

```text
config/telas/demo/demo.json
demo/demo.py
demo/teste_demo.py
demo/teste_demo_console.py
demo/teste_diagnostico.py
docs/NOMENCLATURA.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_tela_json.md
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
```

Arquivos nao rastreados acumulados na worktree incluem fixtures H-0037,
relatorios H-0037/ADR-0028, handoff H-0037, ADR-0028 e suites de teste.
A origem desses arquivos nao foi confirmada como pertencente exclusivamente
a este relatorio de revalidacao:

```yaml
arquivos_inesperados:
  origem: NAO_CONFIRMADA
```

(Fim do relatorio)
