# Relatorio de QA pos-patch da ADR-0023

```yaml
etapa: QA_ADR
subetapa: QA_POS_PATCH_ADR
adr: ADR-0023
artefato_auditado: docs/adr/ADR-0023-largura-minima-funcional-lancador.md
status_literal: ADR_APPROVED_WITH_NOTES
status_normalizado: APROVADA_COM_OBSERVACOES
data: 2026-07-15
auditoria: independente_pos_patch
```

## 1. Identificacao

Este relatorio audita exclusivamente a correcao aplicada a
`docs/adr/ADR-0023-largura-minima-funcional-lancador.md` apos o primeiro QA.

Nenhuma correcao foi aplicada a ADR. Nenhum contrato, nomenclatura, indice,
handoff, codigo, teste ou configuracao foi alterado por esta auditoria.

## 2. Artefato auditado

Artefato principal:

`docs/adr/ADR-0023-largura-minima-funcional-lancador.md`

A ADR permanece com status `aceita`, data 2026-07-15 e declara que a
insuficiencia da area atribuida ao `lancador` para conter uma coluna valida
aciona o `quadro mínimo de terminal pequeno` com escopo global.

## 3. Decisao explicita do usuario

Decisao material auditada:

> Quando a area atribuida ao `lancador` nao comportar nem uma unica coluna
> valida completa, deve ser acionado o quadro minimo global ja existente. Toda a
> tela ou sessao TUI normal e substituida. Nao deve existir mensagem ou variante
> local dentro da area ou caixa do `lancador`.

Consequencias auditadas:

- fallback global;
- substituicao integral da tela normal;
- nenhum componente da tela normal permanece visivel;
- ausencia de estado local especifico do `lancador`;
- reutilizacao do mecanismo canonico existente;
- nenhuma mensagem nova;
- estado transitorio;
- recuperacao automatica;
- retorno do `lancador` como `fila` ou `matriz`;
- ausencia de truncamento, overflow, paginacao, omissao ou perda de itens.

## 4. Primeiro relatorio de QA

Relatorio consultado:

`docs/relatorios/RELATORIO_QA_ADR-0023.md`

O primeiro QA registrou:

```yaml
status_literal: ARCHITECTURE_REVIEW_REQUIRED
status_normalizado: REVISAO_ARQUITETURAL_REQUERIDA
achados:
  - QA-ADR0023-BLOQUEANTE-001
  - QA-ADR0023-ALTO-001
  - QA-ADR0023-MEDIO-001
```

Contexto do bloqueio original consultado:

`docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md`

O bloqueio original relevante era a ausencia de regra para o caso em que nem a
coluna unica do `lancador` coubesse.

## 5. Autoridades consultadas

- `docs/adr/ADR-0023-largura-minima-funcional-lancador.md`, integralmente.
- `docs/relatorios/RELATORIO_QA_ADR-0023.md`, integralmente.
- `docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md`, para contexto do bloqueio original.
- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`, secao 9.
- `docs/NOMENCLATURA.md`, secoes 6.2 e 8.1 a 8.3.
- `docs/contratos/contrato_tela_json.md`, secao 24.
- `docs/contratos/contrato_composicao_corpo.md`, secoes 5.10 e 5.21.
- `docs/contratos/contrato_lancador.md`, secoes 6 a 9.
- `docs/contratos/contrato_json_lancador.md`, secoes 2, 5 e 7.
- `docs/adr/INDICE_ADR.md`.
- `docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`, apenas para confirmar ausencia de correcao prematura.

## 6. Estado Git inicial e final

### Inicial

Comando executado a partir da raiz:

```bash
git status --short
```

Resultado:

```text
?? demo/__pycache__/
?? docs/adr/ADR-0023-largura-minima-funcional-lancador.md
?? docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
?? docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
?? docs/relatorios/RELATORIO_QA_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
?? tela/__pycache__/
```

Comando executado a partir da raiz:

```bash
git diff --no-index /dev/null docs/adr/ADR-0023-largura-minima-funcional-lancador.md
```

Resultado: codigo 1, esperado para comparacao entre `/dev/null` e arquivo novo.
O diff exibiu a ADR inteira como arquivo novo.

### Final

Comandos executados apos a criacao deste relatorio:

```bash
git status --short
git diff --no-index /dev/null docs/adr/ADR-0023-largura-minima-funcional-lancador.md
```

Resultado final registrado na secao 15 deste relatorio: o status passou a
incluir somente este relatorio novo alem dos itens iniciais; o diff da ADR
permaneceu com codigo 1 esperado e conteudo da ADR como arquivo novo.

## 7. Proveniencia de itens nao rastreados

```yaml
demo/__pycache__/:
  presente_no_status_inicial: CONFIRMADO
  presente_no_status_final: CONFIRMADO
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

tela/__pycache__/:
  presente_no_status_inicial: CONFIRMADO
  presente_no_status_final: CONFIRMADO
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/adr/ADR-0023-largura-minima-funcional-lancador.md:
  presente_no_status_inicial: CONFIRMADO
  presente_no_status_final: CONFIRMADO
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md:
  presente_no_status_inicial: CONFIRMADO
  presente_no_status_final: CONFIRMADO
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md:
  presente_no_status_inicial: CONFIRMADO
  presente_no_status_final: CONFIRMADO
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/RELATORIO_QA_ADR-0023.md:
  presente_no_status_inicial: CONFIRMADO
  presente_no_status_final: CONFIRMADO
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md:
  presente_no_status_inicial: CONFIRMADO
  presente_no_status_final: CONFIRMADO
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md:
  presente_no_status_inicial: NAO
  presente_no_status_final: CONFIRMADO
  origem: QA_POS_PATCH_ADR-0023
  produzido_pelo_executor: CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
```

Os caches nao foram removidos.

## 8. Resultado individual dos achados anteriores

```yaml
- achado: QA-ADR0023-BLOQUEANTE-001
  estado: CORRIGIDO
  evidencia: |
    A ADR agora declara que o quadro minimo global substitui integralmente toda
    a tela ou sessao TUI normal (linhas 147-184), que cabecalho, corpo,
    lancador, dashboards e barra_de_menus nao sao exibidos (linhas 155-163),
    e que nao ha mensagem, estado ou variante local (linhas 167-184, 295-297).
    A secao 5.1 explicita que o escopo visual e identico e global nas duas
    situacoes (linhas 245-280).
  residuos: |
    Nao foram identificados residuos materiais de ambiguidade entre quadro
    global e estado local.
  regressoes: |
    Nenhuma regressao identificada.
  conclusao: |
    A escolha arquitetural global ficou inequivoca e exequivel.

- achado: QA-ADR0023-ALTO-001
  estado: CORRIGIDO
  evidencia: |
    A ADR separa `terminal_w`, `area_lancador_w`,
    `lancador_caixa_min_w`, `coluna_minima_content_w` e o `content_w`
    derivado por conversao (linhas 88-145 e 186-195). Ela proibe comparar
    `terminal_w` com `coluna_minima_content_w` e `area_lancador_w` com
    `coluna_minima_content_w` sem conversao (linhas 112-127). As relacoes
    equivalentes `content_w < coluna_minima_content_w` e
    `area_lancador_w < lancador_caixa_min_w` estao declaradas (linhas
    112-124, 305-306, 506-508).
  residuos: |
    A frase "distingue quatro grandezas" nao enumera `content_w` como item
    autonomo, mas a semantica de `content_w` esta presente como largura de
    conteudo resultante da conversao da caixa. O residuo e editorial, nao
    bloqueia aplicacao.
  regressoes: |
    Nenhuma regressao identificada.
  conclusao: |
    As comparacoes dimensionais agora sao normativamente compativeis.

- achado: QA-ADR0023-MEDIO-001
  estado: CORRIGIDO
  evidencia: |
    A secao 9 agora classifica `docs/contratos/contrato_lancador.md`,
    `docs/NOMENCLATURA.md`, `docs/adr/INDICE_ADR.md`,
    `docs/contratos/contrato_tela_json.md` e
    `docs/contratos/contrato_composicao_corpo.md` como afetados para futura
    `APLICAR_ADR` (linhas 371-447), marca
    `docs/contratos/contrato_json_lancador.md` como nao afetado (linhas
    449-457) e separa H-0034 para `PATCH_HANDOFF` posterior (linhas
    459-474).
  residuos: |
    Ver observacao QA-POS-ADR0023-BAIXO-001 sobre o frontmatter
    `rastreabilidade.contratos_afetados`, que permanece abreviado. A lista
    normativa de propagacao, entretanto, esta clara na secao 9.
  regressoes: |
    Nenhuma regressao identificada.
  conclusao: |
    A lista material de documentos afetados foi corrigida.
```

## 9. Auditoria das onze areas

### 9.1 Fidelidade da decisao global

Conforme.

A ADR declara alcance visual global, substituicao integral da tela normal,
desaparecimento de cabecalho, corpo, `lancador`, dashboards e
`barra_de_menus`, ausencia de mensagem local, ausencia de variante local,
reutilizacao do mecanismo canonico e recuperacao automatica.

Buscas por `local`, `area`, `caixa` e `quadro mínimo` nao revelaram formulacao
remanescente que permita interpretar o fallback como restrito a area ou caixa
do `lancador`. As ocorrencias negativas ("nao ha estado local", "nao criar
variante local") sao consistentes com a decisao.

### 9.2 Compatibilidade com o quadro minimo existente

Conforme.

Autoridades:

- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`, secao 9: define quadro
  minimo para dimensoes validas mas insuficientes, sem encerrar sessao, sem
  scroll, sem residuo e com recuperacao automatica.
- `docs/NOMENCLATURA.md`, secao 6.2: registra `quadro mínimo de terminal pequeno`
  como quadro substituto recuperado automaticamente.
- `docs/contratos/contrato_tela_json.md`, secao 24: aplica o comportamento a
  sessao TUI.

A ADR-0023 estende o gatilho, mas preserva alcance global, recuperacao reativa
e ausencia de mensagem textual nova.

### 9.3 Grandezas de largura

Conforme, com observacao editorial.

A ADR diferencia:

- `terminal_w`: largura total do terminal ou viewport;
- `area_lancador_w`: largura total alocada ao elemento, incluindo caixa;
- `lancador_caixa_min_w`: largura minima da caixa;
- `coluna_minima_content_w`: largura minima do conteudo para uma coluna valida;
- `content_w`: largura de conteudo obtida ao descontar bordas e padding.

As comparacoes normativas estao em dominios compativeis. Bordas e padding ficam
no dominio da caixa; chip, vao e texto ficam no dominio do conteudo.

### 9.4 Definicao de coluna minima

Conforme.

A formula contempla margem minima, subcoluna de chip, vao minimo chip-texto,
subcoluna de texto e margem minima. A ADR deixa bordas e padding fora de
`coluna_minima_content_w` e dentro de `lancador_caixa_min_w`, evitando duplicacao.

### 9.5 Sequencia normativa

Conforme.

A sequencia declarada e:

```text
obter area_lancador_w
→ converter para content_w
→ testar fila
→ testar matrizes validas
→ testar coluna minima valida
→ acionar quadro minimo canonico global
```

A coluna minima aparece como limite inferior de validade, nao como novo modo de
layout. Ausencia de itens e tratada como 0 linhas de conteudo, sem erro. A ADR
proibe coluna invalida, truncamento, paginacao, omissao e perda de itens.

### 9.6 Recuperacao automatica

Conforme.

A ADR determina reavaliacao a cada redesenho, reconstrucao integral da tela
normal quando houver espaco, retorno do `lancador` como `fila` ou `matriz`,
ausencia de reinicio, ausencia de acao do usuario e nao persistencia do estado.

### 9.7 Documentos afetados

Conforme, com nota de rastreabilidade.

Classificacao auditada:

```yaml
docs/contratos/contrato_lancador.md:
  classificacao: APLICAR_ADR
  avaliacao: correta

docs/contratos/contrato_tela_json.md:
  classificacao: APLICAR_ADR
  avaliacao: correta

docs/contratos/contrato_composicao_corpo.md:
  classificacao: APLICAR_ADR
  avaliacao: correta

docs/NOMENCLATURA.md:
  classificacao: APLICAR_ADR
  avaliacao: correta

docs/adr/INDICE_ADR.md:
  classificacao: APLICAR_ADR
  avaliacao: correta

docs/contratos/contrato_json_lancador.md:
  classificacao: nao_afetado
  avaliacao: correta

docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md:
  classificacao: PATCH_HANDOFF_posterior
  avaliacao: correta
```

Nota: o frontmatter `rastreabilidade.contratos_afetados` da ADR continua mais
estreito que a secao 9. A secao normativa de documentos afetados esta correta,
mas a rastreabilidade de topo deve ser conferida na aplicacao documental.

### 9.8 Ausencia de aplicacao prematura

Conforme.

A ADR nao afirma que contratos, nomenclatura, indice ou handoff ja foram
atualizados. Tambem nao afirma que implementacao existe, que testes foram
executados ou que a decisao ja foi aplicada ao codigo.

O H-0034 permanece sem os termos da correcao (`ADR-0023`,
`area_lancador_w`, `coluna_minima_content_w`, `lancador_caixa_min_w` ou
`quadro mínimo canônico` nao foram localizados), confirmando que nao foi
corrigido prematuramente por esta ADR.

### 9.9 Compatibilidade e escopo negativo

Conforme.

A ADR nao cria mensagem especifica, estado local, variante visual local,
truncamento, reticencias, quebra de linhas, overflow, paginacao, rolagem,
navegacao, selecao, novo tipo de componente, mudanca da `barra_de_menus`,
mudanca de cabecalho, mudanca de `destino_minimo`, mudanca de `grupo_minimo`,
reabertura do H-0030 ou inicio do H-0033.

### 9.10 Relacao com ADRs e contratos anteriores

Conforme.

A ADR-0017 permanece autoridade do comportamento global. A ADR-0023 apenas
estende a condicao que torna a tela normal inviavel. Nenhuma ADR anterior e
declarada como substituida. Os contratos atuais sao descritos como aguardando
futura propagacao.

Nao foi identificada contradicao normativa material remanescente dentro da ADR.

### 9.11 Exequibilidade da aplicacao futura

Conforme.

A ADR fornece informacao suficiente para futura aplicacao sem nova decisao sobre
alcance visual, mecanismo reutilizado, grandezas comparadas, limite inferior de
validade, documentos afetados, recuperacao, proibicoes e posterior correcao do
H-0034.

Nao falta escolher mensagem, nivel visual, formula normativa ou documento
materialmente afetado.

## 10. Busca de residuos

Buscas focais executadas em `docs/adr/ADR-0023-largura-minima-funcional-lancador.md`
por:

```text
local
area
caixa
quadro mínimo
content_w
terminal_w
area_lancador_w
lancador_caixa_min_w
coluna_minima_content_w
documentos afetados
contratos atualizados
handoff corrigido
implementação concluída
```

Resultado:

- `local`, `area`, `caixa`: ocorrencias consistentes com a decisao global ou
  negacoes explicitas de estado/variante local.
- `quadro mínimo`: ocorrencias coerentes com o mecanismo canonico global.
- `content_w`, `area_lancador_w`, `lancador_caixa_min_w`,
  `coluna_minima_content_w`, `terminal_w`: comparacoes em dominios compativeis.
- `documentos afetados`: secao 9 unica de propagacao material.
- `contratos atualizados`, `handoff corrigido`, `implementação concluída`: nao
  foram encontradas afirmacoes de aplicacao ja concluida.

Residuo nao bloqueante: o frontmatter contem `contratos_afetados` abreviado em
relacao a secao 9.

## 11. Regressoes

Nenhuma regressao material foi identificada.

A ADR nao introduziu decisao adicional substantiva, nao aplicou a decisao ao
codigo, nao corrigiu o H-0034 prematuramente e nao criou nova contradicao
normativa material.

## 12. Novos achados

### QA-POS-ADR0023-BAIXO-001

Severidade: baixo.

Evidencia:

- O frontmatter da ADR, linhas 13-16, lista em `contratos_afetados` apenas
  `docs/contratos/contrato_lancador.md` e `docs/NOMENCLATURA.md`.
- A secao 9 da mesma ADR lista corretamente, para futura `APLICAR_ADR`,
  `docs/contratos/contrato_lancador.md`,
  `docs/contratos/contrato_tela_json.md`,
  `docs/contratos/contrato_composicao_corpo.md`,
  `docs/NOMENCLATURA.md` e `docs/adr/INDICE_ADR.md`.

Regra violada:

A rastreabilidade de topo nao deve ficar materialmente menos completa que a
lista normativa de documentos afetados.

Impacto:

Baixo. A secao 9 fornece a lista material suficiente para aplicacao futura, mas
um executor que use apenas o frontmatter pode subestimar o escopo documental.

Correcao ou decisao necessaria:

Na futura `APLICAR_ADR`, confirmar se o frontmatter deve ser alinhado a lista
normativa da secao 9 ou se o projeto trata `contratos_afetados` apenas como
resumo nao exaustivo.

Secao afetada:

Frontmatter `rastreabilidade.contratos_afetados`.

## 13. Status literal e normalizado

```yaml
status_literal: ADR_APPROVED_WITH_NOTES
status_normalizado: APROVADA_COM_OBSERVACOES
achados_anteriores:
  QA-ADR0023-BLOQUEANTE-001: CORRIGIDO
  QA-ADR0023-ALTO-001: CORRIGIDO
  QA-ADR0023-MEDIO-001: CORRIGIDO
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 1
observacoes: 1
regressoes: 0
```

Justificativa: os tres achados anteriores foram materialmente corrigidos. A
unica nota remanescente e de rastreabilidade de frontmatter, sem bloquear a
aprovacao da ADR para futura aplicacao.

## 14. Proxima categoria

```yaml
proxima_categoria: APLICAR_ADR
gerar_prompt: false
```

## 15. Estado Git final registrado

Comando executado a partir da raiz:

```bash
git status --short
```

Resultado:

```text
?? demo/__pycache__/
?? docs/adr/ADR-0023-largura-minima-funcional-lancador.md
?? docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
?? docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
?? docs/relatorios/RELATORIO_QA_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md
?? tela/__pycache__/
```

Comando executado a partir da raiz:

```bash
git diff --no-index /dev/null docs/adr/ADR-0023-largura-minima-funcional-lancador.md
```

Resultado:

```text
codigo: 1
interpretacao: esperado; comparacao entre /dev/null e arquivo novo
resumo: o diff exibiu docs/adr/ADR-0023-largura-minima-funcional-lancador.md como arquivo novo integral
```
