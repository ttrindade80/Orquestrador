---
name: REL-PATCH-H0041-P02-cor-inativo-e-enter-todos
description: "Patch do handoff H-0041 incorporando a decisão do usuário (cor_inativo: cinza) e a segunda revalidação manual TTY"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_HANDOFF
  status: HANDOFF_PATCH_COMPLETED_AWAITING_QA
  data: 2026-07-28
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: H-0041
  predecessor_imediato: docs/relatorios/RELATORIO_REVALIDACAO_MANUAL_H-0041_R02.md
  achados_tratados:
    - H0041-MANUAL-R02-001
    - H0041-MANUAL-R02-002
    - H0041-MANUAL-R02-003
---

# REL-PATCH-H0041-P02 — Patch

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_HANDOFF
status_literal: HANDOFF_PATCH_COMPLETED_AWAITING_QA
```

## 2. Cadeia

```yaml
raiz: docs/handoff/H-0041-selecao-multipla-estado-comandos-e-apresentacao.md
predecessor_imediato: docs/relatorios/RELATORIO_REVALIDACAO_MANUAL_H-0041_R02.md
achados_tratados:
  - H0041-MANUAL-R02-001
  - H0041-MANUAL-R02-002
  - H0041-MANUAL-R02-003
achados_resolvidos: []
achados_pendentes:
  - H0041-MANUAL-R02-001
  - H0041-MANUAL-R02-002
  - H0041-MANUAL-R02-003
novos_achados: []
```

Nenhum achado é considerado resolvido por este patch: é uma correção documental (autorização), não implementação. Os três permanecem pendentes até o patch técnico P04 e nova revalidação TTY (seção 6.5.8 do handoff).

## 3. Delta aplicado

```yaml
delta_material:
  - id_achado: H0041-MANUAL-R02-002 e H0041-MANUAL-R02-003
    alteracao: >-
      handoff passa a exigir cor_inativo (cinza), origem config/estilo.json,
      hardcode no renderer proibido, capitalizacao normal preservada; proibe
      caixa baixa como indicador de inatividade
  - id_achado: H0041-MANUAL-R02-001
    alteracao: >-
      handoff preserva o achado e exige investigacao/correcao no caminho
      real do TTY (leitura da tecla -> dispatch -> selecao de todos ->
      atualizacao do estado -> redesenho), com teste via ponto de entrada
      e loop reais, nao apenas chamada direta de funcao
arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_H-0041_HANDOFF_P02.md
arquivos_alterados:
  - caminho: docs/handoff/H-0041-selecao-multipla-estado-comandos-e-apresentacao.md
    delta: >-
      rastreabilidade: acrescenta revalidacoes_manuais e patches_documentais;
      nova secao 3.1 registra a revalidacao R02 e a decisao do usuario;
      secao 5 (manifesto de leitura) recebe nota de excecao para P04
      (config/estilo.json, contrato_estilo.md, trecho de tela/loader.py,
      tela/teste_loader.py); secao 6.2 corrigida para nao contradizer a
      nova autorizacao de tela/loader.py/tela/teste_loader.py; nova secao
      6.5 (com subsecoes 6.5.1 a 6.5.8) autoriza nominalmente o patch
      tecnico P04 -- requisito visual obrigatorio, delta de
      config/estilo.json, delta de tela/loader.py (campo cor_inativo em
      EstiloResolvido, ainda inexistente, confirmado por leitura focal),
      delta de tela/renderizador.py (_texto_chip_barra, remover
      texto.lower(), aplicar cor_inativo), preservacao do achado
      Enter/Todos, lista nominal fechada, testes exigidos e exigencia de
      revalidacao futura; secao 9 recebe CA-13/CA-14; secao 10 acrescenta
      tela/teste_loader.py ao comando focal; secao 11 recebe nota de que
      "inativo" no roteiro TTY significa cor_inativo, nunca caixa baixa
arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: "git branch --show-current / rev-parse --short HEAD / diff --cached / diff --check"
    resultado_compacto: "branch master, HEAD 721f8f1, stage vazio, diff --check limpo — conforme esperado no gate"
  - comando_ou_metodo: "grep focal em tela/renderizador.py (_texto_chip_barra, ~1524-1557) e tela/loader.py (EstiloResolvido/carregar_estilo, ~2440-2560), ambos já citados no manifesto do H-0041"
    resultado_compacto: >-
      confirmado que o mecanismo vigente de inatividade e caixa baixa
      (texto.lower()), que cor_inativo e citado no docstring como
      "mecanismo normativo... ainda nao tem valor ANSI concreto", e que
      EstiloResolvido nao possui campo cor_inativo nem carregar_estilo o
      le hoje -- base factual da secao 6.5 do handoff
  - comando_ou_metodo: "git diff --check pos-edicao"
    resultado_compacto: "limpo (arquivo permanece nao rastreado; sem espacos em branco invalidos)"
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
```

Nenhum bloqueio. Estado Git ao final: branch `master`, HEAD `721f8f1`, stage vazio; único arquivo alterado é o handoff (`docs/handoff/H-0041-...md`, ainda não rastreado); único arquivo criado é este relatório. Nenhum arquivo técnico ou normativo adicional foi tocado.
