# RELATORIO_PATCH_HANDOFF_H-0071_P03

```yaml
item: ITEM-0010
adr: ADR-0046
handoff: docs/handoff/H-0071-correcao-chips-multitecla-barra-menus-estilo.md
patch_handoff: P03
raiz: docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0071.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0071_P02.md
```

## Motivo do patch

O QA pós-patch da implementação `P02` retornou `I3_HANDOFF_PATCH_REQUIRED`.
Todos os resíduos funcionais e de expectativas anteriormente conhecidos
foram reconciliados; o único resíduo remanescente são duas inspeções
estruturais desatualizadas em `tela/testes_renderizador/fundamentos.py`,
que ainda buscam literalmente `estilo.cor_texto` e `estilo.cor_fundo`
dentro de `tela/renderizacao/barra_menus.py`. Ambas foram classificadas
pelo QA como `TESTE_FONTE_DESATUALIZADO_PELO_H0071`: a Barra não acessa
mais essas cores por acesso direto local, e sim delega a composição do
chip ao compositor compartilhado `tela/renderizacao/estilo.py
::compor_chip_multitecla`, comportamento correto e necessário deste
handoff. O H-0071 não autorizava, até este patch, alteração de
`tela/testes_renderizador/fundamentos.py`.

## Inclusão nominal de `fundamentos.py`

Foi acrescentada a subseção 8.3.2 ("Ampliação de escopo — patch P03"),
adicionando nominalmente `tela/testes_renderizador/fundamentos.py` ao
escopo de implementação/testes autorizado.

## Natureza restrita da autorização

A autorização é estritamente limitada às duas inspeções estruturais
relacionadas ao consumo de `cor_texto` e de `cor_fundo`. Nenhuma outra
inspeção do arquivo é autorizada a mudar por este patch. A subseção
explicita a lista de proibições: remoção sem substituição equivalente,
conversão em teste trivial, skip, xfail, alteração de produção para
satisfazer a inspeção antiga, reintrodução de acesso direto a
`cor_texto`/`cor_fundo` em `barra_menus.py`, criação de compositor visual
paralelo na Barra, alteração de `demo/teste_diagnostico.py`, alteração de
`tela/teste_renderizador.py` por causa deste resíduo, alteração de
configuração/schema/presets, e alteração de cursor, toggle, hierarquia ou
`MF-ITEM0010-003`.

## Invariável arquitetural preservada

A subseção 8.3.2 reafirma explicitamente que a intenção arquitetural
original permanece obrigatória: a Barra deve consumir cor de texto e cor
de fundo do estilo global, não pode hardcodar essas cores, não pode manter
mecanismo visual paralelo, e o compositor compartilhado permanece
responsável pela materialização da aparência do chip. A futura adaptação
das duas inspeções deve verificar, estrutural/focalmente, a delegação da
Barra ao compositor compartilhado e o consumo real de `cor_texto`/
`cor_fundo` por esse compositor, sem voltar a exigir acesso direto dentro
de `barra_menus.py`.

## Critérios de aceite acrescentados

Foram adicionados à seção 9: `CA-H0071-20` (reconhecimento da delegação
vigente, sem exigir acesso direto), `CA-H0071-21` (prova de consumo real de
`cor_texto`/`cor_fundo` no caminho da Barra real), `CA-H0071-22` (proteção
contra hardcoding e compositor paralelo), `CA-H0071-23` (sem alteração de
produção nem enfraquecimento da invariável), `CA-H0071-24` (runner direto
de `tela/teste_renderizador.py` com código zero) e `CA-H0071-25`
(`demo/teste_diagnostico.py` inalterado, com o erro derivado
desaparecendo pela correção das falhas-raiz).

## `demo/teste_diagnostico.py` fora do escopo

A subseção 8.3.2 reafirma explicitamente que
`demo/teste_diagnostico.py::teste_invariantes_anteriores` não é
adicionado ao escopo de alteração. Seu erro é derivado exclusivamente do
código de saída do runner direto de `tela/teste_renderizador.py` e deve
desaparecer, sem edição própria, quando as duas inspeções-raiz forem
reconciliadas.

## Bloqueios

Nenhum. A evidência transportada foi suficiente para determinar
nominalmente a ampliação de escopo, sem exigir busca ampla adicional.
