# IMP-0063 — Tela de Estilo: estrutura e navegação em dois níveis

```yaml
rastreabilidade:
  etapa: IMPLEMENTAR
  objeto: H-0063
  artefato_principal:
    docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md
  handoff_historico: H-0062
  item: ITEM-0010
  adr: ADR-0046

execucao:
  status: IMPLEMENTED
  arquivos_criados:
    - config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json
    - tela/teste_estilo_h0063.py
    - demo/teste_demo_estilo_h0063.py
    - docs/relatorios/IMP-0063-tela-estilo-estrutura-navegacao-dois-niveis.md
  arquivos_alterados:
    - tela/estilo.py
    - tela/renderizacao/estilo.py
    - tela/renderizador.py
    - demo/demo.py
  arquivos_removidos:
    - tela/teste_estilo.py
    - demo/teste_demo_estilo.py

autorizacao_adicional_de_escopo:
  arquivos:
    - tela/teste_estilo.py
    - demo/teste_demo_estilo.py
  motivo:
    - residuos_executaveis_do_H-0062_substituido

tratamento_testes_historicos:
  removidos:
    - tela/teste_estilo.py
    - demo/teste_demo_estilo.py
  cobertura_migrada: []
  cobertura_ja_existente_no_h0063:
    - quatro_pais_e_presets_dinamicos
    - escolhas_iniciais_preset_default
    - cursor_vs_filho_escolhido
    - espaco_exclusivo_observacional
    - decoder_F4
    - F4_abre_tela_e_ignora_F1_F2_F3_F5_F11
    - saida_pela_pilha_sem_mutacao
```

## Resultado

### fatos_materiais

- F4 abre a tela declarativa `h0063_estilo_estrutura_navegacao_dois_niveis`
  pelo dispatcher vigente (Cabeçalho + Console + Barra de Menus).
- Console usa `dois_niveis_por_foco` com `politica_selecao: multipla` apenas
  como compatibilidade declarativa; cada pai mantém uma escolha exclusiva.
- Quatro pais fixos; filhos vêm dinamicamente de `presets` em
  `config/estilo.json` (leitura via baseline do runtime).
- Espaço/Esc/setas reutilizam a navegação canônica; Espaço não altera
  candidato, `preset_default` persistido, global nem publicação.
- Resize usa o pipeline normal (`SIGWINCH` / `_resolver_conteudo`); paginação
  canônica evita geometria fixa de popup.
- Removidos os módulos de teste executáveis do H-0062 substituído; nenhuma
  cobertura vigente foi perdida — o que restava já está em
  `teste_estilo_h0063` / `teste_demo_estilo_h0063`.

### delta_material

- Controlador observacional em `tela/estilo.py` (projeção `ConteudoExterno`).
- Shell JSON H-0063 sem Aplicar/popup.
- `demo/demo.py`: F4 → H-0063; render pela tela normal; rótulo Esc
  “Retornar aos pais” só nesta tela.
- Renderer popup-like H-0062 substituído por `associar_conteudo_estilo`.

### verificacoes_executadas

- `pytest tela/teste_estilo_h0063.py demo/teste_demo_estilo_h0063.py`
  → 19 passed.
- `pytest` completo → 1197 passed (coleta sem símbolos H-0062).
- `git diff --check` nos arquivos autorizados → limpo.
- `config/estilo.json` sem delta; stage vazio.
- H-0062 documental e normativos não alterados nesta execução.

### demonstracao

- `python demo/demo.py h0063_estilo_estrutura_navegacao_dois_niveis` (non-TTY,
  100×30): entrada/transferência/Esc/saída; quadro com pais; sem Aplicar;
  global inalterado.

### validacao_manual_necessaria

- F4 físico em TTY.
- Aparência inequívoca de tela completa (não popup).
- Navegação física entre níveis e resize físico sem resíduos.
- Legibilidade estrutural em terminal real.

### desvios

- Chip `[PgUp][PgDn]` declarado para paginação canônica necessária ao resize
  em dimensões usuais; fora da lista mínima do handoff, mas coerente com
  H-0055/`dois_niveis_por_foco`.

### bloqueios

- Nenhum após a autorização adicional dos dois módulos de teste H-0062.
