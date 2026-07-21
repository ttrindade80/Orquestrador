# Relatório de QA pós-patch — ADR-0029

## 1. Identificação

```yaml
etapa_executada: QA_ADR
rodada: POS_PATCH
papel_exercido: auditor documental independente
artefato_auditado: docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md
relatorio_anterior: docs/relatorios/RELATORIO_QA_ADR-0029.md
relatorio_criado: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0029.md
data_execucao: 2026-07-20
```

## 2. Objetivo e limites

Objetivo: verificar integralmente o tratamento dos cinco achados da primeira rodada de QA e auditar regressões documentais próximas introduzidas pelo patch.

Limites cumpridos:

- A ADR não foi corrigida.
- A ADR não foi aplicada.
- O relatório de QA anterior não foi alterado.
- O relatório de levantamento não foi alterado.
- Nenhum módulo, handoff, stage ou commit foi criado.
- A proposta externa não foi usada como autoridade documental.

## 3. Estado factual de entrada

CONFORME: `docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md` está não rastreada no Git e foi auditada como artefato pós-patch.

CONFORME: `docs/relatorios/RELATORIO_QA_ADR-0029.md` registra cinco achados ativos na primeira rodada: dois altos, dois médios e um baixo.

CONFORME: a autoridade específica fornecida para D-NOM-13 nesta rodada declara a lista concreta de 16 conceitos como `DECISAO_EXPLICITA_USUARIO`; portanto, essa lista não foi reclassificada como inferência ou decisão ausente.

CONFORME: a ADR mantém `metadata.status: proposta` no frontmatter, declara que a aplicação não foi executada e encerra com `status_literal: ADR_CREATED_AWAITING_QA` e `proxima_categoria: QA_ADR`.

## 4. Autoridades consultadas

Autoridades lidas integralmente:

- `docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md`
- `docs/relatorios/RELATORIO_QA_ADR-0029.md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_REORGANIZACAO_NOMENCLATURA.md`

Autoridades consultadas seletivamente para frontmatter e consumidores:

- `docs/NOMENCLATURA.md`
- `docs/INDICE.md`
- `docs/adr/INDICE_ADR.md`
- `docs/contratos/contrato_estilo.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_cabecalho.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_console.md`
- `docs/contratos/contrato_chip.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_console.md`

## 5. Verificação dos achados originais

| ID | Estado anterior | Evidência do patch | Resultado pós-patch |
| -- | --------------- | ------------------ | ------------------- |
| QA-ADR0029-ALTO-001 | D-NOM-11 a D-NOM-15 sem origem explícita local | D-NOM-11, D-NOM-12, D-NOM-13, D-NOM-14 e D-NOM-15 possuem `Origem: DECISAO_EXPLICITA_USUARIO` imediatamente associada; D-NOM-01 a D-NOM-10 e D-NOM-16 preservam origem explícita | RESOLVIDO |
| QA-ADR0029-ALTO-002 | `contratos_afetados` contraditório e incompleto | O frontmatter distingue `documentos_afetados` com `docs/NOMENCLATURA.md`, `docs/INDICE.md`, `docs/adr/INDICE_ADR.md` e `contratos_afetados` com os nove contratos solicitados; o YAML foi carregado com sucesso | RESOLVIDO |
| QA-ADR0029-MEDIO-001 | D-NOM-13 continha lista concreta sem autoridade local suficiente | D-NOM-13 mantém exatamente os 16 conceitos aprovados, preserva as exclusões e acrescenta origem local `DECISAO_EXPLICITA_USUARIO` | RESOLVIDO |
| QA-ADR0029-MEDIO-002 | Alternativa tinha motivação adicional sem genealogia explícita | A alternativa "Dividir por tipo de conteúdo (schema, regra, histórico) sem separação por domínio" agora é recusada somente porque não atende à organização por domínio aprovada em D-NOM-04 | RESOLVIDO |
| QA-ADR0029-BAIXO-001 | Critério 10 misturava duplicação de definição e preservação de obrigação | O critério 10 distingue regras completas nos contratos, obrigação normativa que não pode desaparecer e definição terminológica ativa sem duplicação entre módulos proprietários ou fachada; o critério 11 reforça que nenhuma regra pode desaparecer por parecer duplicada | RESOLVIDO |

CONFORME: nenhuma decisão D-NOM-01 a D-NOM-16 foi materialmente alterada em relação ao escopo aprovado; os deferimentos da seção 5.3 permanecem deferimentos e nenhum deferimento foi convertido em decisão.

CONFORME: os nove contratos em `contratos_afetados` são consumidores comprovados pelo levantamento e pelos próprios contratos. Há referências diretas a `docs/NOMENCLATURA.md` ou às seções pertinentes em `contrato_estilo`, `contrato_composicao_corpo`, `contrato_barra_de_menus`, `contrato_cabecalho`, `contrato_lancador`, `contrato_console`, `contrato_chip`, `contrato_tela_json` e `contrato_json_console`.

CONFORME: a lista de `contratos_afetados` não é apresentada como lista final de `dependencias_obrigatorias` e `dependencias_condicionais`; D-NOM-10 mantém essa declaração como responsabilidade futura de cada contrato, e a seção 5.3 preserva a "lista exata de dependências de cada contrato" como deferimento não bloqueante.

## 6. Verificação de regressões próximas

CONFORME: o frontmatter é sintaticamente válido; a leitura YAML retornou `metadata.status: proposta`, três `documentos_afetados` e nove `contratos_afetados`.

CONFORME: nenhum documento comum permanece classificado como contrato. `docs/NOMENCLATURA.md`, `docs/INDICE.md` e `docs/adr/INDICE_ADR.md` foram movidos para `documentos_afetados`.

CONFORME: D-NOM-01 a D-NOM-16 possuem origem explícita, com origem nominalmente preservada em todas as decisões.

CONFORME: D-NOM-13 está íntegra: não houve remoção de termo aprovado, inserção de termo adicional, reclassificação como deferimento ou troca de autoridade.

CONFORME: a seção 11 preserva os critérios 10 e 11 sem proibir a coexistência legítima entre definição terminológica no módulo proprietário e regra comportamental completa no contrato.

CONFORME: a seção 12 limita a motivação da alternativa corrigida à incompatibilidade com D-NOM-04.

CONFORME: os deferimentos da seção 5.3 permanecem não bloqueantes, incluindo a lista exata de dependências de cada contrato.

CONFORME: o encerramento mantém:

```yaml
migracao_executada: false
contratos_alterados: false
indice_geral_alterado: false
nomenclatura_monolitica_alterada: false
implementacao_funcional_afetada: false
decisoes_semanticas_reabertas: false
status_literal: ADR_CREATED_AWAITING_QA
proxima_categoria: QA_ADR
```

OBSERVACAO: a seção 7 da ADR não repete todos os nove contratos do frontmatter na tabela de consumidores com referências por seção. Isso não gera correção obrigatória nesta rodada porque os nove consumidores estão comprovados no levantamento e nos contratos, e porque a tabela não é usada como lista final de dependências obrigatórias ou condicionais.

OBSERVACAO: o campo de encerramento `dependencias_por_contrato_definidas: true` deve ser lido como política documental definida, não como dependências individuais já materializadas. Essa leitura é sustentada por D-NOM-10 e pelo deferimento explícito da seção 5.3.

## 7. Achados

Não há achado corretivo novo.

| ID | Classificação | Resultado | Evidência | Impacto |
| -- | ------------- | --------- | --------- | ------- |
| OBS-QA-POS-ADR0029-001 | OBSERVACAO | CONFORME_COM_NOTA | Seção 7 não espelha nominalmente todos os nove contratos do frontmatter, mas os consumidores estão comprovados por levantamento e contratos | Nota de leitura para a futura aplicação; não bloqueia a ADR |
| OBS-QA-POS-ADR0029-002 | OBSERVACAO | CONFORME_COM_NOTA | `dependencias_por_contrato_definidas: true` convive com D-NOM-10 e seção 5.3, que deixam as dependências individuais para etapa futura | Nota de interpretação; não converte deferimento em decisão executada |

## 8. Estado Git

Comandos executados a partir da raiz Git antes da criação deste relatório:

```text
git branch --show-current
master

git log -1 --oneline
c90349c feat: implementa apresentacoes multinivel com modos por tela

git status --short
?? docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_REORGANIZACAO_NOMENCLATURA.md
?? docs/relatorios/RELATORIO_QA_ADR-0029.md

git diff --cached --name-only
<vazio>
```

Checagem executada antes da criação deste relatório:

```text
git diff --no-index --check /dev/null docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md
saida: <vazio>
codigo_de_saida: 1
observacao: codigo 1 esperado para diff contra /dev/null
```

Comandos executados após a criação deste relatório:

```text
git diff --no-index --check /dev/null docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0029.md
saida: <vazio>
codigo_de_saida: 1
observacao: codigo 1 esperado para diff contra /dev/null

git status --short
?? docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_REORGANIZACAO_NOMENCLATURA.md
?? docs/relatorios/RELATORIO_QA_ADR-0029.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0029.md

git diff --cached --name-only
<vazio>
```

Confirmação factual desta etapa:

- A ADR não foi alterada pelo auditor.
- O relatório de QA anterior não foi alterado.
- O relatório de levantamento não foi alterado.
- Somente `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0029.md` foi criado nesta etapa.
- Stage permanece vazio.
- Nenhum commit foi criado.

## 9. Status final

```yaml
status_literal: ADR_APPROVED_WITH_NOTES
status_normalizado: APROVADA_COM_OBSERVACOES
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 2
bloqueios: nenhum
```

## 10. Próxima categoria

```yaml
proxima_categoria: APLICAR_ADR
executar_proxima_categoria: false
```

## 11. Encerramento

```yaml
etapa_executada: QA_ADR
rodada: POS_PATCH
artefato_auditado: docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md
relatorio_anterior: docs/relatorios/RELATORIO_QA_ADR-0029.md
relatorio_criado: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0029.md

achados_originais:
  QA-ADR0029-ALTO-001: RESOLVIDO
  QA-ADR0029-ALTO-002: RESOLVIDO
  QA-ADR0029-MEDIO-001: RESOLVIDO
  QA-ADR0029-MEDIO-002: RESOLVIDO
  QA-ADR0029-BAIXO-001: RESOLVIDO

status_literal: ADR_APPROVED_WITH_NOTES
status_normalizado: APROVADA_COM_OBSERVACOES
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 2
bloqueios: nenhum
git:
  branch: master
  head: c90349c feat: implementa apresentacoes multinivel com modos por tela
  stage: vazio
  commit_criado: false
  arquivos_alterados_pelo_auditor:
    - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0029.md
proxima_categoria: APLICAR_ADR
```
