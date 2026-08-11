# Relatório QA pós-patch — H-0056 P02

```yaml
item: ITEM-0017
adr: ADR-0044
handoff: H-0056
patch_handoff: P02
status: H1_HANDOFF_APPROVED
```

## Resultado

O achado `QA-H0056-001` está corrigido. A declaração de
`popups.popup_basico.chips` usa a entidade canônica `chip`, com `id`, `tipo`,
`tecla`, `texto`, `referencia_regra`, `regra_existencia`, `regra_ativo` e
`forma_exibicao`. `popup_basico_voltar` é um ID estável de chip, distinto da
chave `popup_basico` da declaração do pop-up. `especifico`, `Esc`, `Voltar`,
`sempre` e `ativo` são compatíveis com os contratos aplicáveis.

`referencia_regra` está declarada como objeto, conforme o contrato, e conduz
ao resultado não confirmatório do pop-up. `texto: Voltar` permanece somente
visual; não há `rotulo` substitutivo nem ação de negócio. A área própria de
chips continua distinta de `barra_de_menus`, sem sua ordem canônica ou
aparência hardcoded. `Esc` retorna exatamente `status: ABORTADO`, sem payload,
confirmação ou `Enter`.

## Regressão e evidência

O handoff preserva configuração `popups.popup_basico`, conteúdo pronto em
runtime fora da declaração, moldura, título, geometria, centralização, bloqueio
modal, retorno à mesma tela, caminhos, demonstração e relatório futuro. Os
testes previstos cobrem validação do chip, campos ausentes, domínios, separação
entre texto e semântica, `Esc`, retorno sem payload e independência da barra.
As exclusões de H-0057, H-0058 e H-0059 permanecem intactas. `git diff --check`
foi executado sem apontamentos.

Não há achados adicionais.
