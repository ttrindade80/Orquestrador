# Validação manual — H-0058

## Identificação

- Hipótese: H-0058 — Pop-up: lista navegável e marcação exclusiva/múltipla.
- Execução: usuário, em TTY real, na demonstração vigente.
- Natureza do registro: evidência factual da validação manual transportada.

## Cenários executados

- **Marcação exclusiva:** a lista abriu corretamente; o foco navegável ficou visível; o foco moveu-se sem alterar a marcação; Espaço transferiu a marcação para outro item; permaneceu exatamente uma marcação.
- **Enter na seleção exclusiva:** Enter não confirmou, o pop-up permaneceu aberto e nenhuma ação externa ocorreu.
- **Redimensionamento:** o pop-up respondeu ao resize e acionou a política de terminal pequeno quando a representação completa deixou de caber.
- **Esc na seleção exclusiva:** Esc fechou o pop-up, restaurou a tela subjacente e não executou ação de negócio.
- **Marcação múltipla:** o estado inicial múltiplo foi exibido; Espaço permitiu marcar e desmarcar itens; o foco permaneceu independente das marcações.
- **Enter e Esc na seleção múltipla:** Enter permaneceu sem efeito confirmatório; Esc fechou e restaurou a tela subjacente; não houve confirmação, payload ou ação de negócio.

## Resultado

Os comportamentos observados foram conformes. A observação referente às formações intermediárias no resize foi registrada e resolvida como não bloqueante.

## Observação de resize

Na sessão TTY não foram observadas visualmente as transições para matriz e linha antes do quadro de terminal pequeno. A verificação documental posterior estabeleceu que coluna, matriz e linha são formações garantidas pelas autoridades do componente e devem ser cobertas pelos testes determinísticos. Não há exigência documental de que uma única sessão TTY atravesse obrigatoriamente as três formações, nem comprovação de faixas reais alcançáveis na demonstração para todas as transições antes do terminal pequeno. Portanto, a ausência visual de matriz/linha não prova defeito de runtime e não bloqueia a validação final.

## Evidência automática complementar

Na mesma `PopupInstancia`, a cobertura determinística confirmou a sequência:

```text
50x20 -> coluna
40x10 -> matriz
77x8  -> linha
50x20 -> coluna
```

Foram preservados identidade da instância, cursor por ID, marcações por ID, ordem e envelope. Resultados transportados: testes focais `60_passed`, novo teste isolado `1_passed`, testes canônicos `1157_passed` e `git_diff_check` sem achados. Essa evidência complementa, mas não substitui, a validação humana.

## Status

`MANUAL_VALIDATION_APPROVED`
