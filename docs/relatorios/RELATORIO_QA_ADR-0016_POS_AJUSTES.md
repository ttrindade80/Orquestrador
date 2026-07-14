# Relatório de QA da ADR-0016 pós-ajustes

## 1. Identificação da etapa

- Etapa executada: `QA_ADR`.
- Ciclo: `H-0022 / ADR-0016`.
- Escopo: auditoria formal exclusivamente da versão atualmente presente de
  `docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md`.
- Data da coleta: 2026-07-11.

## 2. Arquivo e versão auditada

- Arquivo: `docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md`.
- Quantidade: 212 linhas.
- SHA-256: `50b314e00322c6a28b376520761483527328f301da9ff741f709ef2662d579d4`.
- Estado Git: não rastreado (`??`).
- Identificação textual: frontmatter nas linhas 1–19; status literal
  `proposta` nas linhas 6 e 23–25; decisão em 11 itens nas linhas 71–135.
- Como o arquivo não é rastreado, a versão foi observada por
  `git diff --no-index /dev/null ...`, que mostrou a criação integral das 212
  linhas. `git diff -- <arquivo>` não produziu diff por não haver versão no
  índice.

## 3. Autoridades e evidências consultadas

Autoridades normativas:

- `docs/contratos/contrato_processo_desenvolvimento.md`, especialmente linhas
  28–48, 50–64 e 83–94;
- `docs/contratos/contrato_tela_json.md`, lido integralmente;
- `docs/contratos/contrato_console.md`, lido integralmente;
- `docs/handoff/H-0009-layout-terminal-entrada-sem-echo.md`, nos trechos
  diretamente invocados pela ADR (linhas 57, 332–374, 393–416 e 730);
- `docs/handoff/H-0021-correcao-preenchimento-horizontal-orquestrador.md`, nos
  trechos relativos à preservação do ramo não-TTY.

Evidência factual e histórica:

- `docs/relatorios/RELATORIO_AUDITORIA_ADR-0016.md`;
- `docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md`;
- `docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md`;
- `docs/relatorios/RELATORIO_QA_H-0022_HANDOFF.md`;
- `docs/adr/INDICE_ADR.md`;
- trechos de `tela/demo.py` e `tela/teste_demo.py` somente para conferir as
  afirmações factuais sobre a implementação existente.

Nenhuma ADR anterior é citada diretamente pela ADR-0016. H-0009 e H-0021 são
handoffs, portanto foram usados como contratos/precedentes factuais de menor
autoridade, não como decisões do usuário equivalentes a ADR aceita.

## 4. Evidência da decisão do usuário

**Não localizada.** A ADR registra `rfc_origem: null` na linha 10 e aponta em
`issues_relacionadas` apenas o relatório de implementação IMP-0022 (linhas
11–12). Esse relatório comprova uma implementação anterior e seus mecanismos,
mas não comprova que o usuário escolheu os itens normativos 1–11, em especial:
`cbreak`, DECAWM, synchronized output, captura silenciosa de Ctrl+C, aceitação
do risco de não haver saída de emergência, divisão entre contratos e exclusão
de detecção de capacidade.

O contrato de processo atribui ao usuário a aprovação de decisões e proíbe
substituí-lo por inferência automática (linhas 41–48). A implementação, o
handoff atual e relatórios posteriores derivam da própria ADR ou têm autoridade
inferior; não são prova independente da decisão que a ADR pretende registrar.
Assim, não é possível determinar que a ADR apenas materializa uma decisão já
fechada, em vez de escolher política ou derivar arquitetura da implementação.

## 5. Comparação com a auditoria anterior

O relatório anterior corresponde a versão diferente. Evidências objetivas:

- ele se declara “segunda iteração” e relata versões anteriores nas linhas
  11–19;
- nas linhas 125–134 e 379–393, avalia redação que reservava H-0023 para
  `SIGWINCH`; a versão atual, linhas 183–193, afirma justamente que não há
  número reservado;
- nas linhas 233–239 e 394–419, avalia prosa que destinava os 11 itens também
  ao `contrato_console.md`; a versão atual, linhas 147–151, limita esse contrato
  ao item 9;
- o relatório anterior confirmou a inexistência de H-0022 (linhas 138–171),
  fato que deixou de ser atual depois da criação do arquivo atual.

Situação dos achados anteriores:

| Tema anterior | Resultado na versão atual |
|---|---|
| Ausência da seção Data | Corrigido; linhas 27–29. |
| Suposição de H-0022 anterior | A redação foi alterada, mas voltou a ficar factualmente falsa após a criação posterior do H-0022; achado atual QA-ADR16-02. |
| Texto narrativo em `handoffs_bloqueados` | Ainda aplicável e agora também desatualizado; absorvido por QA-ADR16-02. |
| Reserva ambígua de H-0023 | Corrigida nas linhas 183–193. |
| Amplitude contraditória de `contrato_console.md` | Corrigida nas linhas 147–151 e 164–166. |
| Contrato de tela não lido integralmente | Limitação eliminada neste QA. |
| Prescrição técnica excessiva | Continua relevante, mas torna-se parte do bloqueio por falta de decisão comprovada. |

Não há evidência no relatório anterior de que os trechos atuais tenham sido
reavaliados depois dessas alterações. Seu status anterior não é reutilizado.

## 6. Verificação item a item

| Verificação | Resultado | Evidência |
|---|---|---|
| Correspondência com decisão fechada | **NÃO VERIFICÁVEL** | ADR 10–12; contrato de processo 41–48; ausência de fonte independente. |
| Contexto e problema | **PARCIAL** | ADR 33–69 descreve a tentativa anterior, mas 41–48 usa presente desatualizado. |
| Decisão | **COERENTE INTERNAMENTE, NÃO AUTORIZADA** | ADR 71–135; não há evidência superior para validar as escolhas. |
| Consequências e preservações | **PARCIAL** | ADR 137–185; consequências sobre inexistência/abertura de handoff estão desatualizadas. |
| Compatibilidade com H-0009/H-0021 | **PARCIAL** | Preserva ramo não-TTY e vedação de bibliotecas, mas amplia a guarda de stdin para stdin+stdout e substitui `raw` por `cbreak`; isso exige decisão própria. |
| Contratos ativos | **PARCIAL** | Não há política TTY concorrente; porém `contrato_console.md:489–492` põe renderização terminal e decisões de buffer/refresh fora de seu escopo atual. O item 9 pode demandar outro contrato ou revisão explicitamente aprovada. |
| Duas políticas concorrentes | **NÃO**, no nível normativo ativo | A política nova ainda é proposta; a implementação existente não vira autoridade. |
| Aplicação prematura | **SIM, factual e externa à ADR** | Existem H-0022, implementação posterior e QA, embora a ADR siga `proposta`. A ADR não os aprova, mas sua narrativa não distingue esse estado atual. |
| Escopo funcional | **PARCIAL** | O núcleo limita-se à sessão TTY, mas o item 9 normatiza mecanismo para execução futura de script que a própria documentação posterior declara inexistente. |
| Implementação detalhada indevida | **PARCIAL** | ADR 77–115 prescreve APIs, sequências e quantidade de `write`/`flush`; sem evidência da decisão, não se pode distinguir decisão arquitetural de desenho de implementação. |
| Relação com itens 9 e 10 | **AMBÍGUA** | ADR 124–131 exige ignorar Ctrl+C mantendo a sessão e simultaneamente diz que o `finally` cobre esse evento. |
| Documentos afetados | **INCOMPLETO/DESATUALIZADO** | ADR 159–166 não identifica H-0022 e relatórios posteriores como artefatos já existentes que precisam de reconciliação documental. |
| Índice | **COERENTE COM QA, MAS EM TENSÃO COM A REGRA DO ÍNDICE** | `INDICE_ADR.md:13–17` diz registrar ADRs aceitas; linha 46 registra ADR-0016 como proposta. O status `proposta` é adequado durante QA e não é defeito isolado. |
| Fora de escopo | **ADEQUADO** | ADR 187–198 não reserva capacidades futuras nem amplia para Windows/terminfo. |

## 7. Achados por severidade

### QA-ADR16-01

```text
id: QA-ADR16-01
severidade: bloqueante
arquivo: docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
linhas: 10-12, 71-135, 154-157, 187-212
evidencia: rfc_origem é null; a única issue é um relatório de implementação; nenhuma evidência independente registra aprovação do usuário para as onze escolhas e para o risco aceito.
regra_afetada: contrato_processo_desenvolvimento.md:41-48; ordem de autoridade definida para este QA.
impacto: não é possível provar que a ADR registra decisão já fechada; aprová-la permitiria que engenharia/implementação substituíssem a decisão do usuário.
correcao_necessaria: vincular evidência verificável da decisão explícita do usuário cobrindo a política normativa, ou obter a decisão que falta antes de novo QA.
exige_decisao_do_usuario: sim
```

### QA-ADR16-02

```text
id: QA-ADR16-02
severidade: alto
arquivo: docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
linhas: 17-18, 37-48, 141-146, 152-153, 176-182
evidencia: a ADR afirma no presente que nenhum H-0022 existe e manda abrir um handoff novo; atualmente existe docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md (236 linhas), além de QA e implementação posteriores.
regra_afetada: correspondência com o estado factual atual e distinção entre contexto histórico e estado presente.
impacto: rastreabilidade, consequências e próxima ação documental ficam falsas ou ambíguas; um leitor pode tentar criar handoff duplicado.
correcao_necessaria: preservar como histórico a inexistência anterior, distinguir explicitamente o estado atual e reconciliar consequências/documentos afetados com os artefatos posteriores, sem tratá-los como autoridade superior.
exige_decisao_do_usuario: não
```

### QA-ADR16-03

```text
id: QA-ADR16-03
severidade: médio
arquivo: docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
linhas: 117-131
evidencia: o item 9 determina que Ctrl+C fora do escopo seja capturado e ignorado, mantendo a sessão; o item 10 diz que o finally cobre Ctrl+C fora desse escopo.
regra_afetada: coerência interna e critério inequívoco para aplicação.
impacto: pode-se interpretar que o mesmo Ctrl+C simultaneamente mantém a sessão e dispara restauração/saída; handoff e QA posteriores já registraram a ambiguidade.
correcao_necessaria: distinguir proteção lexical do loop pela restauração final da execução efetiva do finally e da permanência da sessão após Ctrl+C ignorado.
exige_decisao_do_usuario: não, se a intenção já estiver coberta por evidência explícita; caso contrário, sim.
```

### QA-ADR16-04

```text
id: QA-ADR16-04
severidade: médio
arquivo: docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
linhas: 121-126, 147-151, 164-165
evidencia: a ADR normatiza captura durante execução de script/processo interno e destina o item ao contrato_console, mas o H-0022:155-162 declara que esse fluxo não existe e contrato_console.md:489-492 exclui renderização terminal e decisões de buffer/refresh do escopo atual.
regra_afetada: escopo, capacidade futura e identificação correta do contrato afetado.
impacto: a ADR pode impor mecanismo futuro e ampliar contrato de módulo sem demonstrar que a capacidade pertence ao ciclo ou que esse é o limite documental correto.
correcao_necessaria: demonstrar pela decisão autorizada que o comportamento futuro integra este ciclo e identificar o contrato normativo correto; caso contrário, manter a capacidade futura fora da decisão atual.
exige_decisao_do_usuario: sim
```

### QA-ADR16-05

```text
id: QA-ADR16-05
severidade: baixo
arquivo: docs/adr/INDICE_ADR.md
linhas: 13-17, 46
evidencia: o índice declara registrar ADRs aceitas, mas inclui ADR-0016 como proposta.
regra_afetada: coerência do índice com sua própria finalidade.
impacto: mistura catálogo de decisões aceitas com propostas; não invalida o status proposta, que é adequado durante QA.
correcao_necessaria: após definição da política de indexação, manter propostas em seção própria ou ajustar a regra do índice; não promover a ADR antes da aprovação.
exige_decisao_do_usuario: não
```

### QA-ADR16-OBS-01

```text
id: QA-ADR16-OBS-01
severidade: observação
arquivo: docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
linhas: 6, 23-25
evidencia: status literal proposta no frontmatter e no corpo.
regra_afetada: estado documental durante QA.
impacto: nenhum defeito isolado; a ADR ainda não foi aprovada.
correcao_necessaria: nenhuma nesta etapa; só alterar o status no fluxo autorizado após aprovação.
exige_decisao_do_usuario: não
```

Contagem: 1 bloqueante, 1 alto, 2 médios, 1 baixo e 1 observação.

## 8. Contradições documentais

1. ADR 17–18, 41–48, 144–146 e 178–182 versus existência atual de
   `docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md`.
2. ADR 152–153 e 178–182 versus ciclo posterior já materializado em H-0022,
   IMP-0023 e relatórios de QA.
3. ADR 124–131: Ctrl+C é ignorado para manter a sessão, mas o `finally` é dito
   como cobrindo o mesmo evento sem distinguir cobertura lexical de execução.
4. ADR 121–126/147–151 versus H-0022 155–162: a ADR decide comportamento de
   execução interna; o handoff declara que tal funcionalidade ainda não existe.
5. `INDICE_ADR.md` 13–17 versus 46: índice declarado de aceitas contém proposta.

## 9. Documentos afetados após eventual aprovação

A lista mínima da ADR (linhas 159–166) contém:

- `docs/adr/INDICE_ADR.md`;
- `docs/contratos/contrato_tela_json.md`;
- `docs/contratos/contrato_console.md`;
- `docs/contratos/contrato_processo_desenvolvimento.md`.

Antes de aplicação, a versão corrigida também precisa identificar para
reconciliação, sem aprovação retroativa automática:

- `docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md`;
- `docs/relatorios/RELATORIO_QA_H-0022_HANDOFF.md`;
- `docs/relatorios/IMP-0023-implementacao-h0022-tela-cheia-tty.md`;
- `docs/relatorios/RELATORIO_QA_H-0022_IMPLEMENTACAO.md`;
- `tela/demo.py` e `tela/teste_demo.py`, apenas como implementação a validar em
  etapa própria posterior.

## 10. Estado Git observado

```text
branch: master
HEAD: 0b09fa6a99a6d0ed61e9488ecb7e78f16d37cfdf

git status --short (antes da criação deste relatório):
 M docs/adr/INDICE_ADR.md
 M tela/demo.py
 M tela/teste_demo.py
?? docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
?? docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
?? docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md
?? docs/relatorios/IMP-0023-implementacao-h0022-tela-cheia-tty.md
?? docs/relatorios/RELATORIO_AUDITORIA_ADR-0016.md
?? docs/relatorios/RELATORIO_QA_H-0022_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_H-0022_IMPLEMENTACAO.md
```

O HEAD coincide com o levantamento, mas foi observado novamente. Não houve
`git add`, alteração de stage ou commit. O diff do índice confirma que a linha
da ADR-0016 ainda é modificação não commitada. O relatório atual passa a
aparecer adicionalmente como arquivo não rastreado após sua criação.

## 11. Arquivos alterados nesta etapa

Somente:

`docs/relatorios/RELATORIO_QA_ADR-0016_POS_AJUSTES.md`

## 12. Status final

`BLOCKED_USER_DECISION`

Fundamento determinante: falta evidência verificável de decisão explícita do
usuário que autorize as escolhas normativas registradas. Há ainda defeitos
fatuais corrigíveis, mas eles não removem nem substituem esse bloqueio.

## 13. Próxima categoria processual

`AGUARDAR_DECISAO_USUARIO`

Esta categoria é apenas registrada; não foi executada.
