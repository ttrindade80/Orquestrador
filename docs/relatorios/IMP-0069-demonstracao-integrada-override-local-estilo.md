# IMP-0069 — Demonstração integrada com override local de estilo

```yaml
rastreabilidade:
  etapa: IMPLEMENTAR
  objeto: H-0069

execucao:
  status: IMPLEMENTED
  arquivos_criados:
    - config/telas/demo/h0069_estilo_demonstracao_integrada.json
    - tela/teste_estilo_h0069.py
    - demo/teste_demo_estilo_h0069.py
    - docs/relatorios/IMP-0069-demonstracao-integrada-override-local-estilo.md
  arquivos_alterados:
    - demo/demo.py
```

## Delta material

- **Nova fixture** `h0069_estilo_demonstracao_integrada.json`: Cabeçalho +
  Console (5 itens navegáveis, seleção múltipla) + Dashboard (2 campos
  literais) + Barra de Menus (Esc/Marcar), sem chip com `regra_ativo`
  ligado a `candidato_divergente` — a barra da demonstração é puramente
  visual, não reintroduz o fluxo de Aplicar.
- **`demo/demo.py`** — único arquivo de produção alterado, dentro do ramo
  já autorizado pelo handoff (~linhas 1203-1231) e do ramo `CONFIRMADO`/
  `ABORTADO` (~linhas 862-906):
  - Ao acionar `Enter/Aplicar` com solicitação válida, chama
    `runtime.materializar_local(solicitacao.candidato)` (infraestrutura
    H-0061/H-0066 já existente em `tela/carregamento/estilo.py:347`, não
    alterada) e carrega o modelo da nova fixture via
    `_carregar_modelo_por_id`. Nenhum novo runtime, nenhuma réplica do
    algoritmo de resolução.
  - A demonstração e a origem (`tela_atual` continua `h0063` — sem pilha
    paralela) são guardadas em três chaves de estado novas e
    exclusivamente runtime: `_sessao_demonstracao_estilo` (modelo da
    demonstração), `_modelo_origem_demonstracao_estilo` (modelo real de
    Estilo, para `_modelo_corrente` resolver corretamente mesmo após o
    encerramento) e `estilo_demonstracao_local` (materialização de `C`).
    Padrão espelhado do mecanismo já existente `_sessao_resultado_controle`
    / `_modelo_origem_controle` (H-0044/H-0050).
  - O popup `ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO` (H-0067, inalterado)
    passa a abrir com `fonte=modelo` de Estilo (sua declaração já vive lá)
    mas é **renderizado** sob a mesma `estilo_demonstracao_local` da
    demonstração — `renderizar_estado` seleciona essa materialização em
    vez de `estado["estilo"]` sempre que a sessão de demonstração está
    ativa, sem tocar o `EstiloResolvido` global.
  - `ABORTADO` e `CONFIRMADO` encerram a demonstração (removem
    `_sessao_demonstracao_estilo`/`estilo_demonstracao_local`) preservando
    a origem. `CONFIRMADO` reutiliza `aplicar_solicitacao_confirmada`
    (H-0068) sem modificação de mecanismo, substituindo apenas o `modelo`
    passado para o real modelo de Estilo (necessário porque o `modelo`
    corrente do loop, nesse instante, é o da demonstração).
- Nenhuma alteração em `tela/carregamento/estilo.py`, `tela/estilo.py` ou
  renderizadores genéricos.

## Testes

- `tela/teste_estilo_h0069.py` (5 testes): prova, no nível do runtime, que
  `materializar_local` reflete o candidato sem tocar `baseline`/
  `global_vigente`, sem persistir em `config/estilo.json` (tmp_path), sem
  criar segundo runtime, cobrindo duas categorias simultâneas e o descarte
  equivalente a `ABORTADO`.
- `demo/teste_demo_estilo_h0069.py` (10 testes): candidato divergente abre
  demonstração com as quatro regiões; materialização local corresponde a
  `C`; isolamento de `global_vigente`/`baseline`/`config` durante a
  demonstração; `estado["estilo"]` nunca vira `C`; popup renderizado sob a
  mesma materialização local (prova via caracteres de borda do candidato
  presentes no quadro único e os da baseline ausentes); render real das
  quatro regiões simultâneas; `ABORTADO` preserva `C`/`G1`/`B1` e mantém
  Aplicar ativo; `CONFIRMADO` integra H-0068 (`C` vira `G2`, `estado["estilo"]`
  sincronizado, Aplicar inativo); duas categorias visíveis na fixture; e
  confirmação de que `config/estilo.json` de produção não sofre delta.
- Todos os 15 testes novos passam. Suíte focada H-0063–H-0069
  (`tela/teste_estilo_h006{3..9}.py` + `demo/teste_demo_estilo_h006{3..9}.py`):
  **128 passed, 14 failed** — as 14 falhas pertencem exclusivamente a
  H-0063/H-0064/H-0065/H-0066/H-0067 (ausência de "Ajuda"/"Voltar"/
  "Selecionar"/"Aplicar" no quadro renderizado da barra de Estilo) e foram
  confirmadas **pré-existentes**: reproduzem-se identicamente executando
  apenas os arquivos predecessores, sem carregar nenhum arquivo de H-0069.
  H-0068 e H-0069 (runtime e demo) passam 100%.
- Suíte completa (`PYTHONDONTWRITEBYTECODE=1 python -m pytest`): **1249
  passed, 77 failed, 17 errors**. Reexecutada excluindo os dois arquivos
  novos de H-0069: **1234 passed, 77 failed, 17 errors** — contagem de
  falhas/erros idêntica, confirmando que H-0069 não introduz nenhuma
  regressão; a diferença de 15 aprovados é exatamente a suíte nova.
- `config/estilo.json` de produção: sem delta provocado pelos testes desta
  etapa (todos usam `tmp_path`); a divergência pré-existente contra `HEAD`
  já estava presente no início desta etapa (item de WIP anterior).

## Demonstração reproduzível

```
comando: python demo/demo.py
percurso:
  1. F4 — abre a tela Estilo.
  2. Espaço — entra nos filhos da primeira categoria.
  3. Seta baixo, Espaço — seleciona outro preset (candidato diverge da baseline).
  4. Enter — abre a demonstração integrada (Cabeçalho+Console+Dashboard+Barra)
     com o popup de confirmação sobreposto, ambos sob o candidato.
  5a. Esc — ABORTADO: retorna à tela Estilo; candidato preservado; Aplicar ativo.
  5b. Enter — CONFIRMADO: aplica definitivamente (H-0068); Aplicar inativo.
  6. Redimensionar o terminal durante a demonstração e o popup (regressão
     geométrica H-0067/P01).
resultado_automatizado: >
  128 passed / 14 failed (pré-existentes, fora de escopo H-0069) na suíte
  focada; 1249 passed / 77 failed / 17 errors na suíte completa, com
  regressão zero comprovada por execução comparativa.
```

## Exceções e bloqueios

- **Bloqueios**: nenhum bloqueio à implementação de H-0069.
- **Exceções**: as 14 falhas focadas e o conjunto de 77 falhas/17 erros da
  suíte completa são pré-existentes a esta etapa (fixtures/testes de
  H-0063–H-0067 e de outras áreas do repositório, alheias a ADR-0046);
  não foram alteradas, por estarem fora da lista nominal de arquivos
  autorizados pelo handoff H-0069 e por não corresponderem a expectativa
  superada pelo novo fluxo de demonstração.

```yaml
resultado:
  validacao_manual_H0069: OBRIGATORIA
  validacao_manual_final_item_0010: OBRIGATORIA
  ultimo_handoff_funcional_do_item: true
```
