---
name: RELATORIO_QA_HANDOFF_H-0043
description: "Auditoria independente do handoff H-0043 (carregamento e apresentação da tela padrão de resultado)"
metadata:
  type: relatorio_qa
  etapa_qa: QA_HANDOFF
  camada_auditada: HANDOFF
  status: H2_HANDOFF_PATCH_REQUIRED
  data: 2026-07-29
rastreabilidade:
  handoff_origem: docs/handoff/H-0043-carregamento-apresentacao-tela-padrao-resultado.md
  adr_auditada: docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md
  contrato_alvo:
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
---

# RELATORIO_QA_HANDOFF_H-0043 — Relatório de QA

## 1. Identificação e status

```yaml
revisao: H-0043 — carregamento e apresentação da tela padrão de resultado
etapa_qa: QA_HANDOFF
camada_auditada: HANDOFF
status_literal: H2_HANDOFF_PATCH_REQUIRED
status_normalizado: patch_do_handoff_necessario
proxima_categoria: PATCH_HANDOFF
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: docs/handoff/H-0043-carregamento-apresentacao-tela-padrao-resultado.md
autoridades_materiais:
  - ADR-0036 D-H3-01 a D-H3-19
  - contrato_tela_json.md §34; contrato_json_console.md §14; contrato_console.md §23; contrato_composicao_corpo.md §3.1.1; contrato_barra_de_menus.md §23.4
  - tela/loader.py (baseline preservado, alteração limitada pela seção 6.5.10 do handoff)
escopo:
  - fidelidade normativa, fronteira H3/H4, coesão de responsabilidades, exequibilidade do manifesto, testes, demonstração e validação manual
```

## 3. Verificações executadas

```yaml
verificacoes:
  - id: V01
    comando_ou_metodo: leitura integral do handoff, ADR-0036 e dos cinco contratos-alvo; leitura focal das seções indicadas do backlog e INDICE_ADR
    evidencia_focal: fronteira H3/H4 (D-H3-19), envelope (D-H3-11 a D-15a), seis cenários (D-H3-16/17), manifesto (D-H3-18) todos fielmente reproduzidos pelo handoff
    resultado: OK
  - id: V02
    comando_ou_metodo: verificação de existência de todos os arquivos preexistentes citados pelo handoff (loader.py, execucao_focal.py, demo.py, executor_sintetico.py, demo_execucao_focal.py, suítes de teste) e das funções reutilizadas
    evidencia_focal: `resultado_json_sintaticamente_valido` (tela/execucao_focal.py:107), `resultado_semanticamente_valido` (:224) existem; todos os caminhos do manifesto (seção 6.1) e da seção 6.2 conferem com o repositório real
    resultado: OK
  - id: V03
    comando_ou_metodo: simulação estrutural do JSON normativo da seção 6.5.1 contra `tela/loader.py::_console_em_escopo_d23` (linhas 1574-1607) e comparação com o precedente aprovado `config/telas/demo/h0037_console_verboso_dois_niveis.json`
    evidencia_focal: o elemento `console_resultado` de 6.5.1 declara simultaneamente os seis campos do envelope pré-ADR-0028 (`origem_dados`, `itens`, `politica_composicao`, `politica_navegacao`, `politica_selecao`, `politica_paginacao`, `politica_exibicao`) e o marcador D23 `formato.excesso.politica_modo`; o loader rejeita essa combinação com `TelaEstruturaInvalida` ("envelope pré-ADR-0028 e consumidor multinivel externo são mutuamente exclusivos")
    resultado: FALHA
```

## 4. Achados

| ID | Severidade | Requisito violado | Evidência focal | Impacto | Correção necessária |
|---|---|---|---|---|---|
| QA-H0043-001 | bloqueante | `tela/loader.py::_console_em_escopo_d23` (baseline preservado, fora do escopo de alteração da seção 6.5.10); ADR-0036 §8 (truncamento fora de escopo); H-0043 §6.4 (truncamento proibido); H-0043 §6.5.1 texto próprio ("modo_inicial não é declarado") | H-0043 §6.5.1 declara, no mesmo elemento `console_resultado`, os campos do envelope pré-ADR-0028 (`origem_dados: null`, `itens: []`, `politica_composicao` com `overflow_normal: truncar_com_reticencias`, `politica_navegacao`, `politica_selecao`, `politica_paginacao`, `politica_exibicao: {modo_inicial: normal, verboso: false}`) junto do marcador D23 `formato.excesso.politica_modo: somente_verboso`. `_console_em_escopo_d23` rejeita essa combinação (`n_base>=1 and _tem_d23`) com `TelaEstruturaInvalida`. O precedente aprovado `config/telas/demo/h0037_console_verboso_dois_niveis.json` (mesma política `somente_verboso`) declara apenas `id`/`tipo`/`titulo`/`formato.excesso.politica_modo`, sem nenhum campo do envelope clássico. Adicionalmente, `overflow_normal: truncar_com_reticencias` contradiz a exclusão explícita de truncamento (ADR-0036 §8; H-0043 §6.4), e `modo_inicial: normal` contradiz a própria regra vinculante do handoff que proíbe `modo_inicial` em política fixa. | O artefato nominal central do manifesto (`config/telas/demo/resultado_execucao.json`) seria rejeitado pelo loader existente exatamente como especificado; nenhum dos seis cenários poderia ser carregado sem desvio silencioso da especificação. | Reescrever a seção 6.5.1: o elemento `console_resultado` deve ser um consumidor D23 puro — apenas `id`, `tipo`, `titulo`, `formato: {excesso: {politica_modo: somente_verboso}}` (sem `modo_inicial`) —, removendo `origem_dados`, `itens` e as cinco políticas do envelope pré-ADR-0028 do JSON estrutural estático; ajustar a seção 6.5.2 (validação do loader) e os critérios/testes correspondentes (CA-03, CA-04) para essa forma corrigida. |

## 6. Testes, demonstração e validação manual

```yaml
testes_ou_metodos:
  - comando_ou_metodo: comandos da seção 10 (pytest -q --tb=short sobre os quatro grupos e suíte completa)
    resultado_compacto: todos os arquivos preexistentes citados existem; `tela/teste_resultado_execucao.py` é novo, conforme manifesto; comando canônico `PYTHONDONTWRITEBYTECODE=1 python -m pytest` é o vigente no repositório
    prova_semantica: casos mínimos cobrem schema/perfil, escolha documento/envelope, ordem e conteúdo do envelope, sessão/SIGWINCH, integração e regressão de H-0042/seleção — mas dependem da correção de QA-H0043-001 para serem executáveis contra a tela nominal
demonstracao:
  resultado: seis cenários especificados via demo/demo.py, sem impressão direta de quadros nem bypass do loader/módulo/renderer; mecanismo de despacho adicional em demo.py explicitamente autorizado e justificado (catálogo 1:1 atual não comporta seis cenários para uma única tela estrutural)
  evidencia: seção 11, IDs/fixtures/quadros nominais completos e consistentes com o manifesto
validacao_manual:
  necessaria: true
  metodo_reproduzivel: seis roteiros TTY 80x24 com respostas fechadas (seção 11.1), corretamente reservados ao usuário e não preenchíveis pelo agente de implementação
  resultado: pendente_do_usuario
  criterios_pendentes: [QA-H0043-001 corrigido]
```

## 8. Estado Git e itens inesperados

```yaml
estado_git_compacto:
  branch: master
  HEAD: 6ecc4cd
  staged_inicial: []
  preexistentes_iniciais:
    - docs/adr/INDICE_ADR.md (modificado, fora deste ciclo)
    - docs/backlog.md (modificado, fora deste ciclo)
    - docs/contratos/contrato_barra_de_menus.md (modificado, fora deste ciclo)
    - docs/contratos/contrato_composicao_corpo.md (modificado, fora deste ciclo)
    - docs/contratos/contrato_console.md (modificado, fora deste ciclo)
    - docs/contratos/contrato_json_console.md (modificado, fora deste ciclo)
    - docs/contratos/contrato_tela_json.md (modificado, fora deste ciclo)
    - docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md (não rastreado)
    - docs/handoff/H-0043-carregamento-apresentacao-tela-padrao-resultado.md (não rastreado)
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0036.md, RELATORIO_PATCH_APLICACAO_ADR-0036_P01.md, RELATORIO_QA_ADR-0036.md, RELATORIO_QA_APLICACAO_ADR-0036.md, RELATORIO_QA_POS_PATCH_ADR-0036_P01.md, RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0036_P01.md (não rastreados)
  criado_nesta_etapa: docs/relatorios/RELATORIO_QA_HANDOFF_H-0043.md
itens_inesperados: nenhum — todos os artefatos preexistentes pertencem ao ciclo acumulado da ADR-0036, conforme o estado transportado
hashes_handoff_adr:
  antes:
    handoff: 671ec49344dd7e2f02b47199fa793a674a21e62c618a5188ed90e85cc5eca65f
    adr: 27a5474e4c0c97bd80ae2d81e3939ff225535b94f6ad942c821206471f07d9b3
  depois:
    handoff: 671ec49344dd7e2f02b47199fa793a674a21e62c618a5188ed90e85cc5eca65f
    adr: 27a5474e4c0c97bd80ae2d81e3939ff225535b94f6ad942c821206471f07d9b3
```

## 9. Conclusão

O handoff é fiel à ADR-0036 e aos contratos vigentes em todas as decisões semânticas (fronteira H3/H4, regra de escolha documento/envelope, schema do envelope, manifesto nominal, testes e validação manual exigidos), e não antecipa nenhuma responsabilidade do Handoff 4. Contudo, QA-H0043-001 é bloqueante: o JSON normativo da seção 6.5.1 — o artefato central do manifesto — é estruturalmente rejeitado pelo `tela/loader.py` preservado, tornando o próprio handoff inexequível como especificado, sem que nenhuma alteração de arquivo fora do manifesto seja necessária para corrigi-lo (a correção está inteiramente dentro do próprio texto do handoff). H-0043 requer patch antes de autorizar implementação; permanece não implementado.
