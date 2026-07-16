# Relatorio de QA da Aplicacao da ADR-0023

```yaml
etapa: QA_APLICACAO_ADR
adr_aplicada: ADR-0023
status_literal: ADR_APPLICATION_APPROVED_WITH_NOTES
status_normalizado: APROVADA_COM_OBSERVACOES
data: 2026-07-15
auditoria: independente
relatorio_auditado: docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md
```

## 1. Identificacao

Este relatorio audita exclusivamente a aplicacao documental da ADR-0023.

Nenhum documento normativo foi corrigido por esta auditoria. Nenhum codigo,
teste, configuracao, ADR, handoff ou stage Git foi alterado. O unico arquivo
criado por esta etapa e este relatorio:

`docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0023.md`

## 2. ADR aplicada

Autoridade principal:

`docs/adr/ADR-0023-largura-minima-funcional-lancador.md`

A ADR esta com status `aceita`, data 2026-07-15, e define que, quando a area
alocada ao `lancador` nao comportar nem uma coluna valida completa, o resultado
deve ser o quadro minimo canonico global da ADR-0017, sem fallback local.

## 3. QA que aprovou a ADR

Relatorio consultado:

`docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md`

Status do QA da ADR:

```yaml
status_literal: ADR_APPROVED_WITH_NOTES
status_normalizado: APROVADA_COM_OBSERVACOES
achado_baixo_remanescente: QA-POS-ADR0023-BAIXO-001
```

O QA pos-patch aprovou a ADR com observacao sobre a lista resumida do
frontmatter. A aplicacao declarou ter usado a secao 9 da ADR como lista
normativa completa de propagacao.

## 4. Relatorio de aplicacao auditado

Arquivo auditado:

`docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md`

O relatorio declara:

```yaml
etapa: APLICAR_ADR
status: CONCLUIDA
arquivos_alterados:
  - docs/contratos/contrato_lancador.md
  - docs/contratos/contrato_tela_json.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/NOMENCLATURA.md
  - docs/adr/INDICE_ADR.md
arquivo_criado:
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md
```

A lista nominal corresponde ao diff real e ao estado Git observado.

## 5. Autoridades consultadas

Lidos integralmente:

- `docs/adr/ADR-0023-largura-minima-funcional-lancador.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/NOMENCLATURA.md`
- `docs/adr/INDICE_ADR.md`

Consultados para comparacao:

- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`
- `docs/contratos/contrato_json_lancador.md`
- `docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`
- `docs/relatorios/RELATORIO_QA_ADR-0023.md`

## 6. Estado Git inicial e final

### Inicial

Comandos executados a partir da raiz:

```bash
git status --short
git diff --name-only
git diff --check
git diff --cached --name-only
```

Resultado de `git status --short`:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_lancador.md
 M docs/contratos/contrato_tela_json.md
?? demo/__pycache__/
?? docs/adr/ADR-0023-largura-minima-funcional-lancador.md
?? docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
?? docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md
?? tela/__pycache__/
```

Resultado de `git diff --name-only`:

```text
docs/NOMENCLATURA.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_tela_json.md
```

`git diff --check`: sem saida.

`git diff --cached --name-only`: sem saida; stage vazio.

### Final registrado apos criacao deste relatorio

Comandos executados novamente a partir da raiz:

```bash
git status --short
git diff --name-only
git diff --check
git diff --cached --name-only
```

Resultado de `git status --short`:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_lancador.md
 M docs/contratos/contrato_tela_json.md
?? demo/__pycache__/
?? docs/adr/ADR-0023-largura-minima-funcional-lancador.md
?? docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
?? docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md
?? tela/__pycache__/
```

Resultado de `git diff --name-only`:

```text
docs/NOMENCLATURA.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_tela_json.md
```

`git diff --check`: sem saida.

`git diff --cached --name-only`: sem saida; stage vazio.

## 7. Arquivos alterados e nao rastreados

Arquivos rastreados alterados no diff:

```yaml
- docs/NOMENCLATURA.md
- docs/adr/INDICE_ADR.md
- docs/contratos/contrato_composicao_corpo.md
- docs/contratos/contrato_lancador.md
- docs/contratos/contrato_tela_json.md
```

Arquivos nao rastreados observados antes deste relatorio:

```yaml
- demo/__pycache__/
- docs/adr/ADR-0023-largura-minima-funcional-lancador.md
- docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
- docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
- docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md
- docs/relatorios/RELATORIO_QA_ADR-0023.md
- docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
- docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md
- tela/__pycache__/
```

Item criado por esta auditoria:

```yaml
- docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0023.md
```

## 8. Proveniencia dos itens

```yaml
demo/__pycache__/:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

tela/__pycache__/:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/adr/ADR-0023-largura-minima-funcional-lancador.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md:
  origem: CONFIRMADA
  produzido_pelo_executor: CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/RELATORIO_QA_ADR-0023.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0023.md:
  origem: QA_APLICACAO_ADR-0023
  produzido_pelo_executor: CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
```

Nenhum cache ou arquivo nao rastreado foi removido.

## 9. Analise do diff

O diff real dos cinco documentos aplicados mostra somente propagacao
documental:

- `docs/contratos/contrato_lancador.md`: adiciona ADR-0023 ao frontmatter,
  nova secao 6.7, regras R-11 a R-14 e criterios de validacao.
- `docs/contratos/contrato_tela_json.md`: adiciona ADR-0023 ao frontmatter e
  nova subseccao na secao 24 sobre area insuficiente do `lancador`.
- `docs/contratos/contrato_composicao_corpo.md`: adiciona ADR-0023 ao
  frontmatter, paragrafo na secao 5.10, regra R-33 e criterios de validacao.
- `docs/NOMENCLATURA.md`: adiciona secao 6.3 com termos e regras derivadas.
- `docs/adr/INDICE_ADR.md`: adiciona linha da ADR-0023 no padrao existente.

Nao ha diff em codigo, testes, configuracao, ADR-0023, H-0034 ou
`docs/contratos/contrato_json_lancador.md`.

## 10. Auditoria dos cinco documentos

### `docs/contratos/contrato_lancador.md`

Conforme, com nota baixa.

Evidencias:

- Define `terminal_w`, `area_lancador_w`, `lancador_caixa_min_w` e
  `coluna_minima_content_w` na secao 6.7.
- Declara comparacoes validas: `content_w < coluna_minima_content_w` e
  `area_lancador_w < lancador_caixa_min_w`.
- Proibe comparacoes dimensionais invalidas.
- Define formula de `coluna_minima_content_w` com chip, vao e texto, sem
  incluir bordas/padding.
- Declara ordem decisoria: obter `area_lancador_w`, converter para
  `content_w`, testar fila, testar matrizes validas, testar coluna minima,
  acionar quadro minimo global.
- Proibe mensagem local, estado local, truncamento, overflow, omissao,
  duplicacao, reordenacao, paginacao e rolagem especifica.
- Declara recuperacao automatica a cada redesenho.
- Preserva regras anteriores de itens, chips, texto, destino, alinhamento,
  ausencia de navegabilidade e ausencia de paginacao.

Nota: a secao diz "quatro grandezas" e nao enumera `content_w` na lista
principal, embora `content_w` seja definido operacionalmente pela conversao e
usado nas comparacoes normativas. Isso nao cria contradicao material, mas e
registrado como achado baixo.

### `docs/contratos/contrato_tela_json.md`

Conforme.

O quadro minimo continua global. A nova regra e restrita a inviabilidade do
`lancador`, nao cria campo JSON, nao cria quadro minimo local, nao generaliza
para qualquer componente interno e explicita que nenhum cabecalho, corpo,
`lancador`, dashboard ou `barra_de_menus` permanece visivel.

As formulacoes anteriores sobre terminal pequeno foram preservadas e
complementadas. Elas continuam validas para o gatilho por dimensoes totais e
nao excluem o novo gatilho por area interna.

### `docs/contratos/contrato_composicao_corpo.md`

Conforme.

A composicao reconhece `area_lancador_w`, declara que
`area_lancador_w < lancador_caixa_min_w` nao e renderizacao normal valida,
eleva o resultado ao quadro minimo global, proibe truncamento/mensagem local e
declara recuperacao no redesenho seguinte. A regra e explicitamente exclusiva
do `lancador`; politicas de outros componentes foram preservadas.

### `docs/NOMENCLATURA.md`

Conforme.

Define sem concorrencia os termos `area_lancador_w`,
`lancador_caixa_min_w`, `coluna_minima_content_w`, `content_w`, `coluna
valida completa`, quadro minimo global por inviabilidade do `lancador`,
fallback local proibido e recuperacao automatica. Distingue largura total do
terminal, caixa e conteudo. Nao cria nome privado de funcao como termo
arquitetural.

### `docs/adr/INDICE_ADR.md`

Conforme.

A ADR-0023 foi incluida no padrao real do indice: ID correto, titulo/resumo
compatibil com a ADR aprovada, estado `aceita`, data `2026-07-15`, sem nova
coluna, sem status inventado e sem renumeracao de outras entradas.

## 11. Contrato JSON do `lancador`

`docs/contratos/contrato_json_lancador.md` permaneceu fora do diff.

A preservacao e coerente porque:

- nao existe campo JSON novo;
- o gatilho e calculado pelo renderer;
- a configuracao nao escolhe fallback global ou local;
- o contrato JSON declara que regras de layout pertencem a
  `contrato_lancador.md`;
- nao ha contradicao ativa com a ADR-0023.

## 12. Grandezas de largura

Resultado geral: conforme, com nota baixa ja registrada em
`contrato_lancador.md`.

As grandezas mantidas pela aplicacao sao:

```yaml
terminal_w: largura total do terminal ou viewport
area_lancador_w: largura total da caixa alocada ao lancador
lancador_caixa_min_w: largura minima total da caixa do lancador
content_w: largura interna de conteudo apos descontar bordas e padding
coluna_minima_content_w: largura minima de conteudo para uma coluna valida
```

Comparacoes validas encontradas:

```text
content_w < coluna_minima_content_w
area_lancador_w < lancador_caixa_min_w
```

Nao foram encontradas comparacoes normativas novas de `terminal_w` contra
`coluna_minima_content_w`, nem de `area_lancador_w` contra
`coluna_minima_content_w` sem conversao. Bordas e padding permanecem no dominio
da caixa; chip, vao e texto permanecem no dominio do conteudo.

## 13. Alcance global

Conforme.

```yaml
alcance: GLOBAL
substitui_tela_normal: true
componentes_normais_visiveis: nenhum
fallback_local: proibido
mensagem_especifica_lancador: proibida
recuperacao: automatica
```

Nao foi localizada formulacao nova que permita manter cabecalho, corpo,
dashboard, `lancador` ou `barra_de_menus` visiveis durante o quadro minimo.
Tambem nao foi localizada autorizacao para mensagem somente na caixa,
representacao parcial do `lancador` ou variante local do quadro minimo.

## 14. Recuperacao

Conforme.

A recuperacao e reavaliada em cada redesenho. Quando
`area_lancador_w >= lancador_caixa_min_w`, o quadro minimo desaparece, a tela
normal e reconstruida e o `lancador` e redistribuido como `fila` ou `matriz`.
Nao ha reinicio, comando humano obrigatorio ou persistencia do estado de
insuficiencia.

## 15. Ausencia de generalizacao indevida

Conforme.

As novas formulacoes restringem o gatilho adicional ao `lancador`. Nao foi
criada regra generica para qualquer elemento, qualquer filho, qualquer
container ou qualquer insuficiencia local. As formulacoes genericas
preexistentes sobre paginacao, overflow ou terminal pequeno permanecem como
autoridades anteriores e nao foram ampliadas indevidamente pela aplicacao.

## 16. Nota do frontmatter

Conforme.

A aplicacao nao alterou a ADR aprovada. A secao 9 da ADR foi usada como lista
normativa completa, incluindo `contrato_tela_json.md` e
`contrato_composicao_corpo.md`, apesar de o frontmatter da ADR resumir
`contratos_afetados`. A divergencia do frontmatter foi registrada no relatorio
de aplicacao e nao causou omissao de escopo.

## 17. Buscas de residuos

Buscas focais executadas com `rg` nos documentos alterados e nos artefatos de
comparacao por termos relacionados a:

- quadro minimo;
- terminal pequeno;
- fallback local;
- mensagem local;
- largura minima;
- coluna valida;
- `terminal_w`;
- `area_lancador_w`;
- `lancador_caixa_min_w`;
- `content_w`;
- `coluna_minima_content_w`;
- truncamento;
- overflow;
- paginacao;
- campo JSON;
- qualquer componente;
- qualquer filho.

Classificacao das ocorrencias:

- Regra ativa nova: coerente com ADR-0023 nos cinco documentos alterados.
- Negacoes/proibicoes: coerentes; nao foram classificadas como residuos.
- Historico ou pendencia: H-0034 preservado ainda contem a lacuna que motivou
  a ADR, mas a propria ADR classifica sua correcao como `PATCH_HANDOFF`
  posterior, fora de `APLICAR_ADR`.
- Contrato JSON preservado: coerente e sem campo novo.

Nao foi encontrada contradicao normativa ativa nos cinco documentos alterados.

## 18. Achados

### QA-APLICACAO-ADR0023-BAIXO-001

```yaml
severidade: baixo
arquivo: docs/contratos/contrato_lancador.md
secao: 6.7 Largura minima funcional e fallback global
```

Evidencia:

A secao afirma distinguir "quatro grandezas" e enumera `terminal_w`,
`area_lancador_w`, `lancador_caixa_min_w` e `coluna_minima_content_w`. A
grandeza `content_w` aparece nas comparacoes e na sequencia decisoria como
resultado de conversao da caixa, mas nao e enumerada na lista principal.

Regra ou decisao violada:

As grandezas normativas devem permanecer distintas, incluindo `content_w`.

Impacto:

Baixo. A semantica de `content_w` esta recuperavel no proprio contrato e esta
formalmente definida em `docs/NOMENCLATURA.md`, mas a redacao do contrato
principal fica editorialmente menos completa.

Correcao necessaria:

Em etapa propria, ajustar a enumeracao de grandezas em
`contrato_lancador.md` para incluir `content_w` explicitamente ou explicar que
ela e grandeza derivada da conversao.

### QA-APLICACAO-ADR0023-BAIXO-002

```yaml
severidade: baixo
arquivo: docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md
secao: 5. Estado Git inicial
```

Evidencia:

O relatorio de aplicacao registra linhas `M` para os cinco documentos
aplicados, acompanhadas da anotacao "`-- (nao existia)`", e em seguida afirma
que, na abertura da etapa, os cinco arquivos autorizados ja eram `M`.

Regra ou decisao violada:

O relatorio de aplicacao deve representar o estado Git de forma fiel e sem
ambiguidade.

Impacto:

Baixo. O estado Git atual, o diff real e a lista final de arquivos alterados
sao coerentes; a ambiguidade afeta apenas a narrativa do estado inicial da
etapa de aplicacao, que esta auditoria nao consegue reconstruir
retrospectivamente.

Correcao necessaria:

Em etapa propria, se necessario, esclarecer no relatorio de aplicacao se o
bloco representa o estado antes ou depois das edicoes da aplicacao.

## 19. Status literal e normalizado

```yaml
status_literal: ADR_APPLICATION_APPROVED_WITH_NOTES
status_normalizado: APROVADA_COM_OBSERVACOES
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 2
observacoes: 1
```

Justificativa:

A propagacao material da ADR-0023 esta completa e coerente nos cinco documentos
alterados. As notas registradas sao de baixa severidade e nao autorizam
rejeicao da aplicacao.

## 20. Proxima categoria

```yaml
proxima_categoria: PATCH_HANDOFF
gerar_prompt: false
```
