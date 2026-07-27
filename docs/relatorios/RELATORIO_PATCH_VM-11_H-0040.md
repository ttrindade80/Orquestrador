# Relatório do Patch VM-11 H-0040

## 1. Identificação

```yaml
etapa: IMPLEMENTACAO_PATCH_VM11_H0040
handoff: H-0040
adr: ADR-0031
origem: VALIDACAO_MANUAL
data: 2026-07-26
```

## 2. Estado de entrada

```yaml
handoff:
  id: H-0040
  classificacao: H1_HANDOFF_APPROVED
  gate: docs/relatorios/RELATORIO_QA_POS_PATCH_HANDOFF_H-0040.md

validacao_manual:
  VM_01_a_VM_10: APROVADOS
  VM_11: FALHOU
  resultado_global: FALHOU_PATCH_NECESSARIO

nova_ADR: nao
relatorio_patch_preexistente: ausente
```

## 3. Reprodução da falha

```yaml
cenario: config/telas/demo/h0040_nav_console_grade_2x3.json
comando_ou_chamada: >
  PYTHONDONTWRITEBYTECODE=1 python -c
  "carregar grade_2x3; estado com g11; largura=32; desconto=3;
   demo.processar_comando(estado, seta_baixo, modelo)"
dimensoes_controladas:
  formacao_inicial: {largura: 80, formacao: 2x3}
  formacao_redimensionada: {largura: 32, formacao_renderer: 3x2}
item_selecionado: g11
item_preservado: true
indicador_reposicionado: true
vizinho_esperado_apos_resize_DOWN: g00
vizinho_efetivamente_usado_antes_da_correcao: g01
primeira_seta_apos_resize_usa_geometria_antiga: true
prova: runtime (processar_comando), nao apenas inferencia estatica
```

Na largura 32, o renderer (com `desconto_estrutural=3`) produz formação `3×2`
e posiciona `g11` em `(2,0)`. Antes da correção, `processar_comando` descartava
`desconto_estrutural`; a primeira seta recalculava a grade com desconto `0`,
ainda em `2×3`, e o DOWN de `g11@(1,1)` ia para `g01` (geometria antiga) em vez
de `g00` (formação atual).

## 4. Causa-raiz

```yaml
causa:
  componente: demo.demo.processar_comando
  defeito: descarte_de_desconto_estrutural_entre_comandos
  efeito: >
    navegacao e renderer consumiam areas uteis diferentes na fronteira de
    formacao; a primeira seta apos resize podia reutilizar vizinhos/toroide
    da formacao anterior apesar do indicador ja estar na celula nova
  decisao_afetada: D10
```

## 5. Correção do runtime

```yaml
preservar_apos_resize:
  - id_do_item_logico
  - console_focado
  - pagina_atual_quando_aplicavel
  - modo_atual
  - desconto_estrutural
  - largura
  - altura

descartar:
  - formacao_anterior
  - linha_coluna_vizinhos_anteriores
  # (nao ha cache explicito; geometria sempre recalculada)

recalcular_antes_da_primeira_seta:
  - formacao_atual
  - linha_coluna_atual
  - vizinhos
  - retorno_toroidal

alteracoes:
  - processar_comando preserva largura/altura/altura_interna/desconto_estrutural
  - loop TTY e non-TTY reafirmam geometria corrente antes de cada comando
  - navegacao.redimensionar aceita nova_altura e documenta ausencia de cache
```

## 6. JSON de 26 itens

```yaml
arquivo: config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json
quantidade_itens: 26
ordem: item_01_a_item_26
todos_navegaveis: true
formacao:
  politica: preferencia_linhas
  linhas: {minimo: 1, maximo: 26}
distribuicao_horizontal: {politica: uniforme}
vao_horizontal: {minimo: 2, dinamico: true}
margem_superior: {minimo: 1, maximo: 1}
vao_vertical: {minimo: 1, maximo: 1}
dimensionamento:
  colunas: maior_da_coluna
  linhas: maior_da_linha
estado_runtime_no_JSON: ausente
```

## 7. Formações encontradas

| Formação | Dimensão encontrada | Tela normal | Item preservado | Navegação correta |
| -------- | ------------------- | ----------: | --------------: | ----------------: |
| 1×26     | 282×80              |        sim |            sim |              sim |
| 2×13     | 151×80              |        sim |            sim |              sim |
| 4×7      | 85×80               |        sim |            sim |              sim |
| 7×4      | 52×80               |        sim |            sim |              sim |
| 13×2     | 28×80               |        sim |            sim |              sim |
| 26×1     | 20×80               |        sim |            sim |              sim |

```yaml
desconto_estrutural_usado: 3
descoberta: varredura empirica de larguras com o JSON real
```

## 8. Distribuição horizontal

```yaml
espacamento_horizontal:
  duas_larguras_com_mesma_formacao:
    formacao: 13x2
    largura_A: 28
    intervalo_A: 2
    largura_B: 39
    intervalo_B: 6
    intervalo_recalculado: true
politica: uniforme
minimo_entre_colunas: 2
```

## 9. Separação vertical

```yaml
espacamento_vertical:
  margem_superior: 1
  linha_vazia_entre_linhas: true
  quantidade: 1
  origem: vao_vertical_da_distribuicao_matricial
  itens_vazios_ou_celulas_falsas: nao
```

## 10. Navegação e toroide

```yaml
navegacao:
  item_logico_preservado: true
  primeira_seta_usa_nova_formacao: true
  vizinhos_recalculados: true
  toroide_recalculado: true
  renderer_navegacao_correspondem: true
  tab_shift_tab_inalterados: true
```

## 11. Arquivos modificados

```yaml
arquivos_modificados:
  - demo/demo.py
  - demo/teste_demo_navegacao.py
  - tela/navegacao.py
  - tela/teste_navegacao.py
  - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
```

## 12. Arquivos criados

```yaml
arquivos_criados:
  - config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json
  - docs/relatorios/RELATORIO_PATCH_VM-11_H-0040.md
```

## 13. Arquivos preservados

```yaml
preservados:
  - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
  - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
  - docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0040.md
  - todos_os_relatorios_de_QA
  - todos_os_relatorios_de_patch_anteriores
  - contratos
  - nomenclatura
  - backlog
  - indices
  - demais_JSONs_h0040
  - tela/distribuicao_matricial.py
  - tela/renderizador.py
  - tela/teste_distribuicao_matricial.py
  - tela/teste_renderizador.py
  - demo/demo_navegacao.py
arquivos_fora_da_lista_alterados: []
```

`distribuicao_matricial` e o renderer já suportavam `preferencia_linhas`,
`uniforme`, `maior_da_coluna`/`maior_da_linha` e `vao_vertical`; nenhuma
alteração material neles foi necessária.

## 14. AT e PN fortalecidos

```yaml
criterios_AT:
  total: 40
  preservados: true
  fortalecidos: [AT-0031, AT-0032]

provas_PN:
  total: 17
  preservadas: true
  fortalecidas: [PN-0012, PN-0016]

novos_IDs: []
```

## 15. Testes focais

```yaml
comando: >
  PYTHONDONTWRITEBYTECODE=1 python -m pytest
  tela/teste_navegacao.py demo/teste_demo_navegacao.py -q
coletados: 57
aprovados: 57
falhas: 0
erros: 0
```

## 16. Regressão direta

```yaml
comando: >
  PYTHONDONTWRITEBYTECODE=1 python -m pytest
  tela/teste_renderizador.py tela/teste_distribuicao_matricial.py
  demo/teste_demo.py tela/teste_loader.py -q
coletados: 352
aprovados: 352
falhas: 0
erros: 0
```

## 17. Suíte canônica

```yaml
comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
coletados: 480
aprovados: 480
ignorados: 0
falhas: 0
erros: 0
duracao: 16.70s
```

## 18. Smoke checks

```yaml
matriz_26:
  comando: >
    printf 's\n' | PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao
    --tela config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json
  exit: 0
  STDERR: vazio
  traceback: ausente
  primeira_renderizacao: tela_normal_com_matriz_e_linha_vazia_entre_linhas
  quadro_minimo: nao
  encerramento_limpo: sim

grade_2x3:
  comando: >
    printf 's\n' | PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao
    --tela config/telas/demo/h0040_nav_console_grade_2x3.json
  exit: 0
  STDERR: vazio
  traceback: ausente
  primeira_renderizacao: tela_normal_2x3
  encerramento_limpo: sim

linear_verboso:
  comando: >
    printf 's\n' | PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao
    --tela config/telas/demo/h0040_nav_console_unico_linear.json --verboso
  exit: 0
  STDERR: vazio
  traceback: ausente
  primeira_renderizacao: tela_normal_verbosa_com_continuacoes
  encerramento_limpo: sim
```

## 19. Compatibilidade

```yaml
VM_01_a_VM_10: materialmente_preservados
Tab_Shift_Tab: inalterados
modo_verboso_forcado: inalterado
Enter: inalterado
espaco: inalterado
paginacao: inalterada
loader_JSONs_anteriores: aceitos
distribuicoes_anteriores: validas
estado_runtime_no_novo_JSON: ausente
logica_independente_do_nome_da_fixture: true
```

## 20. QA não executado

```yaml
QA_executado: nao
```

## 21. Validação manual não executada

```yaml
validacao_manual_executada: nao
motivo: EXCLUSIVA_DO_USUARIO
roteiro_VM11: secao_23_do_H-0040_com_cenario_de_26_itens
```

## 22. Operações Git

```yaml
operacoes_git_de_escrita: []
commit_executado: nao
comandos_leitura:
  - git diff --cached --name-only
  - git diff --name-only
  - git ls-files --others --exclude-standard
  - git status --short --untracked-files=all
  - git diff --check
  - git diff --cached --check
git_diff_check: limpo
```

## 23. Encerramento

```yaml
implementacao_executada: sim
QA_executado: nao
validacao_manual_executada: nao
operacoes_git_de_escrita: []
commit_executado: nao
encerramento: IMPLEMENTATION_PATCH_COMPLETED
```

IMPLEMENTATION_PATCH_COMPLETED
