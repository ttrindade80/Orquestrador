# Relatório — Criação do Handoff H-0072

## Etapa

`CRIAR_HANDOFF`

## Objeto

`H-0072` — capacidade genérica de formatação dos filhos de
`dois_niveis_por_foco`.

## ADR

`ADR-0047-formatacao-filhos-dois-niveis-por-foco`, `QA_ADR: ADR_APPROVED`,
`QA_APLICACAO_ADR: ADR_APPLICATION_APPROVED`. Nenhum achado material
pendente da ADR ou de sua aplicação foi reaberto ou revisitado nesta etapa;
os relatórios de QA não foram lidos para reconfirmação, conforme instruído.

## Capacidade

O handoff autoriza a implementação de suporte, no sistema já existente de
`dois_niveis_por_foco` (ADR-0042), ao bloco declarativo
`formato.dois_niveis_por_foco.filho` do elemento `console`: tabulação
mínimo/máximo pai→filho, designador local (`decimal_composto`,
`alfabetico_maiusculo`, `nenhum`), apresentação `texto`/`tabela`, colunas
locais (`tabela.colunas[].campo`) e espaçamento entre colunas
(mínimo/máximo). A ordem física, a separação entre configuração de
apresentação (JSON estrutural da tela) e conteúdo/dados (documento externo),
o alinhamento global de colunas entre pais diferentes e a preservação
integral da navegação/seleção de `dois_niveis_por_foco` foram transportados
literalmente da ADR-0047 e das seções já aplicadas de
`contrato_console.md` §25, `contrato_tela_json.md` §36 e
`contrato_json_console.md` §15.

## Arquivos futuros autorizados para implementação

Levantamento focal fechou nominalmente:

**Existentes (edição autorizada)**: `tela/modelo.py`,
`tela/carregamento/tela_json.py`, `tela/navegacao.py`, `tela/selecao.py`,
`tela/renderizacao/console.py`, `tela/renderizacao/conteudo_externo.py`,
`tela/renderizacao/designadores.py`, `tela/renderizacao/matriz_participantes.py`,
`demo/demo.py`.

**Novo (autorizado, ainda não existe)**: `tela/carregamento/formato_dois_niveis_por_foco.py`
— análogo em forma a `tela/carregamento/d23_console.py`, precedente
estrutural já usado para `formato.excesso`.

**Testes existentes associados a H-0055/`dois_niveis_por_foco` (extensão
autorizada)**: `tela/teste_navegacao.py` (seção H-0055, ~L2032),
`tela/teste_loader.py` (validação de `politica_navegacao.tipo`,
~L5211–L5360), `demo/teste_demo_console.py` (cenário `h0055_dois_niveis_por_foco`,
~L157–L566).

**Testes e fixtures novos (dedicados à capacidade genérica)**:
`config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco.json`,
`..._conteudo.json`, `tela/teste_formato_filho_dois_niveis_por_foco.py`,
`demo/teste_demo_h0072_formatacao_generica.py`.

Arquivos preservados e listados explicitamente como não alteráveis:
`h0055_dois_niveis_por_foco.json`, `..._conteudo.json`,
`h0063_estilo_estrutura_navegacao_dois_niveis.json`, `h0062_estilo.json`,
além de ADR/contratos/nomenclatura usados como autoridade.

## Buscas focais executadas

`rg -n 'dois_niveis_por_foco|politica_navegacao|formato\.dois_niveis_por_foco'`
em `tela`, `demo`, `config/telas/demo` (o caminho `tests` não existe no
repositório e foi ignorado pela busca). Buscas complementares estritamente
focais para fechar nominalmente os arquivos de loader/modelo/renderer:
localização de `politica_modo`/`formato.excesso` (precedente estrutural),
localização do wiring de validadores em `tela/carregamento/tela_json.py`,
localização da extração de `formato` em `tela/modelo.py`, e localização do
catálogo de cenários em `demo/demo.py`. Nenhuma busca genérica (`find .`,
`tree`, inventário de `docs/relatorios`) foi executada.

## Principais critérios materializados

Separação configuração×conteúdo; ordem física
`tabulação → ec → tg → designador → conteúdo` como unidade deslocada;
mínimo/máximo de tabulação (5–10) e de espaçamento (3–8) com critério de
maior valor que couber e sobra à direita; apresentação `texto` preservando
fluxo vigente; apresentação `tabela` sem cabeçalho/borda/título, com
alinhamento global entre pais diferentes; quebra multilinha sem novo item
lógico; resize sem persistência de geometria; onze casos de rejeição de
schema; dezoito casos de teste semânticos, todos executáveis por `pytest`
sem TTY real; demonstração via `demo/demo.py`.

## H-0073 preservado fora de escopo

O handoff declara explicitamente, em metadata e em escopo negativo, que a
aplicação da capacidade a `h0055` e `h0063` pertence a H-0073 e não foi
antecipada. Nenhuma fixture existente foi alterada por este handoff.

## Verificações

Confirmado: todos os arquivos nominais de implementação existem no
repositório ou estão explicitamente autorizados como novos; o handoff não
depende de descoberta ampla futura; configuração (JSON estrutural) e
conteúdo/dados (documento externo) permanecem separados em todas as seções;
H-0073 não foi antecipado; os dezoito testes propostos são executáveis por
`pytest`; o handoff e este relatório existem materialmente no repositório.

`git diff --check` executado sobre os dois arquivos novos: sem erros de
espaço em branco.

## Bloqueios

nenhum
\n