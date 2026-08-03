---
name: RELATORIO_PATCH_HANDOFF_H-0045_P12
description: "Autorização complementar nominal de dois testes em demo/teste_demo.py para desbloquear o PATCH_IMPLEMENTACAO P24"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_HANDOFF
  status: HANDOFF_PATCHED
  data: "2026-08-02"
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: H-0045 / VM-H0045-R08-001
  cadeia_raiz: VM-H0045-R08-001
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P24.md
  achados_tratados:
    - IMP-H0045-P24-001
---

# RELATÓRIO — PATCH_HANDOFF P12 (H-0045 / VM-H0045-R08-001)

## status: HANDOFF_PATCHED

## 1. Bloqueio tratado

`IMP-H0045-P24-001`: a correção de `QA-H0045-P23-002` (relançar erro
estrutural em `_resolver_conteudo`) e de `QA-H0045-P23-003` (unificar o
quadro controlado para altura insuficiente) colide com duas asserções
vigentes em `demo/teste_demo.py`, arquivo fora do escopo autorizado pelo
P24. A correção em si permanece viável dentro do escopo já autorizado
(`demo/demo.py`); o único bloqueio é documental.

## 2. Autorização complementar aplicada

Acrescentada ao handoff a §24, cumulativa à §23, autorizando nominalmente
`demo/teste_demo.py` restrito a dois testes e ao suporte local diretamente
indispensável dentro deles:

1. `teste_redimensionamento_reativo_h0023` (seção 8.12, `:2313-2317`) —
   nova expectativa: `RenderizadorErro("r")` é erro estrutural sintético,
   sem produtor geométrico correspondente; `_resolver_conteudo` deve
   relançá-lo; o teste passa a exigir propagação explícita, não quadro
   mínimo.
2. `test_h0044_p01_redimensionamento_resolve_bloqueio_visual`
   (`:3984-3985`) — nova expectativa: altura insuficiente usa o mesmo
   quadro controlado do H-0045; o teste deve verificar as duas mensagens
   (`"Terminal pequeno demais"` e `"Aumente a janela para continuar"`), sem
   depender apenas da capitalização antiga, preservando a prova de
   recuperação após aumentar a dimensão.

## 3. Limites da autorização

Restrita aos dois testes nominados; não autoriza alteração de outros testes
do arquivo, refatoração geral, alteração de helpers compartilhados além do
indispensável, remoção de cobertura legada, alteração produtiva de H-0023
ou H-0044, alteração do renderer, ou de contratos/configurações.

## 4. Preservação da §23

A §23 (autorização focal de largura horizontal/terminal insuficiente na
barra de cinco chips) permanece integralmente vigente e não foi reescrita
além do necessário para registrar a autorização adicional. A correção
produtiva futura do P24 (remover `startswith("DA-0")`, reconhecer apenas o
formato específico de `erro_layout` e os produtores reais de `altura
insuficiente`, unificar o quadro controlado em `80x8`) foi registrada em
§24.4 como pendente, não antecipada por esta etapa.

## 5. Testes futuros e `git diff --check`

Registrados em §24.5: suíte focal filtrada (`-k "P23 or p23 or P24 or p24
or redimensionamento_reativo_h0023 or h0044_p01"`), suíte dos quatro
arquivos autorizados, suíte completa, e `git diff --check` sobre os cinco
arquivos autorizados. Nenhum desses comandos foi executado nesta etapa
documental.

## 6. Bloqueios

Nenhum. `git diff --check` sobre o handoff está limpo. `VM-H0045-R08-001`
permanece aberto até continuação do P24, QA técnico e validação manual.
