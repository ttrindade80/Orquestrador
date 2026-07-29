---
name: REL-PATCH-H0041-P04
description: "Patch técnico P04 do H-0041: cor_inativo cinza, chips sem caixa baixa, Enter/Todos no caminho TTY"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCH_COMPLETED_AWAITING_QA
  data: 2026-07-28
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0041
  cadeia_raiz: docs/relatorios/IMP-0041-selecao-multipla-estado-comandos-e-apresentacao.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_H-0041_HANDOFF_P02_P01.md
  handoff: docs/handoff/H-0041-selecao-multipla-estado-comandos-e-apresentacao.md
  achados_tratados:
    - H0041-MANUAL-R02-001
    - H0041-MANUAL-R02-002
    - H0041-MANUAL-R02-003
---

# REL-PATCH-H0041-P04 — Patch implementação

> Relatório incremental. Registre somente o delta desta execução e não repita achados já preservados.
>
> Teto normal: 600 palavras. Este relatório não executa nem substitui o QA pós-patch.

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCH_COMPLETED_AWAITING_QA
```

## 2. Cadeia

```yaml
raiz: docs/relatorios/IMP-0041-selecao-multipla-estado-comandos-e-apresentacao.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_H-0041_HANDOFF_P02_P01.md
handoff: docs/handoff/H-0041-selecao-multipla-estado-comandos-e-apresentacao.md
achados_tratados:
  - H0041-MANUAL-R02-001
  - H0041-MANUAL-R02-002
  - H0041-MANUAL-R02-003
achados_resolvidos:
  - H0041-MANUAL-R02-001
  - H0041-MANUAL-R02-002
  - H0041-MANUAL-R02-003
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

```yaml
causas_raiz:
  H0041-MANUAL-R02-001:
    causa: >-
      tty.setcbreak preserva ICRNL; Enter do teclado (CR) chega ao loop TTY
      como LF (\n). processar_comando só reconhecia \r; a tecla era descartada.
      Chamada direta com "\r" mascarava o defeito.
    correcao: demo/demo.py aceita \r e \n como Enter no dispatch de seleção.
  H0041-MANUAL-R02-002:
    causa: _texto_chip_barra usava texto.lower() para inatividade; sem cor_inativo.
    correcao: >-
      cor_inativo=cinza em config/estilo.json; loader transporta o nome
      semântico; renderer aplica ANSI via paleta R-7 e restaura foreground;
      rótulo Executar preservado.
  H0041-MANUAL-R02-003:
    causa: mesma apresentação por caixa baixa; chip Espaço inativo parecia ativo.
    correcao: >-
      Marcar preservado; item não selecionável usa cor_inativo (cinza);
      regra_ativo item_focalizado_selecionavel preservada.

delta_material:
  - id_achado: H0041-MANUAL-R02-001
    alteracao: Enter LF/CR → Todos no caminho TTY real
  - id_achado: H0041-MANUAL-R02-002
    alteracao: Executar + cor_inativo; sem lower()
  - id_achado: H0041-MANUAL-R02-003
    alteracao: Marcar + cor_inativo em item não selecionável

arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_H-0041_P04.md
arquivos_alterados:
  - caminho: config/estilo.json
    delta: adiciona cor_inativo: cinza (demais chaves preservadas)
  - caminho: tela/loader.py
    delta: EstiloResolvido.cor_inativo; _resolver_cor_inativo (V-26; sem fallback)
  - caminho: tela/renderizador.py
    delta: >-
      remove lower(); aplica estilo.cor_inativo; largura visual sem ANSI;
      restaura FG após chip
  - caminho: demo/demo.py
    delta: comando Enter reconhece \r e \n
  - caminho: tela/teste_loader.py
    delta: cobertura cor_inativo presente/ausente/tipo
  - caminho: tela/teste_renderizador.py
    delta: capitalização + sequência de cor; chip Espaço/Enter
  - caminho: demo/teste_demo.py
    delta: Enter LF; apresentação Executar; associação participante→ID
  - caminho: demo/teste_demo_selecao.py
    delta: PTY ponto de entrada real Enter/Todos
arquivos_removidos: []
arquivos_autorizados_inalterados_pelo_P04:
  - config/telas/demo/h0041_selecao_multipla_oito_itens.json
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: reproducao ICRNL (cbreak; write \r → read \n)
    resultado_compacto: confirmado
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tela/teste_loader.py
    resultado_compacto: "coletados=24 aprovados=24 falhas=0"
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tela/teste_renderizador.py
    resultado_compacto: "coletados=311 aprovados=311 falhas=0"
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest -q demo/teste_demo_selecao.py demo/teste_demo.py
    resultado_compacto: "coletados=46 aprovados=46 falhas=0"
  - comando_ou_metodo: conjunto focal (loader+selecao+renderizador+demos)
    resultado_compacto: "coletados=406 aprovados=406 falhas=0"
  - comando_ou_metodo: PYTHONDONTWRITEBYTECODE=1 python -m pytest
    resultado_compacto: "coletados=559 aprovados=559 falhas=0"
  - comando_ou_metodo: PTY demo.demo_selecao + Enter \r
    resultado_compacto: >-
      quatro tg; Executar capitalizado; ANSI cor_inativo; uma tecla
```

Verificação local não equivale a QA independente. PTY é evidência técnica, não validação manual.

```yaml
contagens:
  teste_loader: {coletados: 24, aprovados: 24, falhas: 0}
  teste_renderizador: {coletados: 311, aprovados: 311, falhas: 0}
  testes_demo: {coletados: 46, aprovados: 46, falhas: 0}
  conjunto_focal: {coletados: 406, aprovados: 406, falhas: 0}
  suite_completa: {coletados: 559, aprovados: 559, falhas: 0}
regressoes: nenhuma
```

## 5. Bloqueios e evidências

```yaml
bloqueios: []
estado_git_inicial:
  branch: master
  HEAD: 721f8f1
  stage: vazio
  diff_check: limpo
  patch_P04_antes: AUSENTE
estado_git_final:
  stage: vazio
  diff_check: limpo
  relatorio_P04: criado
nao_declarado:
  - QA aprovado
  - validacao manual aprovada
  - encerramento do H-0041
```
