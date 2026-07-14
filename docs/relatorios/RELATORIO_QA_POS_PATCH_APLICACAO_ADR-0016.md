# Relatório de QA Pós-Patch da Aplicação da ADR-0016

## 1. Identificação da etapa

```yaml
etapa: QA_POS_PATCH
projeto: Orquestrador
ciclo: H-0022 / ADR-0016
data: 2026-07-11
relatorio_criado: docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0016.md
escopo: revalidacao exclusiva do achado QA-APL-ADR16-MED-001
```

Esta auditoria verificou somente a resolução do achado
`QA-APL-ADR16-MED-001`, regressões diretamente relacionadas ao patch de
numeração e o escopo documental da correção. Não foram corrigidos documentos,
contratos, ADRs, relatórios anteriores, handoff, código ou testes.

## 2. ADR e hash de referência

Comandos executados:

```text
wc -l docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
215 docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md

sha256sum docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
afa961fc63d56a02108a8a5b30b8af4ee25668587d0a7907c00e42b824d8faa7  docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
```

Versão confirmada:

```yaml
arquivo: docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
linhas: 215
sha256: afa961fc63d56a02108a8a5b30b8af4ee25668587d0a7907c00e42b824d8faa7
status: aceita
resultado: corresponde_a_referencia
```

## 3. Relatório de QA original

Relatório lido integralmente:

```text
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0016.md
```

O relatório original registrou `ADR_APPLICATION_REJECTED` por um único achado
médio em `docs/contratos/contrato_console.md`, sem achados bloqueantes, altos
ou baixos.

## 4. Achado original

Texto recuperado do relatório original:

```text
id: QA-APL-ADR16-MED-001
severidade: médio
arquivo: docs/contratos/contrato_console.md
linhas: 99, 135, 324
evidencia: as linhas 99 e 135 referenciam "Ver seção 11" para paginação/quebra de página; após a inserção da seção 10, "Paginação" está na seção 12, iniciada na linha 324.
regra_da_adr_ou_contrato: a aplicação declarou renumerar seções posteriores em RELATORIO_APLICACAO_ADR-0016.md, linhas 46-48; o prompt de QA exige verificar referências internas a números de seção.
impacto: referência normativa interna aponta para "Filtros" em vez de "Paginação", prejudicando rastreabilidade e leitura correta do contrato.
correcao_necessaria: atualizar as duas referências internas para apontarem à seção 12.
exige_decisao_do_usuario: não
```

## 5. Verificação antes/depois

Arquivo auditado integralmente:

```text
docs/contratos/contrato_console.md
```

Estado atual confirmado:

- `politica_paginacao`, linha 99: aponta para `Ver seção 12`.
- `politica_quebra`, linha 135: aponta para `Ver seção 12`.
- `## 11. Filtros`, linha 302: seção 11 atual permanece sendo Filtros.
- `## 12. Paginação`, linha 324: seção 12 atual é exatamente Paginação.
- Não há ocorrência residual das duas referências apontando para seção 11.

Classificação do achado:

```text
QA-APL-ADR16-MED-001: RESOLVIDO
```

## 6. Buscas de resíduos

Busca contextual obrigatória executada:

```text
rg -n -C 3 \
'politica_paginacao|politica_quebra|Ver seção 11|Ver a seção 11|Ver seção 12|Ver a seção 12|## 11\.|## 12\.' \
docs/contratos/contrato_console.md
```

Resultado relevante:

```text
99: politica_paginacao ... Ver seção 12.
135: politica_quebra ... Ver seção 12.
302: ## 11. Filtros
324: ## 12. Paginação
```

Busca adicional de variantes de capitalização e acentuação:

```text
rg -n -i -C 2 'ver (a )?se[cç][aã]o 11|ver (a )?secao 11|se[cç][aã]o 11|secao 11|ver (a )?se[cç][aã]o 12|ver (a )?secao 12' docs/contratos/contrato_console.md
```

Resultado: somente as referências esperadas a `Ver seção 12` nas linhas 99 e
135. Busca específica por variantes de `Ver seção 11` não retornou ocorrência.

## 7. Verificação da numeração

Sequência atual das seções em `docs/contratos/contrato_console.md`:

```text
24:## 1. Objetivo
38:## 2. Natureza do `console`
70:## 3. Estrutura mínima da instância
104:## 4. Itens internos heterogêneos
154:## 5. Política de composição
185:## 6. Modo normal e modo verboso
210:## 7. Navegação
234:## 8. Seleção
264:## 9. Enter / ação do item em foco
284:## 10. Ctrl+C em execução interna (ADR-0016)
302:## 11. Filtros
324:## 12. Paginação
351:## 13. Colunas
370:## 14. Relação com `chip` e `barra_de_menus`
393:## 15. Relação com `dashboard` e `lancador`
410:## 16. Regras de uso
448:## 17. Critérios de validação
486:## 18. Pendências fora de escopo
```

Resultado: sequência 1-18 sem duplicações ou saltos introduzidos pela
renumeração. A seção 10 é Ctrl+C em execução interna, a seção 11 é Filtros e
a seção 12 é Paginação.

Não foi encontrada outra referência interna desatualizada causada pela mesma
renumeração no recorte auditado.

## 8. Regressões

Regressões diretamente relacionadas ao patch:

```text
nenhuma
```

Preservação de conteúdo:

- Texto normativo da seção `## 10. Ctrl+C em execução interna (ADR-0016)`:
  sem regressão observada no diff atual, mas proveniência fina do patch:
  `NAO_CONFIRMADO`.
- Texto da seção `## 12. Paginação`: sem regressão observada no diff atual,
  mas proveniência fina do patch: `NAO_CONFIRMADO`.
- Nomes dos campos `politica_paginacao` e `politica_quebra`: preservados.
- Regras, exemplos e terminologia ligados ao achado: preservados.
- Numeração das demais seções: coerente.
- Outros documentos: não alterados por esta auditoria; alterações
  preexistentes no workspace foram preservadas.

A limitação `NAO_CONFIRMADO` decorre do fato de o arquivo já conter alterações
contra `HEAD`; esta auditoria não atribui todo o diff do contrato ao patch.

## 9. Estado Git

Confirmação antes da auditoria:

```text
git branch --show-current
master

git rev-parse HEAD
0b09fa6a99a6d0ed61e9488ecb7e78f16d37cfdf
```

`git status --short` antes da criação deste relatório:

```text
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
```

Verificações executadas:

```text
git diff --check
resultado: sem saída

git diff --cached --name-only
resultado: sem saída
```

`git diff --name-only` antes da criação deste relatório:

```text
scripts/docs/adr/INDICE_ADR.md
scripts/docs/contratos/contrato_console.md
scripts/docs/contratos/contrato_processo_desenvolvimento.md
scripts/docs/contratos/contrato_tela_json.md
scripts/tela/demo.py
scripts/tela/teste_demo.py
```

Conclusões:

- Ausência de stage confirmada.
- `git diff --check` limpo.
- Workspace sujo preexistente preservado.
- Esta auditoria criou somente o relatório pós-patch.

## 10. Arquivos alterados nesta auditoria

Somente:

```text
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0016.md
```

## 11. Novos achados

```text
nenhum
```

## 12. Status final

```text
QA_POS_PATCH_APPROVED_WITH_NOTES
```

Justificativa: o achado `QA-APL-ADR16-MED-001` foi resolvido e não foram
identificadas regressões diretamente relacionadas ao patch. A aprovação é com
notas por limitação de proveniência: o contrato e o workspace já continham
alterações contra `HEAD`, portanto a preservação de todo o conteúdo não pode
ser isolada tecnicamente apenas a partir do diff atual.

## 13. Resultado normalizado da aplicação

```text
resultado_normalizado_da_aplicacao: ADR_APPLICATION_APPROVED
base_documental: APROVADA
```

Este resultado fecha somente a aplicação documental da ADR-0016. Não aprova o
handoff nem a implementação.

## 14. Próxima categoria

```text
QA_HANDOFF
```
