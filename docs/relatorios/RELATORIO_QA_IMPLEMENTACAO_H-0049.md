# Relatório QA da implementação H-0049

```yaml
cadeia:
  raiz: docs/handoff/H-0049-materializacao-local-dos-parametros-do-cabecalho.md
  predecessor_imediato: docs/relatorios/IMP-0049-materializacao-local-dos-parametros-do-cabecalho.md

objeto_auditado:
  - implementacao_do_schema_local_do_cabecalho
  - migracao_das_72_telas
  - preservacao_dos_8_conteudos
  - adequacao_das_58_fixtures
  - remocao_da_configuracao_obsoleta

resultado:
  status: IMPLEMENTATION_APPROVED
  jsons_estruturais: 72
  jsons_com_preservar: 72
  conteudos_externos: 8
  hashes_ok: 8
  fixtures_incompativeis_restantes: 0
  teste_desc_fab:
    passou: true
    entrada: desc fab
    resultado_observado: desc fab
    expectativa_alterada: false
  testes_focais_h0049: 34
  testes_onze_arquivos: 514
  suite_integral: 998
  consumidores_residuais: 0
  configuracao_obsoleta_removida: true
  alteracoes_fora_do_manifesto: []
  novos_achados: []
  implementacao_aprovada: true
```

## Evidências

O baseline auditado foi `master` em `19085f420bf4dc0c2f094a809febac0933b25f77`, sem alterações staged. O inventário classificou 80 JSONs por raiz e loader: 72 telas estruturais e 8 conteúdos externos. Os 72 estruturais têm o schema local exato, com `descricao.capitalizacao: preservar`; títulos e descrições foram comparados ao baseline quanto aos demais campos. Os oito conteúdos mantêm raiz `dados/formato/tipo`, não receberam `cabecalho` e seus oito SHA-256 coincidem com o manifesto.

O loader valida objeto fechado, campos obrigatórios, tipos não booleanos, enums e limites inclusivos, sem fallback. Os casos positivos e negativos do schema foram exercitados. O modelo transporta o cabeçalho integralmente; o renderizador consome os parâmetros locais tanto no cálculo quanto na renderização, e a geometria aplica corte, capitalização, alinhamento/recuo e formato na ordem contratada. Não há consumidor residual nem fallback de cabeçalho; ocorrências de `formato.apresentacao` pertencem ao conteúdo externo. As 17 telas que mudariam sob capitalização `inicio_de_frase` permanecem protegidas por `preservar`.

As 58 ocorrências incompatíveis em 13 arquivos foram eliminadas sem alterar a finalidade dos testes; as quatro negativas intencionais do H-0049 continuam separadas e não há negativas intencionais nos 11 arquivos adicionais. A fixture `desc fab` preserva exatamente o texto observado. A configuração obsoleta `config/elementos/cabecalho.json` foi removida e `config/estilo.json` não tem diff. O diff de implementação contém apenas o schema/consumo e a materialização declarada; documentos e caches transportados preexistentes foram preservados.

Resultados executados: 34 testes focais H-0049 (`26 loader, 2 modelo, 6 renderer`), scripts diretos do loader e modelo com respectivamente 562 e 186 verificações aprovadas, 514 testes nos 11 arquivos e 998 na suíte integral, todos sem falhas ou erros. `git diff --check` também foi aprovado. Não há achados novos; a implementação, o escopo e as evidências estão aprovados.
