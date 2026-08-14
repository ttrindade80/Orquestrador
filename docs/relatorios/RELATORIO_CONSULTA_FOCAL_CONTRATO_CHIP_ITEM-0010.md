# Consulta focal — `contrato_chip.md` × resíduos ITEM-0010

**Arquivo lido:** `docs/contratos/contrato_chip.md` (existe; v0.1; status ativo).
**Não lidos:** ADRs, handoffs, relatórios, código, config, backlog, demais contratos/nomenclaturas.
**Normativo vs inferência:** só o texto do contrato; ausência não é autorização.

## Tabela das 12 perguntas

| # | Resposta factual | Seção |
|---|---|---|
| 1. Entidade `chip` na barra e/ou outros renderers? | **Sim.** Entidade declarativa de interface textual; uso primário `barra_de_menus`; a mesma entidade visual/semântica pode ser consumida pela área de chips do pop-up. Chips do `lancador` não são chips da barra. | §§2, 3, 3.1 |
| 2. Representação de ações com múltiplas teclas? | **Não fecha** a forma visual de *uma* ação com 2+ teclas. `tecla` é tecla física ou combinação. Notação documental concatena chips (`[PgUp][PgDn]`, `[-][+]`). `forma_exibicao` admite agrupamento de dois ou mais *chips*. Layout detalhado fora de escopo. | §§5, 7, 10, 11, 18 |
| 3. Separador entre teclas? | **Não define.** Nenhum separador entre teclas. "/" só em usos alheios (ex.: «Sair / Voltar / Limpar»; «página 1/1»). | ausente; "/" alheio em §§7, 9 |
| 4. Unidade visual das múltiplas teclas? | **Em aberto** para ação multitecla. O contrato descreve agrupamento de *chips* concatenados, cada um delimitado (`[PgUp][PgDn]`), sem dependência de preset. | §§7, 10, 18 |
| 5. Onde aplicar delimitadores E/D na ação multitecla? | **Não determina.** Moldura por chip: `caractere_esquerdo` / `caractere_direito` do estilo. Notação documental delimita por chip; §7: identificadores documentais, não valores renderizáveis obrigatórios. | §§7, 12 |
| 6. Natureza de "/"? | **Não classificado.** Não é campo do schema (§4). §12 proíbe hardcoding de cor, caractere de moldura ou símbolo de chip, sem nomear "/". | §§4, 12 |
| 7. Cor/fundo (laterais, tecla, unidade, isolamento)? | Cores do *chip*: `cor_texto`, `cor_fundo`, `cor_inativo`, `cor_alerta`. **Não** há regra para espaços laterais, unidade multitecla completa, nem reset/isolamento contra vazamento. Espaçamento fora de escopo. | §§9, 10, 12, 18 |
| 8. Coloração assimétrica E vs D? | **Não admite nem define.** Cores são do chip, não por lado. | §12 |
| 9. R2 muda? | **INDETERMINADO_PELO_CONTRATO_CHIP** | §§7, 10, 11, 18 |
| 10. R7 muda? | **INDETERMINADO_PELO_CONTRATO_CHIP** | §§12, 18 |
| 11. Tensão do "/"? | **NAO_RESOLVIDA** | — |
| 12. Impacto em R1, R3, R4, R5, R6, R8, R9? | Formulações dessas R **não estão** neste artefato. Reitera aparência via `estilo.json` e proibição de hardcoding de chip/tecla/texto/cor/moldura/símbolo — sem reclassificar esses resíduos. | §§2, 12, 17 |

## Decisões factuais

**R2:** INDETERMINADO_PELO_CONTRATO_CHIP (§§7, 10, 11, 18). O contrato não exige `tecla1/tecla2` com delimitadores só nas extremidades; o agrupamento documental `[A][B]` não é valor renderizável obrigatório; layout está fora de escopo. Não se infere incompatibilidade nem compatibilidade.

**R7:** INDETERMINADO_PELO_CONTRATO_CHIP (§§12, 18). Há `cor_fundo`/`cor_texto` do chip; não há «Destaque Texto», espaços laterais nem assimetria E/D.

**"/":** NAO_RESOLVIDA. Não é aparência configurável, caractere normativo, glue estrutural nem hardcoding nomeado.

## Conclusão

Após este contrato, **permanece incerteza documental relevante**: composição multitecla, papel de "/", delimitadores externos vs por tecla, e assimetria lateral de cor **não estão decididos** aqui.
