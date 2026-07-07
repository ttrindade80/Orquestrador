# Relatorio QA — DOC-0025 — Contrato de composicao do corpo conforme ADR-0008

## Status final

`APROVADO_COM_AJUSTES`

O conteudo de `docs/contratos/contrato_composicao_corpo.md` aplica a ADR-0008
de forma coerente para o escopo do DOC-0025. A aprovacao fica com ajuste porque
o estado atual do worktree mostra outros artefatos documentais modificados ou
nao rastreados; portanto, nao e possivel confirmar de forma limpa, apenas pelo
estado Git atual, que nenhum outro contrato, ADR ou indice tenha sido alterado
no conjunto de trabalho em aberto.

## Escopo verificado

- `docs/build_docs/instruction.md`
- `docs/build_docs/to_do.md`
- `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/NOMENCLATURA.md`
- `docs/contratos/contrato_composicao_corpo.md`

Comandos executados:

```bash
git status --short
git diff --check -- docs/contratos/contrato_composicao_corpo.md docs/build_docs/to_do.md
git diff -- docs/contratos/contrato_composicao_corpo.md docs/build_docs/to_do.md
```

Resultado tecnico dos comandos:

- `git diff --check` nao apontou problemas de whitespace nos dois arquivos
  verificados.
- O diff escopado confirma alteracoes em `docs/build_docs/to_do.md` e
  `docs/contratos/contrato_composicao_corpo.md`.
- `git status --short` tambem mostrou outros artefatos modificados ou nao
  rastreados no worktree.

## Evidencias objetivas

| Item | Resultado | Evidencia |
|---|---|---|
| Regra fundamental atualizada para `tela.json` | Conforme | `contrato_composicao_corpo.md:43-58` declara que toda propriedade concreta de composicao do corpo vem do `tela.json`, e que renderer, `barra_de_menus`, `estilo.json` e estado de runtime nao decidem composicao. |
| Taxonomia `console`, `lancador`, `dashboard` preservada | Conforme | `contrato_composicao_corpo.md:64-80` mantem lista fechada com os tres tipos e extensoes futuras por ADR. |
| Composicao concreta migrada de classe/codigo para JSON da tela | Conforme | `contrato_composicao_corpo.md:101-128`, `386-389` e `448-450` tornam o `tela.json` a fonte da composicao e proíbem hardcoding. |
| `dashboard` passivo, nao navegavel, opcional e sem `config/dashboard.json` | Conforme | `contrato_composicao_corpo.md:231-243` registra passividade, nao obrigatoriedade, ausencia de `config/dashboard.json` e conteudo por instancia no `tela.json`. |
| Estrutura antiga do `Info` apenas como draft da tela raiz | Conforme | `contrato_composicao_corpo.md:246-276` trata os 8 campos, Total e marcadores como draft da instancia de `dashboard` do Orquestrador, nao regra universal. |
| `lancador` como instancia no `tela.json` e nao navegavel por `[✥]` | Conforme | `contrato_composicao_corpo.md:163-172` e `209-227` declaram itens por instancia e nao navegabilidade por `[✥]`. |
| `console` como container generico sem detalhar demais itens internos | Conforme | `contrato_composicao_corpo.md:286-303` define politica geral, itens heterogeneos e remete tipos internos a DOC-B008/DOC-0024. |
| Filtros antes da paginacao | Conforme | `contrato_composicao_corpo.md:294`, `452-454` e criterio em `467`. |
| Modo verboso como estado reutilizavel | Conforme | `contrato_composicao_corpo.md:157` e `296-297`. |
| `barra_de_menus` fora do corpo e sem decisao de composicao | Conforme | `contrato_composicao_corpo.md:368-380`; tambem alinhado a `contrato_tela_json.md:452-463`. |
| `[✥]`, `[␣]`, `[⏎]` coerentes | Conforme | `contrato_composicao_corpo.md:298-300` e `373-376`: `[✥]` restrito a `console` navegavel, `[␣]` condicionado a selecao multipla, `[⏎]` ativo/inativo por acao valida no item em foco. |
| `tiling`/arranjo atualizado conforme ADR-0008 | Conforme | `contrato_composicao_corpo.md:131-148` e `341-359` declaram arranjo no `tela.json`, default de estilo apenas quando nao declarado e `dashboard` fora desse eixo. |
| Sem contradicao com `contrato_tela_json.md` | Conforme | `contrato_tela_json.md:158-185`, `191-200`, `208-236`, `240-275`, `279-303`, `425-427` e `555-565` batem com a estrutura e pipeline usados pelo contrato de composicao. |
| `to_do.md` criou/fechou DOC-0025 e atualizou DOC-0018 | Conforme | `to_do.md:237-243` mantem DOC-0018 aberto para contratos remanescentes e informa que `contrato_composicao_corpo.md` foi tratado em DOC-0025; `to_do.md:294-301` registra DOC-0025 como `concluido`. |
| Nenhum outro contrato, JSON, ADR, indice ou codigo alterado nesta tarefa | Parcial / nao confirmavel pelo worktree atual | `git status --short` mostrou `docs/INDICE.md`, `docs/NOMENCLATURA.md`, `docs/adr/INDICE_ADR.md`, `docs/build_docs/to_do.md`, `docs/contratos/contrato_composicao_corpo.md` modificados, alem de `ADR-0008`, `contrato_tela_json.md` e relatorios nao rastreados. Nao ha JSON nem codigo listado como alterado. |

## Problemas encontrados

1. O conteudo do DOC-0025 esta coerente, mas a confirmacao de isolamento total
   do worktree nao pode ser dada sem ressalva: ha outros documentos/indices/ADR
   modificados ou nao rastreados no estado Git atual.
2. O contrato ainda referencia `config/layout_console.json` e
   `config/lancador.json` como artefatos ativos transicionais a reavaliar. Isso
   nao contradiz a ADR-0008 porque o texto marca a transicionalidade, mas deve
   permanecer visivel nas proximas tarefas de aplicacao.

## Recomendacoes de ajuste

- Antes do fechamento operacional do DOC-0025, isolar o pacote de mudancas ou
  registrar explicitamente que as alteracoes em `INDICE`, `NOMENCLATURA`,
  `ADR-0008`, `contrato_tela_json.md` e relatorios pertencem a tarefas
  anteriores/correlatas, nao ao DOC-0025.
- Manter DOC-0018 em `pronto_para_execucao` ate revisar os contratos
  remanescentes (`lancador`, `barra_de_menus`, `cabecalho`, `estilo`).
- Em DOC-0020/DOC-0024, remover ou consolidar o que ainda estiver em modo
  transicional nos contratos especificos de `lancador` e `console`.

## Confirmacao de escopo de alteracao

Durante este QA, o unico arquivo criado/alterado foi este relatorio:

`docs/relatorios/RELATORIO_QA_DOC-0025_CONTRATO_COMPOSICAO_ADR-0008.md`

Nao foram alterados por este QA: contratos, JSONs, ADRs, indices ou codigo.

Pelo estado Git anterior a este relatorio, nao ha JSON nem codigo alterado.
Ha, contudo, outros documentos/indices/ADR modificados ou nao rastreados no
worktree, o que impede a confirmacao absoluta de isolamento do DOC-0025 sem
contexto externo sobre a origem dessas mudancas.
