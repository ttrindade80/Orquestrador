# RELATORIO_AUDITORIA_H-0017_HANDOFF

```text
auditor:        Claude Code (papel QA/auditoria de handoff)
data:           2026-07-09
alvo:           scripts/docs/handoff/H-0017-script-exploracao-combinacoes-barra-de-menus.md
commit-base:    ab5ad68  feat: renderiza barra de menus horizontal responsiva
ciclo:          H-0017
```

---

## Status final

```text
AUDIT_APPROVED_WITH_NOTES
```

O handoff H-0017 está suficiente, coerente e seguro para implementação. Cobre
todos os 39 pontos obrigatórios de auditoria. Nenhum achado bloqueante nem de
alta severidade. Três achados de baixa severidade e duas notas, todos não
bloqueantes.

---

## Arquivos analisados

### Handoff alvo

```text
scripts/docs/handoff/H-0017-script-exploracao-combinacoes-barra-de-menus.md
```

### Referência (lidos integralmente)

```text
scripts/docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
scripts/docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
scripts/docs/relatorios/RELATORIO_QA_H-0016_MIGRACAO_JSON_BARRA_DE_MENUS_HORIZONTAL_RESPONSIVA.md
scripts/docs/relatorios/RELATORIO_AUDITORIA_H-0016_HANDOFF_POS_REVISAO.md
scripts/docs/adr/ADR-0014-barra-horizontal-termos-especificos.md
scripts/docs/contratos/contrato_barra_de_menus.md
scripts/docs/contratos/contrato_json_barra_de_menus.md
scripts/docs/contratos/contrato_chip.md
scripts/docs/contratos/contrato_processo_desenvolvimento.md
scripts/docs/NOMENCLATURA.md
```

### Implementação (lidos integralmente)

```text
scripts/tela/renderizador.py
```

---

## Comandos executados

```bash
# Estado do repositório
git log --oneline -6
git status --short
git diff --stat
git diff --name-only
```

### Saídas

```text
git log --oneline -6:
  ab5ad68 feat: renderiza barra de menus horizontal responsiva
  b2eb458 feat: ocupa altura do terminal pelo corpo
  4762583 docs: registra ocupacao vertical e barra responsiva
  8a6403a feat: migra arranjo vertical e barra declarativa
  ceaf0be docs: registra ADRs de arranjo e barra declarativa
  ab48702 feat: adiciona acesso demonstravel ao grupo minimo

git status --short:
  ?? scripts/docs/handoff/H-0017-script-exploracao-combinacoes-barra-de-menus.md

git diff --stat:   (vazio)
git diff --name-only: (vazio)
```

Estado do workspace **conforme esperado**: HEAD em `ab5ad68`; único arquivo
não rastreado é o handoff H-0017. **Nenhum achado de escopo** antes da criação
deste relatório.

---

## Resumo executivo

O handoff H-0017 define um ciclo exploratório/diagnóstico para exercitar
sistematicamente `_linhas_barra` do renderer implementado no H-0016. O
handoff:

1. Define claramente o caráter exploratório do ciclo e a separação de
   responsabilidade com H-0016.
2. Especifica script alvo, teste automatizado e relatório IMP-0017 com caminhos
   claros.
3. Define matriz de cenários finita (14 casos padrão) com variações de chips,
   larguras, `linhas.maximo`, preenchimentos, espaçamentos, âncoras e overflow.
4. Especifica parâmetros CLI completos (incluindo `--limite-casos`) que evitam
   explosão combinatória.
5. Define 12 invariantes verificáveis para cenários OK e 5 regras para cenários
   de erro esperado.
6. Proíbe explicitamente alterações a ADRs, contratos, NOMENCLATURA, JSONs
   ativos e comportamento do renderer.
7. Alinha-se integralmente ao ADR-0014 e aos contratos vigentes.
8. Define escopo negativo abrangente e critérios de bloqueio
   `ARCHITECTURE_REVIEW_REQUIRED`.

Os achados identificados são de baixa severidade (um sobre ambiguidade de
invariantes com chips de textos repetidos, um sobre indeterminação do cenário
de multilinha, um sobre caso de teste 9) e duas notas sobre uso de API privada
`_linhas_barra` e permissão condicional de alteração de `renderizador.py`.
Nenhum compromete a segurança da implementação.

---

## Verificação de relação com H-0016

| Ponto | Verificação | Status |
|---|---|---|
| H-0017 usa o renderer implementado no H-0016 sem alterá-lo | Explícito nas seções "Relação com H-0016" e "Objetivo" | OK |
| H-0017 não reabre escopo do H-0016 | Escopo negativo proíbe alterar semântica, ADRs, contratos | OK |
| H-0017 referencia commit-base ab5ad68 (H-0016 implementado) | Cabeçalho do handoff | OK |
| IMP-0016 e QA H-0016 listados como leitura obrigatória | Seção "Leitura obrigatória" itens 2 e 3 | OK |
| H-0017 depende de H-0016 implementado como pré-requisito | `depende-de: H-0016 (implementado, IMP-0016, QA aprovado — commit ab5ad68)` | OK |
| Bug no renderer encontrado pelo script → registrar no IMP-0017 e bloquear se comportamento mudar | Seção "Relação com H-0016" parágrafo 3 | OK |

---

## Verificação do objetivo exploratório

| Ponto obrigatório | Verificação | Status |
|---|---|---|
| 1. Define claramente que o ciclo é exploratório/diagnóstico | Seção "Objetivo" item 7; seção "Relação com H-0016"; escopo negativo | OK |
| 2. Não cria nova regra normativa da barra_de_menus | Escopo negativo + seção "Integração futura" | OK |
| 3. Não altera ADR, contrato ou NOMENCLATURA | Escopo negativo + arquivos proibidos | OK |
| 4. Não altera JSONs ativos | Escopo negativo + arquivos proibidos | OK |
| 5. Não muda comportamento aprovado do renderer H-0016 | "Script deve usar o comportamento implementado no H-0016 sem alterá-lo" | OK |
| 36. Não cria formato normativo definitivo de validação de telas futuras | Escopo negativo explícito; seção "Integração futura" | OK |

---

## Verificação do script alvo

| Ponto obrigatório | Verificação | Status |
|---|---|---|
| 6. Define script alvo com caminho claro | `scripts/tela/explorar_barra_de_menus.py` | OK |
| 7. Define teste automatizado alvo com caminho claro | `scripts/tela/teste_explorar_barra_de_menus.py` | OK |
| 8. Define relatório IMP-0017 | `scripts/docs/relatorios/IMP-0017-script-exploracao-combinacoes-barra-de-menus.md` com estrutura mínima | OK |

O handoff justifica o caminho `scripts/tela/` por coesão com `renderizador.py`
e permite caminho alternativo se o implementador encontrar diretório mais
adequado, com documentação no IMP-0017. Critério aceito.

---

## Verificação dos parâmetros CLI

| Ponto obrigatório | Verificação | Status |
|---|---|---|
| 9. Especifica parâmetros de linha de comando mínimos | `--larguras`, `--chips`, `--linhas-max`, `--preenchimentos`, `--modo-saida`, `--mostrar-ok`, `--mostrar-erros`, `--limite-casos` | OK |
| 10. Especifica saída textual determinística | Seção "Saída esperada do script" com formatos detalhado e resumo | OK |
| 11. Especifica exit codes 0, 1 e 2 | Seção "Exit codes" com definições precisas | OK |

Semântica dos flags `--mostrar-ok`/`--mostrar-erros` está corretamente
especificada: executa toda a matriz independente dos flags; os flags controlam
o que é exibido na saída, não o que é executado. O exit code depende do resultado
de toda a matriz, não do subconjunto exibido.

---

## Verificação da matriz de cenários

| Ponto obrigatório | Verificação | Status |
|---|---|---|
| 12. Especifica matriz padrão sem argumentos | 14 cenários definidos, executáveis sem argumentos | OK |
| 13. Varia quantidade de chips | 1, 2, 3, 4, 5, 6, 8, 10, 12 | OK |
| 14. Varia larguras de terminal/disponíveis | Muito estreita (≤20), estreita (25–40), média (50–70), larga (≥80) | OK |

A matriz padrão de 14 cenários cobre: linha única com 3 chips (ampla), linha
única com 6 chips (ampla), duas linhas com 6 e 8 chips (estreita), três linhas
com 10 chips, overflows forçados, coluna_a_coluna e linha_a_linha, âncoras
válida/inexistente/posição errada, espaçamentos mínimos e máximos.

**Nota sobre content_w vs terminal_w**: o handoff usa `content_w` como parâmetro
passado a `_linhas_barra`, não largura de terminal. O parâmetro CLI `--larguras`
mapeia para `content_w`, conforme o handoff e o algoritmo do H-0016.

---

## Verificação das invariantes

| Ponto obrigatório | Invariante | Status |
|---|---|---|
| 24. Verifica cada chip declarado exatamente uma vez | Invariante 1 | OK |
| 25. Verifica ausência de chip inventado | Invariante 2 | OK |
| 26. Verifica ausência de chip omitido | Invariante 3 | OK |
| 27. Verifica ausência de truncamento | Invariante 5 | OK |
| 28. Verifica preservação da ordem | Invariante 4 | OK |
| 29. Verifica largura máxima por linha | Invariante 7 | OK |
| 30. Verifica respeito a linhas.maximo | Invariante 6 | OK |

**Achado AUD-01 (baixo)**: O handoff especifica invariante 1 ("Cada chip
declarado aparece exatamente uma vez na saída") e invariante 4 ("A ordem
declarada é preservada"), mas não exige que os cenários sintéticos usem textos
e teclas únicos por chip. Se um cenário criar chips com textos idênticos (ex.:
múltiplos chips com texto "Ok"), a verificação por contagem/busca de strings na
saída renderizada seria ambígua — é impossível distinguir se chip A apareceu uma
vez versus chip B aparecer duas vezes por texto da saída. A verificação de ordem
também seria afetada. Recomenda-se que o implementador use textos sintéticos
únicos (ex.: "Ok-1", "Ok-2") ou teclas únicas para garantir verificabilidade.
Não é bloqueante: o implementador pode resolver ao projetar os cenários.

---

## Verificação de linha única/multilinha

| Ponto obrigatório | Verificação | Status |
|---|---|---|
| Cenário linha única | Cenário 1 (3 chips, content_w≥80) e Cenário 2 (6 chips, content_w≥100) | OK |
| Cenário duas linhas | Cenários 3, 4, 8, 9, 13 | OK |

---

## Verificação de coluna_a_coluna e linha_a_linha

| Ponto obrigatório | Verificação | Status |
|---|---|---|
| 31. Verifica distribuição coluna_a_coluna | Invariante 11; Cenário 3, 4, 8, 13 | OK |
| 32. Verifica distribuição linha_a_linha | Invariante 12; Cenário 9 | OK |

**Atenção especial 3 — `linha_a_linha`**: O IMP-0016 confirma que `linha_a_linha`
foi implementado deterministicamente (seção "Decisões locais" item 1: "ambos foram
implementados e selecionados pelo campo `preenchimento_multilinha`"). O handoff
H-0017 referencia esse fato no caso de teste 5: "Conforme IMP-0016,
`linha_a_linha` foi implementado deterministicamente." O handoff não exige suporte
que não esteja implementado. **Aprovado**.

**Achado AUD-02 (baixo)**: O cenário 9 da matriz padrão especifica "linha_a_linha
com 5 chips, content_w = 60, perfil misto, linhas.maximo=2". Dependendo dos
textos misto gerados pelo implementador, 5 chips em content_w=60 podem caber em
linha única, tornando o cenário de multilinha não exercitado. O handoff permite
ao implementador ajustar content_w (seção "O implementador pode ajustar os valores
concretos de content_w"), mas não indica como garantir que o caso seja realmente
multilinha. O implementador deve ser cauteloso ao projetar o perfil misto para
esse cenário. Não é bloqueante.

---

## Verificação de linhas.maximo 1/2/3

| Ponto obrigatório | Verificação | Status |
|---|---|---|
| 15. Varia linhas.maximo 1, 2 e 3 | Seção "Variações obrigatórias" item 4: `1, 2, 3`; Cenário 5: `linhas.maximo=3` | OK |

**Atenção especial 2 — linhas.maximo = 3**:

- O renderer aceita `linhas.maximo = 3` sem alteração. A validação em
  `_validar_distribuicao` exige apenas `maximo >= 1` e tipo `int` (não-bool). A
  iteração `for n_linhas in range(2, maximo + 1)` funciona corretamente para
  maximo=3, iterando n_linhas=2 e n_linhas=3.
- O handoff deixa claro que `linhas.maximo=3` é cenário sintético do script:
  "variações obrigatórias" item 4 lista `linhas.maximo` em `1, 2, 3` como
  parâmetro do script.
- O IMP-0016 documenta como limitação conhecida: "linhas.maximo > 2 não é caso
  testado adicionalmente" — mas a implementação itera genericamente até `maximo`.
- O handoff não implica nova regra normativa: os JSONs ativos permanecem com
  `linhas.maximo = 2`; o script usa apenas cenários sintéticos em memória.
- A ADR-0014 não proíbe explorar `linhas.maximo > 2` em contexto diagnóstico.
- **Aprovado**.

---

## Verificação de âncoras e overflow

| Ponto obrigatório | Verificação | Status |
|---|---|---|
| 19. Testa âncora válida | Cenário 10: chip_esc primeiro, chip_ajuda último, content_w=39 | OK |
| 20. Testa âncora inexistente | Cenário 11: id "chip_x" inexistente em chips[] | OK |
| 21. Testa âncora em posição errada | Cenário 12: chip_ajuda declarado primeiro mas âncora primeiro exige chip_esc | OK |
| 22. Testa overflow esperado | Cenários 6 (10 chips, content_w=20) e 7 (12 chips, content_w=15) | OK |
| 23. Classifica erro esperado sem abortar a matriz | Invariante 3 de erros esperados + critério de aceite 24 | OK |

Para erros esperados, o handoff especifica cinco regras que garantem:
(1) determinismo, (2) associação ao tipo correto de erro (overflow/âncora),
(3) continuação da matriz, (4) mensagem com "erro_layout" para overflow,
(5) mensagem com id/posição para âncoras. Todas cobertas.

---

## Verificação de arquivos permitidos/proibidos

| Ponto obrigatório | Verificação | Status |
|---|---|---|
| 37. Define arquivos permitidos/proibidos de modo suficiente | Seções "Arquivos permitidos" e "Arquivos proibidos" | OK |

**Arquivos permitidos** (conforme handoff):

```text
scripts/tela/explorar_barra_de_menus.py          (criar)
scripts/tela/teste_explorar_barra_de_menus.py    (criar)
scripts/tela/renderizador.py                     (apenas se necessário)
scripts/docs/relatorios/IMP-0017-...md           (criar)
```

**Arquivos proibidos** (conforme handoff — verificado contra lista da instrução):

```text
scripts/docs/contratos/                          ← todos os contratos    OK
scripts/docs/adr/                                ← todos os ADRs         OK
scripts/docs/NOMENCLATURA.md                                             OK
scripts/docs/INDICE.md                                                   OK
scripts/config/telas/                            ← todos os JSONs ativos OK
scripts/config/estilo.json                                               OK
scripts/config/lancador.json                                             OK
scripts/config/layout_console.json                                       OK
scripts/tela/loader.py                                                   OK
scripts/tela/modelo.py                                                   OK
scripts/tela/demo.py                                                     OK
scripts/tela/diagnostico.py                                              OK
scripts/tela/teste_loader.py                                             OK
scripts/tela/teste_modelo.py                                             OK
scripts/tela/teste_renderizador.py                                       OK
scripts/tela/teste_demo.py                                               OK
scripts/tela/teste_diagnostico.py                                        OK
```

A divisão é coerente. O teste novo (`teste_explorar_barra_de_menus.py`) pode
usar `subprocess.run` para invocar o script e chamadas diretas a `_linhas_barra`
para verificar comportamento do renderer — ambos possíveis sem alterar nenhum
arquivo proibido. Reutilização de utilitários de testes proibidos por importação
não é necessária para os casos especificados.

**Nota AUD-N-01**: `renderizador.py` está na lista de permitidos com restrição
condicional ("apenas se necessário expor helper já existente"). Como `_linhas_barra`
já é acessível por importação direta desde o H-0016 (é função de módulo, não
método de classe), a probabilidade de necessitar alterar `renderizador.py` é
mínima. O handoff trata isso corretamente: "A preferência é não alterar
`renderizador.py`." Sem achado bloqueante.

---

## Verificação de escopo negativo

| Item do escopo negativo | Verificação | Status |
|---|---|---|
| Nova regra normativa da barra_de_menus | Proibido explicitamente | OK |
| Alteração de ADR | Proibido | OK |
| Alteração de contrato | Proibido | OK |
| Alteração de NOMENCLATURA | Proibido | OK |
| Alteração dos JSONs ativos | Proibido | OK |
| Mudança no comportamento do renderer H-0016 | Proibido; alteração de renderizador.py restrita a expor helper já existente | OK |
| Mudança de semântica de chips | Proibido | OK |
| Mudança no lancador | Proibido | OK |
| Uso de chips do lancador na barra | Proibido | OK |
| Composição horizontal do corpo | Proibido | OK |
| corpo.arranjo = "horizontal" | Proibido | OK |
| Distribuição de altura entre elementos do corpo | Proibido | OK |
| Correção do preenchimento vertical do H-0015 | Proibido | OK |
| Console real | Proibido | OK |
| Integração automática ao diagnóstico principal | Proibido + seção "Integração futura" | OK |
| Integração automática à demo | Proibido + seção "Integração futura" | OK |
| Formato normativo definitivo de validação de telas futuras | Proibido | OK |
| Dependência de terminal real (curses, termios) | Proibido | OK |

---

## Verificação de testes obrigatórios

| Ponto obrigatório | Verificação | Status |
|---|---|---|
| 38. Exige testes existentes e teste novo | Seção "Testes obrigatórios" | OK |
| Suítes existentes: 5 arquivos de teste | `teste_loader.py`, `teste_modelo.py`, `teste_renderizador.py`, `teste_demo.py`, `teste_diagnostico.py` | OK |
| Suíte nova: `teste_explorar_barra_de_menus.py` | Especificado explicitamente | OK |
| Execuções manuais do script | 3 modos: sem argumentos, resumo com parâmetros, detalhado com limite | OK |
| 39. Exige relatório com limitações e fora de escopo | Estrutura do IMP-0017 especificada com seções "Limitações conhecidas" e "Confirmação de fora de escopo" | OK |

**Conteúdo obrigatório da seção "Confirmação de fora de escopo"** — listado e
verificado no handoff (seção "Relatório de implementação" → "Seção 'Confirmação
de fora de escopo'"). Cobre 9 itens explícitos. **OK**.

**10 casos obrigatórios do teste automatizado**:

| # | Caso | Observação |
|---|---|---|
| 1 | Matriz padrão sem argumentos → exit code 0 | OK |
| 2 | Modo resumo determinístico (duas chamadas idênticas) | OK |
| 3 | Linha única com 3 chips curtos → OK, 1 linha física | OK |
| 4 | Multilinha coluna_a_coluna com 4 chips estreito → OK, 2 linhas | OK |
| 5 | Multilinha linha_a_linha com 4 chips estreito → OK, 2 linhas | OK |
| 6 | Overflow forçado → erro_layout, script continua | OK |
| 7 | Âncora inexistente → RenderizadorErro com menção ao id | OK |
| 8 | Âncora em posição errada → RenderizadorErro com menção à posição | OK |
| 9 | Exit code 1 para violação inesperada (com ressalva de subprocess) | **Nota AUD-N-02** |
| 10 | Exit code 2 para parâmetro inválido | OK |

**Nota AUD-N-02**: O caso 9 admite verificação apenas por inspeção do código se
a simulação via subprocess não for determinística. O handoff trata isso com
clareza: "O implementador pode verificar apenas via inspeção do código do script
e registrar no IMP-0017." Não é bloqueante — é flexibilidade intencional.

---

## Achados

### AUD-01 — Ambiguidade de invariantes com chips sintéticos de textos repetidos

- **ID**: AUD-01
- **Severidade**: baixa
- **Evidência**: O handoff especifica invariante 1 ("Cada chip declarado aparece
  exatamente uma vez na saída") e invariante 4 ("A ordem declarada é preservada"),
  mas não exige que os cenários sintéticos da matriz usem textos ou teclas únicos
  por chip. A saída renderizada de `_linhas_barra` é uma lista de strings com o
  formato `"[{tecla}] {texto}"`. Se o script criar chips com teclas/textos
  iguais (ex.: 4 chips com tecla "x" e texto "Ok"), a verificação por contagem
  de strings na saída seria ambígua — impossível distinguir chip A de chip B.
- **Impacto**: Implementador pode criar cenários onde as invariantes 1, 2, 3 e 4
  não são verificáveis de forma confiável. Isso não compromete a ferramenta
  diagnóstica, mas reduz a qualidade das verificações.
- **Recomendação**: Usar textos sintéticos únicos por chip em todos os cenários
  (ex.: "Ok-1", "Ok-2", "Ir-3") ou teclas únicas por chip. O implementador deve
  documentar essa escolha no IMP-0017.

### AUD-02 — Cenário 9 da matriz não garante multilinha

- **ID**: AUD-02
- **Severidade**: baixa
- **Evidência**: O cenário 9 da matriz padrão especifica "linha_a_linha com 5
  chips, content_w = 60, perfil misto, linhas.maximo=2". Chips de perfil misto
  com content_w=60 podem caber em linha única dependendo dos textos gerados
  (`_montar_linha_a_linha` não é chamada se linha única couber em content_w).
  O handoff permite ao implementador ajustar content_w, mas não especifica como
  garantir que o caso realmente force multilinha.
- **Impacto**: O cenário 9 pode não exercitar `linha_a_linha` na prática se o
  implementador escolher textos curtos e content_w generoso. A invariante 12
  ("Para multilinha linha_a_linha, o padrão de distribuição linha por linha é
  observável") não seria verificada nesse cenário.
- **Recomendação**: O implementador deve garantir que os textos do perfil misto
  no cenário 9 sejam longos o suficiente para que linha única não caiba em
  content_w=60 (ou reduzir content_w). Documentar a escolha no IMP-0017.

### AUD-03 — Caso de teste 9 com verificação por inspeção de código

- **ID**: AUD-03
- **Severidade**: baixa
- **Evidência**: O caso 9 do teste automatizado ("script retorna exit code 1
  para violação inesperada") admite verificação por inspeção do código quando
  simulação via subprocess não for determinística. A condição de violação
  inesperada requer que um cenário projetado para caber produza `RenderizadorErro`
  — o que não ocorre normalmente em cenários corretos.
- **Impacto**: O teste 9 pode ser apenas formal (verificação estática do código)
  em vez de comportamental (execução real via subprocess). Isso reduz a cobertura
  da condição de exit code 1.
- **Recomendação**: O implementador pode simular a violação via parâmetro que
  injete um cenário com expectativa errada (ex.: esperar OK mas injetar
  distribuição que levante `RenderizadorErro` inesperadamente). Se não for
  viável, documentar a limitação no IMP-0017 conforme autorizado pelo handoff.

### AUD-N-01 — Uso de `_linhas_barra` como API prefixada com `_`

- **ID**: AUD-N-01
- **Severidade**: nota
- **Evidência**: O handoff autoriza `from tela.renderizador import _linhas_barra,
  RenderizadorErro` para o script. O prefixo `_` em Python indica API de uso
  interno/privado por convenção. O handoff reconhece isso ao permitir o uso
  explicitamente como ferramenta diagnóstica e ao especificar que não cria
  formato normativo definitivo.
- **Impacto**: Nenhum no ciclo atual. O script é ferramenta diagnóstica não
  integrada ao fluxo normal da aplicação. Não cria contrato normativo sobre
  a estabilidade de `_linhas_barra` como API pública.
- **Recomendação**: Sem ação necessária. O uso é explicitamente autorizado e
  circunscrito ao script diagnóstico.

### AUD-N-02 — Permissão condicional de alteração de `renderizador.py`

- **ID**: AUD-N-02
- **Severidade**: nota
- **Evidência**: O handoff permite alterar `renderizador.py` "apenas se
  necessário expor um helper já existente de forma segura, sem alterar
  comportamento". Como `_linhas_barra` já é acessível por importação direta
  (é função de módulo no escopo global de `renderizador.py`, não método de
  classe privada), a necessidade de alterar o arquivo é improvável. O handoff
  indica: "A preferência é não alterar `renderizador.py`."
- **Impacto**: Nenhum no ciclo atual. A condição de alteração é improvável
  de ser ativada dado o estado atual do renderer.
- **Recomendação**: O implementador deve confirmar no IMP-0017 se `renderizador.py`
  foi ou não alterado e por qual motivo.

---

## Conclusão

O handoff H-0017 está **suficiente, coerente e seguro para implementação**. Todos
os 39 pontos obrigatórios de auditoria foram verificados e aprovados. O handoff:

- Define ciclo exploratório/diagnóstico sem criar normas novas.
- Especifica script, teste e relatório com caminhos claros.
- Cobre matriz finita com variações adequadas.
- Define invariantes verificáveis (com ressalva AUD-01).
- Preserva escopo negativo abrangente.
- Não contradiz ADR-0014 nem contratos vigentes.
- Não altera comportamento do H-0016.

As verificações especiais concluem:

1. `_linhas_barra` existe, tem assinatura compatível e é acessível sem alteração
   do renderer. Aprovado com nota AUD-N-01.
2. `linhas.maximo = 3` é suportado pelo renderer genérico e não exige nova norma
   normativa. Aprovado.
3. `linha_a_linha` foi implementado deterministicamente no H-0016 conforme IMP-0016.
   O handoff trata isso corretamente. Aprovado.
4. A matriz combinatória é finita e controlável via `--limite-casos`. Aprovado.
5. As invariantes são robustas com ressalva sobre chips de textos repetidos
   (AUD-01). Baixo risco.
6. Os arquivos permitidos/proibidos são coerentes e suficientes. Aprovado.
7. Os testes obrigatórios cobrem suítes existentes e nova suíte. Aprovado.

---

## Próxima ação recomendada

```text
1. Liberar handoff H-0017 para implementação com status AUDIT_APPROVED_WITH_NOTES.
2. Recomendar ao implementador (OpenCode / GLM) que:
   a. Use textos/teclas únicos em todos os cenários sintéticos para garantir
      verificabilidade das invariantes 1–4 (AUD-01).
   b. Garanta que o cenário 9 (linha_a_linha com 5 chips) realmente force
      multilinha via content_w adequado ou textos longos (AUD-02).
   c. Documente no IMP-0017 a abordagem para o caso de teste 9 (exit code 1).
   d. Confirme no IMP-0017 se renderizador.py foi ou não alterado.
3. Após implementação, criar relatório QA H-0017 verificando:
   - Todos os 32 critérios de aceite do handoff.
   - Exit codes 0, 1 e 2 funcionando corretamente.
   - 451 verificações nas 5 suítes existentes continuam passando.
   - Teste novo passa com exit code 0.
```
