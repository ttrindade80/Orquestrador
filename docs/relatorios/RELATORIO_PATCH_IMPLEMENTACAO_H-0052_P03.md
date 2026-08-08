# Relatório — Patch de implementação H-0052 P03

```yaml
status: PATCH_IMPLEMENTACAO_CONCLUIDO
handoff: H-0052
patch: P03
origem: validacao_manual_2_de_3_pos_P02
defeito: indicador_navegar_ausente_com_multiplos_itens_navegaveis
causa: >-
  exibir_chip_navegar() retornava True para o console focalizado com item_a e
  item_b, mas a fixture declarava somente chip_esc e chip_ajuda; a composição
  da barra materializa apenas chips declarados e não inventa indicadores.
arquivos_alterados:
  - config/telas/demo/h0052_nivel_unico_explicito.json
  - tela/teste_navegacao.py
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0052_P03.md
testes:
  focal: "1 passed, 50 deselected"
  escopo_autorizado: "135 passed"
suite_integral: "1060 passed in 28.91s"
validacao_manual: PENDENTE_REEXECUCAO_2_DE_3
bloqueios: nenhum automatizado; validacao visual permanece pendente do usuario
```

Diagnóstico: `exibir_chip_navegar()` não era a causa; para a fixture, a
condição semântica era verdadeira. A barra deixou de materializar o indicador
porque seu proprietário (`tela/renderizacao/barra_menus.py`) filtra e renderiza
somente chips presentes em `barra_de_menus.chips`. O caso legado equivalente,
`h0040_nav_console_unico_linear`, declara o mesmo `chip_navegar` canônico e
passa pela mesma infraestrutura.

A correção adicionou à fixture H-0052 o chip canônico `[✥] Navegar`, com a
regra de existência já contratada. O teste preventivo carrega a fixture real,
confirma console focalizável, pelo menos dois itens, movimento efetivo,
`exibir_chip_navegar() == True` e a materialização final de `[✥] Navegar`.

Nenhuma capacidade nova foi criada: `nivel_unico`, A/B, setas, paginação,
seleção e as demais fixtures foram preservados. A observação visual manual não
é declarada aprovada neste relatório.
