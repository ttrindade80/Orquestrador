# Relatório de aplicação documental da ADR-0024

```yaml
etapa: APLICAR_ADR
adr: ADR-0024
titulo: Proibição de preenchimento vazio externo do corpo
relatorio: docs/relatorios/RELATORIO_APLICACAO_ADR-0024.md
data: 2026-07-15
papel: autor_documental
status_literal: APLICACAO_COMPLETA_PENDENTE_QA
status_normalizado: COMPLETA

arquivos_modificados:
  - docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
  - docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_tela_json.md
  - docs/NOMENCLATURA.md
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_json_tela_minima.md

arquivos_criados:
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0024.md

arquivos_nao_modificados_com_conflito_ativo: []

decisoes_propagadas:
  - DA-01
  - DA-02
  - DA-03
  - DA-04

novas_decisoes_introduzidas: []
alteracoes_json_realizadas: false
handoff_criado: false
commit_realizado: false
```

## 1. Escopo

Esta aplicação documental propagou a ADR-0024 — Proibição de preenchimento vazio
externo do corpo — nos documentos normativos afetados. A ADR-0024 estava aprovada
(`status_literal: ADR_APPROVED`, QA pós-patch `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0024.md`).

Não foram realizadas implementações de código, não foram alterados JSONs de
configuração, não foi criado o H-0033 e não foram introduzidas novas decisões
arquiteturais além das DA-01 a DA-04 já aprovadas na ADR-0024. A ADR-0024 não
foi modificada.

## 2. Autoridades lidas

- `docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md` — autoridade
  normativa principal desta aplicação
- `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0024.md` — QA com
  `status_literal: ADR_APPROVED`, zero achados bloqueantes/altos/médios/baixos
- `docs/relatorios/RELATORIO_QA_ADR-0024.md` — histórico; não é autoridade

## 3. Alterações realizadas

### 3.1 `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`

**Substituição parcial pela ADR-0024:** adicionada seção ao final do documento
identificando a cláusula 4 como historicamente substituída. O texto original da
cláusula 4 foi preservado como registro histórico. As cláusulas 1, 2, 3, 5, 6,
7, 8, 9 e 10 permanecem integralmente válidas. Documentadas as regras DA-01 a
DA-04 como nova norma complementar vigente.

### 3.2 `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`

**Três alterações:**

1. **D2 (seção "Decisão"):** adicionada anotação após o bullet que autorizava
   preenchimento externo vazio na ausência de `distribuicao`, identificando-o como
   substituído pela ADR-0024 e indicando DA-01 a DA-04.

2. **Seção "Semântica da ausência de `distribuicao`":** substituído o trecho
   "espaço vertical excedente pode permanecer como preenchimento externo do corpo,
   conforme a ocupação vertical já normatizada pela ADR-0013" por redação alinhada
   com DA-01 e DA-02.

3. **Seção "Relação com a ADR-0013":** atualizado último parágrafo que afirmava
   que "o preenchimento externo da ADR-0013 permanece o comportamento aplicável
   (D2)"; substituído por texto que remete à ADR-0024 e às regras DA-01/DA-02.

4. **Seção final adicionada:** "Substituição parcial pela ADR-0024 (2026-07-15)"
   com a distinção normativa entre DA-01 (cardinalidade unitária, válida) e DA-02
   (múltiplos elementos sem distribuição, inválida).

### 3.3 `docs/contratos/contrato_composicao_corpo.md`

**Cinco alterações:**

1. **Seção 4.7 (título atualizado para "ADR-0013, ADR-0024"):** substituído
   parágrafo que descrevia linhas em branco preenchendo a área por texto que
   exige ocupação por elementos visuais conforme DA-01 a DA-04.

2. **Seção 5.7 "Ausência de distribuicao":** subsistema normativo completamente
   substituído; inseridos os quatro blocos normativos (DA-01 a DA-04) no lugar
   do texto que autorizava preenchimento externo vazio e sobra externa do container.

3. **Seção 5.9:** atualizado último período para referenciar DA-01 a DA-04 e
   ADR-0024 em vez de "(seção 5.7, ADR-0013)".

4. **Seção 8 (critérios de verificação):** atualizado o critério sobre ausência
   de `distribuicao`; adicionados três novos critérios de validação declarativa
   (DA-01 a DA-04).

5. **Seção 10:** atualizado último parágrafo que afirmava que "o preenchimento
   externo da ADR-0013 é o comportamento aplicável na ausência de distribuição".

### 3.4 `docs/contratos/contrato_tela_json.md`

**Duas alterações:**

1. **Seção 8 (bloco "Semântica de `corpo.distribuicao`"):** substituído o trecho
   que afirmava "a sobra permanece como preenchimento externo, conforme a ocupação
   vertical da ADR-0013"; adicionados os quatro blocos de validação declarativa
   obrigatória (DA-01 a DA-04 com critérios por tipo de situação); referências
   atualizadas para incluir ADR-0024.

2. **Seção 9 (bloco "Ocupação vertical da janela"):** substituído "com
   preenchimento de linhas em branco pelo renderer quando o conteúdo declarado
   for menor" por texto que exige ocupação por elementos visuais, proíbe linhas
   em branco externas e remete a DA-01 a DA-04.

### 3.5 `docs/NOMENCLATURA.md`

**Três alterações em 14.1 e seção 14.2 adicionada:**

1. **14.1 bullet "Ausência de `corpo.distribuicao` ≠ modo `igual`":** substituído
   "sobra permanece como preenchimento externo do corpo (`ocupacao_vertical_terminal`,
   ADR-0013)" por texto que exige ocupação por elementos visuais conforme DA-01/DA-02.

2. **14.1 último parágrafo:** substituído "o preenchimento externo da ADR-0013 é
   o comportamento aplicável na ausência de distribuição" por redação que remete
   à ADR-0024 e às regras DA-01 a DA-04; adicionada referência à ADR-0024 ao
   lado da ADR-0018 no encerramento da seção.

3. **Seção 14.2 adicionada:** "Glossário da proibição de preenchimento vazio
   externo do corpo (ADR-0024)" com tabela de termos normativos (`elemento visual`,
   `grupo`, `espaço externo proibido`, `espaço interno`, `cardinalidade unitária`,
   `composição inválida`) e quatro regras normativas derivadas.

### 3.6 `docs/adr/INDICE_ADR.md`

Adicionada linha de entrada para ADR-0024 com sumário normativo completo incluindo
DA-01 a DA-04, substituições parciais (ADR-0013 cláusula 4, ADR-0018 D2) e
referência ao H-0033.

### 3.7 `docs/contratos/contrato_json_tela_minima.md` — PATCH_DOCUMENTACAO (APADR0024-DOC-001)

Arquivo identificado como fora da lista original da etapa APLICAR_ADR. Conflito
normativo corrigido em etapa complementar PATCH_DOCUMENTACAO.

**Duas correções:**

1. **Seção 6.2 — Nó estrutural `grupo`:** substituído o trecho "e a sobra permanece
   como preenchimento externo do container, conforme a ocupação já normatizada
   (ADR-0013)" por texto que: proíbe explicitamente sobra como preenchimento externo;
   propaga DA-03 (grupo repassa área aos descendentes visuais); propaga DA-01
   (descendente único ocupa integralmente a área); propaga DA-02 e DA-04 (múltiplos
   descendentes sem `distribuicao` tornam a composição inválida com rejeição
   explícita). Referência à ADR-0013 como autoridade de preenchimento externo
   removida; ADR-0024 adicionada.

2. **Seção 6.3 — Distribuição por container:** substituído o trecho "e a sobra
   permanece como preenchimento externo do container (ADR-0013)" por texto que:
   proíbe explicitamente sobra como preenchimento externo; propaga DA-01, DA-02 e
   DA-04; enuncia explicitamente que composição que não consiga atribuir toda a área
   a elemento visual é inválida e deve ser rejeitada sem fallback silencioso, sem
   distribuição implícita e sem alteração automática do JSON. Referência à ADR-0013
   como autoridade de preenchimento externo removida; ADR-0024 adicionada.

**Frontmatter:** ADR-0024 adicionada a `adrs_aplicadas`.

## 4. Conflito ativo em arquivo não modificado — histórico preservado

O bloqueio abaixo foi identificado ao final da etapa APLICAR_ADR original e
registrado como `BLOCKED_DOCUMENTATION`. Foi corrigido em etapa complementar
PATCH_DOCUMENTACAO (achado APADR0024-DOC-001). O histórico é preservado.

```yaml
arquivo: docs/contratos/contrato_json_tela_minima.md
status_original: CONFLITO_ATIVO_NAO_RESOLVIDO
status_atual: RESOLVIDO
motivo_original: arquivo_fora_da_lista_permitida
linhas_conflitantes_originais:
  - linha: 252-253
    texto: >
      "a sobra permanece como preenchimento externo do container, conforme a
      ocupação já normatizada (ADR-0013)"
  - linha: 277-278
    texto: >
      "a sobra permanece como preenchimento externo do container (ADR-0013)"
classificacao_original: bloqueio_documental
resolucao: PATCH_DOCUMENTACAO
achado_corrigido: APADR0024-DOC-001
bloqueio_removido: BLOCKED_DOCUMENTATION
```

## 4.1 Reconciliação documental — PATCH_DOCUMENTACAO (APADR0024-DOC-001)

```yaml
reconciliacao_documental:
  achado: APADR0024-DOC-001
  arquivo_corrigido: docs/contratos/contrato_json_tela_minima.md
  motivo_da_correcao: >
    O arquivo preservava regra normativa incompatível com a ADR-0024 nos trechos
    das seções 6.2 (grupo) e 6.3 (distribuição por container), autorizando sobra
    como preenchimento externo do container com referência à ADR-0013, em
    contradição direta com DA-01 a DA-04.
  trechos_corrigidos:
    - secao: "6.2 — Nó estrutural grupo"
      texto_anterior: >
        "a sobra permanece como preenchimento externo do container, conforme a
        ocupação já normatizada (ADR-0013)"
      texto_posterior: >
        "A ausência de `distribuicao` não autoriza sobra como preenchimento externo
        do container; toda área atribuída ao grupo deve ser repassada integralmente
        aos descendentes visuais (DA-03, ADR-0024): com exatamente um descendente
        visual, esse elemento ocupa integralmente a área disponível (DA-01); com
        múltiplos descendentes disputando o mesmo eixo, `distribuicao` é obrigatória
        — a ausência torna a composição inválida e exige rejeição explícita
        (DA-02, DA-04)."
    - secao: "6.3 — Distribuição por container"
      texto_anterior: >
        "a sobra permanece como preenchimento externo do container (ADR-0013)"
      texto_posterior: >
        "A ausência de `distribuicao` não autoriza sobra como preenchimento externo
        do container (ADR-0024): com exatamente um descendente visual aplicável,
        esse elemento ocupa integralmente a área disponível (DA-01); com múltiplos
        elementos disputando o mesmo eixo, `distribuicao` é obrigatória — a ausência
        torna a composição inválida e exige rejeição explícita (DA-02, DA-04);
        composição que não consiga atribuir toda a área a elemento visual é inválida
        e deve ser rejeitada explicitamente, sem fallback silencioso, sem distribuição
        implícita e sem alteração automática do JSON (DA-04)."
  regras_propagadas:
    - DA-01
    - DA-02
    - DA-03
    - DA-04
  bloqueio_anterior: BLOCKED_DOCUMENTATION
  bloqueio_apos_correcao: nenhum
  busca_de_residuos: >
    Uma ocorrência residual encontrada após a correção (seção 6.2): "distribuicao
    não autoriza sobra como preenchimento externo do container" — classificada como
    normativa ativa e conforme: enuncia a proibição (não a permissão). Nenhum
    conflito residual remanescente.
  proxima_categoria: QA_APLICACAO_ADR
```

## 5. Resíduos aceitos como histórico preservado

Os trechos abaixo foram identificados na busca de resíduos e classificados como
**contexto histórico preservado** — não são normas ativas em conflito:

| Arquivo | Linha | Classificação |
|---|---|---|
| `ADR-0013:182` | "inclusive com preenchimento de linhas em branco quando o conteúdo declarado for menor" | Seção "Consequências / Testes futuros" — texto histórico anterior à ADR-0024; ADR-0013 já possui seção de substituição parcial ao final |
| `ADR-0018:38-39` | "com preenchimento de linhas em branco pelo renderer / quando o conteúdo declarado for menor" | Seção "Contexto" — descrição do estado histórico ao tempo da ADR-0018; não é seção normativa "Decisão" |

## 6. Verificação do escopo

| Restrição | Status |
|---|---|
| Não implementar código | Cumprida — nenhum arquivo `.py` ou equivalente foi tocado |
| Não alterar JSONs de configuração | Cumprida — nenhum arquivo em `config/` foi tocado |
| Não criar H-0033 | Cumprida |
| Não executar QA de aplicação | Cumprida |
| Não introduzir novas decisões | Cumprida — apenas DA-01 a DA-04 propagadas |
| Não modificar ADR-0024 | Cumprida |
| Não fazer commit | Cumprida |
| Modificar apenas os arquivos permitidos | Cumprida — 7 documentos modificados na APLICAR_ADR original; `contrato_json_tela_minima.md` corrigido em PATCH_DOCUMENTACAO (APADR0024-DOC-001) |

## 7. Estado git ao final da aplicação

Estado ao final da APLICAR_ADR original:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
 M docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
?? docs/relatorios/RELATORIO_QA_ADR-0024.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0024.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0024.md
```

Estado esperado após PATCH_DOCUMENTACAO (adicionado `contrato_json_tela_minima.md`):

```text
 M docs/NOMENCLATURA.md
 M docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
 M docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_tela_json.md
 M docs/contratos/contrato_json_tela_minima.md
?? docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
?? docs/relatorios/RELATORIO_QA_ADR-0024.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0024.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0024.md
```

Nenhum arquivo em `config/`, `tela/` ou `docs/handoff/` foi tocado.

## 8. Próximas etapas previstas

1. ~~**Resolver bloqueio documental**~~ — **resolvido** em etapa PATCH_DOCUMENTACAO
   (achado APADR0024-DOC-001, arquivo `docs/contratos/contrato_json_tela_minima.md`).
   Nenhum bloqueio documental remanescente.
2. **QA_APLICACAO_ADR:** executar auditoria independente da aplicação documental
   completa. O bloqueio `BLOCKED_DOCUMENTATION` foi zerado; a aplicação está apta
   para QA de aplicação.
3. **Criar H-0033:** implementar DA-01 a DA-04 no renderer, conforme previsto pela
   ADR-0024 (seção 22), após aprovação do QA de aplicação.
4. **Commit:** após conclusão do QA de aplicação, criar commit único com ADR-0024
   e todas as alterações de aplicação documental.
