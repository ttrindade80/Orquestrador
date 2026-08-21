# Relatório do patch de implementação H-0076 P02

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0076.md
  origem_reabertura: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_ITEM-0027_R01.md
  handoff_atualizado: docs/relatorios/RELATORIO_QA_HANDOFF_H-0076_POS_P01.md

decisao_aplicada:
  - D-0027-10
```

## Causa

O núcleo anterior formava faixas por largura visual de células e podia
partir palavras. Assim, a linha física era tratada como unidade lógica e o
resize podia perpetuar fragmentos anteriores.

## Correção do núcleo

`composicao_textual.py` agora reconhece palavras como sequências de células
não brancas e forma cada linha adicionando palavras inteiras com seus vãos.
Não há hifenização, separação silábica, clipping ou truncamento. Uma palavra
maior que a largura permanece íntegra em uma linha lógica mais larga.

A recomposição é stateless: cada chamada recebe o parágrafo original e não
usa linhas ou segmentos de chamadas anteriores. A justificação é aplicada
somente depois da formação das linhas, apenas nos vãos das linhas solicitadas;
`justificar_ultima` permanece como opção do consumidor.

ANSI continua usando `texto_ansi.py`. CSI não é partido; palavras estilizadas
participam da largura visual e o SGR é fechado/restabelecido entre linhas.

## Popup

O popup continua consumindo `compor_texto` para o texto lógico completo em
cada layout, inclusive após resize. Geometria, moldura, largura útil,
alinhamento e chips permanecem responsabilidades locais. Não foi introduzido
algoritmo concorrente nem foi alterado `texto_ansi.py`.

## Arquivos alterados

- `tela/renderizacao/composicao_textual.py`
- `tela/teste_composicao_textual.py`
- `tela/teste_popup.py`
- `demo/teste_demo_popup.py`

`tela/renderizacao/popup.py` foi revisado e já consumia o núcleo canônico;
nenhuma alteração funcional adicional foi necessária.

## Testes e resultados

Executado:

```text
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  tela/teste_composicao_textual.py \
  tela/teste_popup.py \
  demo/teste_demo_popup.py
```

Resultado: `91 passed`.

A cobertura inclui palavras indivisíveis, palavra maior que a largura,
recomposição em três larguras, não reutilização de linhas no popup,
justificação posterior, ANSI e resize de popup com parágrafo longo.

## Fronteira H-0077

Nenhum consumidor ou artefato funcional de H-0077 foi alterado. A regressão
dos consumidores externos permanece fora desta etapa.

## Bloqueios

Nenhum bloqueio para o patch H-0076 P02.
