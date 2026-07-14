# Levantamento de consistência e rastreabilidade — H-0022 / ADR-0016

## 1. Identificação e limite

```yaml
status_do_levantamento: LEVANTAMENTO_CONSISTENCIA_COMPLETO
data_da_coleta: 2026-07-11
papel: investigador_documental_neutro
decisao_do_usuario_considerada:
  adr_0016: APROVADA
  conflito_documental_anterior: CORRIGIDO_PELA_ADR_0016
  implementacao_atual: DECLARADA_FUNCIONAL_EM_TERMOS_GERAIS
  preservacoes: codigo_testes_handoff_e_relatorios_de_qa
  remocoes_autorizadas: nenhuma
efeito_da_decisao: o BLOCKED_USER_DECISION de RELATORIO_QA_ADR-0016_POS_AJUSTES.md e historico; a declaracao nao confirma individualmente os criterios manuais de TTY
escopo_da_escrita: somente este relatorio
```

Este documento levanta fatos; não aprova ADR, handoff, implementação ou fechamento e não executa tratamentos.

## 2. Estado Git e método

```text
branch: master
HEAD: 0b09fa6a99a6d0ed61e9488ecb7e78f16d37cfdf
log -1: 0b09fa6 fix: corrige preenchimento horizontal do orquestrador
```

Estado antes da criação deste relatório:

```text
 M docs/adr/INDICE_ADR.md
 M tela/demo.py
 M tela/teste_demo.py
?? docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
?? docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
?? docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md
?? docs/relatorios/IMP-0023-implementacao-h0022-tela-cheia-tty.md
?? docs/relatorios/RELATORIO_AUDITORIA_ADR-0016.md
?? docs/relatorios/RELATORIO_QA_ADR-0016_POS_AJUSTES.md
?? docs/relatorios/RELATORIO_QA_H-0022_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_H-0022_IMPLEMENTACAO.md
```

- `git diff --stat`: 3 arquivos, 683 inserções e 43 remoções (`INDICE_ADR.md`, `demo.py`, `teste_demo.py`).
- `git diff --name-only`: os mesmos três arquivos.
- `git diff --check`: código 0, sem saída.
- Stage: vazio; `git diff --cached --stat`, `--name-only` e `--check` sem saída.
- Stash: `stash@{0}: On master: pre-H-0022`; não foi aplicado nem alterado.
- O histórico alcançável não contém commit de H-0022/ADR-0016; todos os artefatos específicos continuam fora do HEAD.
- Foram usados conteúdo, SHA-256, contagem de linhas, Git, referências internas e stash. Datas de filesystem não foram usadas como prova de ordem.
- Para cada arquivo não rastreado foi observada sua criação integral por `git diff --no-index /dev/null <arquivo>`; a saída é equivalente ao conteúdo corrente e não é repetida aqui.

## 3. Inventário

### 3.1 Artefatos centrais

| caminho | tipo | Git | linhas | SHA-256 | status literal/data | ciclo e referências | papel aparente |
|---|---|---:|---:|---|---|---|---|
| `docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md` | ADR | não rastreado | 212 | `50b314e00322c6a28b376520761483527328f301da9ff741f709ef2662d579d4` | `proposta`; 2026-07-10 | ADR-0016; H-0009, H-0021, IMP-0022, índice e três contratos | norma aprovada pelo usuário, ainda não atualizada documentalmente |
| `docs/adr/INDICE_ADR.md` | índice | rastreado/modificado | 50 | `df8a54eb239aa9543a8861909eaee41b545c44d2b85773d1e5528a8624fa8b5c` | ADR-0016=`proposta`; 2026-07-10 | ADR-0016 | catálogo de ADRs |
| `docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md` | handoff | não rastreado | 236 | `ba37585352bdc16d91d1f883ebba85a9c97e85d813ce52ebd02b09de55f9f7fe` | `proposto`; 2026-07-10 | H-0022; ADR-0016, IMP-0022, `demo.py`, `teste_demo.py` | especificação corretiva atual |
| `docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md` | implementação | não rastreado | 231 | `9853679bee9a15e79e40e1b899437cdae003c47835ac1fd5e04ed715abd411cf` | `IMPLEMENTADO — PENDENTE_QA_MANUAL`; 2026-07-10 | rótulo H-0022 sem handoff; cita futuro H-0023 | relatório da tentativa pré-ADR |
| `docs/relatorios/IMP-0023-implementacao-h0022-tela-cheia-tty.md` | implementação | não rastreado | 205 | `1761b92433c6cb52693ea025a2503dd41af0c6791d32e5d2d1a08e65adfaabb1` | sem campo de status; 2026-07-10 | IMP-0023/H-0022; ADR, handoff, IMP-0022, stash | relatório da implementação pós-ADR, hoje desatualizado em contagem/versão |
| `docs/relatorios/RELATORIO_AUDITORIA_ADR-0016.md` | auditoria ADR | não rastreado | 488 | `93d26a5a6871662212acf74cc5fa8813758299ce5f3abad9eeda6146ec519851` | `APROVADO_COM_RESSALVAS`; 2026-07-10 | ADR-0016, iteração anterior substituída no próprio arquivo | auditoria de versão antiga da ADR |
| `docs/relatorios/RELATORIO_QA_ADR-0016_POS_AJUSTES.md` | QA ADR | não rastreado | 278 | `4cb2a9ccfcc5ed99b6af1906a34d532efcc9bda2392ddbb265aad9528189b8f2` | `BLOCKED_USER_DECISION`; 2026-07-11 | ADR-0016 e cadeia posterior | QA exato da ADR atual, anterior à decisão do usuário |
| `docs/relatorios/RELATORIO_QA_H-0022_HANDOFF.md` | QA handoff | não rastreado | 225 | `943aeffc277d6e2f8f4267b1504ca0aa99571fd9b8b89de52154fcd6ab4bc318` | `REPROVADO`; data não declarada | ADR-0016 e H-0022 de 216 linhas | QA de versão antiga do handoff |
| `docs/relatorios/RELATORIO_QA_H-0022_IMPLEMENTACAO.md` | QA implementação | não rastreado | 147 | `6628f934a927322209d7cfdac04bede34a69b22d5760317099dd92185e41b6fa` | `APROVADO_COM_RESSALVAS`; data não declarada | H-0022, IMP-0023, código/testes e stash | QA posterior de implementação com 172 testes, não da versão corrente comprovada |
| `tela/demo.py` | código | rastreado/modificado | 375 | `28567039619b9731501752fb0444264393c32c57876b9e7812acf0c2d1de1bef` | sem status/data | H-0008/H-0009/H-0010A/H-0022; ADR-0016 | implementação atual |
| `tela/teste_demo.py` | teste executável | rastreado/modificado | 1744 | `62494b9627f935bd7ab628dd35102424063ef64894578b58988e709fc87c22a6` | sem status/data | H-0008/H-0009/H-0010A/H-0022; ADR-0016 | testes atuais; 176 verificações |

### 3.2 Autoridades, precedentes e ocorrências contextuais

| caminho | linhas | SHA-256 | Git | relação |
|---|---:|---|---|---|
| `docs/contratos/contrato_tela_json.md` | 742 | `f3cc4f0e495df709c02b25c379ace66b795e4837ccb370311ea1db1ced979060` | rastreado | contrato que a ADR manda aplicar; ainda sem política TTY |
| `docs/contratos/contrato_console.md` | 492 | `989c03a6c5e22ffd5a929e207c3e339d3e3e114faa79a487aedea3604354b2e0` | rastreado | contrato destinado ao item 9; linhas 489–492 ainda excluem renderização/buffer/refresh |
| `docs/contratos/contrato_processo_desenvolvimento.md` | 177 | `e16a047559efa4a13623a11849cfab97b18570b3421f1c902d229ef47ee6dce7` | rastreado | autoridade processual e destino do registro do desvio pré-ADR |
| `docs/handoff/H-0009-layout-terminal-entrada-sem-echo.md` | 1053 | `509bcd3481a9e0e368e5fb427b6490f91220573b12a02c40bed29a628f62d5ff` | rastreado | precedente TTY/raw/não-TTY citado; não é ADR |
| `docs/handoff/H-0021-correcao-preenchimento-horizontal-orquestrador.md` | 961 | `c4b9dda6b5a61fca992c8dac1609f2ee3bae179aa757e3002ebc32aaceb319fd` | rastreado | precedente do ramo não-TTY; menções antigas a H-0022 como ciclo futuro de outro assunto são históricas |
| `docs/relatorios/IMP-0021-correcao-preenchimento-horizontal-orquestrador.md` | 300 | `e1c45b17e499c5babef483a3cd6345270a46eddd6db9dc7fcfa21e53dffcc96a` | rastreado | ocorrência contextual anterior, não pertence ao H-0022 TTY |
| `docs/relatorios/RELATORIO_AUDITORIA_H-0021_HANDOFF.md` | 486 | `f8aafa19fc9b1821698c715269621387317bddf81a31b3617244e624231143ce` | rastreado | ocorrência contextual anterior, trata H-0022 como futuro |
| `docs/relatorios/RELATORIO_INVESTIGACAO_POS_H0020_HORIZONTAL_ORQUESTRADOR.md` | 508 | `8406e0762d591335d4c169b882abdab3720ff152e4d0ff8b23303e209c1978e5` | rastreado | ocorrência contextual anterior, outro significado planejado de H-0022 |

Ocorrências de `raw` fora desta cadeia (por exemplo `_raw` do modelo JSON e H-0009) foram inspecionadas para desambiguação e não constituem artefatos do ciclo TTY. A ADR-0016 não cita ADR anterior; cita H-0009 e H-0021. Todos os arquivos diretamente citados pela ADR foram inspecionados integralmente, assim como os artefatos centrais, código, testes, histórico e stash pertinentes.

### 3.3 Stash `pre-H-0022`

| objeto | linhas | SHA-256 | papel |
|---|---:|---|---|
| `stash@{0}:scripts/tela/demo.py` | 300 | `590860405c794372794a91ada8dc234eb8db6b237db73df7d8a358982af0062c` | implementação pré-ADR preservada |
| `stash@{0}:scripts/tela/teste_demo.py` | 1462 | `ee77156458b6abb4302922c3930f0765669e290ef7d069f275201ca763b52897` | testes pré-ADR preservados |
| base `stash@{0}^1` | 249 / 1231 linhas | não necessário para identificar o snapshot | HEAD 0b09fa6 antes da tentativa |

O stat do stash registra 89 linhas alteradas em `demo.py` e 231 em `teste_demo.py` (301 inserções, 19 remoções). Isso comprova que a tentativa anterior foi isolada em snapshot antes da implementação posterior; não comprova autoria, prompt único ou contexto limpo.

## 4. Duas linhas de trabalho

### Linha A — tentativa anterior à ADR-0016

1. Sobre o HEAD `0b09fa6`, `demo.py` e `teste_demo.py` foram modificados para sessão TUI com `tty.setraw`, alternate screen e redesenho por cursor ao topo.
2. A execução produziu `IMP-0022-controle-tela-cheia-terminal-sem-echo.md`, que se rotula H-0022 apesar de não existir handoff precedente. O relatório declara que criou/modificou o próprio relatório, o código e os testes e inclui resultados e autoavaliação; logo implementação e avaliação interna foram produzidas juntas. Não existe QA formal separado identificado para essa versão.
3. A solução desligava `OPOST`/`ISIG` por `raw`, não normatizava DECAWM/synchronized output e não atendia ao redesenho posteriormente aprovado. A ADR a rejeita nos pontos `raw` e limpeza/redesenho.
4. O snapshot foi preservado em `stash@{0}` como `pre-H-0022` antes da Linha B.
5. O relatório ainda é referenciado ativamente pela ADR, handoff e IMP-0023 como evidência histórica. O código antigo é referenciado indiretamente pelo stash, não está na árvore atual.
6. A reserva declarada de “H-0023 — Redimensionamento reativo” em IMP-0022 foi rejeitada pela ADR atual (linhas 183–193): não há reserva antecipada.

### Linha B — fluxo posterior à ADR-0016

1. ADR-0016 teve ao menos três estados inferíveis pelo conteúdo dos relatórios: versão com suposição de handoff; segunda versão auditada em `RELATORIO_AUDITORIA_ADR-0016.md`; versão atual de 212 linhas/hash `50b314...`, auditada exatamente no QA pós-ajustes. Os textos anteriores não preservam hashes/arquivos completos das duas primeiras versões; detalhes além dos deltas citados são `NAO_CONFIRMADO`.
2. `RELATORIO_AUDITORIA_ADR-0016.md` substituiu no mesmo caminho uma auditoria anterior e avalia redações que já não existem. É histórico.
3. `RELATORIO_QA_ADR-0016_POS_AJUSTES.md` auditou exatamente a ADR atual e terminou `BLOCKED_USER_DECISION`. A decisão explícita de 2026-07-11 resolve a causa, mas não altera retroativamente o relatório nem as demais inconsistências que ele listou.
4. Foi criado H-0022. Seu primeiro QA auditou 216 linhas e reprovou “no máximo uma vez”. O handoff atual tem 236 linhas e exige “exatamente uma vez”; não existe QA posterior identificado dessa versão corrigida.
5. Após o stash, foram criados código/testes pós-ADR e IMP-0023. O relatório executou 169 verificações e fez autoavaliação item a item na mesma etapa.
6. Houve QA posterior separado da implementação com 172 verificações. Depois dele, código/testes mudaram novamente: a árvore atual tem 375/1744 linhas e 176/176 verificações, incluindo tratamento/testes de sequência de escape. Sem hashes no QA, ele não corresponde comprovadamente à versão corrente.
7. Não há validação manual específica registrada. A declaração geral do usuário não é distribuída aos sete critérios.

## 5. Proveniência e independência

| relatório | objeto e versão registrada | SHA atual | atual? | arquivos que declara alterar | execução separada | contexto limpo | autoavaliação possível | conclusão |
|---|---|---|---|---|---|---|---|---|
| `RELATORIO_AUDITORIA_ADR-0016.md` | ADR, sem hash; versão com redações antigas; contagem não fixada | `50b314...` | não | só o próprio relatório; também diz substituir versão anterior no mesmo arquivo | `NAO_CONFIRMADO` | `NAO_CONFIRMADO`; “sessão somente leitura” é autodeclaração | sim | auditoria histórica de versão antiga; não usar como QA atual |
| `RELATORIO_QA_ADR-0016_POS_AJUSTES.md` | ADR, 212 linhas, `50b314...` | `50b314...` | sim | só o próprio relatório | separação da criação da ADR é sustentada pelo estado coletado e pelo arquivo exclusivo; identidade exata de execução externa não é demonstrável | `NAO_CONFIRMADO` | possível, mas objeto/hash foram fixados | evidência formal mais recente e exata da ADR; conclusão de bloqueio é histórica após decisão do usuário |
| `RELATORIO_QA_H-0022_HANDOFF.md` | H-0022, 216 linhas, sem hash | `ba3758...` (236 linhas) | não | só o relatório | sim quanto à auditoria declarada após criação; prova externa de execução: `NAO_CONFIRMADO` | `NAO_CONFIRMADO` | possível | primeiro QA não avaliou a versão atual; não existe QA posterior localizado |
| `IMP-0023-implementacao-h0022-tela-cheia-tty.md` | código/testes sem hash; 169 testes | `demo.py=285670...`; `teste_demo.py=62494b...`; 176 testes | não | `demo.py`, `teste_demo.py` e o próprio relatório por consequência factual | mesma execução com autoavaliação: sim, pelo próprio conteúdo | não alegado/comprovado | sim, confirmada | relatório de implementação e autoavaliação da versão inicial pós-ADR, não evidência formal atual |
| `RELATORIO_QA_H-0022_IMPLEMENTACAO.md` | código/testes sem hash; linhas antigas citadas e 172 testes | hashes acima; 176 testes | não comprovado e factualmente posterior em testes/linhas | só o relatório | separado do IMP-0023 segundo cadeia e declaração; prova externa de identidade de sessão: `NAO_CONFIRMADO` | `NAO_CONFIRMADO` | possível | QA posterior separado, porém de versão anterior à atual ou versão não identificável por hash |

Respostas diretas:

1. O primeiro QA do handoff avaliou a versão atual? **Não**: 216 versus 236 linhas e critério textual diferente.
2. Existe QA posterior da versão corrigida do handoff? **Não foi localizado.**
3. O relatório atual de implementação foi produzido junto com autoavaliação? **Sim** para IMP-0023: ele registra alterações, execução e classifica itens 1–11; além disso, já não descreve a versão corrente.
4. Existe QA posterior separado da implementação pós-ADR? **Sim**, o relatório de QA de 172 testes, mas não da versão atual comprovada (176 testes).
5. Evidência formal mais recente: ADR atual → QA pós-ajustes + decisão posterior do usuário; handoff atual → nenhum QA correspondente; implementação atual → nenhum QA correspondente, sendo o QA de 172 a evidência histórica mais recente; tentativa pré-ADR → IMP-0022 e stash.

Nenhuma afirmação de contexto limpo é comprovável por evidência independente. Ferramenta/auditor igual ou diferente não foi inferido como independência; datas próximas não foram usadas para isso.

## 6. Matriz ADR → código → testes atuais

| item ADR (linhas) | código atual | testes atuais | cobertura / manual | resultado factual | divergência |
|---|---|---|---|---|---|
| 1. TTY duplo (73–75) | `demo.py:339` | 7G `1582–1637`; subprocesses anteriores | automatizada; sem manual exigido | `APLICADO_E_COBERTO` | nenhuma factual |
| 2. cbreak, não raw (77–80) | `265–275`; `setcbreak`; nenhuma string `setraw` | 7A `1221–1228`; 7B `1288–1306` | parcial; TTY real para ausência de escada | `APLICADO_COBERTURA_PARCIAL` | OPOST/ISIG são inferidos de `setcbreak`, não inspecionados bit a bit |
| 2a. preservar OPOST | `268–274` | teste de `setcbreak`, ausência de `setraw` | parcial; observação visual pendente | `APLICADO_COBERTURA_PARCIAL` | nenhuma objetiva |
| 2b. preservar ISIG | `249–273`, sem mascaramento | 7E e 7H | automatizada comportamental parcial | `APLICADO_E_COBERTO` | nenhuma objetiva |
| 3. alternate screen (82–85) | entrada `274`; saída `290` | 7A/7B/7C `1230–1244`, `1311–1329`, `1390–1420` | parcial; restauração visual pendente | `APLICADO_COBERTURA_PARCIAL` | nenhuma objetiva |
| 3a. cursor oculto/restaurado | `274`, `290` | mesmos blocos | parcial; visual pendente | `APLICADO_COBERTURA_PARCIAL` | nenhuma objetiva |
| 4. DECAWM (87–90) | `274`, `290` | 7A/7B/7C/7F | parcial; scroll na última coluna pendente | `APLICADO_COBERTURA_PARCIAL` | nenhuma objetiva |
| 5. posição absoluta por linha (92–96) | `_apresentar_quadro:296–318` | 7D `1422–1502` | parcial; alinhamento real pendente | `APLICADO_COBERTURA_PARCIAL` | nenhuma objetiva |
| 6. preencher largura (98–102) | `305–315` | 7D `1475–1482` | parcial; resíduos visuais pendentes | `APLICADO_COBERTURA_PARCIAL` | nenhuma objetiva |
| 7a. escrita atômica (104–107) | `310–318` | 7D conta uma `write`/`flush` por quadro | automatizada | `APLICADO_E_COBERTO` | nenhuma objetiva |
| 7b. limpeza inicial única (107–109) | única ocorrência em `274` | 7A `1257–1262`; 7B `1323–1329` | automatizada; cintilação manual pendente | `APLICADO_COBERTURA_PARCIAL` | nenhuma objetiva |
| 8. synchronized output (111–115) | `310`, `315`; função chamada por atualização | 7A/7D | automatizada | `APLICADO_E_COBERTO` | nenhuma objetiva |
| 9a. Ctrl+C em script/processo interno (117–123) | context manager `249–262`; nenhum fluxo real existente | 7E `1504–1535` | mecanismo testado; integração não aplicável agora | `APLICADO_COBERTURA_PARCIAL` | requisito preparado, não exercitável em fluxo inexistente |
| 9b. Ctrl+C fora do escopo (124–126) | loop captura em `345–356` | 7H `1639–1698` | automatizada por injeção | `APLICADO_E_COBERTO` | nenhuma objetiva; a redação ADR 9/10 continua ambígua |
| 10. restauração em finally (128–131) | `_encerrar...:279–293`; `finally:357–358` | 7C e 7F | parcial; estado real após saída pendente | `APLICADO_COBERTURA_PARCIAL` | Ctrl+C ignorado não executa `finally` naquele instante; loop está lexicalmente coberto |
| 11. não-TTY (133–135) | `360–371` | seção 4 e 7G; dois pipes iguais | automatizada | `APLICADO_E_COBERTO` | nenhuma objetiva |
| fora de escopo (187–198) | sem SIGWINCH/curses/textual/rich/terminfo/Windows específico; mecanismo ANSI assumido | inspeções de proibições `1190–1204` | automatizada por ausência parcial | `NAO_APLICAVEL_NO_ESTADO_ATUAL` | tratamento adicional de sequências de escape em `209–246` não implementa SIGWINCH nem biblioteca excluída |

Conclusão factual: todos os itens aplicáveis aparecem no código atual e têm alguma cobertura automatizada; sete dependem também de observação humana. Isso não é aprovação formal. O acréscimo atual de leitura robusta de Esc/sequências não diverge objetivamente da ADR, mas foi feito depois da versão de 172 testes e carece de QA correspondente.

## 7. Critérios manuais recuperados

Os dez critérios de IMP-0022 pertencem à solução histórica e são preservados como evidência; os sete critérios atuais abaixo são a consolidação do H-0022/IMP-0023/QA de implementação.

| critério atual | origem | evidência automática | evidência humana específica | estado |
|---|---|---|---|---|
| ausência de progressão diagonal/linha começa na coluna 1 | H-0022 item 2; QA item 2 | cbreak + posição absoluta | nenhuma | `PENDENTE` |
| Esc recupera conteúdo pré-sessão e cursor visível | H-0022 item 3 | sequências e restauração simulada | declaração geral de funcionamento, não específica | `PARCIALMENTE_CONFIRMADO` |
| última coluna não causa scroll com DECAWM off | H-0022 item 4 | sequências on/off | nenhuma | `PENDENTE` |
| quadro fica alinhado à esquerda independentemente do cursor | H-0022 item 5 | CSI por linha | nenhuma | `PENDENTE` |
| quadro novo não deixa resíduos | H-0022 item 6 | padding até largura | nenhuma | `PENDENTE` |
| não há flash/cintilação entre quadros | H-0022 item 7 | limpeza única, escrita atômica e sync output | declaração geral, não específica | `PARCIALMENTE_CONFIRMADO` |
| terminal final é idêntico ao anterior (atributos, cursor, autowrap, alternate screen) | H-0022 item 10 | finally/restauração simulada | declaração geral, não específica | `PARCIALMENTE_CONFIRMADO` |

Critérios históricos de IMP-0022 (conteúdo anterior some; prompt oculto; teclas sem echo; mudanças no mesmo espaço; última linha não sobe; Esc encerra; conteúdo anterior reaparece; cursor reaparece; shell volta a ecoar; comando posterior funciona) permanecem `NAO_CONFIRMADO` individualmente. Alguns se sobrepõem aos sete atuais, mas não há registro humano específico que permita promovê-los.

## 8. Consistência documental

### Inconsistências ativas

| id | arquivo/linhas | evidência e impacto no fechamento | tratamento mínimo possível | decisão do usuário? |
|---|---|---|---|---|
| AT-01 | ADR `6`, `23–25`; índice `46` | status literal `proposta` contradiz aprovação explícita | `PATCH_ADR` e índice, depois QA | não; decisão já dada |
| AT-02 | ADR `17–18`, `37–48`, `141–146`, `152–153`, `176–182` | usa presente para dizer que H-0022 não existe/manda abri-lo; hoje existe | marcar sequência histórica e reconciliar cadeia | não |
| AT-03 | ADR `117–131` | itens 9/10 podem sugerir que Ctrl+C simultaneamente mantém sessão e dispara restauração | esclarecer cobertura lexical versus execução do finally sem mudar intenção aprovada | não, se mantida a intenção explícita |
| AT-04 | ADR `147–166`; três contratos atuais | decisões aprovadas ainda não foram aplicadas aos contratos/registro processual | `APLICAR_ADR` e QA da aplicação | não |
| AT-05 | índice `13–17`, `46` | índice se declara de aceitas, mas contém proposta | harmonizar com status aprovado/política do índice | não |
| AT-06 | H-0022 atual; QA handoff | handoff de 236 linhas não tem QA correspondente; QA disponível é de 216 | novo `QA_HANDOFF` | não |
| AT-07 | código/testes atuais; IMP-0023; QA implementação | relatório diz 169, QA diz 172, atual é 176; sem hashes, versão atual não foi formalmente auditada | reconciliar documentação e executar `QA_IMPLEMENTACAO` atual | não |
| AT-08 | IMP-0023 `41–195` | autoavaliação invadiu escopo de QA e relatório está desatualizado | marcar/reconciliar como histórico ou substituir conforme política | não |
| AT-09 | todos os sete critérios manuais | não há evidência humana específica | `VALIDACAO_MANUAL` | requer execução humana, não nova decisão arquitetural |
| AT-10 | IMP-0023/H-0022 | número do relatório difere do ciclo e pode colidir semanticamente com futuro H-0023 | documentar convenção ou escolher preservação/renome/substituição em etapa própria | sim para solução final de nomenclatura |

### Inconsistências históricas explicáveis

| id | arquivo | fato histórico |
|---|---|---|
| HI-01 | QA ADR pós-ajustes | `BLOCKED_USER_DECISION` era correto antes da decisão explícita; não deve ser reescrito |
| HI-02 | auditoria ADR antiga | aprovou com ressalvas versão anterior e descreveu textos depois substituídos |
| HI-03 | QA handoff | reprovação do critério “no máximo uma vez” explica a correção atual, mas não avalia o arquivo atual |
| HI-04 | IMP-0022 e stash | documentam tentativa pré-ADR inválida; não são norma nem implementação vigente |
| HI-05 | H-0021 e relatórios relacionados | usavam H-0022 para distribuição vertical antes de o número ser usado pelo ciclo TTY; são contexto anterior, não autoridade atual |

### Diferenças sem impacto normativo

- 169, 172 e 176 verificações descrevem versões diferentes; a diferença isolada não muda a política, mas precisa ser rastreada.
- Linhas citadas pelo QA de implementação não coincidem com as atuais devido às inserções posteriores.
- O tratamento adicional de setas/Esc não altera os itens decisórios identificados.

### Lacunas de rastreabilidade

- Auditoria ADR antiga, QA do handoff e QA da implementação não registram SHA do objeto.
- As versões antigas substituídas de ADR/relatório não existem como arquivos separados.
- Não há evidência externa de contexto limpo nem identificador técnico de execução.
- Não há QA do handoff atual, QA da implementação atual, aplicação da ADR aos contratos nem validação manual específica.
- Os artefatos centrais não estão commitados; sua ordem é reconstruída por conteúdo/stash, não por commits.

## 9. Classificação dos artefatos

| artefato | categoria única | fundamento |
|---|---|---|
| ADR-0016 | `INCONSISTENTE_CORRIGIVEL` | norma aprovada, mas status/narrativa estão desatualizados |
| INDICE_ADR | `INCONSISTENTE_CORRIGIVEL` | status e regra do índice ainda conflitantes |
| H-0022 atual | `ATUAL_E_NECESSARIO` | especifica implementação vigente; falta QA próprio |
| IMP-0022 | `SUPERSEDIDO_MAS_REFERENCIADO` | evidência pré-ADR recebendo referências ativas |
| stash `pre-H-0022` | `HISTORICO_VALIDO_NECESSARIO` | prova técnica preservada da Linha A enquanto regularização não fecha |
| IMP-0023 | `INCONSISTENTE_CORRIGIVEL` | relatório pós-ADR necessário, mas numeração/contagem/versão e autoavaliação exigem tratamento |
| auditoria ADR antiga | `HISTORICO_VALIDO_OPCIONAL` | explica iterações, mas não corresponde à ADR atual |
| QA ADR pós-ajustes | `HISTORICO_VALIDO_NECESSARIO` | fixa hash atual e explica o bloqueio resolvido pela decisão |
| QA handoff | `HISTORICO_VALIDO_NECESSARIO` | explica correção de 216→236 linhas, sem aprovar versão atual |
| QA implementação | `HISTORICO_VALIDO_NECESSARIO` | QA separado mais recente, porém anterior à versão corrente |
| `demo.py` atual | `ATUAL_E_NECESSARIO` | implementação que o usuário decidiu preservar |
| `teste_demo.py` atual | `ATUAL_E_NECESSARIO` | cobertura atual que o usuário decidiu preservar |
| contratos afetados | `INCONSISTENTE_CORRIGIVEL` | autoridades atuais ainda não refletem a ADR aprovada |
| H-0009/H-0021 | `HISTORICO_VALIDO_NECESSARIO` | precedentes citados necessários à interpretação |

Nenhum arquivo é classificado agora como `CANDIDATO_A_REMOCAO` sem ressalva: IMP-0022 é candidato abstrato mencionado pelo usuário, mas recebe referências ativas e a própria ADR manda preservá-lo. Remoção só poderia ser reconsiderada após substituição da cadeia e decisão específica. O stash pode tornar-se candidato a arquivamento/remoção após a cadeia histórica ser fixada, mas hoje é evidência necessária.

## 10. IMP-0023 versus futuro H-0023

- A série predominante associa `IMP-NNNN` a `H-NNNN` (IMP-0001…0021); `IMP-0023` ligado a H-0022 é exceção real.
- Precedente próximo de não coincidência: `IMP-0020` menciona H-0019 e `IMP-0021` menciona H-0020 em seus conteúdos, mostrando que o nome pode seguir sequência de relatórios/correções, não identidade obrigatória absoluta. Há também séries alfanuméricas/documentais (`IMP-DOC-*`). Não foi encontrada regra normativa dizendo que números devem coincidir.
- Mesmo assim, `IMP-0023-implementacao-h0022...` cria ambiguidade visual com eventual H-0023 porque os dois identificadores aparecem no mesmo ciclo histórico e IMP-0022 já tentou reservar H-0023 para SIGWINCH.
- Referências ativas ao nome IMP-0023: QA da implementação e QA ADR pós-ajustes; o próprio handoff não o referencia porque o precede.
- Preservar: mantém rastreabilidade e links, mas exige explicação explícita da exceção.
- Renomear: reduz ambiguidade, mas quebra referências e exige atualização/registro de supersessão; não deve apagar histórico.
- Substituir por novo relatório: permite hash/contagem atuais e cadeia clara, mas cria duplicação a administrar e não autoriza apagar o original.
- A escolha final depende da política documental e de decisão do usuário; nenhuma alternativa foi executada.

## 11. Testes executados

Somente comandos diretamente exigidos pelo H-0022 atual foram executados:

| comando | saída/código | verificações/falhas |
|---|---|---|
| `python tela/teste_demo.py` | 0 | 176/176; 0 falhas |
| `printf 'b\ns\n' \| python tela/demo.py` | 0 | stderr não registrado pelo comando isolado; suíte 7G o confirma vazio |
| `printf 'b\n\x1b\n' \| python tela/demo.py` | 0 | saída byte a byte igual à anterior (`cmp`=0) |
| `grep -c '\\x1b\[2J' tela/demo.py` | 0; saída `1` | limpeza exatamente uma vez |
| `grep -c 'setraw' tela/demo.py` | 1; saída `0` | ausência confirmada; código 1 é sem correspondência, não falha do critério |

Contagens anteriores: IMP-0022=143 para `teste_demo.py`; IMP-0023=169; QA de implementação=172; atual=176. Antes e depois, `find` não encontrou `__pycache__` ou `.pytest_cache`; nenhum cache temporário foi produzido/identificado. Os arquivos de comparação foram criados apenas em `/tmp`, fora do repositório. Testes passando não aprovam formalmente a implementação.

## 12. Quadro de fechamento documental

```yaml
adr_0016:
  decisao_usuario: APROVADA
  versao_atual_identificada: "212 linhas; sha256 50b314e00322c6a28b376520761483527328f301da9ff741f709ef2662d579d4"
  qa_correspondente: "RELATORIO_QA_ADR-0016_POS_AJUSTES.md; objeto exato, conclusão BLOCKED_USER_DECISION historicamente superada"
  inconsistencias_ativas: "status proposta; narrativa presente desatualizada; ambiguidade itens 9/10; aplicação a contratos pendente"
  acao_processual_minima: "PATCH_ADR, QA_ADR, APLICAR_ADR, QA_APLICACAO_ADR"

handoff_h_0022:
  versao_atual_identificada: "236 linhas; sha256 ba37585352bdc16d91d1f883ebba85a9c97e85d813ce52ebd02b09de55f9f7fe"
  qa_correspondente: null
  aprovado_formalmente: false
  inconsistencias_ativas: "QA existente cobre versão de 216 linhas"
  acao_processual_minima: QA_HANDOFF

implementacao_h_0022:
  relatorio_atual: "IMP-0023, mas desatualizado (169 versus 176) e numericamente ambíguo"
  qa_separado_correspondente: "existe para versão de 172 verificações; não corresponde comprovadamente à atual"
  aderencia_factual_a_adr: "todos os itens aplicáveis presentes; cobertura automática completa ou parcial; sem aprovação formal"
  validacoes_manuais: "sete sem confirmação humana específica"
  inconsistencias_ativas: "versão atual sem relatório/hash/QA correspondente; IMP autoavaliativo"
  acao_processual_minima: "PATCH_DOCUMENTACAO/QA_DOCUMENTACAO, QA_IMPLEMENTACAO, VALIDACAO_MANUAL"

artefatos_anteriores_a_adr:
  lista: ["IMP-0022", "stash@{0}: pre-H-0022"]
  referencias_ativas: ["ADR-0016", "H-0022", "IMP-0023"]
  classificacao: "SUPERSEDIDO_MAS_REFERENCIADO / HISTORICO_VALIDO_NECESSARIO"
  acao_processual_minima: "preservar e marcar inequivocamente como histórico; decidir destino somente depois"

estado_git:
  arquivos_rastreados: ["M docs/adr/INDICE_ADR.md", "M tela/demo.py", "M tela/teste_demo.py"]
  arquivos_nao_rastreados: "oito artefatos centrais antes deste relatório; este relatório é o nono após criação"
  arquivos_staged: []
  caches_temporarios: []
  diff_check: LIMPO

pronto_para_verificar_fechamento:
  valor: false
  justificativa: "faltam reconciliação/aplicação documental e seus QAs, QA das versões atuais do handoff e implementação, validação manual específica e resolução rastreável da nomenclatura/relatório atual"
```

## 13. Plano mínimo de regularização não executado

1. `PATCH_ADR` — atualizar status e temporalidade/rastreabilidade sem mudar a decisão aprovada.
2. `QA_ADR` — auditar a versão corrigida e vincular a decisão explícita.
3. `APLICAR_ADR` — refletir a decisão nos contratos e índice/registro processual afetados.
4. `QA_APLICACAO_ADR` — verificar a aplicação normativa.
5. `PATCH_DOCUMENTACAO` — reconciliar IMP-0023/contagens/versões e explicitar a política escolhida para sua numeração, preservando históricos.
6. `QA_DOCUMENTACAO` — auditar a cadeia reconciliada.
7. `QA_HANDOFF` — auditar o H-0022 atual de 236 linhas.
8. `QA_IMPLEMENTACAO` — auditar hashes atuais e as 176 verificações, incluindo o tratamento posterior de sequências de escape.
9. `VALIDACAO_MANUAL` — registrar separadamente os sete critérios de TTY.
10. `VERIFICAR_FECHAMENTO`.
11. `PREPARAR_COMMIT`.

Não há divergência objetiva da ADR que sustente alteração de código/testes neste plano. Nenhuma categoria foi executada.

## 14. Síntese final

```text
status: LEVANTAMENTO_CONSISTENCIA_COMPLETO
relatorio: docs/relatorios/RELATORIO_LEVANTAMENTO_CONSISTENCIA_H-0022.md
branch: master
head: 0b09fa6a99a6d0ed61e9488ecb7e78f16d37cfdf
estado_git: sujo, sem stage, diff-check limpo, stash pre-H-0022 preservado
linha_anterior_a_adr: IMP-0022 + snapshot pre-H-0022; raw/redesenho supersedidos; sem handoff precedente nem QA separado
linha_posterior_a_adr: ADR iterada, handoff corrigido, implementação/IMP-0023, QAs e alterações posteriores até 176 testes
qa_adr_atual: QA pós-ajustes corresponde ao hash atual; bloqueio de decisão é histórico e foi resolvido pelo usuário
qa_handoff_atual: inexistente; QA disponível cobre 216, não 236 linhas
qa_implementacao_atual: inexistente; QA disponível executou 172, versão atual executa 176 e não tem hash no QA
aderencia_adr_codigo_testes: factual presente em todos os itens aplicáveis; cobertura automática completa/parcial; não é aprovação
validacoes_manuais: sete pendentes de evidência humana específica
inconsistencias_ativas: status/narrativa ADR, contratos não aplicados, QAs de versões atuais ausentes, IMP-0023 desatualizado/ambíguo, manual pendente
inconsistencias_historicas: bloqueio anterior, auditoria ADR antiga, reprovação do handoff antigo, tentativa pre-ADR e antigo uso semântico de H-0022
artefatos_atuais: ADR, índice, H-0022, código, testes, IMP-0023 sujeito a reconciliação
artefatos_historicos: IMP-0022, stash, auditoria ADR antiga, QAs de versões antigas
candidatos_a_remocao: nenhum autorizado; IMP-0022 não é removível enquanto referenciado; stash só reavaliável após fixação histórica
ambiguidade_imp_0023: real mas não fatal; convenção predominante coincide com H, há precedentes de diferença; decisão de preservar/renomear/substituir pendente
testes_executados: teste_demo 176/176; dois pipes código 0 e saídas iguais; limpeza=1; setraw=0
evidencias_ausentes: hashes nos QAs antigos, QA do handoff/código atuais, contexto limpo independente, validações humanas específicas, versões antigas completas da ADR
plano_minimo_de_regularizacao: PATCH_ADR, QA_ADR, APLICAR_ADR, QA_APLICACAO_ADR, PATCH_DOCUMENTACAO, QA_DOCUMENTACAO, QA_HANDOFF, QA_IMPLEMENTACAO, VALIDACAO_MANUAL, VERIFICAR_FECHAMENTO, PREPARAR_COMMIT
arquivos_alterados: somente docs/relatorios/RELATORIO_LEVANTAMENTO_CONSISTENCIA_H-0022.md
```
