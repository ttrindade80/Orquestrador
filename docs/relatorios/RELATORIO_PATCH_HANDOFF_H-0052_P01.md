# Relatório de Patch — Handoff H-0052 (P01)

```yaml
status: PATCH_HANDOFF_CONCLUIDO
handoff: H-0052
patch: P01
cadeia:
  raiz: docs/relatorios/RELATORIO_QA_HANDOFF_H-0052.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_HANDOFF_H-0052.md
```

## H-0052-A — fallback além da ausência de `tipo`

**Correção realizada.** §7.1 foi reescrita: o fallback para `nivel_unico`
agora só ocorre quando `politica_navegacao` **é** `dict` e não há chave
`tipo`. Foi acrescentado bullet explícito afirmando que, quando
`politica_navegacao` **não** é `dict`, a função de resolução não normaliza
para `nivel_unico` — a entrada permanece estruturalmente inválida, sujeita à
rejeição já existente no carregamento (§7.3), sem mascarar o erro
estrutural. §3 item 1 e §15 foram atualizados para refletir a restrição.
Foi adicionado o caso NAO_OBJETO em §8 e o teste de fronteira (item 2) em
§11, distinto da regressão de rejeição estrutural (item 5).

## H-0052-B — enumeração fechada deixada opcional

**Correção realizada.** §7.3 substitui a antiga observação "não é
obrigatório" por uma validação obrigatória no mesmo ponto de intervenção
(`_validar_valores_envelope_pre_adr_0028`): aceitar somente os cinco
literais fechados, rejeitar valor textual desconhecido e forma não textual
incompatível via `TelaEstruturaInvalida`, sem alias, coerção ou conversão
para `nivel_unico`, e sem criar matriz geral `navegavel × tipo` além da
incompatibilidade já decidida de `tabela`. §3 item 1 e a tabela de
proprietários (§5) foram atualizados. Foram acrescentados os casos
TIPO_DESCONHECIDO e TIPO_NAO_TEXTUAL em §8, e os testes 7–9 em §11
(discriminador aceito para os cinco valores, rejeição de valor desconhecido,
rejeição de forma não textual quando aplicável). §15 recebeu critério de
aceite correspondente.

## H-0052-C — setas em `tabela`

**Correção realizada.** A afirmação categórica de que "nenhum `mover_*`
precisa mudar" foi removida de §7.2. Em seu lugar, o handoff agora distingue
as funções que continuam inalteradas (`itens_navegaveis`, `grade_de_itens`,
`avancar_foco`, `recuar_foco`, `exibir_chip_navegar`, `console_focado`) das
quatro funções de movimento, para as quais foi definido um requisito
comportamental explícito (chamada direta sobre console `tabela` → nenhuma
alteração de cursor) e uma autorização de alteração focal em
`tela/navegacao.py` (funções públicas de movimento ou o ponto comum
imediatamente consumido por elas), com restrições (`nivel_unico`
inalterado, políticas futuras sem antecipação, seleção/paginação
intocadas). A tabela de proprietários (§5) foi atualizada. O teste §11 item
13 foi reescrito para exigir chamada direta das quatro funções sobre
`tabela`, sem a alegação de "por construção" que o QA apontou como
contraditória.

## Preservações QH52-CRIT-03 e QH52-CRIT-04

Ambas preservadas sem alteração de mérito. As três políticas futuras
continuam literais reconhecidos e transportados, sem fallback para
`nivel_unico` e sem comportamento antecipado (§7.2, §7.3, §11 item 15). A
concretização de QH52-CRIT-04 (`TelaEstruturaInvalida` via
`_validar_valores_envelope_pre_adr_0028`) foi mantida como o único mecanismo
de falha estrutural, agora também reutilizado para a validação da
enumeração fechada — nenhuma segunda camada de erro foi criada.

## Seções materialmente alteradas

§3 (item 1), §5 (tabela de proprietários), §7.1, §7.2, §7.3, §8 (três casos
novos), §11 (renumerada 1–17, com dois testes novos e um reescrito), §15,
§17 (referências cruzadas de numeração).

## Verificações

- Escopo nominal (§6) inalterado — nenhum arquivo novo autorizado além dos
  já previstos.
- Nenhum novo mecanismo de erro criado; `TelaEstruturaInvalida` permanece
  único.
- Nenhuma coerção ou alias introduzidos para `tipo` inválido.
- Todas as referências cruzadas a números de teste em §11 foram
  atualizadas (13 → 17 testes focais).
- `git diff --check` sem achados nos dois arquivos alterados.

## Bloqueios

Nenhum.
