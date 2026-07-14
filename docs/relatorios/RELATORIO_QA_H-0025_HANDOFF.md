# RELATORIO_QA_H-0025_HANDOFF

## 1. Identificacao

Etapa executada: `QA_HANDOFF`

Artefato auditado:

```text
docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md
```

Relatorio criado:

```text
docs/relatorios/RELATORIO_QA_H-0025_HANDOFF.md
```

Data: 2026-07-11

Status final:

```text
H1_HANDOFF_APPROVED
```

Unica proxima categoria:

```text
IMPLEMENTAR
```

## 2. Escopo

Auditoria formal do H-0025 contra a ADR-0018, aplicacao documental aprovada,
contratos ativos, ADRs relacionadas e evidencias historicas do H-0024.

Este QA nao corrigiu o H-0025, nao alterou o H-0024, nao implementou codigo,
nao alterou JSON, nao alterou testes, nao criou ADR, nao manipulou stash, nao
preparou commit e nao executou etapa posterior. Criou somente este relatorio.

## 3. Estado Git

O caminho deste relatorio estava livre antes da criacao (`test -e` retornou
ausencia). O estado operacional foi verificado por comandos de leitura.

| Comando | Resultado |
|---|---|
| `git status --short` | 6 documentos rastreados modificados; ADR-0018, H-0024, H-0025 e relatorios do ciclo como nao rastreados; stage vazio |
| `git status` | branch `master`; nenhum arquivo staged |
| `git branch --show-current` | `master` |
| `git rev-parse HEAD` | `3332773a3f10e716115a164148af323fa86e608f` |
| `git log -1 --oneline` | `3332773 feat: implementa redimensionamento reativo da TUI` |
| `git diff --check` | sem saida |
| `git diff --stat` | 6 arquivos, 267 insercoes, 19 remocoes |
| `git diff --name-only` | somente documentos da aplicacao ADR-0018 |
| `git diff --cached --stat` | sem saida |
| `git diff --cached --name-only` | sem saida |
| `git diff --no-index /dev/null docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md` | codigo 1 esperado; confirmou H-0025 como arquivo novo com conteudo |

Confirmacoes:

- Branch esperada: conforme.
- HEAD esperado: conforme.
- Stage vazio: conforme.
- Ausencia de conflito ou operacao Git ativa: conforme; nao foram encontrados `MERGE_HEAD`, `REBASE_HEAD`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, diretorios de rebase ou locks Git.
- Documentos e relatorios da ADR-0018 presentes no worktree: conforme.
- H-0025 como arquivo novo nao rastreado: conforme.
- O relatorio de implementacao exigido pelo H-0025 (`IMP-0026`) esta livre.

## 4. Estado do stash

| Comando | Resultado |
|---|---|
| `git stash list` | `stash@{0}: pre-H-0022 recuperado apos drop acidental` |
| `git rev-parse stash@{0} 2>/dev/null || true` | `21f98d0f4a479d72e6df21b1dca1511c3ad38937` |

O stash esperado foi preservado. Nenhum comando de manipulacao de stash foi
executado.

## 5. Seguranca entre sessoes

Antes da escrita deste relatorio, foram feitas apenas verificacoes de leitura.
Nao foi identificada outra sessao modificando o workspace: nao havia operacao
Git ativa, lock Git, stage preenchido ou processo relevante alem da propria
execucao encapsulada do Codex observada por `pgrep`.

## 6. Artefatos auditados

Lidos integralmente ou auditados na versao atual:

- `docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md`
- `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
- `docs/relatorios/RELATORIO_QA_ADR-0018.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0018.md`
- `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0018.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0018.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/NOMENCLATURA.md`
- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`
- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`

Evidencia historica, sem autoridade normativa superior:

- `docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md`
- `docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH.md`
- `docs/relatorios/RELATORIO_QA_H-0024_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0024_HANDOFF.md`

Tambem foram consultados para evidencia objetiva: `tela/teste_demo.py`,
`tela/demo.py` e `config/telas/orquestrador.json`.

## 7. Autoridades

Autoridade primaria: ADR-0018.

Autoridades normativas ativas: contratos de composicao, tela JSON, JSON minimo,
processo de desenvolvimento e `NOMENCLATURA.md`, ja com aplicacao documental da
ADR-0018 aprovada em QA pos-patch.

Autoridades relacionadas preservadas: ADR-0013, ADR-0015 e ADR-0017.

Relatorios e H-0024 foram usados como evidencia historica e operacional, nao
como fonte normativa superior.

## 8. Metodo

1. Conferencia de caminho livre para o relatorio.
2. Conferencia de branch, HEAD, stage, diff, stash, operacao Git ativa e H-0025
   como arquivo novo.
3. Leitura do H-0025 com linhas numeradas e `git diff --no-index`.
4. Comparacao do H-0025 com D1-D10 da ADR-0018, contratos ativos e QA
   pos-patch da aplicacao documental.
5. Validacao do JSON real do Orquestrador e do teste historico de altura 15.
6. Verificacao de arquivos permitidos/proibidos, criterios, testes, relatorio
   de implementacao e condicoes de bloqueio.
7. Registro de conclusao sem corrigir o handoff.

## 9. Matriz D1-D10

| Decisao | Classificacao | Evidencia principal no H-0025 |
|---|---|---|
| D1 | CONFORME | linhas 42-53 e 198-208: arranjo vertical organiza; distribuicao explicita dispara reparticao; ausencia preservada |
| D2 | CONFORME | linhas 182-194 e 410-412: ausencia preserva altura natural, nao materializa `igual` e nao altera telas existentes |
| D3 | CONFORME | linhas 196-208, 359-363 e 431-447: altura util integral, filhos diretos, soma exata e ausencia de sobra externa |
| D4 | CONFORME | linhas 210-220, 441-447 e 612-614: moldura ocupa cota; sobra vira linhas internas |
| D5 | CONFORME | linhas 222-227, 414-416 e 604: `igual` explicito, sem fallback da ausencia |
| D6 | CONFORME | linhas 229-235, 418-419 e 605-611: percentual com um valor por filho, soma 100, maiores restos e desempate |
| D7 | CONFORME | linhas 237-255, 421-429 e 616-618: fracao generica, pesos positivos, exemplos nao exaustivos, sem hardcode de `[2,1,2]` |
| D8 | CONFORME | linhas 257-265, 470-472, 580-589 e 626-627: terminal insuficiente fora de escopo; vetor valido nao vira invalido |
| D9 | CONFORME | linhas 269-318 e 619-623: `config/telas/orquestrador.json`, declaracao `[2,1,2]`, ordem e validacao |
| D10 | CONFORME | linhas 396-472 e 628: testes minimos suficientes; cobertura ampla diferida |

## 10. Relacao H-0025 x H-0024

Conforme. O H-0025 trata o H-0024 como historico bloqueado, identifica a causa
do bloqueio e afirma que o H-0024 permanece preservado como evidencia
historica, sem autoridade normativa superior. A nova ordem operacional depende
da ADR-0018, nao da semantica superada de ausencia equivalente a `igual`.

## 11. Analise da ausencia de distribuicao

Conforme. O H-0025 exige que, sem `corpo.distribuicao`, o caminho orientado pelo
conteudo seja preservado, cada filho mantenha altura natural, nenhum objeto
`distribuicao` seja criado implicitamente e telas existentes sem distribuicao
nao sofram alteracao comportamental indevida.

## 12. Analise da distribuicao explicita

Conforme. O H-0025 especifica que, em container vertical com `distribuicao`
declarada, a altura util entre `cabecalho` e `barra_de_menus` e repartida
integralmente entre filhos diretos, descontando somente linhas estruturais
normativas e garantindo soma exata das cotas. Os criterios e testes exigem
maiores restos, desempate, preenchimento interno e ausencia de sobra abaixo do
ultimo filho.

## 13. Modos igual, percentual e fracao

Conforme.

- `igual`: explicitamente declarado, sem fallback da ausencia.
- `percentual`: exige cardinalidade por filho direto, soma 100, associacao
  posicional, maiores restos e erros deterministricos.
- `fracao`: aceita qualquer vetor valido de pesos positivos; `[1,1,1]`,
  `[2,1,2]`, `[1,3,1]` e `[5,2,7]` aparecem como exemplos ou testes, nunca
  como regra interna.

## 14. Preenchimento interno

Conforme. O handoff exige que cada moldura ocupe a cota atribuida e que a sobra
entre `NAVEGAR` e `Menus`, no caso do Orquestrador com distribuicao declarada,
seja incorporada internamente nas areas de ITENS, INFO e NAVEGAR. Nao ha
tratamento especial hardcoded para o Orquestrador.

## 15. JSON real do Orquestrador

Conforme. O H-0025 inclui `config/telas/orquestrador.json` na lista fechada de
arquivos alteraveis e especifica exatamente:

```json
"distribuicao": {
  "modo": "fracao",
  "valores": [2, 1, 2]
}
```

O JSON real foi conferido: a ordem dos filhos diretos em
`config/telas/orquestrador.json` e `console_principal`,
`dashboard_info`, `lancador_principal`. A associacao posicional 2, 1, 2 esta
correta, a ordem nao deve ser alterada, os demais campos devem ser preservados e
o JSON deve ser validado por `python -m json.tool` e pelo loader/modelo.

## 16. Caso historico de altura 15

Conforme. O H-0025 identifica objetivamente:

- arquivo: `tela/teste_demo.py`;
- funcao real: `teste_renderizar_estado_altura`;
- trecho real: linhas 695-709 no estado auditado;
- modelo real: `_carregar_modelo()` carrega `config/telas/orquestrador.json`;
- expectativa antiga: `altura=15` produz 15 linhas e saida igual a sem altura;
- motivo do conflito: apos declarar distribuicao no Orquestrador, `altura=15`
  passa a ser terminal insuficiente, caso fora de escopo pela D8;
- preservacao do H-0023: o teste `teste_redimensionamento_reativo_h0023` e
  mencionado como nao removivel.

A evidencia objetiva para altura alternativa existe: `_ALTURA_SUBPROCESS = 24`
em `tela/teste_demo.py:139`, e o proprio teste atual verifica
`renderizar_estado(..., largura=42, altura=24) -> 24 linhas`. O handoff nao
transforma essa altura em minimo normativo do produto.

## 17. Arquivos permitidos e proibidos

Conforme.

Arquivos alteraveis listados no H-0025:

```text
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_demo.py
config/telas/orquestrador.json
docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md
```

Somente leitura:

```text
tela/demo.py
docs/templates/TEMPLATE_RELATORIO_IMPL.md
```

A lista e suficiente para loader, modelo, renderer, testes, adaptacao minima do
teste historico, alteracao declarativa do JSON real e relatorio de
implementacao. Nenhum diretorio inteiro foi autorizado. `tela/demo.py` pode
permanecer somente leitura porque o redimensionamento ja repassa dimensoes ao
renderer e o ciclo nao altera a maquina de sessao.

## 18. Escopo positivo e negativo

Conforme. O escopo positivo cobre parsing opcional, validacao, representacao da
ausencia, preservacao dos valores declarados, calculo de cotas, maiores restos,
desempate, preenchimento interno, preservacao do caminho sem distribuicao,
alteracao do JSON real e relatorio IMP-0026.

O escopo negativo proibe arranjo horizontal distribuido neste ciclo, grupos
aninhados com distribuicao propria, altura minima, overflow, truncamento,
paginacao de `lancador`, politica para conteudo maior que cota, hardcode de
pesos, regra especial para o Orquestrador, alteracao de contratos/ADRs, stash e
commit. A preservacao do arranjo horizontal esta explicitamente testada.

## 19. Criterios de aceite

Conforme. Os 28 criterios do H-0025 sao observaveis e cobrem ausencia,
`igual`, `percentual`, `fracao`, cardinalidade, associacao posicional, soma
exata, maiores restos, desempate, preenchimento interno, vetores genericos, JSON
real, preservacao de telas sem distribuicao, arranjo horizontal, ausencia de
politica nova para terminal insuficiente e ausencia de arquivos fora da lista.

## 20. Testes

Conforme. O H-0025 exige, no minimo:

```bash
python -m json.tool config/telas/orquestrador.json
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
git diff --check
git diff --stat
git diff --name-only
git status --short
```

Os testes previstos cobrem ausencia, `igual` explicito, percentual, fracao
`[1,1,1]`, fracao `[2,1,2]`, outro vetor generico, soma, restos, desempate,
preenchimento interno, JSON real, redimensionamento em altura suficiente,
preservacao horizontal e telas sem distribuicao.

## 21. Relatorio de implementacao

Conforme. O H-0025 exige:

```text
docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md
```

O caminho esta livre. O conteudo exigido cobre relacao com H-0024, ADR-0018,
arquivos alterados, algoritmo generico, caminho sem distribuicao, distribuicao
explicita, JSON real, pesos e ordem, teste historico de altura 15, limitacoes,
testes, Git, stash, validacao manual ou ausencia dela e bloqueios.

## 22. Condicoes de bloqueio

Conforme. O H-0025 manda bloquear se houver divergencia na ordem real dos
filhos, necessidade de hardcodar vetor, necessidade de converter ausencia em
`igual`, necessidade de decidir altura minima ou overflow, alteracao de
contrato/ADR, arquivo fora da lista, teste de altura 15 exigindo politica
normativa ausente, estado Git inseguro, stash divergente, operacao Git ativa,
ou contradicao entre ADR-0018 e contratos ativos.

As condicoes nao bloqueiam indevidamente apenas porque o terminal historico de
altura 15 permanece insuficiente; esse caso e tratado como D8, fora de escopo.

## 23. Integridade documental

Conforme. O H-0025 tem identificacao, rastreabilidade, listas fechadas, escopo
positivo/negativo, criterios, testes, relatorio de implementacao e encerramento
coerentes. Nao ha autorizacao indireta para novos arquivos, implementacao
antecipada ou autoaprovacao da implementacao.

## 24. Escopo da criacao

O estado atual contem alteracoes acumuladas de etapas anteriores: aplicacao
documental da ADR-0018 em seis documentos rastreados e artefatos nao
rastreados de ADR, H-0024, H-0025 e relatorios. O H-0025 declara que sua etapa
criou somente o arquivo de handoff e nao alterou H-0024, ADRs, contratos,
nomenclatura, indices, relatorios anteriores, JSON, codigo, testes, templates,
estado operacional, stash, stage ou historico Git. O diff rastreado atual nao
inclui o H-0025 nem altera esses artefatos historicos; nao ha evidencia de
violacao da criacao especifica do H-0025.

## 25. Achados

Nao ha achados bloqueantes, altos, medios, baixos ou observacoes materiais.

## 26. Riscos residuais

- A politica geral para conteudo maior que a cota permanece fora de escopo por
  decisao explicita; a implementacao deve bloquear se precisar defini-la.
- A adaptacao do teste historico de altura 15 deve seguir a evidencia objetiva
  do H-0025 e nao virar minimo normativo.
- A validacao visual em TTY real pode permanecer pendente se nao houver
  evidencia do usuario, mas deve ser registrada no IMP-0026.

## 27. Classificacao final

```text
H1_HANDOFF_APPROVED
```

Justificativa: o H-0025 e implementavel, D1-D10 estao conformes, os arquivos
permitidos sao suficientes, criterios e testes sao verificaveis, nao ha achado
bloqueante/alto/medio/baixo e nenhuma decisao arquitetural pendente e exigida
para a implementacao em alturas suficientes.

## 28. Unica proxima categoria

```text
IMPLEMENTAR
```

## 29. Arquivos criados ou alterados pelo QA

Criado por este QA:

```text
docs/relatorios/RELATORIO_QA_H-0025_HANDOFF.md
```

Nao alterado por este QA:

- H-0025
- H-0024
- ADRs
- contratos
- NOMENCLATURA
- JSON
- codigo
- testes
- templates
- stash
- stage
- branch
- historico Git
