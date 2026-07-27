---
name: relatorio-qa-h-0040-handoff
description: Relatorio de QA independente do handoff H-0040
metadata:
  type: relatorio
  etapa: QA_HANDOFF
  handoff: H-0040
  status: H2_HANDOFF_PATCH_REQUIRED
---

# Relatorio de QA do Handoff H-0040

## 1. Identificacao

```yaml
handoff: H-0040
titulo: Implementar navegacao simples e selecao unica em console de nivel unico
objeto_auditado: docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
data: 2026-07-25
etapa: QA_HANDOFF
classificacao: H2_HANDOFF_PATCH_REQUIRED
```

## 2. Objeto e escopo

Auditoria independente do handoff H-0040, sem alterar o handoff, sem implementar
codigo, sem aplicar correcoes e sem executar operacoes Git de escrita.

Unico arquivo criado nesta etapa:

```text
docs/relatorios/RELATORIO_QA_H-0040_HANDOFF.md
```

## 3. Estado documental

```yaml
handoff:
  numero: H-0040
  status_confirmado: HANDOFF_CRIADO_AGUARDANDO_QA
  ultima_linha_confirmada: HANDOFF_CRIADO_AGUARDANDO_QA
  secoes_principais_do_handoff: 38
  cabecalhos_em_blocos_de_codigo: exemplos_ou_templates

origem:
  item_de_backlog: ITEM-0002
  adr: ADR-0031

base_documental:
  qa_semantico_da_adr: ADR_QA_APPROVED_WITH_NOTES
  aplicacao_inicial: ADR_APPLICATION_QA_REJECTED
  patch_da_aplicacao: CONCLUIDO
  qa_pos_patch: ADR_APPLICATION_POST_PATCH_QA_APPROVED_WITH_NOTES

implementacao:
  iniciada: false
```

A aplicacao inicial rejeitada foi tratada como historico. A autoridade vigente
e formada pela ADR-0031 aceita, pela aplicacao documental patcheada e pelo QA
pos-patch aprovado com notas.

## 4. Estado Git acumulado

Inventario inicial executado:

```yaml
estado_git_inicial:
  arquivos_staged: []
  arquivos_unstaged:
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
  arquivos_staged_e_unstaged: []
  arquivos_nao_rastreados:
    - __pycache__/conftest.cpython-314-pytest-9.0.3.pyc
    - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
    - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md
    - docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0031.md
    - tela/__pycache__/__init__.cpython-314.pyc
    - tela/__pycache__/teste_distribuicao_matricial.cpython-314-pytest-9.0.3.pyc
```

O estado acumulado nao bloqueia este QA.

## 5. Gate

```yaml
relatorio_qa_h0040_preexistente: false
handoff_h0040_presente: true
ultima_linha_handoff: HANDOFF_CRIADO_AGUARDANDO_QA
conflito_git_nao_resolvido_impedindo_leitura: false
autoridade_documental_indispensavel_ausente: false
resultado_gate: PASSOU
```

## 6. Autoridades consultadas

Foram consultadas as autoridades obrigatorias:

- `docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md`
- `docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md`
- `docs/relatorios/RELATORIO_QA_ADR-0031.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md`
- `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md`
- `docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0031.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0031.md`
- `docs/contratos/contrato_console.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_chip.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_json_console.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/nomenclatura/32_CONSOLE.md`
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`
- `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`
- `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md`

Tambem foram lidos seletivamente os arquivos de codigo, testes e configuracoes
citados nominalmente pelo H-0040.

## 7. Metodo

1. Confirmacao dos gates de arquivo e marcador.
2. Inventario Git sem operacoes de escrita.
3. Leitura das autoridades documentais obrigatorias.
4. Leitura seletiva dos pontos tecnicos citados nominalmente pelo handoff.
5. Reconciliacao de escopo, arquivos, testes, demonstracao e template futuro.
6. Classificacao dos achados conforme taxonomia H1/H2/H3/H4.

## 8. Origem semantica

O H-0040 deriva materialmente de ITEM-0002, ADR-0031 D1-D15, contratos e
nomenclatura propagados. Preserva o foco entre consoles focalizaveis, navegacao
de nivel unico, selecao unica, indicador, chips, redimensionamento e modos.

Nao foi encontrada reincorporacao normativa da aplicacao inicial rejeitada.
Entretanto, ha um desvio de fronteira: a demonstracao permite que Enter seja
ignorado ou exiba ID/texto do item selecionado. Como a ADR-0031 declara que
execucao de acao por Enter nao integra o ciclo, o handoff deve proibir
nominalmente Enter executando acao e remover qualquer comportamento demonstrativo
ambiguous que possa ser implementado como resposta nova de Enter.

## 9. Escopo positivo

```yaml
escopo_positivo:
  lista_ordenada_de_consoles_focalizaveis: COBERTO
  console_atualmente_focado: COBERTO
  item_logico_corrente: COBERTO
  tab_circular: COBERTO
  shift_tab_circular: COBERTO_COM_RISCO
  entrada_no_item_logico_0: COBERTO
  navegacao_horizontal_por_linha: COBERTO
  navegacao_vertical_por_coluna: COBERTO
  toroide_independente_por_eixo: COBERTO
  exclusao_de_celulas_vazias: COBERTO
  selecao_unica_item_sob_cursor: COBERTO
  indicador_apenas_no_console_focado: COBERTO
  coluna_indicadora_estavel: COBERTO
  indicador_do_estilo_global: COBERTO
  chip_alternar_contextual: COBERTO
  chip_navegar_contextual: COBERTO
  preservacao_no_redimensionamento: COBERTO_COM_RISCO
  preservacao_na_troca_de_modo: COBERTO_COM_RISCO
  preservacao_da_paginacao_como_ciclo_separado: COBERTO
```

Riscos: D10 nao esta suficientemente materializado nos AT automatizados, e
Shift+Tab depende de compatibilidade tecnica que o handoff deixa para verificacao.

## 10. Escopo negativo

O handoff proibe parte substancial do escopo negativo: paginacao interativa,
troca de pagina por setas, registro/dispatcher de acoes, abertura e retorno de
telas, selecao multipla, toggle por espaco, indicador de inclusao, navegacao
multinivel, expansao/recolhimento e conteudo composto.

Ausencias ou formulacoes insuficientes:

```yaml
escopo_negativo_insuficiente:
  Enter_executando_acao: nao_proibido_nominalmente
  alteracao_funcional_de_dashboard: nao_proibido_nominalmente
  alteracao_funcional_de_lancador: nao_proibido_nominalmente
  tela_de_estilo: apenas_estilo_por_tela_sem_nomear_tela_de_estilo
  cores_de_alerta_e_inativo: nao_proibido_nominalmente
  tiling: nao_proibido_nominalmente
  cabecalho_estreito: nao_proibido_nominalmente
```

Os deferimentos ITEM-0003 a ITEM-0009 aparecem preservados.

## 11. Inventario tecnico

```yaml
inventario_tecnico:
  politica_navegacao:
    arquivo: tela/loader.py
    simbolo: _validar_valores_envelope_pre_adr_0028
    resultado: CONFIRMADO
  grupos:
    arquivo: tela/modelo.py
    simbolo: _construir_elementos_recursivo
    resultado: CONFIRMADO
  itens:
    arquivo: tela/modelo.py
    simbolo: ElementoCorpo._campos_inertes
    resultado: CONFIRMADO
  distribuicao_visual:
    arquivo: tela/distribuicao_matricial.py
    simbolo: calcular_distribuicao
    resultado: CONFIRMADO
  teclado:
    arquivo: demo/demo.py
    simbolo: processar_comando; _ler_tecla_sessao
    resultado: CONFIRMADO
  estado_runtime:
    arquivo: demo/demo.py
    simbolo: criar_estado_inicial
    resultado: CONFIRMADO
  chips:
    arquivo: tela/renderizador.py
    simbolo: renderizar_tela
    resultado: CONFIRMADO_COM_LACUNA_ATUAL
  console:
    arquivo: tela/renderizador.py
    simbolo: _linhas_console
    resultado: CONFIRMADO_COM_LACUNA_ATUAL
  estilo:
    arquivo: tela/loader.py
    simbolo: EstiloResolvido.selecionado_simbolo; selecionado_off
    resultado: CONFIRMADO
  redimensionamento:
    arquivo: demo/demo.py
    simbolo: _obter_dimensoes_apos_sigwinch; renderizar_estado
    resultado: CONFIRMADO
  modos:
    arquivo: demo/demo.py
    simbolo: _verboso_efetivo; processar_comando
    resultado: CONFIRMADO
  paginacao_atual:
    arquivo: contratos e renderer existentes
    resultado: FRONTEIRA_DOCUMENTADA
  testes:
    arquivos: tela/teste_renderizador.py; demo/teste_demo.py; tela/teste_loader.py
    resultado: CONFIRMADO
  demos:
    arquivos: demo/demo.py; config/telas/demo/*.json
    resultado: CONFIRMADO
  ponto_de_entrada:
    arquivo: demo/demo.py
    resultado: CONFIRMADO
```

## 12. Arquivos modificaveis

| Arquivo | Existe | Responsabilidade atual confirmada | Alteracao autorizada suficiente | Alteracao autorizada excessiva | D1-D15 cobertas | Invariantes preservadas |
|---|---:|---|---|---|---|---|
| `demo/demo.py` | sim | Estado, teclado, demo TTY, redimensionamento, modo | Parcial | Nao, se Enter nao for implementado | D5, D6, D10 | Precisa preservar comandos antigos |
| `tela/renderizador.py` | sim | Renderizacao, chips, console, consumo de estilo | Parcial | Nao, se limitada a indicador/chips | D11, D12, D14 | Precisa preservar assinatura anterior com parametros opcionais |

Dois arquivos modificados mais o novo `tela/navegacao.py` parecem tecnicamente
possiveis, mas a suficiencia fica condicionada ao patch das lacunas de teste,
demo, template e regra de excecao.

## 13. Arquivos novos

| Arquivo | Caminho nominal | Necessidade demonstrada | Convencao | Duplica existente | Nova semantica | Escopo |
|---|---|---|---|---|---|---|
| `tela/navegacao.py` | producao | sim | compativel | nao | implementa ADR-0031 | autorizado |
| `demo/demo_navegacao.py` | demo | sim | compativel | nao | demo TTY especifico | autorizado |
| `demo/teste_demo_navegacao.py` | teste | sim | compativel | nao | testes de integracao | autorizado |
| `tela/teste_navegacao.py` | teste | sim | compativel | nao | testes unitarios | autorizado |
| `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md` | relatorio | sim | compativel | nao | evidencia futura | autorizado |
| 8 JSONs `config/telas/demo/h0040_*.json` | demo | sim, mas incompleta | compativel | nao | cenarios declarativos | autorizado_com_patch |

Defeito: a secao 25 diz "criar exatamente" apenas cinco arquivos, enquanto a
secao 27 acrescenta oito JSONs. A reconciliacao numerica aparece so depois, na
secao 32/37. O handoff deve listar os 13 em uma classificacao unica ou retirar
a formula "sem adicionais" da lista parcial.

## 14. Arquivos preservados

O handoff preserva nominalmente ADR, contratos, nomenclatura, backlog, indice,
`config/estilo.json`, atividades deferidas e relatorios historicos. Nao foi
encontrado arquivo simultaneamente listado como modificar e criar.

Lacuna: nao ha secao propria de arquivos preservados com a completude exigida
pelo QA, e o template de relatorio futuro tambem nao exige lista de preservados.

## 15. Arquivos condicionais

```yaml
arquivos_condicionais_declarados: []
resultado: SEM_CONDICIONAIS_VAGOS
```

Nao ha gatilhos vagos do tipo "se necessario" em lista condicional. O problema
nao e condicionalidade, mas ausencia de regra de excecao para arquivo fora da
lista.

## 16. Regra de excecao

```yaml
lista_fechada: parcialmente_confirmada
regra_de_parada_antes_de_alterar_fora_da_lista: ausente
informar_caminho_necessidade_risco_limite_semantica: ausente
autoriza_arquivos_equivalentes: nao_encontrado
autoriza_diretorios_inteiros: nao_encontrado
autoriza_outros_testes_necessarios: nao_encontrado
autoriza_ajustes_relacionados: nao_encontrado
resultado: EXIGE_PATCH_DO_HANDOFF
```

## 17. Matriz D1-D15

| Decisao | Requisito no H-0040 | Arquivos relacionados | Testes relacionados | Resultado |
|---|---|---|---|---|
| D1 escopo | Nivel unico, selecao unica, chips, indicador | `tela/navegacao.py`, `demo/demo.py`, `tela/renderizador.py` | AT/PN gerais | COBERTA_COM_RISCO |
| D2 elegibilidade | `politica_navegacao` + item navegavel | `tela/navegacao.py`, `modelo.py` | AT-0001..0006, PN-0002..0005 | COBERTA |
| D3 lista linear | DFS, grupos excluidos | `tela/navegacao.py` | AT-0006..0008 | COBERTA |
| D4 ordem espacial | horizontal, vertical, matriz row-major | `tela/navegacao.py` | AT-0009..0010 | COBERTA |
| D5 Tab/Shift+Tab | circular direto/inverso | `demo/demo.py`, `tela/navegacao.py` | AT-0011..0016 | COBERTA_COM_RISCO |
| D6 entrada item 0 | sem restaurar cursor anterior | `demo/demo.py`, `tela/navegacao.py` | AT-0015..0016, PN-0009 | COBERTA |
| D7 ordem logica | row-major por grade visual | `tela/navegacao.py`, `distribuicao_matricial.py` | AT-0017..0021 | COBERTA_COM_RISCO |
| D8 toroide por eixo | linha/coluna independentes, sem vazias | `tela/navegacao.py` | AT-0022..0027, PN-0006..0008 | COBERTA_COM_RISCO |
| D9 degenerados | um item, uma linha, uma coluna | `tela/navegacao.py` | AT-0028..0031 | COBERTA |
| D10 redimensionamento e modo | preservar item logico | `demo/demo.py`, `tela/navegacao.py` | PN-0017; VM-11/12 | COBERTA_COM_RISCO |
| D11 console focado | indicador so no focado | `tela/renderizador.py` | AT-0032..0033, PN-0013 | COBERTA |
| D12 coluna indicadora | estilo global e continuacoes off | `tela/renderizador.py`, `loader.py` | AT-0034..0036, PN-0015 | COBERTA_COM_RISCO |
| D13 selecao unica | item sob cursor, sem toggle | `tela/navegacao.py`, `demo/demo.py` | AT-0037, PN-0012 | COBERTA |
| D14 chips | `[⇆]` e `[✥]` contextuais | `tela/renderizador.py` | AT-0038..0040, PN-0010/0014 | COBERTA_COM_RISCO |
| D15 pagina e deferimentos | setas nao mudam pagina; ITEM-0003 deferido | `tela/navegacao.py` | PN-0011 | COBERTA_COM_RISCO |

## 18. Criterios AT-0001 a AT-0040

```yaml
AT:
  declarados: 40
  identificadores_unicos: 40
  lacunas: []
  duplicatas_de_id: []
```

| AT | Decisao | Superficie observavel | Teste nominal | Exequivel | Achado |
|---|---|---|---|---|---|
| AT-0001..0010 | D2-D4 | lista de foco | `tela/teste_navegacao.py` | sim | ok |
| AT-0011..0016 | D5-D6 | foco/cursor | `tela/teste_navegacao.py`, `demo/teste_demo_navegacao.py` | sim | Shift+Tab exige compatibilidade |
| AT-0017..0021 | D7 | grade | `tela/teste_navegacao.py` | sim | precisa amarrar grade ao renderer |
| AT-0022..0031 | D8-D9 | movimento | `tela/teste_navegacao.py` | sim | ok parcial |
| AT-0032..0037 | D11-D13 | render/indicador/selecao | `tela/teste_navegacao.py`, `demo/teste_demo_navegacao.py` | sim | coluna estavel nao tem AT dedicado |
| AT-0038..0040 | D14 | chips | `demo/teste_demo_navegacao.py` | sim | falta `[✥]` presente com >1 item |

Achado: os AT sao numericamente completos, mas deixam D10 praticamente sem
criterio positivo automatizado; falta teste positivo de preservacao em mudanca
de modo e redimensionamento. Tambem falta criterio positivo para `[✥]` presente
quando o console focado tem mais de um item navegavel.

## 19. Provas PN-0001 a PN-0017

```yaml
PN:
  declarados: 17
  identificadores_unicos: 17
  lacunas: []
  duplicatas_de_id: []
```

| PN | Proibicao | Mecanismo de prova | Falha realmente detectavel | Resultado |
|---|---|---|---|---|
| PN-0001..0005 | grupo/lancador/dashboard/console invalido fora do foco | lista de foco | sim | COBERTA |
| PN-0006..0008 | eixo e celula vazia | `mover_cursor` | parcial | COBERTA_COM_RISCO |
| PN-0009 | sem restaurar cursor | `avancar_foco` | sim | COBERTA |
| PN-0010 | `[✥]` sem inativo | renderer | sim | COBERTA |
| PN-0011 | setas nao mudam pagina | assinatura sem `pagina_atual` | fraca | COBERTA_COM_RISCO |
| PN-0012 | espaco nao alterna selecao | `processar_comando` | sim | COBERTA |
| PN-0013 | indicador fora do focado | renderer | sim | COBERTA |
| PN-0014 | `[✥]` ausente sem foco | renderer | sim | COBERTA |
| PN-0015 | indicador nao hardcoded | estilo `X` | sim | COBERTA |
| PN-0016 | sem diagonal | `mover_cursor` | sim | COBERTA |
| PN-0017 | redimensionamento nao reinicia item | recalculo de grade | sim | COBERTA |

Lacunas materiais: falta prova negativa explicita para `[✥]` com um item, celula
vazia participando do toroide sem receber cursor, indicador em linha de
continuacao, modo reiniciando item, redimensionamento perdendo identidade quando
a grade muda, e Enter executando acao. Algumas proibicoes aparecem em AT ou VM,
mas nao como PN detectavel.

## 20. Reconciliacao numerica

```yaml
AT:
  declarados: 40
  identificadores_unicos: 40

PN:
  declarados: 17
  identificadores_unicos: 17

total:
  declarado: 57
  calculado: 57

arquivos:
  novos_declarados: 13
  calculado_por_secao_32: 13
  contradicao_secao_25: "diz exatamente 5 sem adicionais"
  modificados_declarados: 2
  calculado: 2
```

## 21. Suite canonica

O handoff nao registra o comando canonico exigido:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

Em vez disso, usa `pytest`, `pytest -q` e resultado esperado `423 passed`.

```yaml
contagem_423:
  natureza_correta: COLETA_NO_MOMENTO_DA_AUTORIA
  garantia_da_contagem_pos_implementacao: nao
  comportamento_do_handoff: trata_423_como_gate_de_entrada_e_resultado_esperado
  resultado: EXIGE_PATCH_DO_HANDOFF
```

## 22. Demonstracao

```yaml
arquivo_demo: demo/demo_navegacao.py
ponto_de_entrada_real: citado_mas_comando_nao_fechado
cenario: "ex.: h0040_nav_dois_consoles.json"
dados_utilizados: JSONs_h0040
elementos_visuais_esperados: parcialmente_descritos
```

Cobertura insuficiente:

- nao ha cenario nominal de matriz incompleta;
- nao ha cenario nominal de item multilinha;
- o comando de execucao nao esta fechado;
- "carregar um dos cenarios" e aberto demais para demonstracao obrigatoria;
- a demonstracao permite Enter ignorado ou exibindo ID/texto, embora Enter e
  acoes estejam fora do ciclo.

## 23. Validacao manual

O roteiro VM-01 a VM-15 cobre varios comportamentos essenciais, mas precisa de
patch:

```yaml
exclusiva_do_usuario: nao_declarado
nao_executada_na_autoria: nao_declarado
linguagem_nao_tecnica: insuficiente
explica_console_focado_e_item_apontado: parcial
informa_tela_e_tecla: parcial
informa_resultado_visual: parcial
nao_exige_dimensoes_fixas: parcial
inclui_maximizar_restaurar_reduzir_redimensionar_livremente: nao
inclui_registro_posterior_do_resultado: nao
```

## 24. Relatorio de implementacao

O H-0040 exige um relatorio nominal, mas o template nao segue a convencao
solicitada para este QA. Divergencias principais:

```yaml
arquivo_nominal: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
encerramento_exigido_pelo_QA: IMPLEMENTATION_COMPLETED_AWAITING_QA
encerramento_no_handoff: IMPLEMENTACAO_CONCLUIDA_AGUARDANDO_QA
campos_ausentes:
  - arquivos_preservados
  - excecoes_solicitadas
  - decisoes_implementadas
  - AT
  - PN
  - suite_canonica
  - demonstracao
  - validacao_manual_executada: nao
  - operacoes_git_de_escrita_executadas: []
  - commit_executado: nao
  - bloqueios
```

O template nao aprova a propria implementacao, mas e insuficiente para QA futuro.

## 25. Pontos NC-001 a NC-006

| Ponto | Evidencia | Natureza | Bloqueia implementacao | Tratamento correto |
|---|---|---|---|---|
| NC-001 | `_ler_tecla_sessao` retorna sequencia completa apos Esc; Tab retorna `\t`; Shift+Tab pode chegar como `\x1b[Z` ou `\x1b\t` | compatibilidade tecnica | nao | VERIFICACAO_TECNICA_NAO_BLOQUEANTE, mas testes devem cobrir ambas |
| NC-002 | D23 existe em ADR-0028/nomenclatura 44; `_campos_inertes["itens"]` e real; consoles sem itens devem ser nao focalizaveis | integracao com envelope | nao | VERIFICACAO_TECNICA_NAO_BLOQUEANTE |
| NC-003 | `grade_de_itens()` ainda nao existe; renderer usa `calcular_distribuicao`; H-0040 manda usar mesmo algoritmo | consistencia logica/visual | nao, se patchar teste | EXIGE_PATCH_DO_HANDOFF para amarrar teste de equivalencia |
| NC-004 | `regra_existencia` existe nos contratos; JSONs atuais nao tem `[⇆]`/`[✥]`; novos JSONs dependem do campo | schema existente | nao | VERIFICACAO_TECNICA_NAO_BLOQUEANTE |
| NC-005 | novos campos `foco_console` e `cursores` sao runtime; `demo/teste_demo.py` nao compara dict completo de `criar_estado_inicial`, mas ha muitos estados manuais | regressao tecnica | nao | VERIFICACAO_TECNICA_NAO_BLOQUEANTE |
| NC-006 | largura determina distribuicao visual; navegacao deve usar exibicao atual sem redefinir geometria | risco logico/visual | nao, se delimitado | EXIGE_PATCH_DO_HANDOFF para explicitar fonte de largura/grade renderizada |

Nenhum NC exige nova decisao de usuario ou alteracao de ADR/contrato. Dois
pontos exigem patch de delimitacao tecnica no handoff.

## 26. Riscos

O H-0040 identifica a maioria dos riscos esperados, mas associa alguns apenas a
observacao ou VM. Riscos que precisam de melhor amarracao a AT/PN, preservacao
ou regra de excecao:

- divergencia entre grade logica e visual;
- Shift+Tab nao portatil;
- alteracao involuntaria de paginacao;
- novos campos persistidos por engano;
- excesso/contradicao de arquivos novos;
- mistura entre nivel unico e multinivel;
- modo reiniciando item logico.

## 27. Ausencia de decisao inventada

Nao ha decisao arquitetural nova que exija H3. A criacao de `tela/navegacao.py`
e escolha de handoff, nao da ADR, mas e aceitavel como decisao tecnica de
implementacao. As incertezas restantes sao corrigiveis por patch do handoff:

- protocolo de excecao para arquivos fora da lista;
- comando canonico da suite;
- template de relatorio futuro;
- PN/AT faltantes;
- demonstracao fechada;
- regra sobre Enter.

## 28. Achados

```yaml
achado:
  id: QAH40-001
  severidade: MAIOR
  categoria: [ARQUIVO, NUMERACAO]
  secao_do_handoff: "25, 27, 32, 37"
  autoridade: "Pedido QA §§11-12, 19"
  evidencia_material: "§25 diz criar exatamente 5 arquivos sem adicionais; §27 e §32 exigem mais 8 JSONs; §37 declara 13 novos."
  comportamento_encontrado: "Lista parcial marcada como exata."
  comportamento_esperado: "Lista fechada unica ou classificacao sem contradicao dos 13 arquivos novos."
  correcao_necessaria: "Reformular arquivos novos para declarar 13 de forma unica e inequívoca."
```

```yaml
achado:
  id: QAH40-002
  severidade: MAIOR
  categoria: [TESTE]
  secao_do_handoff: "20, 30"
  autoridade: "Pedido QA §20"
  evidencia_material: "Handoff usa pytest, pytest -q e 423 passed como gate."
  comportamento_encontrado: "Nao registra PYTHONDONTWRITEBYTECODE=1 python -m pytest como suite canonica e trata 423 como expectativa rigida."
  comportamento_esperado: "Comando canonico exato; 423 como coleta no momento da autoria, sem garantir contagem pos-implementacao."
  correcao_necessaria: "Substituir o gate de testes e explicitar crescimento permitido da suite."
```

```yaml
achado:
  id: QAH40-003
  severidade: MAIOR
  categoria: [RELATORIO_FUTURO]
  secao_do_handoff: "23"
  autoridade: "Pedido QA §23"
  evidencia_material: "Template usa IMPLEMENTACAO_CONCLUIDA_AGUARDANDO_QA e omite campos obrigatorios."
  comportamento_encontrado: "Relatorio futuro insuficiente para QA da implementacao."
  comportamento_esperado: "Template com arquivos_alterados/criados/preservados, excecoes, decisoes, AT, PN, suite, demonstracao, validacao_manual_executada: nao, operacoes Git, commit, bloqueios e IMPLEMENTATION_COMPLETED_AWAITING_QA."
  correcao_necessaria: "Atualizar template de relatorio de implementacao."
```

```yaml
achado:
  id: QAH40-004
  severidade: MAIOR
  categoria: [PROVA_NEGATIVA, CRITERIO_AT]
  secao_do_handoff: "18, 19"
  autoridade: "Pedido QA §§17-18; ADR-0031 D10-D15"
  evidencia_material: "AT nao cobre positivamente D10; PN nao cobre Enter, indicador em continuacao, modo reiniciando item, [✥] com um item e celula vazia participando do toroide."
  comportamento_encontrado: "Conjunto numericamente completo, mas materialmente incompleto."
  comportamento_esperado: "57 criterios/provas detectaveis cobrindo todos os comportamentos minimos exigidos."
  correcao_necessaria: "Revisar AT/PN mantendo numeracao e cobrindo lacunas."
```

```yaml
achado:
  id: QAH40-005
  severidade: MAIOR
  categoria: [DEMONSTRACAO, ESCOPO]
  secao_do_handoff: "21, 27"
  autoridade: "Pedido QA §§9, 21"
  evidencia_material: "Demo carrega 'um dos cenarios'; nao ha cenario nominal de matriz incompleta nem item multilinha; Enter pode exibir ID/texto."
  comportamento_encontrado: "Demonstracao aberta e com fronteira ambigua para Enter."
  comportamento_esperado: "Demo nominal com comando, dados e cobertura completa; sem dependencia ou comportamento novo de Enter."
  correcao_necessaria: "Fechar roteiro/comando/cenarios e remover permissao ambigua de Enter."
```

```yaml
achado:
  id: QAH40-006
  severidade: MENOR
  categoria: [VALIDACAO_MANUAL]
  secao_do_handoff: "22"
  autoridade: "Pedido QA §22"
  evidencia_material: "Roteiro nao declara exclusividade do usuario, nao executado na autoria, registro posterior; nao inclui maximizar/restaurar/reduzir/redimensionar livremente."
  comportamento_encontrado: "Roteiro util, mas incompleto e tecnico."
  comportamento_esperado: "Roteiro manual futuro em linguagem nao tecnica, com registro posterior e redimensionamentos exigidos."
  correcao_necessaria: "Reformular validacao manual."
```

```yaml
achado:
  id: QAH40-007
  severidade: MAIOR
  categoria: [ARQUIVO, EXEQUIBILIDADE]
  secao_do_handoff: "25, 26, 32"
  autoridade: "Pedido QA §15"
  evidencia_material: "Handoff proibe adicionais, mas nao instrui parar antes de alterar arquivo fora da lista nem informar caminho, necessidade, risco, limite e nova semantica."
  comportamento_encontrado: "Lista fechada sem protocolo de excecao."
  comportamento_esperado: "Regra de excecao nominal e operacional."
  correcao_necessaria: "Adicionar protocolo de parada e solicitacao de excecao."
```

```yaml
achado:
  id: QAH40-008
  severidade: NOTA
  categoria: [NAO_CONFIRMADO]
  secao_do_handoff: "24"
  autoridade: "ADR-0031; codigo atual"
  evidencia_material: "NC-001..NC-006 sao verificacoes tecnicas reais; D23 existe como decisao da ADR-0028."
  comportamento_encontrado: "Pontos NC em geral nao bloqueantes."
  comportamento_esperado: "Manter como verificacoes tecnicas, com testes/limites reforcados para NC-003 e NC-006."
  correcao_necessaria: "Sem nova ADR; patch de delimitacao tecnica no handoff."
```

## 29. Classificacao final

```yaml
classificacao: H2_HANDOFF_PATCH_REQUIRED
achados_bloqueantes: 0
achados_maiores: 6
achados_menores: 1
notas: 1
justificativa: >
  O escopo central da ADR-0031 e executavel e nao ha decisao arquitetural nova
  pendente. Entretanto, o handoff contem contradicoes e lacunas em arquivos,
  suite canonica, relatorio futuro, AT/PN, demonstracao, validacao manual e
  regra de excecao. Esses defeitos exigem patch antes da implementacao.
```

## 30. Arquivos alterados pelo QA

```yaml
arquivos_criados:
  - docs/relatorios/RELATORIO_QA_H-0040_HANDOFF.md
arquivos_modificados_preexistentes: []
operacoes_git_de_escrita_executadas: []
commit_executado: nao
```

## 31. Estado Git final

```yaml
estado_git_final:
  arquivos_staged: []
  arquivos_unstaged:
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
  arquivos_staged_e_unstaged: []
  arquivos_nao_rastreados:
    - __pycache__/conftest.cpython-314-pytest-9.0.3.pyc
    - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
    - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md
    - docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0031.md
    - tela/__pycache__/__init__.cpython-314.pyc
    - tela/__pycache__/teste_distribuicao_matricial.cpython-314-pytest-9.0.3.pyc
```

A unica alteracao produzida por este QA foi a criacao de
`docs/relatorios/RELATORIO_QA_H-0040_HANDOFF.md`; alteracoes acumuladas
preexistentes permanecem fora do escopo deste QA.

## 32. Encerramento

H2_HANDOFF_PATCH_REQUIRED
