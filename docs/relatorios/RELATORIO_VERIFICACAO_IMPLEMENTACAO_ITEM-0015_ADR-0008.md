# Relatório de verificação — ITEM-0015 / ADR-0008

## Classificação

```yaml
classificacao: HARDCODING_LOCAL_EXISTENTE
```

## Arquivos e símbolos materiais

- `config/telas/demo/*.json`: 72 objetos `cabecalho` estruturais; todos têm
  somente `titulo` e `descricao`. Exemplo: `demo.json:19-22`.
- `config/elementos/cabecalho.json:2-13`: contém os oito parâmetros locais
  esperados, mas não é consumido.
- Loader: `tela/carregamento/tela_json.py::carregar_tela` exige a presença de
  `cabecalho` (`187-188`) e retorna o dicionário bruto (`305-317`), sem
  validar ou materializar seu schema de apresentação.
- Modelo: `tela/modelo.py::ModeloTela` mantém `cabecalho` como `dict`
  (`105-110`); `construir_modelo` apenas o repassa (`415-420`, `519-525`).
- Renderer: `tela/renderizacao/tela.py::renderizar_tela` e
  `_geometria_por_console` leem apenas `titulo` e `descricao` (`112-116`,
  `345-351`). A moldura genérica é montada por `_linha_topo` e
  `_linha_conteudo` (`tela/renderizacao/geometria_caixa.py:35-45,62-72`).

## Fluxo atual

Os textos concretos vêm de `cabecalho.titulo` e `cabecalho.descricao` de cada
JSON de tela, passam sem transformação pelo loader e pelo modelo, e chegam ao
renderer. O título é convertido incondicionalmente por `upper()`; a descrição
é usada como recebida. O renderer recebe estilo global resolvido para a borda,
mas não lê parâmetros locais do cabeçalho.

## Parâmetros

| Parâmetro | Estado factual |
|---|---|
| `posicao` | Não declarado/transportado; topo efetivamente à esquerda por `_linha_topo`. |
| `recuo_lateral` | Não implementado; há apenas um espaço fixo após o canto. |
| `capitalizacao` | Título hardcoded em `upper()`; descrição não é transformada. |
| `formato_na_borda` | Não lido; formato com espaços laterais está fixo em `_linha_topo`. |
| `max_caracteres` | Não implementado; somente o corte genérico pela largura da caixa ocorre. |
| `alinhamento` | Não lido; `_linha_conteudo` preenche à esquerda. |
| `recuo` | Não lido; há um espaço fixo após a borda vertical. |

Não há ocorrência de consumo de `config/elementos/cabecalho.json` nas buscas
focais. Os JSONs de tela atuais não declaram os parâmetros locais.

## Testes encontrados

`tela/teste_loader.py::teste_caminho_feliz` comprova a presença do cabeçalho e
`teste_erros` comprova rejeição da ausência do campo (`506-512`).
`tela/teste_modelo.py::teste_modelo_orquestrador` comprova que o modelo expõe
`titulo` e `descricao` (`112-117`).
`tela/testes_renderizador/fundamentos.py::teste_renderizador_orquestrador`
comprova a renderização dos textos do JSON (`91-98`), e `teste_inercia`
comprova que o renderer não altera o cabeçalho (`643-656`). Não foi encontrado
teste permanente para carregar, transportar ou consumir os oito parâmetros
locais, nem para consumir o arquivo global existente.

## Delta técnico e bloqueios

Permanece o delta de declarar/validar esses parâmetros no JSON estrutural,
transportá-los pelo loader e modelo, consumi-los no renderer e cobrir o fluxo
com testes. Não há bloqueio de leitura; o estado vigente não atende a fronteira
documental da ADR-0008 para os parâmetros locais.
