---
name: REL-QA-0048-reorganizacao-estrutural-dos-testes-do-renderizador
description: "Resultado factual da auditoria independente da implementação do H-0048"
metadata:
  type: relatorio_qa
  etapa_qa: QA_IMPLEMENTACAO
  camada_auditada: IMPLEMENTACAO
  status: I3_HANDOFF_PATCH_REQUIRED
  data: 2026-08-03
rastreabilidade:
  autorizacao_qa: QA_IMPLEMENTACAO — H-0048
  adr_auditada: null
  relatorio_aplicacao: null
  handoff_origem: H-0048
  relatorio_impl: docs/relatorios/IMP-0048-reorganizacao-estrutural-dos-testes-do-renderizador.md
  relatorio_qa_anterior: null
  contrato_alvo: null
  adr_relacionadas:
    - ADR-0039
  issues_relacionadas:
    - ITEM-0022
  cadeia_raiz: H-0048
  predecessor_imediato: H-0047
  achados_tratados: []
---

# REL-QA-0048 — Relatório de QA

## 1. Identificação e status

```yaml
revisao: QA independente da implementação do H-0048 — reorganização estrutural dos testes do renderizador
etapa_qa: QA_IMPLEMENTACAO
camada_auditada: IMPLEMENTACAO
status_literal: I3_HANDOFF_PATCH_REQUIRED
status_normalizado: I3_HANDOFF_PATCH_REQUIRED
proxima_categoria: PATCH_HANDOFF
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: delta técnico do H-0048 e seu relatório de implementação
autoridades_materiais:
  - docs/handoff/H-0048-reorganizacao-estrutural-dos-testes-do-renderizador.md, seções 6.2, 8.2, 8.3, 13, 14 e 17
  - git show HEAD:tela/teste_renderizador.py
  - pytest.ini e docs/templates/TEMPLATE_RELATORIO_QA.md
escopo:
  - fachada, oito proprietários, comum, runner, fixture e equivalência estrutural
  - delta Git, provas reproduzíveis, dependências e relatório IMP-0048
```

## 3. Verificações executadas

```yaml
verificacoes:
  - id: V01
    comando_ou_metodo: baseline Git e inventário fechado de arquivos
    evidencia_focal: master em 5d5d4c794508b1981f5fa65be079b8db748c6064; somente a fachada rastreada e os artefatos previstos
    resultado: OK
  - id: V02
    comando_ou_metodo: comparação AST integral do monólito versionado com os módulos novos
    evidencia_focal: 72 funções, 21 classes, 299 métodos e 371 testes; nenhuma perda ou duplicação; uma diferença de corpo no teste H-0045 PH07
    resultado: FALHA
  - id: V03
    comando_ou_metodo: compilação/importação, coleta, testes focais, módulos, runner e suíte
    evidencia_focal: 12/12, 11/11, 371 coletados, 371 passed, seleção direta 30 passed, runner 1308/1308 e suíte 970 passed; externos 365 passed
    resultado: OK
  - id: V04
    comando_ou_metodo: grafo AST de imports e busca de resíduos
    evidencia_focal: ciclo e resíduos ausentes; integração importa conteudo_externo e comum.py importa tela.loader/tela.modelo
    resultado: FALHA
  - id: V05
    comando_ou_metodo: auditoria do IMP-0048 contra código e template
    evidencia_focal: predecessor H-0047 está correto; a alegação de consumidor em lançador é falsa e os desvios não foram autorizados
    resultado: FALHA
```

## 4. Achados

| ID | Severidade | Requisito violado | Evidência focal | Impacto | Correção necessária |
|---|---|---|---|---|---|
| QA-0048-01 | alto | `_alturas_caixas` deve permanecer em `composicao_corpo.py` | Só é consumido por `_corpo_alturas`; não há consumidor em lançador; implementação define ambos em `comum.py` | propriedade fechada alterada sem autorização | `I2_IMPLEMENTATION_PATCH_REQUIRED` após resolver a arquitetura de `_corpo_alturas` |
| QA-0048-02 | bloqueante | direção/propriedade aprovada para `_corpo_alturas` | Consumido por composição e por `TestCardinalidadeUnitariaH0029` em matriz; handoff o fecha em composição e proíbe dependência entre proprietários | a solução implementada diverge do handoff; o IMP-0048 também afirma, incorretamente, consumo por lançador | `I3_HANDOFF_PATCH_REQUIRED`; o implementador deveria ter emitido `EXCECAO_OPERACIONAL_NECESSARIA` |
| QA-0048-03 | bloqueante | nenhum proprietário deve importar outro proprietário | `integracao.py` importa `conteudo_externo.py` por alias privado para reexecutar `teste_h0037_qapp7_verb_sem_corte_silencioso`; o monólito fazia chamada direta | a preservação da chamada original exige dependência arquitetural não prevista | `I3_HANDOFF_PATCH_REQUIRED`; o implementador deveria ter emitido `EXCECAO_OPERACIONAL_NECESSARIA` |
| QA-0048-04 | alto | `comum.py -> stdlib` | `comum.py` importa `tela.loader` e `tela.modelo`; os helpers compartilhados usam esses tipos e funções | a direção aprovada é inexequível com os proprietários e corpos fechados tal como definidos | `I3_HANDOFF_PATCH_REQUIRED` para autorizar a dependência ou reatribuir os helpers |

Não houve alteração de produção, configuração ou testes externos, nem duplicação de coleta; esses fatos não removem os achados arquiteturais.

## 5. Testes, demonstração e validação manual

```yaml
testes_ou_metodos:
  - comando_ou_metodo: provas H-0048 de compilação, importação, coleta, fixture, módulos, externos e suíte
    resultado_compacto: todas as execuções reproduzidas passaram; 12/12, 11/11, 371, 7, 371, 30, 365 e 970
    prova_semantica: equivalência AST e direção de dependências falham nos achados acima
  - comando_ou_metodo: python tela/teste_renderizador.py contra baseline arquivado
    resultado_compacto: ambos retornam 0 e 1308/1308; saída semântica igual após normalização das raízes absolutas
    prova_semantica: ordem, textos e total preservados
demonstracao:
  resultado: INCOMPLETA
  evidencia: as provas operacionais passam, mas propriedade/direção e equivalência integral não podem ser aprovadas
validacao_manual:
  necessaria: false
```

## 6. Estado Git e itens inesperados

```yaml
estado_git_compacto:
  branch: master
  HEAD: 5d5d4c794508b1981f5fa65be079b8db748c6064
  staged: vazio
  unstaged: tela/teste_renderizador.py
  nao_rastreados: artefatos do H-0048 e resíduos preexistentes previstos no baseline
itens_inesperados: []
```

## 7. Conclusão

A implementação preserva as contagens, a coleta, a fixture, o runner, os testes externos e a suíte completa, mas não cumpre exatamente a arquitetura aprovada. `_corpo_alturas` e o alias entre proprietários exigem decisão formal; a direção de `comum.py` também é contraditória com os helpers fechados. Portanto, o H-0048 não pode ser aprovado nem receber apenas patch de implementação: requer patch do handoff antes de nova implementação.
