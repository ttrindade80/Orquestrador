# Relatório — Criação do Handoff H-0074

## Etapa

`CRIAR_HANDOFF`

## Objeto

`H-0074` — primeira metade da implementação do `ITEM-0026`: leitura,
validação, carregamento e baseline/candidato de runtime de `filho_default`
em `dois_niveis_por_foco`. Divisão planejada: H-0074 de 2 (a segunda metade,
`H-0075`, cobre `Aplicar`, pop-up de confirmação e persistência, e não foi
antecipada nem criada nesta execução).

## ADR

`ADR-0048-persistencia-escolha-filho-por-pai`, patch `P02`, status
`ADR_APPLIED`. Aplicação documental aprovada (`ADR_APPLICATION_APPROVED`),
reconciliando `contrato_console.md` (§22.16, §26), `contrato_json_console.md`
(§16, §16.7) e os módulos de nomenclatura `32`, `42` e `43`. Nenhuma decisão
de schema permanece aberta: o literal público `filho_default` (D-0026-12) já
está fechado. Nenhum achado de QA foi reaberto ou revisitado; relatórios de
QA não foram lidos, conforme fronteira de leitura desta etapa.

## Capacidade delimitada

O handoff autoriza exclusivamente o caminho de leitura: `filho_default` no
documento externo → validação de carga (fail-closed, sem fallback
silencioso) → representação interna já suportada por `NoConteudo.campos` →
baseline persistida → candidato de runtime inicializado por
`selecao.inicializar_escolhas_dois_niveis`. Não autoriza gravação de volta ao
documento externo, ação `Aplicar`, pop-up de confirmação nem qualquer estado
`CONFIRMADO`/`ABORTADO` — tudo isso permanece fora, reservado a `H-0075`.

## Achados operacionais fechados pelo handoff

A leitura focal do código real produziu três decisões que, sem essa
investigação, teriam ficado abertas para o implementador — todas fechadas no
próprio handoff (§5–§7):

1. O comportamento predecessor de "primeiro filho" existe em dois pontos
   (`tela/selecao.py::_reconciliar_ids_dois_niveis`, causal, e
   `tela/navegacao.py::entrar_nivel_filhos`, defensivo/não causal); apenas o
   primeiro precisa mudar.
2. `tela/modelo.py` já transporta `filho_default` sem alteração (campo
   desconhecido preservado em `NoConteudo.campos`, mesmo padrão já usado por
   `navegavel`/`selecionavel`/`titulo`) — permanece preservado.
3. A validação de `filho_default` deve ocorrer como nova função em
   `tela/navegacao.py`, levantando exceção (`TelaCampoObrigatorioAusente`/
   `TelaEstruturaInvalida`, de `tela.carregamento.erros`), chamada a partir
   de `demo/demo.py::_carregar_modelo_por_id` após `construir_modelo` — não
   dentro do validador genérico de conteúdo externo (que desconhece política
   de navegação) nem misturada à checagem silenciosa de topologia já
   existente em `estrutura_dois_niveis_valida` (papel distinto, preservado).

Um quarto achado factual excluiu `h0063_estilo_estrutura_navegacao_dois_niveis`
do escopo de reconciliação: essa tela usa `dois_niveis_por_foco`, mas seu
conteúdo é sintetizado por `tela/estilo.py` a partir de `preset_default`
(`config/estilo.json`), fora do caminho de carregamento validado por este
handoff e fora da autoridade do `ITEM-0026` (ADR-0048 §6, §10).

## Arquivos futuros autorizados

**Editar**: `tela/selecao.py`, `tela/navegacao.py`, `demo/demo.py`,
`config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json`,
`tela/teste_navegacao.py`, `tela/teste_loader.py`.

**Preservados explicitamente** (com motivo factual registrado no handoff):
`tela/modelo.py`, `tela/carregamento/conteudo_externo.py`,
`tela/carregamento/formato_dois_niveis_por_foco.py`, todo `tela/renderizacao/*`,
`tela/estilo.py`, `config/estilo.json`,
`config/telas/demo/h0055_dois_niveis_por_foco.json` (estrutural),
`config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`,
`config/telas/demo/h0072_*` (fora do manifesto de leitura autorizado),
contratos, ADR, nomenclatura, backlog, mecanismo de pop-up e persistência
(H-0075).

## Fixtures e testes identificados

Fixture de produto: `h0055_dois_niveis_por_foco_conteudo.json` (5 pais, 4
filhos cada) — valores nominais de `filho_default` fechados no handoff (§8.1),
deliberadamente não posicionais (2º, 3º, 1º, 4º, 2º filho) para provar que a
baseline não deriva de posição. Fixtures de teste Python:
`tela/teste_navegacao.py::_arvore_h0055` (e variantes) — valores fechados em
§8.2. Testes reais a estender: `tela/teste_navegacao.py` (bloco H-0055
existente, ~L2032–L2270) e `tela/teste_loader.py` (bloco de
`dois_niveis_por_foco`/`validar_conteudo_externo`, ~L2722, ~L5211–L5360).
Nenhum diretório paralelo de testes foi proposto.

## Demonstração definida

Reutiliza a fixture estrutural real `h0055_dois_niveis_por_foco` (inalterada)
com o conteúdo reconciliado, pelo ponto de entrada real `demo/demo.py`.
Critérios de observação fechados no handoff §11: cada pai inicia pelo seu
`filho_default`; pais com posições diferentes comprovam ausência de
fallback posicional; cursor e escolha permanecem distintos; nenhuma escrita
em disco ocorre ao transferir escolha em runtime.

## Separação explícita de H-0075

Metadata, §1, §14 e a checklist de §15 do handoff declaram explicitamente que
persistência, `Aplicar`, pop-up, `CONFIRMADO`/`ABORTADO` e atomicidade
pertencem a `H-0075` e não são antecipados. `H-0075` não foi criado nesta
execução.

## Buscas e leituras executadas

Leitura integral do manifesto fechado: ADR-0048, `contrato_console.md`
(seções 22.16, 25, 26), `contrato_json_console.md` (seções 7.1, 15, 16),
`docs/nomenclatura/32_CONSOLE.md`, `42_DADOS_EXTERNOS_MULTINIVEL.md`,
`43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md`. Leitura focal de
`tela/carregamento/formato_dois_niveis_por_foco.py`,
`tela/carregamento/conteudo_externo.py`, `tela/selecao.py`, `tela/navegacao.py`,
`tela/modelo.py`, `demo/demo.py`, `tela/renderizacao/console.py`,
`config/telas/demo/h0055_dois_niveis_por_foco*.json`,
`h0063_estilo_estrutura_navegacao_dois_niveis.json`,
`tela/teste_navegacao.py` (bloco H-0055 completo), `tela/teste_loader.py`
(localização dos testes de conteúdo externo). Leitura pontual de
`tela/estilo.py` para fechar a exclusão de `h0063` (§5.6 do handoff), com
`grep` prévio confirmando ausência de `h0063` em `_CATALOGO_CONTEUDO_EXTERNO`.
`docs/relatorios/**`, outros ADRs, outros handoffs e módulos de nomenclatura
não enumerados não foram lidos.

## Verificações

Confirmada a existência dos dois artefatos desta etapa:
`docs/handoff/H-0074-filho-default-carregamento-baseline-runtime.md` e este
relatório. Nenhum outro arquivo foi criado, editado ou removido por esta
execução — nenhum código, configuração, contrato, ADR, nomenclatura ou
backlog foi tocado.

## Bloqueios

nenhum
