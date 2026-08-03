---
name: REL-PATCH-H0045-P07-geometria-recursiva-por-console
description: "Torna geometria_console recursiva (grupo/matriz) e remove o fallback silencioso para console ausente (QA-H0045-P06-001)"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCHED
  data: 2026-07-31
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0045-P07
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P06.md
  achados_tratados:
    - QA-H0045-P06-001
---

# REL-PATCH-H0045-P07 — Patch

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
```

## 2. Cadeia

```yaml
raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P06.md
achados_tratados:
  - QA-H0045-P06-001
achados_resolvidos:
  - QA-H0045-P06-001
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

### Causa raiz confirmada

`_geometria_por_console` reimplementava manualmente, à mão, apenas a partição
de PRIMEIRO NÍVEL do corpo raiz (vertical/horizontal), sem nunca descer em
`grupo`/`estrutura: matriz` — documentado explicitamente como limitação.
`geometria_console` reagia à ausência de `console.id` no mapa resultante com
`next(iter(geometria.values()))`: a geometria de QUALQUER outro elemento do
corpo raiz, entregue silenciosamente a um console ausente ou a um console
dentro de grupo (que nunca chegava ao mapa). `navegacao.lista_foco` já
atravessa grupos (`_atravessar_elementos`), então consoles em grupo já eram
focalizáveis/pagináveis pelo runtime — só a autoridade geométrica ficara para
trás.

### Direção adotada

Em vez de reimplementar as regras de DA-01/DA-02/matriz/maiores-restos numa
segunda função (duplicação vedada pelo prompt), `_geometria_por_console`
passou a **delegar inteiramente** a `_renderizar_container` — a MESMA função
usada por `renderizar_tela` para montar o corpo real, já com a recursão em
`grupo`/`estrutura: matriz` implementada (H-0027/H-0035). Um parâmetro opcional
`registro_geometria` (dict) foi enfiado por `_renderizar_container` →
`_renderizar_container_vertical`/`_horizontal`/`_matriz` → `_caixa_de_elemento`
— o ÚNICO ponto de despacho de console de toda a árvore. Ali, quando o
elemento é um console e `altura_alvo` é um inteiro concreto (cota física
resolvida pelo container pai, nunca `None`/natural), a geometria
(`inner_w + 2`, `altura_alvo - 2`) é registrada como efeito colateral —
exatamente os mesmos valores usados para montar a caixa real. `renderizar_tela`
não passa esse parâmetro, então o render normal fica byte-a-byte inalterado.

`geometria_console` deixou de ter fallback: `console=None`, `console.id`
ausente do mapa, ou geometria global insuficiente devolvem `None`
explicitamente (`dict.get`, sem `next(iter(...))`). Os dois únicos chamadores
(`demo._com_geometria_real_do_console`, `demo._reconciliar_paginacao_apos_resize`)
já tratavam `None` preservando o estado corrente sem processar o comando —
nenhuma mudança foi necessária ali.

```yaml
delta_material:
  - id_achado: QA-H0045-P06-001
    alteracao: >
      _geometria_por_console agora delega a _renderizar_container(...,
      registro_geometria=resultado) em vez de calcular apenas o corpo raiz;
      registro_geometria é roteado por _renderizar_container_vertical/
      _horizontal/_matriz até _caixa_de_elemento, onde é populado por
      console.id sempre que altura_alvo é uma cota concreta; geometria_console
      usa dict.get (sem fallback para next(iter(...))).
arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P07.md
arquivos_alterados:
  - caminho: tela/renderizador.py
    delta: >
      _caixa_de_elemento, _renderizar_container_vertical,
      _renderizar_container_horizontal, _renderizar_container_matriz e
      _renderizar_container ganham o parâmetro registro_geometria
      (repassado inalterado; sem novo comportamento quando None).
      _geometria_por_console reescrita para delegar a _renderizar_container
      (com try/except RenderizadorErro -> {}). geometria_console usa
      dict.get e retorna None sem fallback; console=None retorna None cedo.
  - caminho: tela/teste_renderizador.py
    delta: >
      6 testes novos (H-0045-P07): console direto (regressão), console em
      grupo, dois consoles no mesmo grupo, grupo aninhado (cota considera
      ancestrais), console ausente (None sem fallback), estrutura matriz.
  - caminho: demo/teste_demo_paginacao.py
    delta: >
      1 teste integrado novo (Teste 7): sequência foco distante / seleção /
      resize / seta / expansão / alternância de foco / paginação
      independente, com os dois consoles DENTRO do mesmo grupo horizontal.
      Cobertura via modelo construído inteiramente em memória
      (ElementoCorpo/ModeloTela), sem depender de fixture em
      config/telas/demo/.
arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: >
      pytest tela/teste_paginacao.py tela/teste_navegacao.py
      tela/teste_renderizador.py demo/teste_demo_paginacao.py -q
    resultado_compacto: 400 passed
  - comando_ou_metodo: >
      pytest tela/teste_paginacao.py tela/teste_navegacao.py
      tela/teste_renderizador.py tela/teste_loader.py tela/teste_selecao.py
      tela/teste_fluxo_execucao.py demo/teste_demo_paginacao.py
      demo/teste_demo_navegacao.py demo/teste_demo_selecao.py
      demo/teste_demo.py -q
    resultado_compacto: 570 passed
  - comando_ou_metodo: pytest -q (suíte completa)
    resultado_compacto: 802 passed (795 pré-patch + 7 novos)
  - comando_ou_metodo: >
      script não-TTY cobrindo console direto, console em grupo, dois
      consoles no mesmo grupo, console ausente, resize, página
      seguinte/anterior, seta e quadro final
    resultado_compacto: >
      concluído sem exceção; console_p/console_q em grupo receberam
      {"largura": 40, "altura_interna": 16} cada (nunca o fallback
      {"largura": 80, "altura_interna": 17} do corpo raiz); console ausente
      retornou None
```

Verificação local não equivale a QA independente.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
evidencias_separadas:
  - arquivo: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0045_P06.md
    finalidade: achado QA-H0045-P06-001 (causa raiz e evidência original)
    leitura_necessaria_para: [QA_POS_PATCH]
```

Validação manual (R05 consolidada) permanece **pendente do usuário** —
não foi iniciada nesta etapa, conforme instrução do prompt.
