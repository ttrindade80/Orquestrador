# Relatório de patch documental — H-0056 P02

## Achado corrigido

Foi corrigido o achado `QA-H0056-001 — declaração demonstrativa de chip
incompatível com o contrato`.

A forma anterior era:

```json
{
  "tecla": "Esc",
  "rotulo": "Voltar"
}
```

Essa forma não declarava a entidade `chip` canônica e usava `rotulo` no lugar
de `texto`.

## Correção aplicada

O exemplo de `popups.popup_basico.chips` passou a declarar o chip com:

```text
id: popup_basico_voltar
tipo: especifico
tecla: Esc
texto: Voltar
referencia_regra: resultado.status = ABORTADO
regra_existencia: sempre
regra_ativo: sempre
forma_exibicao: ativo
```

Foram contemplados todos os campos mínimos previstos em `contrato_chip.md`:
`id`, `tipo`, `tecla`, `texto`, `acao` ou `referencia_regra`,
`regra_existencia`, `regra_ativo` e `forma_exibicao`. A referência usa a regra
de retorno do pop-up, sem criar ação de negócio. A aparência ativa continua
derivada do estilo universal, sem cor, borda, símbolo ou formatação exclusivos.

## Semântica e testes

`Esc` permanece a tecla física; `Voltar` permanece apenas texto visual. O
encerramento é não confirmatório, produz `status: ABORTADO` e não possui
payload. Os testes exigidos foram reforçados para validar o schema canônico,
rejeitar a ausência de campo obrigatório, separar texto de ação, verificar o
retorno sem payload e confirmar que a área própria consome `chip` sem se tornar
`barra_de_menus` ou adotar sua ordem.

## Escopo e verificações

Nenhum contrato, ADR, nomenclatura, backlog, código, configuração, teste ou
fixture real foi alterado. H-0056 permanece não implementado; H-0057, H-0058 e
H-0059 continuam fora do escopo. `git diff --check` passou. Não foram
executados QA ou testes, conforme o limite deste patch. Não há bloqueio
documental restante; a implementação continua remetida ao relatório futuro
`docs/relatorios/IMP-0056-popup-basico-exibicao-voltar.md`.
