# RELATORIO_QA_ADR-0018

## 1. Identificacao

Relatorio: `docs/relatorios/RELATORIO_QA_ADR-0018.md`

Etapa executada: `QA_ADR`

ADR auditada: `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`

Data da auditoria: 2026-07-11

Resultado: `ADR_APPROVED_WITH_NOTES`

## 2. Escopo

Auditoria formal da ADR-0018 contra as decisoes explicitas D1-D10, autoridades anteriores e limites definidos para esta decisao.

Esta etapa nao corrigiu a ADR, nao aplicou a ADR, nao alterou contratos, nomenclatura, indice, H-0024, JSON, codigo, testes, stash, stage, branch ou historico Git.

## 3. Estado Git

Comandos executados e resultado relevante:

| Comando | Resultado |
|---|---|
| `git status --short` | Arquivos nao rastreados: ADR-0018, H-0024 e relatorios contextuais; stage vazio. |
| `git status` | Branch `master`; nada adicionado ao commit; untracked files presentes. |
| `git branch --show-current` | `master` |
| `git rev-parse HEAD` | `3332773a3f10e716115a164148af323fa86e608f` |
| `git log -1 --oneline` | `3332773 feat: implementa redimensionamento reativo da TUI` |
| `git diff --check` | sem saida |
| `git diff --stat` | sem saida |
| `git diff --name-only` | sem saida |
| `git diff --cached --stat` | sem saida |
| `git diff --cached --name-only` | sem saida |
| `git stash list` | `stash@{0}: pre-H-0022 recuperado apos drop acidental` |
| `git rev-parse stash@{0}` | `21f98d0f4a479d72e6df21b1dca1511c3ad38937` |
| `git diff --no-index /dev/null docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` | codigo 1 esperado; confirmou arquivo novo com conteudo. |

Confirmacoes:

- Branch esperada: conforme, `master`.
- HEAD esperado: conforme, `3332773a3f10e716115a164148af323fa86e608f`.
- Stage vazio: conforme.
- Conflito ou operacao Git ativa: nao identificado; nao havia `MERGE_HEAD`, `REBASE_HEAD`, `CHERRY_PICK_HEAD` ou `REVERT_HEAD`.
- Locks Git: nao identificados por `find .git -name '*.lock' -print`.
- Stash esperado: conforme, `stash@{0}` existe e resolve para `21f98d0f4a479d72e6df21b1dca1511c3ad38937`.
- Workspace livre: nao foram identificados locks Git ou operacoes Git ativas concorrentes. Processos encontrados por `pgrep` corresponderam as leituras da propria sessao sandbox.
- Caminho do relatorio: `docs/relatorios/RELATORIO_QA_ADR-0018.md` nao existia antes da criacao.

## 4. Artefatos Auditados

- `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` integralmente.
- Contexto Git e stash conforme comandos da secao 3.

## 5. Autoridades

Autoridades normativas consultadas:

- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`
- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/NOMENCLATURA.md`

Evidencias contextuais, sem autoridade superior:

- `docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH.md`
- `docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md`

## 6. Metodo

1. Conferencia do estado Git, stash, ausencia de locks e ausencia de relatorio preexistente no caminho alvo.
2. Leitura integral da ADR-0018 com numeracao de linhas.
3. Leitura dos trechos aplicaveis das ADRs 0013, 0015 e 0017.
4. Leitura dos trechos aplicaveis dos contratos e da nomenclatura.
5. Leitura contextual dos artefatos H-0024/IMP/levantamento.
6. Classificacao de D1-D10 e verificacoes obrigatorias.
7. Criacao exclusiva deste relatorio.

## 7. Matriz D1-D10

| Decisao | Classificacao | Evidencia na ADR-0018 | Observacao |
|---|---|---|---|
| D1 | conforme | linhas 105-111, 370-371 | Distingue ordem vertical de reparticao de area. |
| D2 | conforme | linhas 113-126, 300-306, 392-394 | Preserva altura natural e rejeita ausencia como `igual`. |
| D3 | conforme | linhas 128-137, 310-316 | Distribuicao explicita reparte area util entre cabecalho e barra_de_menus, descontando linhas estruturais. |
| D4 | conforme | linhas 139-150, 275-296, 346-352 | Sobra vira linhas internas nas molduras; exemplo visual explicita ITENS/INFO/NAVEGAR. |
| D5 | conforme | linhas 152-158, 320-324 | `igual` permanece valido e explicito, sem fallback implicito. |
| D6 | conforme | linhas 160-169, 328-332 | Percentual: um valor por filho, soma 100, maiores restos e empate por ordem. |
| D7 | conforme | linhas 171-193, 336-342, 378-379 | Fracao generica; `[1,1,1]` valido; `[2,1,2]` exemplo, nao hardcode. |
| D8 | conforme | linhas 195-212, 356-364, 469-488 | Conteudo que nao cabe permanece fora de escopo; vetor valido nao se torna invalido. |
| D9 | conforme | linhas 214-226, 382, 458, 502 | Mudanca JSON necessaria deve estar no handoff e nao autoriza hardcode. |
| D10 | conforme | linhas 228-240, 383-384, 485 | Distingue algoritmo/configuracao/cobertura; nao exige combinatoria exaustiva nem novo handoff de testes. |

## 8. Analise de Ausencia de Decisoes Novas

Nao foram identificadas decisoes novas sobre:

- altura minima;
- overflow;
- truncamento;
- paginacao de lancador;
- rejeicao por conteudo maior que a cota;
- degradacao;
- redistribuicao baseada em altura natural;
- prioridade por tipo de elemento;
- vetor padrao;
- hardcode de `[2, 1, 2]`;
- tratamento especial para o Orquestrador;
- politica automatica para terminais insuficientes;
- escopo de futuro handoff de testes;
- implementacao concreta.

Evidencias principais: ADR-0018 linhas 102-103, 195-212, 469-488 e 523-528.

## 9. Relacao com ADR-0013

Classificacao: conforme.

A ADR-0013 preserva a ocupacao vertical da janela e a area entre `cabecalho` e `barra_de_menus`. A ADR-0018 reconhece essa area nas linhas 36-39, 134-135, 312-316 e 404-410.

A ADR-0018 esclarece onde fica a sobra quando ha distribuicao explicita: dentro das areas atribuidas aos filhos. Na ausencia de distribuicao, preserva o preenchimento externo existente, conforme linhas 122-123, 302-306 e 406-410.

Nao houve redefinicao indevida de `corpo.arranjo`; a distincao arranjo/ocupacao vertical da ADR-0013 e preservada.

## 10. Relacao com ADR-0015

Classificacao: conforme.

A ADR-0018 delimita a substituicao normativa ao ponto em que ausencia de `distribuicao` era tratada como equivalente a `igual`, conforme linhas 416-433.

Preservacoes verificadas:

- `igual` explicito: linhas 152-158 e 320-324.
- `percentual`: linhas 160-169 e 328-332.
- `fracao`: linhas 171-193 e 336-342.
- filhos diretos e associacao posicional: linhas 164-165, 176-177, 330-339.
- maiores restos e desempate: linhas 168-169, 330-332, 398-399.
- distribuicao por container: linhas 130-132, 420-423.
- preenchimento de area alocada: linhas 139-150, 346-352, 429.
- composicao hierarquica: linha 430.

A extensao da substituicao esta claramente delimitada e nao invalida indevidamente a composicao hierarquica.

## 11. Relacao com ADR-0017

Classificacao: conforme.

A ADR-0018 preserva a obtencao de dimensoes e o redimensionamento reativo, conforme linhas 41-43 e 437-444.

Nao cria nova arquitetura de evento ou sinal. Mantem SIGWINCH, cadeia `ioctl -> LINES/COLUMNS -> ultimas dimensoes validas` e recalculo dependente de dimensao sem alterar composicao declarada.

## 12. Coerencia Interna

Classificacao: conforme com nota baixa A-001.

Pontos conformes:

- Terminologia consistente entre ausencia, `igual` e distribuicao explicita.
- Distincao entre altura natural e area atribuida.
- Distincao entre arranjo e ocupacao vertical.
- Consequencias e fora de escopo nao contradizem as decisoes D1-D10.
- Exemplos `[1,1,1]` e `[2,1,2]` sao tratados como exemplos, nao regras universais.
- Nao ha condicional que autorize aplicacao ou implementacao nesta etapa.

Nota: a secao de impacto sobre H-0024 captura a proibicao de retomar/corrigir/recriar nesta etapa e remete a aplicacao documental futura, mas a formulacao "retomado, corrigido ou recriado" fica menos direta que a exigencia "corrigido ou recriado" para o handoff futuro. Ver A-001.

## 13. Consequencias Documentais

Classificacao: conforme.

A ADR-0018 identifica os documentos aplicaveis nas linhas 448-461:

- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/NOMENCLATURA.md`
- `docs/adr/INDICE_ADR.md`
- exemplos normativos que afirmem ausencia equivalente a `igual`

A lista e suficiente para aplicacao documental futura e nao executa aplicacao prematura.

## 14. Impacto no H-0024

Classificacao: conforme com nota baixa A-001.

A ADR registra que:

- H-0024 nao e corrigido nesta etapa: linhas 70-72, 463-465 e 518-519.
- H-0024 so pode ser retomado depois de QA da ADR, aplicacao documental e QA da aplicacao: linhas 463-465 e 518-519.
- O algoritmo deve permanecer generico e nao hardcodar vetor concreto: linhas 182-193, 378-379, 476-478 e 500-501.
- Mudancas JSON necessarias pertencem ao proprio handoff: linhas 214-226, 382, 458 e 502.
- Politicas fora de escopo nao podem ser decididas pelo H-0024: linhas 195-212 e 469-488.

A nota A-001 registra apenas que as obrigacoes sobre H-0024 estao distribuidas em secoes distintas e que a frase "retomado, corrigido ou recriado" e menos precisa que a formulacao operacional exigida. O conteudo normativo suficiente esta presente para aplicacao documental.

## 15. Criterios de Aplicacao

Classificacao: conforme.

A ADR exige, para aplicacao futura, remover ausencia como `igual`, preservar `igual` explicito, diferenciar altura natural de area distribuida, localizar preenchimento dentro das molduras quando a distribuicao for explicita, preservar `percentual` e `fracao` genericos, impedir hardcode de exemplos, registrar regra de JSON necessario ao handoff e nao definir minimo/overflow. Evidencia: linhas 492-504.

## 16. Achados

### A-001

- Severidade: baixa.
- Categoria: `ADR_LOCAL`.
- Arquivo e linha: `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md:463` e `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md:518`.
- Decisao ou autoridade afetada: verificacao obrigatoria 8, impacto sobre H-0024.
- Evidencia: a ADR afirma que "O H-0024 devera ser retomado, corrigido ou recriado somente apos..." e que "A retomada ocorrera apenas apos...".
- Impacto: a regra operacional exigida para o H-0024 fica registrada, mas nao em uma formulacao unica e inequivoca de "corrigir ou recriar antes de retomar"; como a ADR tambem proibe alterar H-0024 nesta etapa e registra as restricoes de algoritmo generico, JSON e fora de escopo, o achado nao impede aplicacao documental.
- Classificacao da decisao local: parcial de baixa severidade para a forma da secao de impacto; sem contradicao material de D1-D10.

## 17. Arquivos Alterados na Criacao da ADR

Pelo estado Git auditado, a criacao da ADR aparece como arquivo nao rastreado:

- `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`

Outros arquivos nao rastreados estavam presentes no workspace e foram tratados como contexto/preexistentes desta auditoria:

- `docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md`
- `docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH.md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md`
- `docs/relatorios/RELATORIO_QA_H-0024_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0024_HANDOFF.md`

Nao havia alteracoes rastreadas nem stage.

## 18. Riscos Residuais

- A ADR-0018 ainda nao foi aplicada documentalmente; contratos e nomenclatura continuam contendo trechos conflitantes ate a etapa `APLICAR_ADR`.
- A ADR-0018 esta nao rastreada no Git no momento da auditoria.
- O H-0024 permanece artefato contextual nao aplicado e devera ser corrigido ou recriado apos aplicacao documental aprovada.
- A politica geral de conteudo que nao cabe permanece fora de escopo, por decisao explicita.

## 19. Classificacao Final

`ADR_APPROVED_WITH_NOTES`

Justificativa: D1-D10 estao integralmente registradas; nao ha decisao nova; relacoes com ADR-0013, ADR-0015 e ADR-0017 estao delimitadas; nao ha achados bloqueantes, altos ou medios. Ha uma nota baixa sobre a forma da secao de impacto no H-0024.

## 20. Unica Proxima Categoria

`APLICAR_ADR`

## 21. Arquivos Criados ou Alterados pelo QA

Criado:

- `docs/relatorios/RELATORIO_QA_ADR-0018.md`

Nao alterado pelo QA:

- ADR-0018
- contratos
- nomenclatura
- indice
- handoffs
- JSON
- codigo
- testes
- stash
- stage
- branch
- historico Git
