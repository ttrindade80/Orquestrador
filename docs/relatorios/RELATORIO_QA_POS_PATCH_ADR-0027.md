# Relatório de QA pós-patch da ADR-0027

## 1. Identificação

```yaml
etapa_executada: QA_ADR
tipo_qa: POS_PATCH
adr: ADR-0027
arquivo_auditado: docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
qa_de_origem: docs/relatorios/RELATORIO_QA_ADR-0027.md
achado_verificado: QAADR-0027-001
data: "2026-07-17"
papel: auditor_documental_independente
handoff_relacionado: H-0036
```

## 2. Escopo

Esta auditoria verificou exclusivamente:

- a correção do achado `QAADR-0027-001`;
- a fidelidade do schema semântico incorporado à ADR-0027;
- o escopo real observável do patch;
- a ausência de regressões documentais;
- a suficiência da ADR-0027 para posterior aplicação documental e retomada do
  H-0036 por `PATCH_HANDOFF`.

Nenhuma correção foi feita na ADR. Nenhum contrato, handoff, JSON, teste,
demo ou código foi alterado. Nenhum stage ou commit foi realizado.

## 3. Autoridades e evidências examinadas

Foram lidos integralmente:

```text
docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
docs/relatorios/RELATORIO_QA_ADR-0027.md
docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md
docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
docs/NOMENCLATURA.md
```

O anexo externo `ESTRUTURA_JSON_CONTEUDO_MATRICIAL_E_MULTINIVEL.md` não foi
encontrado como arquivo disponível no repositório nem em
`/home/tiago/.codex/attachments`. Por isso, esta auditoria não o trata como
arquivo normativo ativo do repositório, não afirma sua aplicação aos contratos
e compara a ADR-0027 com a semântica explicitamente descrita no prompt e com o
schema efetivamente incorporado na própria ADR.

## 4. Estado Git

Evidências verificadas antes da criação deste relatório:

```yaml
head: fb9e5be
stage: vazio
commit_novo: nao_realizado
git_diff_check: sem_erros
```

O workspace atual permanece sujo por artefatos acumulados dos ciclos
documentais da ADR-0026, ADR-0027 e H-0036:

```yaml
modificados_rastreados:
  - docs/NOMENCLATURA.md
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_tela_json.md
nao_rastreados:
  - docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
  - docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
  - docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
  - docs/relatorios/RELATORIO_QA_ADR-0026.md
  - docs/relatorios/RELATORIO_QA_ADR-0027.md
  - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md
  - docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md
```

Como a ADR-0027 ainda está não rastreada contra `HEAD`, o Git não permite
isolar historicamente o diff incremental do patch pós-QA. A verificação de
escopo foi, portanto, documental e factual sobre o conteúdo atual da ADR-0027
e sobre o estado Git atual. Não há staged changes, commit novo, erro de
whitespace, alteração de código, alteração de JSON ou alteração de `demo.py`
observável nesta etapa.

## 5. Verificação do achado `QAADR-0027-001`

```yaml
achado_original: QAADR-0027-001
causa_original: ausência do schema semântico mínimo de dados[]
status: corrigido
```

O QA inicial concluiu que a ADR-0027 exigia fixture multinível, validação,
representação semântica, renderização e identidade semântica, mas deixava o
schema de `dados[]` para decisão futura.

Resultado pós-patch:

- a ADR-0027 declara o schema semântico multinível como decidido e obrigatório;
- o schema foi incorporado em D11, com envelope, apresentações, níveis, nós,
  exemplo normativo e exclusão de resultados físicos calculados;
- as validações semânticas mínimas foram incorporadas em D13;
- o schema deixou de aparecer como decisão deferida na seção 14;
- a seção 18 registra explicitamente a correção do achado `QAADR-0027-001`.

Conclusão: o achado original foi resolvido integralmente para o nível de ADR.

## 6. Envelope raiz

A ADR-0027 define como obrigatório o envelope raiz:

```json
{
  "tipo": "multinivel",
  "formato": {
    "apresentacao": "hierarquia",
    "niveis": []
  },
  "dados": []
}
```

A verificação confirmou:

- a raiz é objeto;
- `tipo` é obrigatório;
- `tipo` deve ser `"multinivel"`;
- `formato` é obrigatório e objeto;
- `dados` é obrigatório e array;
- `formato.apresentacao` é obrigatório;
- `formato.niveis` é obrigatório e array;
- os níveis são declarados explicitamente em `formato.niveis`;
- a hierarquia não é inferida de dados de domínio não normalizados.

O valor `"hierarquia"` no exemplo de envelope não torna essa apresentação
obrigatória para todos os documentos, pois a ADR reconhece também `tabela` e
`conjuntos_campos`.

## 7. Schema semântico incorporado

O schema incorporado é fiel ao conjunto declarado no prompt:

```yaml
envelope:
  - tipo
  - formato
  - dados
formato:
  - apresentacao
  - niveis
tipos_de_nivel:
  - container
  - conteudo
  - nome_valor
forma_dos_nos:
  - id
  - nivel
  - titulo
  - nome
  - valor
  - filhos
apresentacoes:
  - tabela
  - hierarquia
  - conjuntos_campos
validacoes_minimas: 20
```

A ADR também separa corretamente representação semântica e representação
física: designadores concretos, geometria, quebras, truncamentos, paginação
física, posições finais, células vazias calculadas e demais resultados
calculados permanecem responsabilidade do renderizador.

## 8. Apresentações multinível

A ADR reconhece as três apresentações exigidas:

```text
tabela
hierarquia
conjuntos_campos
```

Ela define blocos próprios por apresentação e restringe blocos específicos:
`tabela` apenas em apresentação `tabela`, `campos` apenas em
`conjuntos_campos`, e nenhum desses dois blocos em `hierarquia`.

Não foi encontrada regressão que torne `hierarquia` a única apresentação
válida.

## 9. Validações mínimas

A seção D13 contém exatamente 20 validações semânticas mínimas. Elas cobrem:

- envelope raiz;
- valor de `tipo`;
- presença e tipo de `formato` e `dados`;
- `formato.apresentacao`;
- `formato.niveis`;
- integridade dos níveis declarados;
- unicidade de IDs de níveis;
- tipos de nível permitidos;
- forma mínima dos nós;
- referência de `nivel` a nível declarado;
- regras específicas para `container`, `conteudo` e `nome_valor`;
- validação recursiva de filhos;
- preservação da ordem;
- compatibilidade dos campos específicos da apresentação;
- ausência de resultados físicos calculados.

Essas validações removem a lacuna que obrigaria o futuro executor do H-0036 a
inventar schema material de `dados[]`.

## 10. Escopo real do patch

O conteúdo atual da ADR-0027 comprova que o patch foi concentrado na própria
ADR:

- D11 foi expandida com schema semântico multinível;
- D13 foi adicionada com validações mínimas;
- a seção 14 não mantém `schema completo e validações de dados[]` como decisão
  deferida;
- a seção 18 registra o patch e sua relação com `QAADR-0027-001`.

Não há evidência de implementação, alteração de `demo.py`, alteração de JSON,
alteração de contratos ou alteração do H-0036 nesta etapa. O H-0036 permanece
como artefato criado e reprovado, aguardando correção posterior.

Ressalva de auditoria: o workspace acumulado contém vários arquivos
modificados/não rastreados. Assim, a declaração `arquivos_inesperados: []` é
confirmável apenas no escopo lógico do patch da ADR-0027, não como afirmação
de que o workspace inteiro contém somente a ADR-0027.

## 11. Ausência de regressões

Não foram identificadas regressões documentais na ADR-0027. O patch não:

- reintroduz conteúdo externo no JSON estrutural da tela;
- cria campo de vínculo em `tela.json`;
- transforma `config/conteudo/` em convenção global definitiva;
- define protocolo do Pipeline;
- implementa script produtor;
- altera contratos;
- altera o H-0036;
- altera `demo.py`;
- autoriza suporte a `tipo: "matriz"`;
- transfere cálculo físico ao documento externo;
- reabre ADR-0025 ou H-0035.

As tensões remanescentes com os contratos ativos são esperadas: os contratos
ainda refletem a ADR-0026 e deverão ser atualizados em futura aplicação
documental da ADR-0027.

## 12. Suficiência para aplicação documental e retomada do H-0036

A ADR-0027 pós-patch é suficiente para a próxima etapa documental:

```yaml
aplicacao_documental_da_adr_0027: autorizavel
patch_handoff_h_0036: desbloqueavel_apos_aplicacao_documental
implementacao_direta_do_h_0036: nao_autorizada_por_esta_etapa
```

Depois da aplicação documental, o futuro `PATCH_HANDOFF` do H-0036 poderá
remover as premissas bloqueantes identificadas no QA do handoff:

- demo dedicado como prova única;
- ausência do `demo.py` como ponto de entrada real;
- localização global não decidida tratada como convenção;
- schema de `dados[]` por exceção operacional;
- ausência de revisão nominal dos JSONs afetados do H-0035.

A ADR agora fornece autoridade suficiente para fixtures, validações, modelo
semântico, renderização e prova de identidade semântica, desde que primeiro
seja aplicada aos documentos normativos afetados.

## 13. Achados

Nenhum achado novo foi identificado.

```yaml
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
```

## 14. Observações

```yaml
observacoes:
  - id: OBS-QAADRPP-0027-001
    severidade: observacao
    descricao: >
      O anexo externo ESTRUTURA_JSON_CONTEUDO_MATRICIAL_E_MULTINIVEL.md não
      estava disponível como arquivo local auditável. A auditoria comparou a
      ADR contra a semântica explicitada no prompt e contra o conteúdo
      incorporado à ADR, sem tratar o anexo como arquivo normativo ativo do
      repositório.
  - id: OBS-QAADRPP-0027-002
    severidade: observacao
    descricao: >
      O workspace atual está sujo por artefatos acumulados. Isso não indica
      regressão do patch da ADR-0027, mas impede atribuir todo o estado Git
      atual exclusivamente ao patch pós-QA.
```

## 15. Classificação final

```yaml
status_literal: ADR_APPROVED
status_normalizado: ADR-0027 aprovada após patch; achado QAADR-0027-001 corrigido
relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0027.md
achados_originais_corrigidos:
  - QAADR-0027-001
achados_originais_nao_corrigidos: []
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 2
regressoes: []
git:
  head: fb9e5be
  stage: vazio
  commit_novo: nao_realizado
  diff_check: sem_erros
arquivo_criado_nesta_etapa:
  - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0027.md
proxima_categoria: APLICAR_ADR
```
