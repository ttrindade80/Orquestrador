# Relatório de QA do Handoff H-0022 — Pós Base Documental Aprovada

## 1. Identificação da etapa

```yaml
etapa: QA_HANDOFF
projeto: Orquestrador
ciclo: H-0022 / ADR-0016
data: 2026-07-11
relatorio_criado: docs/relatorios/RELATORIO_QA_H-0022_HANDOFF_POS_BASE_DOCUMENTAL.md
handoff_auditado: docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
qa_historico_preservado: docs/relatorios/RELATORIO_QA_H-0022_HANDOFF.md
```

Esta auditoria avalia somente o handoff H-0022 na versão de 236 linhas. Não
corrige o handoff, não altera ADR, contratos, índice ou relatórios anteriores,
não audita a implementação existente, não executa validação manual, não prepara
commit e não inicia etapa posterior.

---

## 2. Versão e hash do handoff auditado

Comandos executados antes da auditoria:

```text
wc -l docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
236 docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md

sha256sum docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
ba37585352bdc16d91d1f883ebba85a9c97e85d813ce52ebd02b09de55f9f7fe  docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
```

Versão confirmada:

```yaml
arquivo: docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
linhas: 236
sha256: ba37585352bdc16d91d1f883ebba85a9c97e85d813ce52ebd02b09de55f9f7fe
status_literal: proposto
correspondencia_com_levantamento: SIM
```

---

## 3. Estado Git

Comandos executados:

```text
git branch --show-current
master

git rev-parse HEAD
0b09fa6a99a6d0ed61e9488ecb7e78f16d37cfdf

git status --short
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_console.md
 M docs/contratos/contrato_processo_desenvolvimento.md
 M docs/contratos/contrato_tela_json.md
 M tela/demo.py
 M tela/teste_demo.py
?? docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
?? docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
?? docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md
?? docs/relatorios/IMP-0023-implementacao-h0022-tela-cheia-tty.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0016.md
?? docs/relatorios/RELATORIO_AUDITORIA_ADR-0016.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_CONSISTENCIA_H-0022.md
?? docs/relatorios/RELATORIO_QA_ADR-0016_POS_AJUSTES.md
?? docs/relatorios/RELATORIO_QA_ADR-0016_POS_PATCH.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0016.md
?? docs/relatorios/RELATORIO_QA_H-0022_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_H-0022_IMPLEMENTACAO.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0016.md

git diff --check
(sem saída)

git diff --cached --name-only
(sem saída)
```

Conclusão: branch `master`, HEAD `0b09fa6`, workspace sujo preexistente, stage
vazio. O handoff H-0022 é não rastreado (??), coerente com sua criação como
artefato de ciclo ainda não commitado. Nenhuma alteração atribuída a esta
auditoria além do relatório presente.

---

## 4. Autoridades consultadas

Lidos integralmente como autoridade:

```text
docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md          (aceita)
docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md              (auditado)
docs/contratos/contrato_tela_json.md                                  (ativo, seção 23)
docs/contratos/contrato_console.md                                    (ativo, item 9)
docs/contratos/contrato_processo_desenvolvimento.md                   (modelo ativo)
docs/relatorios/RELATORIO_QA_ADR-0016_POS_PATCH.md                   (histórico)
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0016.md                   (histórico)
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0016.md         (histórico)
docs/relatorios/RELATORIO_QA_H-0022_HANDOFF.md                       (histórico)
```

Lido somente como referência histórica:

```text
docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md    (não normativo)
```

Ordem de autoridade aplicada:
1. ADR-0016 aceita
2. Contratos ativos pós-aplicação da ADR (`contrato_tela_json.md` seção 23,
   `contrato_console.md` item 10, `contrato_processo_desenvolvimento.md`)
3. Regras processuais vigentes
4. Handoff H-0022 (auditado)
5. Relatórios como evidência histórica
6. IMP-0022 apenas como fato histórico, sem autoridade normativa

---

## 5. Estado da base documental

```yaml
adr_0016: aceita (QA_ADR_APROVADO em RELATORIO_QA_ADR-0016_POS_PATCH.md)
aplicacao_adr: ADR_APPLICATION_APPROVED (resultado normalizado em
               RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0016.md)
contrato_tela_json: secao_23_inserida_e_aprovada
contrato_console: item_10_inserido_aprovado (achado renumeracao RESOLVIDO)
contrato_processo: secao_7_inserida_aprovada
indice_adr: ADR-0016_registrada_como_aceita
estado_documental: BASE_DOCUMENTAL_APROVADA
```

---

## 6. QA histórico e achado anterior

```yaml
qa_historico:
  arquivo: docs/relatorios/RELATORIO_QA_H-0022_HANDOFF.md
  versao_auditada_pelo_historico: 216 linhas
  status_historico: BLOQUEADO
  achado_bloqueante: ACH-BLOQ-01
```

Texto do achado bloqueante histórico (recuperado do relatório original):

```text
ACH-BLOQ-01 — Item 7 aceita zero limpezas de tela

Texto problemático (versão 216 linhas):
  a sequência `\x1b[2J` ocorre "no máximo uma vez".

Regra da ADR:
  limpeza ocorre "uma única vez, na entrada da sessão" — zero é não conformidade.

Impacto: implementação sem `\x1b[2J` satisfaria o handoff, mas violaria a ADR.
```

Verificação na versão atual (236 linhas, linhas 137-142):

```text
- [ ] A sequência de limpeza de tela (`\x1b[2J`) ocorre **exatamente uma vez**
      em `demo.py`, na inicialização da sessão TTY — nunca dentro do loop de
      redesenho (inspeção: a string `\x1b[2J` aparece exatamente uma vez no
      arquivo, fora da lógica de loop; ausência total da sequência é não
      conformidade, não conformidade parcial).
```

Verificação nos testes automatizados (linhas 211-213):

```text
- [ ] Os testes cobrem: ... escrita atômica com `\x1b[2J` presente exatamente
      uma vez e fora do loop (inspeção de código) ...
```

Classificação do achado histórico:

```text
ACH-BLOQ-01: RESOLVIDO
```

A versão atual exige "exatamente uma vez", proíbe explicitamente ausência total
e estende a exigência aos testes automatizados. O critério é agora coerente com
a ADR-0016 item 7.

---

## 7. Matriz ADR-0016 → Handoff H-0022

| item_adr | linhas_adr | criterios_handoff | resultado | omissoes | ampliacoes | contradicoes | verificabilidade |
|---|---|---|---|---|---|---|---|
| 1. Guarda dupla TTY | 73-75 | linhas 80-86 | COBERTO_FIELMENTE | nenhuma | nenhuma | nenhuma | inspeção + comando pipe |
| 2. cbreak, não raw | 77-80 | linhas 87-94 | COBERTO_FIELMENTE | nenhuma | nenhuma | nenhuma | inspeção código + manual |
| 3. Alternate screen e cursor | 82-85 | linhas 97-103 | COBERTO_FIELMENTE | nenhuma | nenhuma | nenhuma | inspeção código + manual |
| 4. DECAWM desativado/restaurado | 87-90 | linhas 104-112 | COBERTO_FIELMENTE | nenhuma | nenhuma | nenhuma | inspeção código + manual |
| 5. Posicionamento absoluto | 92-96 | linhas 113-122 | COBERTO_FIELMENTE | nenhuma | nenhuma | nenhuma | inspeção código + manual |
| 6. Preenchimento até largura | 98-102 | linhas 124-131 | COBERTO_FIELMENTE | nenhuma | nenhuma | nenhuma | inspeção código + manual |
| 7. Escrita atômica; limpeza única | 104-109 | linhas 133-144 | COBERTO_FIELMENTE | nenhuma | nenhuma | nenhuma | inspeção código + manual |
| 8. Synchronized output | 111-115 | linhas 146-153 | COBERTO_FIELMENTE | nenhuma | nenhuma | nenhuma | inspeção código |
| 9. Ctrl+C escopado | 117-126 | linhas 155-183 | COBERTO_FIELMENTE | nenhuma | nenhuma | nenhuma | inspeção código + teste |
| 10. Restauração em finally | 128-134 | linhas 185-194 | COBERTO_PARCIALMENTE | nenhuma | nenhuma | ambiguidade Ctrl+C/finally (F-MED-002) | inspeção código + manual |
| 11. Não-TTY preservado | 136-138 | linhas 196-205 | COBERTO_FIELMENTE | nenhuma | nenhuma | nenhuma | comandos pipe |

---

## 8. Capacidade coesa

O handoff trata somente a capacidade:

```text
correção da execução em tela cheia TTY conforme ADR-0016
```

Verificações de escopo indevido:

| Tema | Presença no handoff | Classificação |
|---|---|---|
| SIGWINCH | Fora de escopo explícito (linha 229) | exclusão correta |
| Navegação por setas | ausente | correto (H-0009 já normatizou) |
| Mouse | ausente | correto |
| Nova arquitetura de console | ausente | correto |
| Execução real de scripts | exclusão explícita (linhas 157-161) | exclusão correta |
| Windows | Fora de escopo explícito (linha 233) | exclusão correta |
| terminfo | Fora de escopo explícito (linha 234) | exclusão correta |
| curses / textual / rich | Fora de escopo explícito (linha 235) | exclusão correta |
| Alteração declarativa de telas | ausente | correto |
| Ciclo futuro | ausente | correto |

Resultado: **capacidade coesa** — o handoff não inclui indevidamente nenhum
tema fora da ADR-0016.

---

## 9. Escopo positivo

O handoff identifica:

- **Módulos alteráveis**: `tela/demo.py` e `tela/teste_demo.py` (linhas 62-69,
  exaustiva por declaração).
- **Comportamento a implementar**: itens 1-11 da seção Decisão da ADR-0016,
  traduzidos em critérios observáveis por item.
- **Testes a atualizar**: `tela/teste_demo.py` — cobertura mínima dos 11 itens
  (linhas 207-218).
- **Preservações obrigatórias**: comportamento não-TTY (Item 11), stash das
  alterações anteriores antes de iniciar (linhas 44-59), IMP-0022 como
  histórico.
- **Comandos de validação**: pipe tests em vários itens, inspeções por string,
  verificações marcadas explicitamente como "verificação manual de QA".
- **Condição de bloqueio principal**: `ARCHITECTURE_REVIEW_REQUIRED` se a
  implementação exigir arquivo além dos dois permitidos (linhas 71-72).

São `tela/demo.py` e `tela/teste_demo.py` suficientes para a implementação
técnica? **Sim.** A ADR-0016 não exige alteração de contratos, ADRs, config
ou outros módulos. Todos os itens 1-11 são implementáveis nesses dois arquivos.

---

## 10. Escopo negativo e arquivos proibidos

O handoff proíbe alteração em (linhas 71-72 + linhas 222-226):

| Categoria | Proibição |
|---|---|
| ADR | explícita ("nenhum ... ADR ... foi alterado") |
| Contratos | explícita ("nenhum contrato ... foi alterado") |
| Índice de ADR | explícita ("nenhum ... índice de ADR ... foi alterado") |
| Outros módulos | implícita pela lista exaustiva |
| config/ | explícita ("qualquer arquivo em `config/`") |
| Artefatos históricos | explícita ("relatório anterior") |
| Funcionalidades fora da ADR | implícita pela cláusula exaustiva |

**Incoerência normativa (F-ALTO-001)**: a cláusula "A lista acima é exaustiva"
(linha 70) aplica-se a "arquivos que podem ser criados ou alterados na
implementação deste handoff" e lista apenas dois arquivos técnicos. O handoff
não carve-out explicitamente os artefatos obrigatórios de processo — em
particular, o relatório de implementação exigido pelo
`contrato_processo_desenvolvimento.md` seção 5. Lida literalmente, a cláusula
exaustiva pode ser interpretada como proibindo a criação do relatório de
implementação. Adicionalmente, o handoff não possui seção "Relatório de
implementação esperado" (ver Verificação 11 e Achado F-ALTO-001).

---

## 11. Relatório de implementação esperado

Verificação sistemática:

| Requisito da verificação | Presente no handoff? |
|---|---|
| Declaração de que deve existir relatório de implementação | NÃO |
| Nome ou regra inequívoca para o caminho do relatório | NÃO |
| Conteúdo mínimo do relatório | NÃO |
| Arquivos alterados a documentar | NÃO |
| Testes executados e resultados | NÃO |
| Ressalvas e bloqueios a documentar | NÃO |
| Validações manuais pendentes a documentar | NÃO |
| Proibição de autoavaliação formal | NÃO |
| Proibição de aprovar a própria implementação | NÃO |

Resultado: o handoff não define o relatório de implementação em nenhum aspecto.
O `contrato_processo_desenvolvimento.md` seção 5 exige "Produzir relatório de
implementação" como etapa obrigatória do ciclo, mas o handoff não traduz essa
obrigação em orientação específica para o executor.

A existência posterior de `docs/relatorios/IMP-0023-implementacao-h0022-tela-cheia-tty.md`
no workspace não corrige retroativamente essa omissão do handoff. Seu conteúdo
não é avaliado nesta etapa.

---

## 12. Verificação — Autoridade e rastreabilidade

### Referência à ADR-0016

Frontmatter (linha 9): `adr_base: docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md` ✓

Corpo (linhas 21-24): objetivo referencia explicitamente "itens 1-11 da seção
Decisão da ADR-0016" ✓

### Respeito ao contrato_tela_json.md seção 23

Todos os 11 itens da seção 23 do contrato encontram critério correspondente no
handoff. Nenhuma contradição com o contrato foi identificada nos critérios
implementáveis (ver F-MED-002 para ambiguidade narrativa).

### Recorte do Item 9 em contrato_console.md

O handoff exige o mecanismo reutilizável de captura de `KeyboardInterrupt`
(linhas 166-172) e o teste isolado desse mecanismo (linhas 179-183), sem
inventar fluxo de execução real. Isso é coerente com o Item 10 do
`contrato_console.md` (seção inserida pela aplicação da ADR-0016), que
normatiza exclusivamente o escopo do Ctrl+C durante execução de script interno.

### Processo de desenvolvimento

O handoff segue a estrutura esperada: critérios observáveis, lista exaustiva
de arquivos, pré-requisito documentado (stash), condição de bloqueio definida.
A ausência de seção de relatório de implementação é achado separado (F-ALTO-001).

### IMP-0022 somente como precedente histórico

Frontmatter (linhas 13-14): `implementacao_anterior` aponta IMP-0022.
Corpo (linhas 38-43): "citado apenas como **evidência histórica do problema**".
Correto — IMP-0022 não é tratado como autoridade normativa.

### Seção "Relação com a implementação anterior" — análise temporal

Texto auditado (linhas 33-43):

```text
Não existe handoff H-0022 anterior a corrigir. Este documento é a **primeira
vez que um handoff cobre este escopo**. Nunca houve arquivo
`docs/handoff/H-0022-*.md` no repositório — a ADR-0016 confirma explicitamente
essa ausência no campo `handoffs_bloqueados` de sua rastreabilidade.
```

**Achado F-MED-001**: a afirmação "a ADR-0016 confirma explicitamente essa
ausência no campo `handoffs_bloqueados`" é factualmente imprecisa. O campo
`handoffs_bloqueados` da ADR-0016 (linha 18 da ADR) LISTA o caminho
`docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md` — isto é, aponta
estruturalmente para o H-0022 como handoff dependente da ADR, não confirma
sua ausência. Além disso, a seção Consequências da ADR (linhas 154-158) afirma
explicitamente: "O H-0022 foi posteriormente criado em
`docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md`". A ADR confirma a
existência estrutural do H-0022, não sua inexistência.

A afirmação historicamente correta seria: antes deste handoff, a tentativa
registrada em IMP-0022 não tinha handoff precedente; a ADR aponta
estruturalmente para o H-0022 como handoff bloqueado (dependente) por ela.

---

## 13. Verificação — Itens 9 e 10 (Ctrl+C e finally)

### Item 9 (linhas 155-183)

O handoff:
- Identifica corretamente que não existe fluxo real de execução de script em
  `tela/demo.py` (linhas 157-161).
- Exige somente o mecanismo reutilizável, sem inventar o fluxo real (linhas
  162-172).
- Exige `ISIG` não desligado por inspeção de código (linhas 164-165).
- Exige captura silenciosa de `KeyboardInterrupt` fora do mecanismo, com sessão
  permanecendo ativa (linhas 173-175).
- Exige teste isolado do mecanismo (linhas 179-183).

O critério "pelo menos um bloco `except KeyboardInterrupt` fora do `finally`"
(linhas 176-178) é mais estreito que o comportamento esperado — favorece
inspeção estrutural em vez de teste comportamental. Anotado como F-BAIX-002,
não bloqueante.

### Item 10 (linhas 185-194)

Segundo critério (linha 191):
```text
- [ ] O bloco `finally` de restauração cobre saída normal (Esc), qualquer
      exceção não tratada, e Ctrl+C fora de escopo de script.
```

**Achado F-MED-002**: listar "Ctrl+C fora de escopo de script" como um dos
eventos que o `finally` "cobre" sugere que esse evento DESENCADEIA a execução
do `finally`. Isto contradiz:

- ADR-0016, linhas 132-134: "Ctrl+C fora do escopo de script continua sendo
  capturado e ignorado no loop (item 9), mantendo a sessão ativa e sem
  executar imediatamente a restauração; o `finally` executa quando o loop
  efetivamente termina, por Esc ou por exceção não tratada."
- `contrato_tela_json.md`, linhas 689-693: "Ctrl+C ignorado no loop mantém
  a sessão ativa e não executa imediatamente a restauração do terminal; ...
  executa quando o loop efetivamente termina."

A ambiguidade persiste não resolvida em relação à ressalva RESS-01 do QA
histórico. A leitura conjunta de Item 9 (sessão permanece ativa) e Item 10
permite que um implementor cuidadoso chegue à implementação correta, mas o
critério do Item 10 isolado é enganoso. Não há cenário de teste no handoff que
diferencie "proteção lexical do loop" de "Ctrl+C ignorado dispara restauração".

---

## 14. Verificação — Critérios de aceite

| Item | Observável | Verificável | Objetivo | Livre de termos vagos | Suficiente |
|---|---|---|---|---|---|
| 1 | Sim | Sim (inspeção + pipe) | Sim | Sim | Sim |
| 2 | Sim | Sim (inspeção + manual) | Sim | Sim | Sim |
| 3 | Sim | Sim (inspeção + manual) | Sim | Sim | Sim |
| 4 | Sim | Sim (inspeção + manual) | Sim | Sim | Sim |
| 5 | Sim | Sim (inspeção + manual) | Sim | Sim | Sim |
| 6 | Sim | Sim (inspeção + manual) | Sim | Sim | Sim |
| 7 | Sim | Sim (inspeção: conta exata) | Sim | Sim | Sim |
| 8 | Sim | Sim (inspeção) | Sim | Sim | Sim |
| 9 | Sim | Sim (inspeção + teste) | Sim | Sim | Sim |
| 10 | Parcial | Parcial (F-MED-002) | Parcial | Parcial | Parcial |
| 11 | Sim | Sim (comandos pipe) | Sim | Sim | Sim |

Separação entre automatizado e manual: correta. As verificações marcadas como
"verificação manual de QA" são explicitamente distinguidas de testes
automatizados. Testes automatizados não são apresentados como substitutos para:
ausência de cintilação visual, restauração perceptível, alinhamento real, scroll
na última coluna, resíduos de quadro ou estado final do terminal. ✓

---

## 15. Verificação — Testes obrigatórios (linhas 207-218)

| Requisito | Presente |
|---|---|
| `python tela/teste_demo.py` retorna código 0 | Sim (linha 209) |
| Comandos pipe não-TTY | Sim (Item 11, linhas 197-205) |
| Contagem exata de `\x1b[2J` (exatamente uma vez) | Sim (linha 212) |
| Ausência de `setraw` | Sim (linha 211) |
| Cobertura dos itens aplicáveis | Sim (linhas 210-218) |
| Critérios manuais explicitamente separados | Sim (marcação "(verificação manual de QA)") |

Os testes descritos cobrem o comportamento exigido sem prescrever implementação
incompatível com a ADR. ✓

---

## 16. Verificação — Preservações

| Preservação | Presente no handoff |
|---|---|
| Comportamento não-TTY | Sim (Item 11) |
| Conteúdo anterior do terminal após alternate screen | Sim (Item 3, manual QA: "conteúdo pré-sessão") |
| termios original | Sim (Item 10: "atributos `termios` originais") |
| Cursor | Sim (Item 10 e Item 3) |
| Autowrap | Sim (Item 4) |
| Esc como saída normatizada | Implícito em Item 9/10; herdado de H-0009 |
| Stash histórico sem aplicação/remoção | Sim (linhas 53-58: "podem ser consultadas como referência histórica") |
| Ausência de fluxo real de script | Sim (linhas 157-161: proibição de inventar) |
| Proibições herdadas de H-0009 (curses/textual/rich) | Sim (linha 235: "permanecem proibidas conforme H-0009") |

---

## 17. Verificação — Condições de bloqueio

| Condição | Instrução no handoff |
|---|---|
| Arquivos permitidos insuficientes | Sim: `ARCHITECTURE_REVIEW_REQUIRED` (linhas 71-72) |
| Necessidade de nova decisão arquitetural | Parcial: coberto por `ARCHITECTURE_REVIEW_REQUIRED` se exigir outro arquivo |
| Contradição entre autoridades | Não explicitada |
| Alterar arquivo proibido | Coberto pela cláusula exaustiva |
| Versão de entrada ou estado do repositório não corresponder | Não explicitado |
| Stash obrigatório falhar | Não explicitado |

`ARCHITECTURE_REVIEW_REQUIRED` é usado apenas para lacuna estrutural (precisar
de arquivo além dos dois permitidos), não para falha operacional. Uso adequado.

Condições não explicitadas são anotadas como F-BAIX-001. O
`contrato_processo_desenvolvimento.md` seção 9 cobre operacionalmente os casos
omitidos; a ausência no handoff cria possível lacuna para executores que não
releiam o contrato.

---

## 18. Verificação — Ausência de implementação antecipada

| Verificação | Resultado |
|---|---|
| Código de implementação pronto | Ausente ✓ |
| Execução do stash | Explicitamente não executa (linha 57) ✓ |
| Modificação de código | Ausente ✓ |
| QA da implementação | Ausente ✓ |
| Aprovação da implementação | Ausente ✓ |
| Preparação de commit | Ausente ✓ |
| Início de ciclo futuro | Ausente ✓ |

Sequências ANSI normativas (ex.: `\x1b[?1049h`) presentes como critérios de
inspeção de código, não como implementação antecipada. ✓

---

## 19. Verificação — Metadados e status

| Campo | Valor | Resultado |
|---|---|---|
| `metadata.type` | handoff | conforme |
| `metadata.status` | proposto | conforme — status correto para handoff em QA |
| `metadata.data` | 2026-07-10 | conforme |
| `rastreabilidade.adr_base` | ADR-0016 (caminho correto) | conforme |
| `rastreabilidade.escopo_permitido` | tela/demo.py, tela/teste_demo.py | conforme |
| `rastreabilidade.implementacao_anterior` | IMP-0022 (como histórico) | conforme |
| Identificação H-0022 | nome do frontmatter e título | conforme |

O status `proposto` é a convenção correta para handoff ainda não aprovado por
QA. O arquivo não deve se automarcar como aprovado antes do QA. ✓

---

## 20. Achados por severidade

### Alto

```text
id: F-ALTO-001
severidade: alto
arquivo: docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
linhas: 62-72 (cláusula exaustiva) + ausência de seção de relatório
evidencia: |
  A cláusula "A lista acima é exaustiva" (linha 70) seguida de lista com
  somente tela/demo.py e tela/teste_demo.py não carve-out explicitamente
  os artefatos obrigatórios de processo. Lida literalmente, proíbe a criação
  de qualquer outro arquivo incluindo o relatório de implementação exigido
  pelo contrato_processo_desenvolvimento.md seção 5.

  O handoff não possui seção "Relatório de implementação esperado" e não
  define em nenhuma linha: que deve existir relatório, qual seu caminho/nome,
  qual conteúdo mínimo, que validações manuais documentar, nem proibição
  de autoavaliação.
autoridade_afetada: |
  contrato_processo_desenvolvimento.md seção 5 (etapa obrigatória:
  "Produzir relatório de implementação")
impacto_na_implementacao_ou_qa: |
  Executor seguindo somente o handoff: (a) pode interpretar a cláusula
  exaustiva como proibindo a criação do relatório de implementação; e/ou
  (b) não tem orientação sobre nome, caminho, conteúdo mínimo, proibição
  de autoavaliação. A conformidade com o processo fica dependente de o
  executor reler o contrato de processo por conta própria.
correcao_necessaria: |
  Acrescentar ao handoff: (1) carve-out explícito na cláusula exaustiva
  distinguindo arquivos técnicos da capacidade de artefatos obrigatórios
  de processo; (2) seção "Relatório de implementação esperado" com nome/
  regra de caminho, conteúdo mínimo, proibição de autoavaliação e proibição
  de aprovar a própria implementação.
exige_decisao_do_usuario: nao
```

### Médios

```text
id: F-MED-001
severidade: medio
arquivo: docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
linhas: 35-36
evidencia: |
  Seção "Relação com a implementação anterior", linhas 35-36:
  "a ADR-0016 confirma explicitamente essa ausência no campo
  `handoffs_bloqueados` de sua rastreabilidade."

  Fato verificável na ADR-0016 linha 18:
  handoffs_bloqueados:
    - docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md

  O campo `handoffs_bloqueados` LISTA o H-0022, indicando o handoff como
  dependente/bloqueado pela ADR — não confirma sua ausência. Adicionalmente,
  a seção Consequências da ADR (linhas 154-158) afirma:
  "O H-0022 foi posteriormente criado em
  `docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md`".
  A ADR confirma a existência estrutural do H-0022, não sua ausência.
autoridade_afetada: ADR-0016 (autoridade máxima do ciclo)
impacto_na_implementacao_ou_qa: |
  A afirmação imprecisa está em seção narrativa de contexto, não em critério
  de aceite ou escopo. Não bloqueia a implementação técnica, mas introduz
  afirmação factualmente incorreta sobre o que a autoridade máxima (ADR-0016)
  diz, o que pode confundir leitores futuros sobre a relação entre a ADR e
  este handoff.
correcao_necessaria: |
  Substituir "a ADR-0016 confirma explicitamente essa ausência no campo
  `handoffs_bloqueados` de sua rastreabilidade" por redação que reflita a
  realidade: antes deste handoff, nenhum handoff cobria este escopo; a
  ADR-0016 aponta estruturalmente para o H-0022 como handoff dependente por
  ela, não confirma sua inexistência.
exige_decisao_do_usuario: nao
```

```text
id: F-MED-002
severidade: medio
arquivo: docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
linhas: 189-191
evidencia: |
  Item 10, segundo critério (linha 191):
  "O bloco `finally` de restauração cobre saída normal (Esc), qualquer
  exceção não tratada, e Ctrl+C fora de escopo de script."

  A listagem de "Ctrl+C fora de escopo de script" como evento que o
  `finally` "cobre" implica que esse evento desencadeia a execução do
  `finally`. Esta implicação contradiz:

  ADR-0016 linhas 132-134:
  "Ctrl+C fora do escopo de script continua sendo capturado e ignorado
  no loop (item 9), mantendo a sessão ativa e sem executar imediatamente
  a restauração; o `finally` executa quando o loop efetivamente termina,
  por Esc ou por exceção não tratada."

  contrato_tela_json.md linhas 689-693:
  "Ctrl+C ignorado no loop mantém a sessão ativa e não executa imediatamente
  a restauração do terminal; ... executa quando o loop efetivamente termina."

  Ambiguidade persiste não resolvida desde a ressalva RESS-01 do QA histórico.
  O handoff não inclui cenário de teste que diferencie proteção lexical de
  execução efetiva do finally por Ctrl+C.
autoridade_afetada: |
  ADR-0016 item 10 e contrato_tela_json.md seção 23 (linhas 689-693)
impacto_na_implementacao_ou_qa: |
  Lendo somente o critério do Item 10 isolado, um implementor poderia
  concluir que Ctrl+C fora de escopo encerra a sessão e restaura o terminal.
  A leitura conjunta de Item 9 e Item 10 dá o comportamento correto, mas
  o critério do Item 10 isolado é enganoso. O QA da implementação também
  fica sem cenário de teste que valide a distinção.
correcao_necessaria: |
  Reformular o segundo critério do Item 10 para deixar claro que o
  `finally` protege LEXICALMENTE o loop e executa quando o loop termina
  (por Esc ou exceção não tratada) — não quando Ctrl+C é ignorado, pois
  nesse caso a sessão permanece ativa. Acrescentar critério de teste que
  distinga proteção lexical de execução efetiva do finally.
exige_decisao_do_usuario: nao
```

### Baixos

```text
id: F-BAIX-001
severidade: baixo
arquivo: docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
linhas: 71-72
evidencia: |
  O handoff define somente uma condição de bloqueio explícita:
  `ARCHITECTURE_REVIEW_REQUIRED` se a implementação exigir alterar outro
  arquivo. Não instrui o executor a parar quando:
  - o stash obrigatório (linha 52) falhar;
  - houver contradição entre autoridades durante a execução;
  - o estado do repositório (versão dos arquivos) não corresponder ao
    esperado antes de iniciar.
autoridade_afetada: contrato_processo_desenvolvimento.md seção 9
impacto_na_implementacao_ou_qa: |
  O contrato de processo já cobre esses casos operacionalmente; um executor
  que releia o contrato não ficará bloqueado. A omissão cria lacuna para
  executor que siga somente o handoff.
correcao_necessaria: |
  Acrescentar condições de bloqueio: falha no stash → BLOCKED;
  contradição entre autoridades → ARCHITECTURE_REVIEW_REQUIRED;
  versão de arquivo não corresponder → parar e reportar.
exige_decisao_do_usuario: nao
```

```text
id: F-BAIX-002
severidade: baixo
arquivo: docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
linhas: 176-178
evidencia: |
  Critério do Item 9: "demo.py contém pelo menos um bloco
  `except KeyboardInterrupt` fora do `finally` de restauração do terminal".
  Este critério estrutural (presença de um bloco Python específico) é mais
  estreito que o comportamento esperado pela ADR (captura e ignorância
  silenciosa de KeyboardInterrupt no loop). Testes comportamentais — como
  simular o evento e verificar que a sessão permanece ativa — forneceriam
  evidência mais robusta.
  Herdado de RESS-03 do QA histórico; persiste não resolvido.
autoridade_afetada: ADR-0016 item 9
impacto_na_implementacao_ou_qa: |
  Implementação que capture KeyboardInterrupt de outra forma válida (ex.:
  signal.signal) poderia satisfazer o comportamento mas falhar no critério
  estrutural. Risco baixo dado que `except KeyboardInterrupt` é a forma
  natural em Python puro.
correcao_necessaria: |
  Complementar o critério estrutural com critério comportamental: verificar
  que após `KeyboardInterrupt` simulado no loop, a sessão continua ativa
  e o `finally` não é executado.
exige_decisao_do_usuario: nao
```

### Observações

```text
id: OBS-001
severidade: observacao
arquivo: docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
linhas: 52-59
evidencia: |
  O pré-requisito de stash (linha 52: `git stash push -m "pre-H-0022"
  -- tela/demo.py tela/teste_demo.py`) não define o comportamento esperado
  se já existir entrada de stash com a mesma mensagem, nem se o stash
  falhar por workspace inesperadamente limpo. São casos de borda de baixo
  impacto prático, pois o executor inspeciona o git status antes de iniciar.
correcao_necessaria: nenhuma obrigatória
exige_decisao_do_usuario: nao
```

---

## 21. Comparação com o QA histórico — Resumo

| Achado histórico | Versão histórica | Versão atual | Classificação |
|---|---|---|---|
| ACH-BLOQ-01 (Item 7: "no máximo uma vez") | BLOQUEANTE | Corrigido: "exatamente uma vez" + "ausência total é não conformidade" | RESOLVIDO |
| RESS-01 (ambiguidade Ctrl+C / finally) | Ressalva não bloqueante | Persiste (F-MED-002) | NAO_RESOLVIDO |
| RESS-02 (cenário de script não concretizado) | Ressalva não bloqueante | Resolvido: seção de escopo em Item 9 esclarece que mecanismo existe sem fluxo real | RESOLVIDO |
| RESS-03 (critério estrutural estreito em Item 9) | Ressalva não bloqueante | Persiste (F-BAIX-002) | NAO_RESOLVIDO |

---

## 22. Arquivos lidos nesta auditoria

```text
docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_console.md                           (primeiras 100 linhas)
docs/contratos/contrato_processo_desenvolvimento.md          (primeiras 150 linhas)
docs/relatorios/RELATORIO_QA_ADR-0016_POS_PATCH.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0016.md
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0016.md
docs/relatorios/RELATORIO_QA_H-0022_HANDOFF.md
docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md  (50 linhas — histórico)
```

---

## 23. Arquivos alterados nesta auditoria

Somente:

```text
docs/relatorios/RELATORIO_QA_H-0022_HANDOFF_POS_BASE_DOCUMENTAL.md
```

O relatório histórico `docs/relatorios/RELATORIO_QA_H-0022_HANDOFF.md`
permanece inalterado como evidência da auditoria da versão de 216 linhas.

---

## 24. Status final

```text
H2_HANDOFF_PATCH_REQUIRED
```

Justificativa: o handoff resolve o achado bloqueante histórico (ACH-BLOQ-01)
e é tecnicamente implementável para os 11 itens da ADR-0016. Entretanto,
contém defeitos corrigíveis pelas autoridades já aprovadas:

- **F-ALTO-001** (alto): ausência de seção "Relatório de implementação
  esperado" e ambiguidade da cláusula exaustiva quanto ao escopo de artefatos
  de processo. O contrato_processo_desenvolvimento.md exige o relatório de
  implementação como etapa obrigatória; o handoff não traduz essa obrigação
  nem carve-out os artefatos de processo da cláusula exaustiva.

- **F-MED-001** (médio): afirmação factualmente incorreta sobre o que a ADR
  confirma no campo `handoffs_bloqueados`.

- **F-MED-002** (médio): ambiguidade persistente no critério do Item 10 sobre
  a relação entre Ctrl+C ignorado e a execução do `finally` — contradiz
  explicitamente o contrato_tela_json.md seção 23.

Todos os defeitos são corrigíveis usando as autoridades já aprovadas (ADR-0016
aceita, contratos ativos, processo vigente) sem necessidade de nova decisão
material do usuário.

---

## 25. Próxima categoria

```text
PATCH_HANDOFF
```

---

## 26. Saída final ao gerente

```text
status: H2_HANDOFF_PATCH_REQUIRED
relatorio: docs/relatorios/RELATORIO_QA_H-0022_HANDOFF_POS_BASE_DOCUMENTAL.md
handoff_auditado: docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
versao_auditada:
  linhas: 236
  sha256: ba37585352bdc16d91d1f883ebba85a9c97e85d813ce52ebd02b09de55f9f7fe
  status_literal: proposto
base_documental: BASE_DOCUMENTAL_APROVADA
qa_historico: docs/relatorios/RELATORIO_QA_H-0022_HANDOFF.md (versao 216 linhas, preservado)
achado_historico: ACH-BLOQ-01 → RESOLVIDO
autoridades:
  - ADR-0016 (aceita)
  - contrato_tela_json.md secao 23 (ativo)
  - contrato_console.md item 10 (ativo)
  - contrato_processo_desenvolvimento.md (modelo ativo)
cobertura_itens_1_11:
  1: COBERTO_FIELMENTE
  2: COBERTO_FIELMENTE
  3: COBERTO_FIELMENTE
  4: COBERTO_FIELMENTE
  5: COBERTO_FIELMENTE
  6: COBERTO_FIELMENTE
  7: COBERTO_FIELMENTE
  8: COBERTO_FIELMENTE
  9: COBERTO_FIELMENTE
  10: COBERTO_PARCIALMENTE (F-MED-002)
  11: COBERTO_FIELMENTE
capacidade_coesa: SIM
escopo_positivo: tela/demo.py e tela/teste_demo.py suficientes para implementação técnica
escopo_negativo: proibições presentes; incoerência na cláusula exaustiva vs relatório de processo (F-ALTO-001)
arquivos_permitidos:
  - tela/demo.py
  - tela/teste_demo.py
arquivos_proibidos: ADR, contratos, índice, config/, artefatos históricos
preservacoes: comportamento não-TTY, termios, cursor, autowrap, alternate screen, Esc, stash histórico, proibições H-0009
criterios_de_aceite: observáveis e verificáveis para itens 1-9 e 11; parcialmente ambíguos para item 10 (F-MED-002)
testes: cobrem 11 itens; separação automatizado/manual correta
validacao_manual: explicitamente marcada; não substituída por testes automáticos
relatorio_implementacao_esperado: AUSENTE no handoff (F-ALTO-001)
condicoes_de_bloqueio: parciais — ARCHITECTURE_REVIEW_REQUIRED presente; stash/contradição/versão ausentes (F-BAIX-001)
achados_bloqueantes: nenhum
achados_altos:
  - F-ALTO-001: ausência de seção de relatório de implementação e ambiguidade da cláusula exaustiva
achados_medios:
  - F-MED-001: afirmação imprecisa sobre ADR no campo handoffs_bloqueados (seção narrativa)
  - F-MED-002: ambiguidade Ctrl+C/finally no critério do Item 10 (contradiz contrato_tela_json.md)
achados_baixos:
  - F-BAIX-001: condições de bloqueio incompletas (stash, contradição, versão)
  - F-BAIX-002: critério estrutural estreito no Item 9 (herdado de RESS-03)
observacoes:
  - OBS-001: pré-requisito de stash sem tratamento de caso de falha
arquivos_lidos:
  - ADR-0016, H-0022, contrato_tela_json, contrato_console (100 linhas),
    contrato_processo (150 linhas), QA_ADR-0016_POS_PATCH,
    QA_APLICACAO_ADR-0016, QA_POS_PATCH_APLICACAO_ADR-0016,
    QA_H-0022_HANDOFF, IMP-0022 (50 linhas)
arquivos_alterados:
  - docs/relatorios/RELATORIO_QA_H-0022_HANDOFF_POS_BASE_DOCUMENTAL.md
git:
  branch: master
  HEAD: 0b09fa6a99a6d0ed61e9488ecb7e78f16d37cfdf
  stage: vazio
  diff_check: limpo
  handoff: nao_rastreado (??)
proxima_categoria: PATCH_HANDOFF
```
