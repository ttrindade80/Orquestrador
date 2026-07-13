# QA pos-patch H-0029 - comandos demo.py

## 1. Identificacao

```yaml
ciclo: H-0029
tipo: QA_POS_PATCH
data: 2026-07-13
auditor: Codex
status_literal: QA_POS_PATCH_COMPLETED
status_normalizado: I5_MANUAL_VALIDATION_REQUIRED
validacao_manual: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

Esta auditoria verifica exclusivamente o patch documental que corrigiu os
comandos de abertura das sete telas permanentes `h0029_*` pelo `tela/demo.py`.
Nenhum codigo, teste, JSON, handoff ou relatorio anterior foi corrigido durante
este QA. A unica saida criada por esta etapa e este relatorio.

## 2. Arquivos consultados

- `scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0029_TELAS_PERMANENTES.md`
- secao 16 de `scripts/docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md`
- `scripts/tela/demo.py`
- `scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md`, somente para confirmar o mecanismo esperado e a validacao manual obrigatoria em TTY real

## 3. Conferencia Git

Raiz Git:

```text
/home/tiago/Dropbox/UFRGS/Survey/versao_0_1
```

`git status --short`, antes da criacao deste relatorio:

```text
 M scripts/tela/renderizador.py
 M scripts/tela/teste_renderizador.py
?? scripts/config/telas/h0029_dashboard_fracao.json
?? scripts/config/telas/h0029_dashboard_igual.json
?? scripts/config/telas/h0029_dashboard_percentual.json
?? scripts/config/telas/h0029_grupo_fracao.json
?? scripts/config/telas/h0029_grupo_igual.json
?? scripts/config/telas/h0029_grupo_pai_distribuido.json
?? scripts/config/telas/h0029_grupo_percentual.json
?? scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
?? scripts/docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
?? scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md
?? scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_DISTRIBUICAO_CONTAINERS_CARDINALIDADE_UNITARIA.md
?? scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_POS_CORRECAO_GRUPO_MINIMO.md
?? scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_POS_PATCH_TELAS_PERMANENTES.md
?? scripts/docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
?? scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0029_TELAS_PERMANENTES.md
```

Conferencias obrigatorias:

```yaml
git_diff_check:
  codigo_saida: 0
  saida: ""
demo_py:
  comando: git diff -- scripts/tela/demo.py
  codigo_saida: 0
  diff: ""
config_telas:
  comando: git diff -- scripts/config/telas/
  codigo_saida: 0
  diff: ""
caches_ou_temporarios_inesperados:
  comando: find scripts -path '*/__pycache__/*' -o -name '.pytest_cache' -o -name '*.tmp' -o -name '*.swp'
  codigo_saida: 0
  saida: ""
```

Conclusao Git:

- `scripts/tela/demo.py` esta sem alteracao.
- Nao ha diff em `scripts/config/telas/`.
- Nenhum JSON existente foi alterado por este patch.
- Os sete JSONs `h0029_*` permanecem como arquivos nao rastreados do ciclo H-0029, sem diff registrado por esta auditoria.
- Nao houve stage nem commit.
- `git diff --check` esta limpo.

## 4. Verificacao do mecanismo corrigido

A construcao documentada na secao 16 segue semanticamente:

```python
original = demo.criar_estado_inicial

def criar_estado_da_tela():
    estado = original()
    estado["tela_atual"] = "<id>"
    return estado

demo.criar_estado_inicial = criar_estado_da_tela
demo.main()
```

Confirmacoes:

- a funcao original e chamada uma unica vez por inicializacao;
- `tela_atual` e alterada no mesmo dicionario retornado por `original()`;
- o mesmo estado modificado e retornado;
- `demo.main()` carrega a tela inicial a partir de `estado["tela_atual"]`;
- a substituicao ocorre somente no namespace do modulo carregado no processo atual;
- o mecanismo nao edita `demo.py`;
- o mecanismo nao edita JSON.

Verificacao nao interativa do estado:

```yaml
- tela: h0029_dashboard_igual
  tela_atual: h0029_dashboard_igual
  chamadas_original: 1
  resultado: APROVADO
- tela: h0029_dashboard_fracao
  tela_atual: h0029_dashboard_fracao
  chamadas_original: 1
  resultado: APROVADO
- tela: h0029_dashboard_percentual
  tela_atual: h0029_dashboard_percentual
  chamadas_original: 1
  resultado: APROVADO
- tela: h0029_grupo_pai_distribuido
  tela_atual: h0029_grupo_pai_distribuido
  chamadas_original: 1
  resultado: APROVADO
- tela: h0029_grupo_igual
  tela_atual: h0029_grupo_igual
  chamadas_original: 1
  resultado: APROVADO
- tela: h0029_grupo_fracao
  tela_atual: h0029_grupo_fracao
  chamadas_original: 1
  resultado: APROVADO
- tela: h0029_grupo_percentual
  tela_atual: h0029_grupo_percentual
  chamadas_original: 1
  resultado: APROVADO
```

## 5. Smoke tests obrigatorios

Os sete comandos finais documentados foram executados a partir de `scripts/`,
em modo pipe, com entrada controlada `s\n` apenas para iniciar a renderizacao
real e encerrar a TUI sem interacao prolongada.

```yaml
- tela: h0029_dashboard_igual
  codigo_saida: 0
  primeira_linha_ou_titulo: "╭ H-0029 DASHBOARD IGUAL"
  tela_alvo_confirmada: sim
  orquestrador_aberto_indevidamente: nao
  tui_real_iniciada: sim
  resultado: APROVADO
- tela: h0029_dashboard_fracao
  codigo_saida: 0
  primeira_linha_ou_titulo: "╭ H-0029 DASHBOARD FRACAO"
  tela_alvo_confirmada: sim
  orquestrador_aberto_indevidamente: nao
  tui_real_iniciada: sim
  resultado: APROVADO
- tela: h0029_dashboard_percentual
  codigo_saida: 0
  primeira_linha_ou_titulo: "╭ H-0029 DASHBOARD PERCENTUAL"
  tela_alvo_confirmada: sim
  orquestrador_aberto_indevidamente: nao
  tui_real_iniciada: sim
  resultado: APROVADO
- tela: h0029_grupo_pai_distribuido
  codigo_saida: 0
  primeira_linha_ou_titulo: "╭ H-0029 GRUPO PAI DISTRIBUIDO"
  tela_alvo_confirmada: sim
  orquestrador_aberto_indevidamente: nao
  tui_real_iniciada: sim
  resultado: APROVADO
- tela: h0029_grupo_igual
  codigo_saida: 0
  primeira_linha_ou_titulo: "╭ H-0029 GRUPO IGUAL"
  tela_alvo_confirmada: sim
  orquestrador_aberto_indevidamente: nao
  tui_real_iniciada: sim
  resultado: APROVADO
- tela: h0029_grupo_fracao
  codigo_saida: 0
  primeira_linha_ou_titulo: "╭ H-0029 GRUPO FRACAO"
  tela_alvo_confirmada: sim
  orquestrador_aberto_indevidamente: nao
  tui_real_iniciada: sim
  resultado: APROVADO
- tela: h0029_grupo_percentual
  codigo_saida: 0
  primeira_linha_ou_titulo: "╭ H-0029 GRUPO PERCENTUAL"
  tela_alvo_confirmada: sim
  orquestrador_aberto_indevidamente: nao
  tui_real_iniciada: sim
  resultado: APROVADO
```

Conclusao dos smokes:

- 7/7 comandos abriram a tela `h0029_*` solicitada.
- 0/7 comandos abriram indevidamente `ORQUESTRADOR` como tela inicial.
- 7/7 comandos exercitaram `demo.main()` e o pipeline real do `demo.py`.
- Nenhum comando alterou arquivos persistentes.

## 6. Regressao proporcional

Como o patch auditado alterou somente comandos documentados no relatorio de
implementacao, e como `demo.py`, testes e JSONs nao apresentam alteracao
posterior detectada por diff, foi executado o teste proporcional obrigatorio:

```yaml
comando: python tela/teste_demo.py
diretorio: scripts/
codigo_saida: 0
total_verificacoes: 303
passaram: 303
falharam: 0
```

A suite canonica `1449/1449` registrada na implementacao permanece aceita como
evidencia anterior, pois a auditoria confirmou ausencia de diff em `demo.py` e
em `scripts/config/telas/` apos o patch documental auditado. Nao houve alteracao
material que exigisse repetir a suite canonica completa.

## 7. Achados

```yaml
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
```

O achado anterior `QA-POS-H0029-001` esta corrigido para o escopo auditado:

```yaml
id: QA-POS-H0029-001
status: CORRIGIDO
evidencia:
  - mecanismo documentado chama a funcao original uma unica vez
  - estado retornado preserva tela_atual h0029_* nos sete identificadores
  - smoke tests confirmam as sete telas alvo
  - nenhum smoke iniciou pela tela raiz ORQUESTRADOR
```

## 8. Classificacao final

```yaml
status_literal: QA_POS_PATCH_COMPLETED
status_normalizado: I5_MANUAL_VALIDATION_REQUIRED
relatorio: scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0029_COMANDOS_DEMO.md
achado_QA_POS_H0029_001: CORRIGIDO
mecanismo_corrigido: sim
telas_alvo_confirmadas: 7/7
orquestrador_aberto_indevidamente: nao
smoke_tests: 7/7 APROVADOS
teste_demo: 303/303
codigo_saida: 0
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes:
  - nao foi realizada validacao visual humana
  - nao foi alterado codigo
  - nao foi alterado teste
  - nao foi alterado JSON
  - nao houve stage nem commit
git:
  git_diff_check: limpo
  demo_py: sem_diff
  config_telas: sem_diff
  caches_ou_temporarios_inesperados: nenhum
validacao_manual: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
proxima_categoria: VALIDACAO_MANUAL
```
