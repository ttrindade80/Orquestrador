# Relatório de Validação Manual — ITEM-0027 — R02

## Cenário executado

Foi executado:

```zsh
python demo/demo.py h0077_texto_amplo_justificado
```

No cenário, o popup longo justificado foi aberto com `w`, seguido de resize da janela.

## Objetivo da validação

Verificar a composição e a justificação global do texto do popup da TUI, inclusive durante o redimensionamento da janela.

## Resultado do popup

O popup apresentou o texto justificado corretamente. Palavras não foram quebradas no meio; não foi observada hifenização automática nem separação silábica. As palavras que deixaram de caber foram recompostas inteiras entre as linhas.

## Comportamento durante resize

O texto foi recomposto adequadamente durante o resize. Não foram observadas perdas ou duplicações de palavras, a justificação acompanhou a nova composição e o popup permaneceu visualmente correto.

## Palavras indivisíveis

A composição respeitou a indivisibilidade das palavras, mantendo cada palavra inteira e reorganizando as linhas conforme a largura disponível.

## Observação sobre o corpo externo não justificado

O corpo externo não justificado está correto e não constitui defeito. Esse corpo não foi especificado para solicitar modo justificado; a justificação é aplicada quando solicitada pelo consumidor. O ITEM-0027 não estabelece que todo texto da TUI seja automaticamente justificado.

```yaml
corpo_externo_nao_justificado:
  resultado: CORRETO
  defeito: false
  motivo: consumidor_nao_solicita_justificacao
```

## Comparação com R01

A R01 foi reprovada porque palavras eram fragmentadas pela largura física e a composição não representava corretamente o parágrafo lógico completo. Esses defeitos não foram reproduzidos após D-0027-10, a correção H-0076 P02 e a reconciliação H-0077 P02.

## Conclusão

```yaml
validacao_manual:
  item: ITEM-0027
  rodada: R02
  resultado: APROVADA
  defeito_original_reproduzido: false
  bloqueio_para_fechamento: false
```

## Bloqueios

Não há bloqueio para fechamento.
