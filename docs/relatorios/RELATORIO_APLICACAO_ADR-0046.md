# RELATORIO_APLICACAO_ADR-0046

## Baseline

- Projeto: Orquestrador.
- Branch: `master`.
- HEAD: `77bd8bf3772985325bc51a850f7c6d76d61ad573`.
- Stage inicial e final: vazio.
- Deltas documentais preexistentes do ciclo, inclusive backlog, ADR-0046 e
  relatórios, preservados sem alteração por esta aplicação.

## Fontes lidas integralmente

- `docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md`.
- `docs/relatorios/RELATORIO_QA_ADR-0046.md`.
- `docs/nomenclatura/10_ESTILO.md`.
- `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`.
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`.
- `docs/nomenclatura/32_CONSOLE.md`.
- `docs/nomenclatura/35_POPUP.md`.
- `docs/contratos/contrato_estilo.md`.
- `docs/contratos/contrato_barra_de_menus.md`.
- `docs/contratos/contrato_console.md`.
- `docs/contratos/contrato_popup.md`.

Nenhum relatório histórico adicional foi explorado.

## Arquivos normativos alterados

- `docs/nomenclatura/10_ESTILO.md`.
- `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`.
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`.
- `docs/nomenclatura/35_POPUP.md`.
- `docs/contratos/contrato_estilo.md`.
- `docs/contratos/contrato_barra_de_menus.md`.
- `docs/contratos/contrato_popup.md`.

## Arquivos avaliados e preservados sem alteração

- `docs/nomenclatura/32_CONSOLE.md`: a política vigente
  `dois_niveis_por_foco` já define pais/filhos, escolha exclusiva por pai,
  transferência por Espaço e independência entre cursor e escolha.
- `docs/contratos/contrato_console.md`: o contrato já materializa integralmente
  a política consumida pelo `ITEM-0010`; nenhuma especialização de estilo era
  necessária no domínio genérico do console.

## Regras antigas substituídas

- A carga única de `config/estilo.json` e a imutabilidade do objeto resolvido
  durante toda a sessão em `10_ESTILO.md` §4.8.
- A imutabilidade/reconstrução de tela de `contrato_estilo.md` R-4.
- A limitação de materialização única por sessão de `contrato_estilo.md` R-10.
- As remissões que ainda mantinham a funcionalidade de estilos fora do
  contrato ou aguardando decisão futura.

## Novas regras materializadas

- Materialização inicial a partir de `config/estilo.json` e exatamente uma
  materialização global vigente em cada instante.
- Separação entre configuração persistida, materialização global vigente,
  configuração candidata e override local de demonstração.
- Materialização de candidato para validação/demonstração sem publicação e
  isolamento do override à demonstração e ao pop-up.
- Ordem obrigatória: persistência completa e válida → publicação/substituição
  controlada do estilo global; atomicidade fechada do ponto de vista dos
  consumidores, sem impor mecanismo físico de gravação.
- Falha de persistência preserva configuração persistida e materialização
  global anteriores e não descarta o candidato.
- No `ITEM-0010`, alteração somente dos `preset_default` de `borda`, `chip`,
  `indicadores.selecionado` e `indicadores.incluido`, preservados os demais
  valores.
- `F4` como acionamento global de Estilo; `Enter/Aplicar` ativo somente quando
  candidato diverge da baseline persistida; barra subjacente suspensa durante
  o pop-up.
- Pop-up textual como consumidor do sistema genérico, renderizável sob
  override local do chamador, com retorno somente `CONFIRMADO` ou `ABORTADO` e
  sem persistência, publicação ou lógica de negócio.

## Decisões sem alteração documental adicional

- A navegação `dois_niveis_por_foco` já cobria integralmente a instanciação do
  `ITEM-0010`; os dois documentos de console foram preservados.
- O tipo genérico `texto` já satisfazia a confirmação; nenhum tipo novo de
  pop-up foi criado.
- Tiling, cores configuráveis, `indicadores.concluido`, F1, F11, mapa de
  F2/F3/F5 e ajuda declarativa dos chips permaneceram fora da aplicação.
- `config/estilo.json`, código, ADRs, backlog, histórico e handoffs não foram
  alterados.

## Verificações mecânicas obrigatórias

- Diff de todos os arquivos alterados: inspecionado.
- Alterações fora do escopo permitido: nenhuma.
- `git diff --check`: **PASS**.
- Regras antigas incompatíveis simultaneamente vigentes: nenhuma; as menções
  remanescentes registram a supersessão pela ADR-0046.
- Stage final: vazio.
- Commit e push: não realizados.

## Bloqueios

Nenhum.

## Status terminal

`ADR_APPLICATION_COMPLETED`
