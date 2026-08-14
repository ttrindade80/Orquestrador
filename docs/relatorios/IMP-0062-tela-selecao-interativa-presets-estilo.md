# IMP-0062 — Tela de seleção interativa de presets de estilo

## rastreabilidade

```yaml
etapa: IMPLEMENTAR
objeto: H-0062
artefato_principal: docs/handoff/H-0062-tela-selecao-interativa-presets-estilo.md
```

## execucao

```yaml
status: IMPLEMENTED
arquivos_criados:
  - tela/estilo.py
  - tela/renderizacao/estilo.py
  - config/telas/demo/h0062_estilo.json
  - tela/teste_estilo.py
  - demo/teste_demo_estilo.py
  - docs/relatorios/IMP-0062-tela-selecao-interativa-presets-estilo.md
arquivos_alterados:
  - demo/demo.py
  - tela/renderizacao/contexto_execucao.py
  - tela/renderizacao/barra_menus.py
  - tela/renderizador.py
```

## resultado

### fatos_materiais

- F4 foi normalizado no decoder físico vigente e encaminhado pelo dispatcher existente; F1, F2, F3, F5 e F11 não receberam ação.
- A tela monta exatamente `borda`, `chip`, `indicadores.selecionado` e `indicadores.incluido`; pais, filhos, escolhas iniciais e amostras são derivados do runtime e dos mapas `presets`.
- O controlador reutiliza `RuntimeEstilo`, `dois_niveis_por_foco` e a transferência exclusiva de seleção. Editar materializa somente o candidato local.
- Enter/Aplicar entrega `SolicitacaoAplicacaoEstilo` imutável, com origem H-0062 e cópias independentes de candidato e baseline. Não há persistência, publicação, popup ou estado de H-0063.
- Esc no nível dos pais reancora o candidato na baseline vigente; `rebase()` preserva uma baseline posteriormente promovida por fluxo externo.

### delta_material

- Adicionados controlador/modelo dinâmico, renderer de amostras, shell declarativo mínimo e integração de ciclo de vida/F4.
- Adicionado estado contextual exclusivo para disponibilidade de Aplicar na barra canônica, mantendo `[?] Ajuda` sempre ativo e último.
- Preservado `config/estilo.json`; nenhuma configuração real foi alterada.

### verificacoes_executadas

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_estilo.py demo/teste_demo_estilo.py` — 13 passed.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest` — 1191 passed.
- `git diff --check` focal — sem achados.
- Inspeção focal de diff/status — stage vazio; deltas documentais e de H-0061 permanecem predecessores esperados.

### demonstracao

- Executado `PYTHONDONTWRITEBYTECODE=1 python demo/demo.py h0062_estilo` com entrada non-TTY contendo Espaço, setas, escolha, Enter e Esc.
- O quadro mostrou as quatro categorias, amostras derivadas, divergência e Aplicar ativo; a saída não persistiu nem publicou estilo.
- O teste de demonstração também abriu a tela por F4 a partir da raiz e confirmou preservação de uma linha contendo somente Espaço.

### validacao_manual_necessaria

- Permanece necessária inspeção visual posterior em TTY real para F4 físico, redesenho, largura/altura e leitura visual das miniaturas. Essa validação não foi declarada automaticamente.

### desvios

[]

### bloqueios

[]
